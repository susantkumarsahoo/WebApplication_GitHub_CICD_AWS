import time
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# Page Configuration (Must be first Streamlit command)
st.set_page_config(
    page_title="Complete Streamlit Demo",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://docs.streamlit.io',
        'Report a bug': 'https://github.com/streamlit/streamlit',
        'About': '# Complete Streamlit Features Demo\nExplore every Streamlit feature!'
    }
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        background: linear-gradient(90deg, #FF4B4B 0%, #FF8C8C 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 2rem 0 1rem 0;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'counter' not in st.session_state:
    st.session_state.counter = 0
if 'data_cache' not in st.session_state:
    st.session_state.data_cache = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# Generate sample data
@st.cache_data
def generate_sample_data(rows=1000):
    """Generate comprehensive sample dataset"""
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', periods=rows, freq='H')
    
    df = pd.DataFrame({
        'timestamp': dates,
        'category': np.random.choice(['A', 'B', 'C', 'D'], rows),
        'value': np.random.randn(rows).cumsum() + 100,
        'count': np.random.randint(1, 100, rows),
        'temperature': np.random.normal(25, 5, rows),
        'humidity': np.random.uniform(30, 90, rows),
        'status': np.random.choice(['Active', 'Inactive', 'Pending'], rows),
        'latitude': np.random.uniform(40.7, 40.8, rows),
        'longitude': np.random.uniform(-74.0, -73.9, rows),
        'score': np.random.uniform(0, 100, rows)
    })
    return df

# Generate additional datasets
@st.cache_data
def generate_timeseries_data():
    dates = pd.date_range(start='2023-01-01', periods=365, freq='D')
    return pd.DataFrame({
        'date': dates,
        'metric1': np.random.randn(365).cumsum() + 50,
        'metric2': np.random.randn(365).cumsum() + 30,
        'metric3': np.random.randn(365).cumsum() + 70
    })

# Main Title
st.markdown('<h1 class="main-header">🎯 Complete Streamlit Features Demo</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar Configuration
with st.sidebar:
    st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=100)
    st.title("Navigation & Controls")
    
    # Sidebar widgets
    page = st.radio(
        "Select Section:",
        ["Overview", "Text Elements", "Data Display", "Input Widgets", 
         "Media Elements", "Layouts", "Charts", "Advanced Features"],
        help="Choose a section to explore"
    )
    
    st.divider()
    
    # Sidebar inputs
    st.subheader("Global Settings")
    theme_color = st.color_picker("Theme Color", "#FF4B4B")
    show_code = st.checkbox("Show Code Examples", value=False)
    data_rows = st.slider("Data Rows", 100, 2000, 1000, step=100)
    
    st.divider()
    
    # Sidebar metrics
    st.metric("Session Views", st.session_state.counter, delta=1)
    st.metric("Data Points", data_rows, delta=None)
    
    st.divider()
    
    # Sidebar buttons
    if st.button("Reset Session", type="primary"):
        st.session_state.counter = 0
        st.rerun()
    
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Increment counter
st.session_state.counter += 1

# Generate data
df = generate_sample_data(data_rows)
ts_data = generate_timeseries_data()

# ==================== PAGE: OVERVIEW ====================
if page == "Overview":
    st.header("📊 Application Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", len(df), delta=100)
    with col2:
        st.metric("Categories", df['category'].nunique(), delta=None)
    with col3:
        st.metric("Avg Value", f"{df['value'].mean():.2f}", delta=f"{df['value'].std():.2f}")
    with col4:
        st.metric("Active Status", len(df[df['status']=='Active']), delta=50)
    
    st.divider()
    
    # Container example
    with st.container():
        st.subheader("🎯 Welcome Message")
        st.info("This comprehensive demo showcases **all** Streamlit features including text elements, data display, input widgets, charts, layouts, media elements, and advanced features.")
        
        # Expander
        with st.expander("📖 See Feature Categories"):
            st.write("""
            - **Text Elements**: Titles, headers, markdown, code, LaTeX
            - **Data Display**: DataFrames, tables, metrics, JSON
            - **Input Widgets**: Buttons, sliders, text inputs, file uploaders
            - **Media Elements**: Images, audio, video
            - **Layouts**: Columns, tabs, sidebar, containers
            - **Charts**: Line, bar, area, scatter, maps
            - **Advanced**: Caching, state management, custom components
            """)
    
    st.divider()
    
    # Columns with different content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Quick Data Preview")
        st.dataframe(df.head(10), use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("📊 Category Distribution")
        category_counts = df['category'].value_counts()
        fig = px.pie(values=category_counts.values, names=category_counts.index, 
                     title="Category Split")
        st.plotly_chart(fig, use_container_width=True)
    
    # Progress and status
    st.subheader("⏳ System Status")
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(100):
        progress_bar.progress(i + 1)
        status_text.text(f"Loading system components... {i+1}%")
        time.sleep(0.01)
    
    status_text.success("System ready! ✅")

# ==================== PAGE: TEXT ELEMENTS ====================
elif page == "Text Elements":
    st.markdown('<div class="section-header"><h2>📝 Text Elements</h2></div>', unsafe_allow_html=True)
    
    # Title and headers
    st.title("This is a Title")
    st.header("This is a Header")
    st.subheader("This is a Subheader")
    st.text("This is simple text")
    st.caption("This is a caption with smaller text")
    
    st.divider()
    
    # Markdown
    st.subheader("Markdown Support")
    st.markdown("""
    ### Markdown Features
    - **Bold text** and *italic text*
    - `Inline code` and code blocks
    - [Links to Streamlit](https://streamlit.io)
    - Lists and sublists
        - Nested item 1
        - Nested item 2
    - > Blockquotes
    - Horizontal rules below
    """)
    
    st.divider()
    
    # Code display
    st.subheader("Code Display")
    code = '''def hello_streamlit():
    st.write("Hello, Streamlit!")
    return "Success"
    
result = hello_streamlit()'''
    st.code(code, language='python', line_numbers=True)
    
    st.divider()
    
    # LaTeX
    st.subheader("LaTeX Formulas")
    st.latex(r'''
    E = mc^2
    ''')
    st.latex(r'''
    \int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
    ''')
    
    st.divider()
    
    # Write (universal)
    st.subheader("st.write() - Universal Function")
    st.write("String:", "This is a string")
    st.write("Number:", 42)
    st.write("DataFrame:", df.head(3))
    st.write("Dictionary:", {"key1": "value1", "key2": [1, 2, 3]})
    
    st.divider()
    
    # Status messages
    st.subheader("Status Messages")
    col1, col2 = st.columns(2)
    with col1:
        st.success("This is a success message!")
        st.info("This is an info message!")
    with col2:
        st.warning("This is a warning message!")
        st.error("This is an error message!")
    
    st.exception(ValueError("This is an exception display"))

# ==================== PAGE: DATA DISPLAY ====================
elif page == "Data Display":
    st.markdown('<div class="section-header"><h2>📊 Data Display Elements</h2></div>', unsafe_allow_html=True)
    
    # DataFrame with all features
    st.subheader("DataFrame Display")
    st.dataframe(
        df.head(20),
        use_container_width=True,
        hide_index=False,
        column_config={
            "timestamp": st.column_config.DatetimeColumn("Date/Time", format="DD/MM/YYYY HH:mm"),
            "value": st.column_config.NumberColumn("Value", format="%.2f"),
            "temperature": st.column_config.ProgressColumn("Temperature", min_value=0, max_value=50),
            "score": st.column_config.ProgressColumn("Score", min_value=0, max_value=100),
            "status": st.column_config.TextColumn("Status", help="Current status"),
        },
        height=400
    )
    
    st.divider()
    
    # Static table
    st.subheader("Static Table")
    st.table(df.head(10)[['category', 'value', 'count', 'status']])
    
    st.divider()
    
    # Metrics row
    st.subheader("Metrics Display")
    col1, col2, col3, col4, col5 = st.columns(5)
    metrics_data = df.groupby('category')['value'].mean()
    
    for idx, (col, cat) in enumerate(zip([col1, col2, col3, col4], metrics_data.index)):
        with col:
            st.metric(
                label=f"Category {cat}",
                value=f"{metrics_data[cat]:.2f}",
                delta=f"{np.random.uniform(-10, 10):.2f}",
                delta_color="normal"
            )
    
    st.divider()
    
    # JSON display
    st.subheader("JSON Display")
    sample_json = {
        "user": "demo_user",
        "settings": {
            "theme": "dark",
            "notifications": True,
            "data_points": data_rows
        },
        "stats": df.describe().to_dict()
    }
    st.json(sample_json)
    
    st.divider()
    
    # Data editor
    st.subheader("Data Editor (Editable DataFrame)")
    edited_df = st.data_editor(
        df.head(10)[['category', 'value', 'count', 'status']],
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "category": st.column_config.SelectboxColumn("Category", options=['A', 'B', 'C', 'D']),
            "value": st.column_config.NumberColumn("Value", min_value=0, max_value=200, step=0.1),
            "status": st.column_config.SelectboxColumn("Status", options=['Active', 'Inactive', 'Pending']),
        }
    )
    
    if st.button("Show Edited Data"):
        st.write("Edited DataFrame:", edited_df)

# ==================== PAGE: INPUT WIDGETS ====================
elif page == "Input Widgets":
    st.markdown('<div class="section-header"><h2>🎛️ Input Widgets</h2></div>', unsafe_allow_html=True)
    
    # Buttons
    st.subheader("Buttons")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Standard Button"):
            st.toast("Standard button clicked!")
    with col2:
        if st.button("Primary Button", type="primary"):
            st.toast("Primary button clicked!")
    with col3:
        if st.download_button("Download CSV", data=df.to_csv(index=False), file_name="data.csv", mime="text/csv"):
            st.toast("Download initiated!")
    with col4:
        st.link_button("Visit Streamlit", "https://streamlit.io")
    
    st.divider()
    
    # Text inputs
    st.subheader("Text Inputs")
    col1, col2 = st.columns(2)
    with col1:
        text_input = st.text_input("Text Input", placeholder="Enter text here...")
        text_area = st.text_area("Text Area", placeholder="Enter multiple lines...")
    with col2:
        number_input = st.number_input("Number Input", min_value=0, max_value=100, value=50, step=1)
        password = st.text_input("Password", type="password", placeholder="Enter password...")
    
    st.divider()
    
    # Selection widgets
    st.subheader("Selection Widgets")
    col1, col2 = st.columns(2)
    with col1:
        checkbox = st.checkbox("Checkbox", value=True)
        toggle = st.toggle("Toggle Switch", value=False)
        radio = st.radio("Radio Buttons", ['Option 1', 'Option 2', 'Option 3'], horizontal=True)
    with col2:
        selectbox = st.selectbox("Select Box", ['Choice A', 'Choice B', 'Choice C', 'Choice D'])
        multiselect = st.multiselect("Multi-Select", ['Item 1', 'Item 2', 'Item 3', 'Item 4'], default=['Item 1'])
        select_slider = st.select_slider("Select Slider", options=['Low', 'Medium', 'High', 'Very High'])
    
    st.divider()
    
    # Sliders
    st.subheader("Sliders")
    slider_val = st.slider("Single Value Slider", 0, 100, 50)
    range_val = st.slider("Range Slider", 0.0, 100.0, (25.0, 75.0))
    
    col1, col2 = st.columns(2)
    with col1:
        date_input = st.date_input("Date Input", value=datetime.now())
    with col2:
        time_input = st.time_input("Time Input", value=datetime.now().time())
    
    st.divider()
    
    # File uploader
    st.subheader("File Uploader")
    uploaded_file = st.file_uploader("Choose a file", type=['csv', 'txt', 'json', 'xlsx'], accept_multiple_files=False)
    if uploaded_file is not None:
        st.success(f"File uploaded: {uploaded_file.name}")
        st.write(f"File size: {uploaded_file.size} bytes")
    
    st.divider()
    
    # Camera input
    st.subheader("Camera Input")
    camera_photo = st.camera_input("Take a picture")
    if camera_photo is not None:
        st.image(camera_photo)
    
    st.divider()
    
    # Color picker
    st.subheader("Color Picker")
    color = st.color_picker("Pick a color", "#FF4B4B")
    st.write(f"Selected color: {color}")
    
    # Display all inputs
    with st.expander("📋 View All Input Values"):
        st.json({
            "text_input": text_input,
            "number_input": number_input,
            "checkbox": checkbox,
            "toggle": toggle,
            "radio": radio,
            "selectbox": selectbox,
            "multiselect": multiselect,
            "slider": slider_val,
            "range": range_val,
            "date": str(date_input),
            "time": str(time_input),
            "color": color
        })

# ==================== PAGE: MEDIA ELEMENTS ====================
elif page == "Media Elements":
    st.markdown('<div class="section-header"><h2>🎨 Media Elements</h2></div>', unsafe_allow_html=True)
    
    # Images
    st.subheader("Images")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://via.placeholder.com/300x200?text=Image+1", caption="Sample Image 1", use_container_width=True)
    with col2:
        st.image("https://via.placeholder.com/300x200?text=Image+2", caption="Sample Image 2", use_container_width=True)
    with col3:
        st.image("https://via.placeholder.com/300x200?text=Image+3", caption="Sample Image 3", use_container_width=True)
    
    st.divider()
    
    # Logo
    st.subheader("Logo Display")
    st.logo("https://streamlit.io/images/brand/streamlit-mark-color.png")
    
    st.divider()
    
    # Audio (placeholder)
    st.subheader("Audio Player")
    st.info("Audio player component (requires actual audio file)")
    # st.audio("path/to/audio.mp3")
    
    st.divider()
    
    # Video (placeholder)
    st.subheader("Video Player")
    st.info("Video player component (requires actual video file)")
    # st.video("path/to/video.mp4")
    
    st.divider()
    
    # Matplotlib/Plotly charts
    st.subheader("Chart as Image")
    fig = px.scatter(df.sample(100), x='value', y='temperature', color='category', 
                     title="Scatter Plot Example", size='count')
    st.plotly_chart(fig, use_container_width=True)

# ==================== PAGE: LAYOUTS ====================
elif page == "Layouts":
    st.markdown('<div class="section-header"><h2>📐 Layout Components</h2></div>', unsafe_allow_html=True)
    
    # Columns
    st.subheader("Columns Layout")
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.info("Wide column (2 units)")
        st.write("This column is twice as wide as the others.")
    with col2:
        st.success("Column 2")
        st.write("Standard width")
    with col3:
        st.warning("Column 3")
        st.write("Standard width")
    
    st.divider()
    
    # Tabs
    st.subheader("Tabs")
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Data", "📈 Charts", "⚙️ Settings", "ℹ️ Info"])
    
    with tab1:
        st.write("Data Tab Content")
        st.dataframe(df.head(10))
    
    with tab2:
        st.write("Charts Tab Content")
        fig = px.line(ts_data, x='date', y=['metric1', 'metric2', 'metric3'], title="Time Series")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.write("Settings Tab Content")
        st.slider("Setting 1", 0, 100, 50)
        st.checkbox("Enable Feature")
    
    with tab4:
        st.write("Info Tab Content")
        st.info("This is additional information about the application.")
    
    st.divider()
    
    # Expander
    st.subheader("Expanders")
    with st.expander("Click to expand - Section 1", expanded=True):
        st.write("This is expanded by default")
        st.line_chart(ts_data.set_index('date')['metric1'])
    
    with st.expander("Click to expand - Section 2"):
        st.write("This is collapsed by default")
        st.bar_chart(df.groupby('category')['value'].mean())
    
    st.divider()
    
    # Container
    st.subheader("Containers")
    container = st.container(border=True)
    container.write("This is inside a bordered container")
    container.metric("Metric in Container", 42, delta=5)
    
    st.divider()
    
    # Empty placeholder
    st.subheader("Empty Placeholder (Dynamic)")
    placeholder = st.empty()
    
    if st.button("Update Placeholder"):
        for i in range(5):
            placeholder.write(f"Update {i+1}/5")
            time.sleep(0.5)
        placeholder.success("Updates complete!")
    
    st.divider()
    
    # Popover
    st.subheader("Popover")
    with st.popover("Open Popover"):
        st.write("This is content inside a popover!")
        st.selectbox("Choose option", ['A', 'B', 'C'])
    
    st.divider()
    
    # Dialog (Modal)
    st.subheader("Dialog (Modal)")
    
    @st.dialog("Sample Dialog")
    def show_dialog():
        st.write("This is a modal dialog!")
        st.text_input("Enter something:")
        if st.button("Close"):
            st.rerun()
    
    if st.button("Open Dialog"):
        show_dialog()

# ==================== PAGE: CHARTS ====================
elif page == "Charts":
    st.markdown('<div class="section-header"><h2>📈 Charts & Visualizations</h2></div>', unsafe_allow_html=True)
    
    # Native Streamlit charts
    st.subheader("Native Streamlit Charts")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Line Chart**")
        st.line_chart(ts_data.set_index('date')[['metric1', 'metric2']])
    with col2:
        st.write("**Area Chart**")
        st.area_chart(ts_data.set_index('date')['metric1'])
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Bar Chart**")
        st.bar_chart(df.groupby('category')['value'].mean())
    with col2:
        st.write("**Scatter Chart**")
        chart_df = df[['value', 'temperature']].head(100)
        st.scatter_chart(chart_df, x='value', y='temperature', size='value', color='temperature')
    
    st.divider()
    
    # Plotly charts
    st.subheader("Plotly Charts")
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(df, x='value', color='category', title="Histogram by Category")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.box(df, x='category', y='temperature', title="Box Plot")
        st.plotly_chart(fig, use_container_width=True)
    
    # 3D Scatter
    st.subheader("3D Visualization")
    fig = px.scatter_3d(df.sample(200), x='value', y='temperature', z='humidity', 
                        color='category', size='count', title="3D Scatter Plot")
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Maps
    st.subheader("Map Visualizations")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Simple Map**")
        map_data = df[['latitude', 'longitude']].head(100)
        st.map(map_data, zoom=11)
    
    with col2:
        st.write("**Scatter Map (Plotly)**")
        fig = px.scatter_mapbox(df.head(100), lat='latitude', lon='longitude', 
                                color='category', size='count',
                                zoom=10, height=400,
                                mapbox_style="open-street-map")
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Heatmap
    st.subheader("Heatmap")
    pivot_data = df.pivot_table(values='value', index='category', columns='status', aggfunc='mean')
    fig = px.imshow(pivot_data, title="Heatmap: Value by Category and Status",
                    labels=dict(x="Status", y="Category", color="Value"))
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Vega-Lite (Alternative)
    st.subheader("Vega-Lite Chart")
    chart_data = df[['value', 'temperature', 'category']].head(100)
    st.vega_lite_chart(chart_data, {
        'mark': {'type': 'circle', 'tooltip': True},
        'encoding': {
            'x': {'field': 'value', 'type': 'quantitative'},
            'y': {'field': 'temperature', 'type': 'quantitative'},
            'color': {'field': 'category', 'type': 'nominal'},
            'size': {'value': 100}
        },
    }, use_container_width=True)

# ==================== PAGE: ADVANCED FEATURES ====================
elif page == "Advanced Features":
    st.markdown('<div class="section-header"><h2>🚀 Advanced Features</h2></div>', unsafe_allow_html=True)
    
    # Session State
    st.subheader("Session State Management")
    st.write(f"Page views this session: {st.session_state.counter}")
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add Message"):
            st.session_state.messages.append(f"Message {len(st.session_state.messages) + 1}")
    with col2:
        if st.button("Clear Messages"):
            st.session_state.messages = []
    
    st.write("Messages:", st.session_state.messages)
    
    st.divider()
    
    # Caching
    st.subheader("Caching Demonstration")
    
    @st.cache_data
    def expensive_computation(n):
        time.sleep(2)  # Simulate expensive computation
        return np.random.randn(n).cumsum()
    
    st.write("First run will take 2 seconds, subsequent runs are instant:")
    start_time = time.time()
    result = expensive_computation(100)
    elapsed = time.time() - start_time
    st.write(f"Computation took {elapsed:.2f} seconds")
    st.line_chart(result)
    
    st.divider()
    
    # Form
    st.subheader("Forms (Batch Input Submission)")
    with st.form("sample_form"):
        st.write("Fill out this form:")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120, value=25)
        category = st.selectbox("Category", ['A', 'B', 'C'])
        submitted = st.form_submit_button("Submit Form")
        
        if submitted:
            st.success(f"Form submitted! Name: {name}, Age: {age}, Category: {category}")
    
    st.divider()
    
    # Spinner and Progress
    st.subheader("Loading Indicators")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Show Spinner"):
            with st.spinner("Processing..."):
                time.sleep(2)
            st.success("Done!")
    
    with col2:
        if st.button("Show Progress"):
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)
            st.success("Complete!")
    
    st.divider()
    
    # Toast notifications
    st.subheader("Toast Notifications")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Show Success Toast"):
            st.toast("Success! 🎉", icon="✅")
    with col2:
        if st.button("Show Info Toast"):
            st.toast("Information", icon="ℹ️")
    with col3:
        if st.button("Show Warning Toast"):
            st.toast("Warning!", icon="⚠️")
    
    st.divider()
    
    # Balloons and Snow
    st.subheader("Celebrations")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎈 Show Balloons"):
            st.balloons()
    with col2:
        if st.button("❄️ Show Snow"):
            st.snow()
    
    st.divider()
    
    # Stop execution
    st.subheader("Execution Control")
    show_stop_demo = st.checkbox("Show stop execution demo")
    if show_stop_demo:
        st.warning("Content below this will not render if you click 'Stop Here'")
        if st.button("Stop Here"):
            st.stop()
        st.info("This only shows if you didn't click the stop button")
    
    st.divider()
    
    # Rerun
    st.subheader("Rerun Application")
    if st.button("🔄 Rerun App"):
        st.rerun()
    
    st.divider()
    
    # Fragment (Partial Rerun)
    st.subheader("Fragment - Partial Reruns")
    st.write("Fragments allow you to rerun only specific sections without rerunning the entire app")
    
    @st.fragment
    def fragment_counter():
        if 'fragment_count' not in st.session_state:
            st.session_state.fragment_count = 0
        
        st.write(f"Fragment counter: {st.session_state.fragment_count}")
        if st.button("Increment (Only Fragment Reruns)", key="frag_btn"):
            st.session_state.fragment_count += 1
    
    fragment_counter()
    st.write(f"Main app counter: {st.session_state.counter} (doesn't change when fragment reruns)")
    
    st.divider()
    
    # Echo - Show code
    st.subheader("Echo - Display Code Being Executed")
    with st.echo():
        # This code will be displayed and executed
        sample_data = pd.DataFrame({
            'x': range(10),
            'y': np.random.randn(10)
        })
        st.write("Data generated inside echo block:")
        st.dataframe(sample_data)
    
    st.divider()
    
    # Help
    st.subheader("Help Documentation")
    if st.button("Show help for st.write"):
        st.help(st.write)
    
    st.divider()
    
    # Query Parameters
    st.subheader("Query Parameters")
    st.write("You can get and set URL query parameters:")
    st.code("""
# Get query params
params = st.query_params
st.write(params)

# Set query params
st.query_params['key'] = 'value'
st.query_params['page'] = '2'
""", language='python')
    
    current_params = st.query_params
    st.write("Current query params:", dict(current_params))
    
    st.divider()
    
    # Status container
    st.subheader("Status Container")
    if st.button("Run Task with Status"):
        with st.status("Downloading data...", expanded=True) as status:
            st.write("Searching for data...")
            time.sleep(1)
            st.write("Found data!")
            time.sleep(1)
            st.write("Processing...")
            time.sleep(1)
            status.update(label="Download complete!", state="complete", expanded=False)
    
    st.divider()
    
    # Chat interface
    st.subheader("Chat Messages")
    st.write("Streamlit has built-in chat message components:")
    
    with st.chat_message("user"):
        st.write("Hello! This is a user message.")
    
    with st.chat_message("assistant"):
        st.write("Hi! This is an assistant response.")
    
    with st.chat_message("user", avatar="🧑‍💻"):
        st.write("Messages can have custom avatars too!")
    
    # Chat input
    user_input = st.chat_input("Type a message...")
    if user_input:
        with st.chat_message("user"):
            st.write(user_input)
        with st.chat_message("assistant"):
            st.write(f"Echo: {user_input}")

# Footer
st.divider()
st.markdown("---")
st.caption("🎯 Complete Streamlit Demo Application | Built with Streamlit")
st.caption(f"Session ID: {id(st.session_state)} | Page Views: {st.session_state.counter}")