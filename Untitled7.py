# Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
a
# Set page configuration
st.set_page_config(
    page_title="Obesity Risk Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load your dataset (replace 'obesity.csv' with your actual file path)
@st.cache_data
def load_data():
    return pd.read_csv('E:\\DATASET PYTHON\\ObesityDataSet_raw_and_data_sinthetic.csv')

df = load_data()

# ============================================
# Dashboard Title and Description
# ============================================
st.title("📊 Obesity Risk Factors Analysis Dashboard")
st.markdown("""
**Objective:** Explore key factors influencing obesity levels (NObeyesdad) through comprehensive visual analysis.
""")

# ============================================
# Helper Functions for Visualizations
# ============================================
def plot_target_distribution():
    """Distribution of target variable (NObeyesdad)"""
    fig = px.bar(df['NObeyesdad'].value_counts().reset_index(), 
                 x='NObeyesdad', y='count', 
                 color='count',
                 title='Distribution of Obesity Levels',
                 labels={'count': 'Number of Cases', 'NObeyesdad': 'Obesity Category'})
    fig.update_layout(title_x=0.5)
    return fig

def plot_age_weight_relationship():
    """Relationship between Age, Weight, and Obesity Level"""
    fig = px.scatter(df, x='Age', y='Weight', 
                    color='NObeyesdad',
                    title='Age vs Weight Colored by Obesity Level',
                    hover_data=['Height', 'Gender'],
                    color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(title_x=0.5)
    return fig

def plot_feature_distributions():
    """Feature distributions split by obesity level"""
    fig = make_subplots(rows=2, cols=2,
                       subplot_titles=('Height Distribution', 'Weight Distribution',
                                      'Physical Activity Frequency', 'Water Consumption'))
    
    # Height Distribution
    fig.add_trace(go.Box(x=df['NObeyesdad'], y=df['Height'], 
                        name='Height', marker_color='#1f77b4'),
                 row=1, col=1)
    
    # Weight Distribution
    fig.add_trace(go.Box(x=df['NObeyesdad'], y=df['Weight'], 
                        name='Weight', marker_color='#ff7f0e'),
                 row=1, col=2)
    
    # Physical Activity
    fig.add_trace(go.Violin(x=df['NObeyesdad'], y=df['FAF'],
                           name='Physical Activity', box_visible=True,
                           marker_color='#2ca02c'),
                 row=2, col=1)
    
    # Water Consumption
    fig.add_trace(go.Violin(x=df['NObeyesdad'], y=df['CH2O'],
                           name='Water Consumption', box_visible=True,
                           marker_color='#d62728'),
                 row=2, col=2)
    
    fig.update_layout(height=800, title_text="Feature Distributions by Obesity Level", 
                     title_x=0.5, showlegend=False)
    return fig

def plot_categorical_relationships():
    """Categorical feature relationships with obesity level"""
    fig = make_subplots(rows=2, cols=2,
                       specs=[[{'type':'domain'}, {'type':'domain'}],
                             [{'type':'domain'}, {'type':'domain'}]],
                       subplot_titles=('Gender Distribution', 'Family History',
                                      'High Caloric Food Consumption', 'Alcohol Consumption'))
    
    # Gender
    gender_df = df.groupby(['NObeyesdad', 'Gender']).size().reset_index(name='count')
    fig.add_trace(go.Pie(labels=gender_df['Gender'], values=gender_df['count'],
                        name="Gender", hole=0.4, showlegend=False),
                 row=1, col=1)
    
    # Family History
    family_df = df.groupby(['NObeyesdad', 'family_history_with_overweight']).size().reset_index(name='count')
    fig.add_trace(go.Pie(labels=family_df['family_history_with_overweight'], 
                        values=family_df['count'], hole=0.4, showlegend=False),
                 row=1, col=2)
    
    # High Caloric Food (FAVC)
    favc_df = df.groupby(['NObeyesdad', 'FAVC']).size().reset_index(name='count')
    fig.add_trace(go.Pie(labels=favc_df['FAVC'], values=favc_df['count'],
                        hole=0.4, showlegend=False),
                 row=2, col=1)
    
    # Alcohol Consumption (CALC)
    calc_df = df.groupby(['NObeyesdad', 'CALC']).size().reset_index(name='count')
    fig.add_trace(go.Pie(labels=calc_df['CALC'], values=calc_df['count'],
                        hole=0.4, showlegend=False),
                 row=2, col=2)
    
    fig.update_layout(height=800, title_text="Categorical Feature Relationships", 
                     title_x=0.5)
    return fig

# ============================================
# Dashboard Layout
# ============================================
# Row 1: Key Metrics
st.header("🔑 Key Metrics Overview")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Samples", len(df))
with col2:
    st.metric("Unique Obesity Categories", df['NObeyesdad'].nunique())
with col3:
    st.metric("Average Age", f"{df['Age'].mean():.1f} years")
with col4:
    st.metric("Average BMI", f"{df['Weight'].mean()/((df['Height'].mean()/100)**2):.1f}")

# Row 2: Target Distribution
st.header("🎯 Target Variable Analysis")
st.plotly_chart(plot_target_distribution(), use_container_width=True)

# Row 3: Feature Distributions
st.header("📈 Feature Distributions by Obesity Level")
st.plotly_chart(plot_feature_distributions(), use_container_width=True)

# Row 4: Relationships
st.header("🤝 Feature Relationships")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(plot_age_weight_relationship(), use_container_width=True)
with col2:
    st.plotly_chart(plot_categorical_relationships(), use_container_width=True)

# ============================================
# Insights Section
# ============================================
st.header("💡 Key Insights")
with st.expander("Show Analysis Insights"):
    st.markdown("""
    1. **Obesity Distribution:** The dataset shows varying prevalence across different obesity categories
    2. **Age-Weight Relationship:** Clear positive correlation between age and weight across categories
    3. **Physical Activity:** Lower obesity levels associated with higher physical activity frequency
    4. **Family History:** Strong connection between family history of overweight and obesity levels
    5. **Gender Differences:** Significant variations in obesity distribution between genders
    6. **Dietary Factors:** High caloric food consumption shows strong relationship with obesity categories
    """)

# ============================================
# Run with: streamlit run obesity_dashboard.py
# ============================================


# In[ ]:




