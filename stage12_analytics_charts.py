"""
WEEK 12 - NumPy, Pandas, Matplotlib Analytics Dashboard
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_mock_data():
    """Simulate a dataset for analytical visualization"""
    return pd.DataFrame({
        'Department': np.random.choice(['CS', 'IT', 'ECE', 'MECH'], 100),
        'Category': np.random.choice(['Academic', 'Hostel', 'Exam', 'Admin'], 100),
        'Status': np.random.choice(['Pending', 'In Progress', 'Resolved'], 100),
        'Month': np.random.choice(['Jan', 'Feb', 'Mar', 'Apr'], 100)
    })

def create_dashboard():
    df = generate_mock_data()
    print("--- 1. Analytics Dashboard (Pandas DataFrame) ---")
    print(df.describe(include='all'))
    
    # Setup Figure and Subplots
    print("\n--- 2. Generating Graphical Dashboards ---")
    fig = plt.figure(figsize=(12, 5))
    
    # 1. Bar Chart: Category-wise Distribution
    ax1 = fig.add_subplot(1, 3, 1)
    category_counts = df['Category'].value_counts()
    category_counts.plot(kind='bar', color='skyblue', ax=ax1)
    ax1.set_title("Grievances by Category")
    ax1.tick_params(axis='x', rotation=45)
    
    # 2. Pie Chart: Status Distribution
    ax2 = fig.add_subplot(1, 3, 2)
    status_counts = df['Status'].value_counts()
    status_counts.plot(kind='pie', autopct='%1.1f%%', colormap='Pastel1', ax=ax2)
    ax2.set_title("Resolution Status")
    ax2.set_ylabel("")  # Hide Y Label for pies
    
    # 3. Bar Chart: Department load
    ax3 = fig.add_subplot(1, 3, 3)
    dept_counts = df['Department'].value_counts()
    dept_counts.plot(kind='bar', color='lightgreen', ax=ax3)
    ax3.set_title("Department Comparison")
    
    # Finalize Layout
    plt.tight_layout()
    plot_file = "stage12_analytics_dashboard.png"
    plt.savefig(plot_file)
    print(f"[SUCCESS] Graphical Analytics generated and rendered to: {plot_file}")

if __name__ == "__main__":
    create_dashboard()
