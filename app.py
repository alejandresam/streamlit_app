import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

web_apps = st.sidebar.selectbox("Select Web Apps", ("Exploratory Data Analysis", "Distributions"))

if web_apps == "Exploratory Data Analysis":
    uploaded_file = st.sidebar.file_uploader("Choose a file")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        show_df = st.checkbox("Show Data Frame", key="disabled")

        if show_df:
            st.write(df)

        column_type = st.sidebar.selectbox('Select Data Type', ("Numerical", "Categorical", "Bool", "Date"))

        if column_type == "Numerical":
            numerical_column = st.sidebar.selectbox('Select a Column', df.select_dtypes(include=['int64', 'float64']).columns)

            # Histogram
            st.subheader("Histogram")
            hist_bins = st.slider('Number of Bins', min_value=5, max_value=150, value=30)
            hist_title = st.text_input('Set Title', 'Histogram')
            hist_xtitle = st.text_input('Set x-axis Title', numerical_column)

            fig, ax = plt.subplots()
            ax.hist(df[numerical_column], bins=hist_bins, edgecolor="black")
            ax.set_title(hist_title)
            ax.set_xlabel(hist_xtitle)
            ax.set_ylabel('Count')

            st.pyplot(fig)

            # Download the plot
            st.subheader("Download Plot")
            download_button = st.button("Download Histogram Plot")

            if download_button:
                filename = f"{numerical_column}_histogram.png"
                fig.savefig(filename, dpi=300)
                st.download_button(label="Download", data=filename, file_name=filename)

# Function to display dataset statistics
def display_dataset_stats(df):
    num_rows = len(df)
    num_cols = len(df.columns)
    num_numerical = len(df.select_dtypes(include=['int64', 'float64']).columns)
    num_categorical = len(df.select_dtypes(include=['object']).columns)
    num_bool = len(df.select_dtypes(include=['bool']).columns)

    st.write(f"Number of rows: {num_rows}")
    st.write(f"Number of columns: {num_cols}")
    st.write(f"Number of numerical variables: {num_numerical}")
    st.write(f"Number of categorical variables: {num_categorical}")
    st.write(f"Number of boolean variables: {num_bool}")


# Function to display five number summary and distribution plot
def display_numerical_stats(df, selected_column):
    st.subheader("Numerical Column Statistics")

    # Five number summary
    five_num_summary = df[selected_column].describe()
    st.write(five_num_summary)

    # Distribution plot
    fig, ax = plt.subplots()
    sns.histplot(data=df, x=selected_column, kde=True)
    ax.set_title("Distribution Plot")
    ax.set_xlabel(selected_column)
    ax.set_ylabel("Frequency")
    st.pyplot(fig)


# Function to display categorical proportions and bar plot
def display_categorical_stats(df, selected_column):
    st.subheader("Categorical Column Statistics")

    # Proportions of each category level
    category_proportions = df[selected_column].value_counts(normalize=True)
    st.write(category_proportions)

    # Customized bar plot
    fig, ax = plt.subplots()
    sns.countplot(data=df, x=selected_column)
    ax.set_title("Bar Plot")
    ax.set_xlabel(selected_column)
    ax.set_ylabel("Count")
    st.pyplot(fig)


def main():
    st.title("Exploratory Data Analysis (EDA)")

    uploaded_file = st.file_uploader("Choose a CSV file")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Display dataset statistics
        st.subheader("Dataset Statistics")
        display_dataset_stats(df)

        # Select a column from the dataset
        selected_column = st.selectbox("Select a column", df.columns)

        if df[selected_column].dtype == "object":
            # Categorical column
            display_categorical_stats(df, selected_column)
        else:
            # Numerical column
            display_numerical_stats(df, selected_column)


if __name__ == "__main__":
    main()
