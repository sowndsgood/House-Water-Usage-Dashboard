import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image

# Load the water usage data from the CSV file
csv_filename = 'april_water_usage_data.csv'
usage_df = pd.read_csv(csv_filename)

# Convert the 'Timestamp' column to datetime format
usage_df['Timestamp'] = pd.to_datetime(usage_df['Timestamp'])

# Sidebar to display the current date and time
st.sidebar.write("## Current Date and Time")
current_datetime = datetime.now()
st.sidebar.write(f"Date: {current_datetime.date()}")
st.sidebar.write(f"Time: {current_datetime.time().strftime('%H:%M:%S')}")


image = Image.open('water.png')

st.sidebar.image(image)

# Sidebar content
st.sidebar.title("About the App")
st.sidebar.markdown("""
This app provides insights into water usage data for different devices over a period of time.
- View total and proportional water usage for each device.
- Analyze water usage trends over time.
- Get useful tips based on your water consumption.
""")

image2 = Image.open('banner.png')
new_image = image2.resize((600, 400))
st.image(new_image)


# Set the title of the app
st.title("Residential Water Usage Analyzer Dashboard")

st.write("Stay on top of your home’s water usage with the Smart Water Monitoring Dashboard. This app provides real-time data and detailed reports to help you conserve water and reduce utility bills.")


# Plot bar chart for total water usage of each device
st.write("### Bar Chart: Total Water Usage for Each Device in April")
fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
usage_df.groupby('Device Name')['Usage (liters)'].sum().plot(kind='bar', color='skyblue', ax=ax_bar)
ax_bar.set_xlabel('Device Name')
ax_bar.set_ylabel('Total Usage (liters)')
ax_bar.set_title('Total Water Usage for Each Device in April')
ax_bar.set_xticklabels(ax_bar.get_xticklabels(), rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig_bar)

# Plot pie chart for proportion of total water usage for each device
st.write("### Pie Chart: Proportion of Total Water Usage for Each Device in April")
fig_pie, ax_pie = plt.subplots(figsize=(8, 8))
usage_df.groupby('Device Name')['Usage (liters)'].sum().plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=plt.cm.tab10.colors, ax=ax_pie)
ax_pie.axis('equal')
ax_pie.set_title('Proportion of Total Water Usage for Each Device in April')
plt.tight_layout()
st.pyplot(fig_pie)

# Dropdown for selecting a device
device_names = usage_df['Device Name'].unique()
selected_device = st.selectbox("Select a device to view its water usage over time:", device_names)

# Plot scatter plot with points joined by lines for the selected device
st.write(f"### Water Usage Over Time for Device: {selected_device}")
device_data = usage_df[usage_df['Device Name'] == selected_device]
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(device_data['Timestamp'], device_data['Usage (liters)'], marker='o', linestyle='-')
ax.set_xlabel('Timestamp')
ax.set_ylabel('Usage (liters)')
ax.set_title(f'Water Usage Over Time for Device: {selected_device} (April)')
ax.grid(True)
plt.tight_layout()
st.pyplot(fig)

# Generate and display tips based on water usage
def generate_tips(total_usage):
    tips = []
    if total_usage > 1000:
        tips.append("Consider installing water-efficient fixtures to reduce usage.")
    if total_usage > 500:
        tips.append("Check for leaks regularly to prevent unnecessary water wastage.")
    if total_usage < 500:
        tips.append("Great job! You're using water efficiently. Keep up the good work.")
    if 'garden' in device_names:
        tips.append("Use a drip irrigation system for your garden to save water.")
    return tips

# Calculate total water usage for all devices
total_usage = usage_df['Usage (liters)'].sum()
tips = generate_tips(total_usage)

# Display tips
st.write("### Water Usage Tips")
for tip in tips:
    st.write(f"- {tip}")
