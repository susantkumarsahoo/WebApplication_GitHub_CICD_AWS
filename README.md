# WebApplication_GitHub_CICD_AWS
A WebApplication_CICD_AWS refers to the automated pipeline for building, testing, and deploying web applications on the Amazon Web Services (AWS) platform.



Docker image 
# ECR - '727646479568.dkr.ecr.us-east-1.amazonaws.com/webapprepo'




# Streamlit App CI/CD Pipeline with GitHub Actions and AWS

## 📁 Project Structure

```
streamlit-app/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── app.py
├── streamlit_app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── README.md
```

## 📋 Step-by-Step Setup Guide

### 1. Prerequisites

Before starting, ensure you have:
- GitHub repository created
- AWS Account with appropriate permissions
- IAM User with programmatic access

### 2. AWS Setup

#### A. Create IAM User and Get Credentials

1. **Create IAM User:**
   - Go to AWS Console → IAM → Users → Add User
   - User name: `github-actions-deployer`
   - Select: "Programmatic access"

2. **Attach Policies:**
   Attach the following managed policies:
   - `AmazonEC2ContainerRegistryFullAccess`
   - `AmazonEC2FullAccess` (or create a custom policy with minimal permissions)

3. **Save Credentials:**
   - Download and save the Access Key ID and Secret Access Key
   - You'll need these for GitHub Secrets

#### B. Create ECR Repository

1. Go to AWS Console → ECR → Repositories → Create repository
2. Repository name: `streamlit-app`
3. Keep settings as default (private repository)
4. Note the repository URI (format: `{AWS_ACCOUNT_ID}.dkr.ecr.{AWS_REGION}.amazonaws.com/streamlit-app`)

#### C. Launch EC2 Instance

1. **Launch Instance:**
   - Go to EC2 → Launch Instance
   - Name: `streamlit-app-server`
   - AMI: Amazon Linux 2023 or Ubuntu 22.04 LTS
   - Instance type: `t2.medium` (or `t3.medium` for better performance)
   - Key pair: Create new or use existing (download .pem file)

2. **Configure Security Group:**
   - Allow SSH (port 22) from your IP
   - Allow HTTP (port 80) from anywhere (0.0.0.0/0)
   - Allow Custom TCP (port 8501) from anywhere for Streamlit
   - Allow HTTPS (port 443) if needed

3. **Storage:**
   - Minimum 20 GB gp3

4. **Launch and Note:**
   - Instance ID
   - Public IP address

#### D. Configure EC2 Instance

SSH into your EC2 instance:

```bash
ssh -i your-key.pem ec2-user@your-ec2-public-ip
```

Then run these commands:

```bash
# Update system
sudo yum update -y  # For Amazon Linux
# OR
sudo apt update && sudo apt upgrade -y  # For Ubuntu

# Install Docker
sudo yum install docker -y  # Amazon Linux
# OR
sudo apt install docker.io -y  # Ubuntu

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add ec2-user to docker group (no sudo needed for docker commands)
sudo usermod -aG docker ec2-user
# OR for Ubuntu
sudo usermod -aG docker ubuntu

# Install AWS CLI (if not already installed)
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo yum install unzip -y  # Amazon Linux
# OR
sudo apt install unzip -y  # Ubuntu
unzip awscliv2.zip
sudo ./aws/install

# Verify installations
docker --version
aws --version

# Log out and log back in for group changes to take effect
exit
```

Log back in:
```bash
ssh -i your-key.pem ec2-user@your-ec2-public-ip
```

### 3. GitHub Repository Setup

#### A. Add GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions → New repository secret

Add the following secrets:

1. **AWS_ACCESS_KEY_ID**: Your IAM user access key
2. **AWS_SECRET_ACCESS_KEY**: Your IAM user secret key
3. **AWS_REGION**: Your AWS region (e.g., `us-east-1`)
4. **AWS_ACCOUNT_ID**: Your 12-digit AWS account ID
5. **EC2_HOST**: Public IP or DNS of your EC2 instance
6. **EC2_USERNAME**: `ec2-user` (for Amazon Linux) or `ubuntu` (for Ubuntu)
7. **EC2_SSH_KEY**: Contents of your .pem private key file

To get the EC2_SSH_KEY value:
```bash
cat your-key.pem
```
Copy the entire output including `-----BEGIN RSA PRIVATE KEY-----` and `-----END RSA PRIVATE KEY-----`

### 4. Project Files

Create the following files in your repository:

#### `requirements.txt`
```
numpy==2.2.6
pandas==2.3.2
plotly==5.24.1
streamlit==1.52.1
```

#### `Dockerfile`
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY streamlit_app.py .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run Streamlit app
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### `.dockerignore`
```
.git
.github
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
pip-log.txt
pip-delete-this-directory.txt
.pytest_cache
.coverage
htmlcov/
dist/
build/
*.egg-info/
.DS_Store
README.md
.gitignore
```

#### `.github/workflows/deploy.yml`
```yaml
name: Deploy Streamlit App to AWS

on:
  push:
    branches:
      - main
      - master
  workflow_dispatch:

env:
  ECR_REPOSITORY: streamlit-app
  ECS_CONTAINER_NAME: streamlit-container

jobs:
  deploy:
    name: Build and Deploy
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.AWS_REGION }}

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1

      - name: Build, tag, and push image to Amazon ECR
        id: build-image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker tag $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG $ECR_REGISTRY/$ECR_REPOSITORY:latest
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest
          echo "image=$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG" >> $GITHUB_OUTPUT

      - name: Deploy to EC2
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
          EC2_HOST: ${{ secrets.EC2_HOST }}
          EC2_USERNAME: ${{ secrets.EC2_USERNAME }}
          EC2_SSH_KEY: ${{ secrets.EC2_SSH_KEY }}
        run: |
          # Save SSH key
          echo "$EC2_SSH_KEY" > private_key.pem
          chmod 600 private_key.pem
          
          # Deploy to EC2
          ssh -o StrictHostKeyChecking=no -i private_key.pem ${EC2_USERNAME}@${EC2_HOST} << 'ENDSSH'
            # Login to ECR
            aws ecr get-login-password --region ${{ secrets.AWS_REGION }} | docker login --username AWS --password-stdin ${{ secrets.AWS_ACCOUNT_ID }}.dkr.ecr.${{ secrets.AWS_REGION }}.amazonaws.com
            
            # Stop and remove existing container
            docker stop streamlit-app || true
            docker rm streamlit-app || true
            
            # Pull latest image
            docker pull ${{ steps.login-ecr.outputs.registry }}/${{ env.ECR_REPOSITORY }}:latest
            
            # Run new container
            docker run -d \
              --name streamlit-app \
              -p 8501:8501 \
              --restart unless-stopped \
              ${{ steps.login-ecr.outputs.registry }}/${{ env.ECR_REPOSITORY }}:latest
            
            # Clean up old images
            docker image prune -af
          ENDSSH
          
          # Clean up SSH key
          rm -f private_key.pem

      - name: Verify deployment
        run: |
          echo "✅ Deployment completed successfully!"
          echo "🌐 Access your app at: http://${{ secrets.EC2_HOST }}:8501"
```

### 5. Configure AWS CLI on EC2

SSH into your EC2 instance and configure AWS CLI:

```bash
aws configure
```

Enter:
- AWS Access Key ID: [Your IAM user access key]
- AWS Secret Access Key: [Your IAM user secret key]
- Default region name: [Your AWS region, e.g., us-east-1]
- Default output format: json

### 6. Deployment

Once everything is set up:

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit with CI/CD pipeline"
   git push origin main
   ```

2. **Monitor the deployment:**
   - Go to your GitHub repository → Actions
   - Watch the workflow execution

3. **Access your app:**
   - Once deployment is complete, visit: `http://YOUR_EC2_PUBLIC_IP:8501`

### 7. Troubleshooting

#### Check Docker container logs on EC2:
```bash
ssh -i your-key.pem ec2-user@your-ec2-public-ip
docker logs streamlit-app
```

#### Check running containers:
```bash
docker ps -a
```

#### Restart container:
```bash
docker restart streamlit-app
```

#### Manual deployment test:
```bash
# Login to ECR
aws ecr get-login-password --region YOUR_REGION | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.YOUR_REGION.amazonaws.com

# Pull and run
docker pull YOUR_ACCOUNT_ID.dkr.ecr.YOUR_REGION.amazonaws.com/streamlit-app:latest
docker run -d -p 8501:8501 --name streamlit-app YOUR_ACCOUNT_ID.dkr.ecr.YOUR_REGION.amazonaws.com/streamlit-app:latest
```

### 8. Optional: Set Up Domain Name

1. Get an Elastic IP for your EC2 instance (to avoid IP changes)
2. Configure Route 53 or your domain provider to point to the Elastic IP
3. Set up SSL/TLS with Let's Encrypt using Nginx as reverse proxy

### 9. Cost Optimization Tips

- Use `t3.micro` or `t3.small` for development/testing
- Stop EC2 instance when not in use
- Use ECR lifecycle policies to clean up old images
- Consider AWS Free Tier limits

### 10. Security Best Practices

✅ **Implemented:**
- IAM user with minimal required permissions
- Private ECR repository
- SSH key authentication for EC2

🔒 **Recommended:**
- Rotate AWS credentials regularly
- Use AWS Secrets Manager for sensitive data
- Enable MFA on AWS account
- Restrict security group rules to specific IPs when possible
- Regularly update Docker base images
- Implement AWS CloudWatch for monitoring

## 📊 Architecture Overview

```
GitHub Repository (Push)
    ↓
GitHub Actions Workflow
    ↓
Build Docker Image
    ↓
Push to Amazon ECR
    ↓
SSH to EC2 Instance
    ↓
Pull Image from ECR
    ↓
Run Container on EC2
    ↓
Streamlit App (Port 8501)
```

## 🎉 Success!

Your Streamlit app is now automatically deployed to AWS whenever you push to the main branch!

Access your app at: `http://YOUR_EC2_PUBLIC_IP:8501`
