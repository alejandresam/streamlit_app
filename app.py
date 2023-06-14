import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import base64


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


def display_numerical_stats(df, selected_column):
    st.subheader("Numerical Column Statistics")

    five_num_summary = df[selected_column].describe()
    st.write(five_num_summary)

    fig, ax = plt.subplots()
    sns.histplot(data=df, x=selected_column, kde=True)
    ax.set_title("Distribution Plot")
    ax.set_xlabel(selected_column)
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    # Save the plot as a PNG file
    save_plot_as_png(fig, "plot.png")


def display_categorical_stats(df, selected_column):
    st.subheader("Categorical Column Statistics")

    category_proportions = df[selected_column].value_counts(normalize=True)
    st.write(category_proportions)

    fig, ax = plt.subplots()
    sns.countplot(data=df, x=selected_column)
    ax.set_title("Bar Plot")
    ax.set_xlabel(selected_column)
    ax.set_ylabel("Count")
    st.pyplot(fig)

    # Save the plot as a PNG file
    save_plot_as_png(fig, "plot.png")


def save_plot_as_png(fig, filename):
    fig.savefig(filename, dpi=300)


def download_file(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV File</a>'
    st.markdown(href, unsafe_allow_html=True)


def main():
    st.title("Exploratory Data Analysis (EDA)")

    web_apps = st.sidebar.selectbox("Select Web Apps", ("Exploratory Data Analysis",))

    if web_apps == "Exploratory Data Analysis":
        uploaded_file = st.sidebar.file_uploader("Choose a CSV file")

        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)

                st.sidebar.subheader("Navigation")
                page = st.sidebar.radio("Go to", ("Dataset Stats", "Numerical Stats", "Categorical Stats"))

                if page == "Dataset Stats":
                    st.subheader("Dataset Statistics")
                    display_dataset_stats(df)

                elif page == "Numerical Stats":
                    numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns

                    if len(numerical_columns) > 0:
                        selected_column = st.selectbox("Select a column", numerical_columns)
                        display_numerical_stats(df, selected_column)

                        # Download the plot
                        st.sidebar.markdown("---")
                        st.sidebar.subheader("Download Plot Image")
                        download_button = st.sidebar.button("Download Plot")
                        if download_button:
                            save_plot_as_png(plt.gcf(), "plot.png")
                            st.sidebar.markdown(get_download_link("plot.png", "Download Plot"), unsafe_allow_html=True)
                    else:
                        st.write("No numerical columns found in the dataset.")

                elif page == "Categorical Stats":
                    categorical_columns = df.select_dtypes(include=['object']).columns

                    if len(categorical_columns) > 0:
                        selected_column = st.selectbox("Select a column", categorical_columns)
                        display_categorical_stats(df, selected_column)

                        # Download the plot
                        st.sidebar.markdown("---")
                        st.sidebar.subheader("Download Plot Image")
                        download_button = st.sidebar.button("Download Plot")
                        if download_button:
                            save_plot_as_png(plt.gcf(), "plot.png")
                            st.sidebar.markdown(get_download_link("plot.png", "Download Plot"), unsafe_allow_html=True)
                    else:
                        st.write("No categorical columns found in the dataset.")

            except pd.errors.ParserError:
                st.write("Invalid CSV file. Please upload a valid CSV file.")

    st.sidebar.markdown("---")
    st.sidebar.subheader("Download Processed Data")
    if 'df' in locals():
        download_file(df, "processed_data.csv")


def get_download_link(file_path, link_text):
    with open(file_path, "rb") as file:
        contents = file.read()
        b64 = base64.b64encode(contents).decode()
        href = f'<a href="data:file/png;base64,{b64}" download="{file_path}">{link_text}</a>'
        return href


if __name__ == "__main__":
    main()
