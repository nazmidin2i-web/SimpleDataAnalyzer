import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Data Analyzer", page_icon="🔍", layout ="wide")

st.title('🔍 Analyze Your Data')
st.write("📂 Upload A **CSV** or An **EXCEL** Files to Explore Your Data Interactively")

# for uploading file
uploaded_file = st.file_uploader("Upload A CSV or An Excel File",type=["csv",'xlsx','xlsm','xlsb'])

if uploaded_file is not None :
    try:
            if uploaded_file.name.endswith(".csv"):
                data = pd.read_csv(uploaded_file)
            else:
                data = pd.read_excel(uploaded_file, engine="openpyxl")

    except Exception as e:
        st.error("Could Not Read Given File. Please Check the File Format")
        st.exception(e)
        st.stop()

    st.success("✔️ File Uploaded Successfully. ")
    st.write("### Preview of Data")
    st.dataframe(data.head())

    st.write("### 🔍Data Overview")
    st.write("Number of Rows : ", data.shape[0])
    st.write("Number of Columns : ", data.shape[1])
    st.write("Number of Missing Values : ", data.isnull().sum().sum()) # calculate the sum of sum of missing values for all data
    st.write("Number of Duplicated Values : ", data.duplicated().sum())   
    
    st.write("### 🔍Complete Summary of Dataset")
    buffer = io.StringIO()
    data.info(buf=buffer)
    i = buffer.getvalue()
    st.text(i)

    # Create Buttons for Summary of Dataset Charts
    all1, numec, nonumec= st.columns(3) # create 3 section/column

    with all1:
        all_button = st.button("View Statistical Summary of Dataset")

    with numec:
        numec_button = st.button("View Statistical Summary For Numerical Feature Only")

    with nonumec:
        nonumec_button = st.button("View Statistical Summary For Non-Numerical Feature Only")

    if all_button:
        st.write("### 🔍Complete Statistical Summary of Dataset")
        st.dataframe(data.describe())

    if numec_button:
        st.write("### 🔍Complete Statistical Summary For Numerical Feature Only")
        num_cols = data.select_dtypes(include=['number']).columns

        if len(num_cols) > 0:
            st.dataframe(data.describe(include=['number']))
        else:
            st.info("No Numerical features found in this dataset.")
    
    if nonumec_button:
        st.write("### 🔍Complete Statistical Summary For Non-Numerical Feature Only")
        non_num_cols = data.select_dtypes(include=['bool', 'object']).columns

        if len(non_num_cols) > 0:
            st.dataframe(data.describe(include=['bool', 'object']))
        else:
            st.info("No non-numerical (bool/object) features found in this dataset.")

    #Multi Select Box
    st.write("### ✂️ Please Select The Desired Column For Analysis")
    selected_columns = st.multiselect('Choose Columns',data.columns.tolist()) # data.columns = shows all column, .tolist - convert the column name to list

    if selected_columns:
        st.dataframe(data[selected_columns].head())
    else:
        st.info("No Columns Selected. Showing Full Dataset")
        st.dataframe(data.head())

    st.write("### 📊 Data Visualisation")
    st.write("Select **Columns** For Data Visualisation")
    st.warning("WARNING! Some Graph might not function correctly based on the selected data.")

    columns = data.columns.tolist()
    x_axis = st.selectbox("Select Columns For X-Axis",options=columns)
    y_axis = st.selectbox("Select Columns For Y-Axis",options=columns)

    # Create Buttons for Diff Charts
    col1, col2, col3= st.columns(3) # create 3 section/column

    with col1:
        line_button = st.button("Click Here to Generate The Line Graph")

    with col2:
        scatter_button = st.button("Click Here to Generate The Scatter Graph")

    with col3:
        bar_button = st.button("Click Here to Generate The Bar Graph")

    col4, col5, col6= st.columns(3) # create 3 section/column

    with col4:
        heat_button = st.button("Click Here to Generate The Heatmap")

    with col5:
        histo_button = st.button("Click Here to Generate The Histogram Graph")

    with col6:
        pie_button = st.button("Click Here to Generate The Pie Chart")

    if line_button:
        st.write("### Showing A Line Graph")
        fig,ax = plt.subplots()
        ax.plot(data[x_axis],data[y_axis])
        ax.set_xlabel(x_axis)
        ax.tick_params(axis='x', labelrotation=90)
        ax.set_ylabel(y_axis)
        ax.set_title(f"Line Graph of {x_axis} vs {y_axis}")
        st.pyplot(fig)

    if scatter_button:
        st.write("### Showing A Line Graph")
        fig,ax = plt.subplots()
        ax.scatter(data[x_axis],data[y_axis])
        ax.set_xlabel(x_axis)
        ax.tick_params(axis='x', labelrotation=90)
        ax.set_ylabel(y_axis)
        ax.set_title(f"Scatter Graph of {x_axis} vs {y_axis}")
        st.pyplot(fig)

    if bar_button:
        st.write("### Showing A Line Graph")
        fig,ax = plt.subplots()
        ax.bar(data[x_axis],data[y_axis])
        ax.set_xlabel(x_axis)
        ax.tick_params(axis='x', labelrotation=90)
        ax.set_ylabel(y_axis)
        ax.set_title(f"Bar Graph of {x_axis} vs {y_axis}")
        st.pyplot(fig)      

    # Create Buttons for Heatmap, Histogram, Box Plot

    if heat_button:
        st.write("### Showing Heatmap (Correlation Matrix)")
        fig, ax = plt.subplots()

        corr = data.select_dtypes(include='number').corr()
        im = ax.imshow(corr)

        ax.set_xticks(range(len(corr.columns)))
        ax.set_yticks(range(len(corr.columns)))
        ax.set_xticklabels(corr.columns, rotation=90, ha="right")
        ax.set_yticklabels(corr.columns)

        fig.colorbar(im, ax=ax)
        ax.set_title("Correlation Heatmap")

        st.pyplot(fig)

    if histo_button:
        st.write("### Showing Histogram")
        fig, ax = plt.subplots()
        ax.hist(data[x_axis])
        ax.set_xlabel(x_axis)
        ax.tick_params(axis='x', labelrotation=90)
        ax.set_title(f"Histogram of {x_axis}")
        st.pyplot(fig)

    if pie_button:
        st.write("### Showing Pie Chart")
        fig, ax = plt.subplots()
        ax.pie(data[y_axis], labels=data[x_axis], autopct='%1.1f%%')
        ax.set_title(f"Pie Chart of {x_axis}")
        st.pyplot(fig)

else:
    st.info("Please Upload A CSV or An Excel File to Get Started")  


    
