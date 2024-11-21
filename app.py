import streamlit as st
import pandas as pd
import os
import altair as alt


@st.cache_data
def load_data(folder_path=r"C:\Documents\pythonProject\streamlit\names"):
    # Initialize an empty DataFrame
    all_data = pd.DataFrame()

    # Verify folder existence
    if not os.path.exists(folder_path):
        st.error(f"The folder '{folder_path}' does not exist.")
        print(f"Folder does not exist: {folder_path}")
        return all_data

    # List files in folder for debugging
    files = os.listdir(folder_path)
    print(f"Files in folder: {files}")

    # Iterate through all files in the folder
    for filename in files:
        if filename.endswith(".txt"):  # Ensure it's a text file
            file_path = os.path.join(folder_path, filename)
            try:
                data = pd.read_csv(
                    file_path,
                    header=None,  # No header in the file
                    names=["Name", "Sex", "Births"]  # Assign column names
                )

                # Append data to the main DataFrame
                all_data = pd.concat([all_data, data], ignore_index=True)
            except Exception as e:
                st.error(f"Error reading file '{filename}': {e}")
                print(f"Error in {filename}: {e}")
        else:
            print(f"Skipping non-txt file: {filename}")

    if all_data.empty:
        print("No data was loaded. Check your folder path and file formats.")

    return all_data


# Attempt to load data
data = load_data()


# Check if data is empty
if data.empty:
    st.error("No data found. Please check the folder and ensure it contains valid files.")
    st.stop()

# Debug information
st.write("Data successfully loaded:")
st.write(data.head())

# Sidebar configuration
st.sidebar.header("Configuration")
selected_gender = st.sidebar.radio("Select Gender", ["M", "F"], index=0)
birth_count_range = st.sidebar.slider("Select Birth Count Range", 0, int(data["Births"].max()), (100, 1000))
selected_name = st.sidebar.text_input("Enter a Name to Explore", "Emma")

# Filter data based on user input
filtered_data = data[
    (data["Sex"] == selected_gender) &
    (data["Births"] >= birth_count_range[0]) &
    (data["Births"] <= birth_count_range[1])
    ]

name_data = filtered_data[filtered_data["Name"].str.lower() == selected_name.lower()]

# Tabs for different app sections
tab1, tab2 = st.tabs(["Name Trends", "Dataset Overview"])

# Tab 1: Name Trends
with tab1:
    st.header("Name Trends")

    if name_data.empty:
        st.write(f"No data found for the name '{selected_name}' in the selected range.")
    else:
        # Bar chart for occurrences of the selected name
        chart = alt.Chart(name_data).mark_bar().encode(
            x="Name:O",
            y="Births:Q",
            tooltip=["Name", "Births"]
        ).properties(title=f"Occurrences of '{selected_name}'")
        st.altair_chart(chart, use_container_width=True)

        # Summary of the selected name
        st.subheader(f"Summary for '{selected_name}'")
        st.write(name_data.describe())

        # Table of top 5 names
        st.subheader("Top 5 Names by Births")
        top_names = filtered_data.groupby("Name")["Births"].sum().sort_values(ascending=False).head(5).reset_index()
        st.table(top_names)

# Tab 2: Dataset Overview
with tab2:
    st.header("Dataset Overview")
    st.write("View the first few rows of the dataset:")
    st.write(filtered_data.head())

    st.write("Summary Statistics:")
    st.write(filtered_data.describe())

# Additional container for insights
with st.container():
    st.write("Additional Insights")
    top_names_by_gender = filtered_data.groupby("Name")["Births"].sum().sort_values(ascending=False).head(10)
    st.write(f"Top 10 {selected_gender} names in the dataset:")
    st.table(top_names_by_gender)

# Deployment Instructions in Sidebar
st.sidebar.write("#### Deployment Instructions")
st.sidebar.write("1. Save the dataset into a file (e.g., 'names.csv').")
st.sidebar.write("2. Run `streamlit run app.py` to start the app.")
