import streamlit as st

import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data sweeper",layout='wide')
st.title("Data sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization")

uploaded_files = st.file_uploader("Upload you files (CVS or Excel):", type=["csv","xlsx"],accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext =os.path.splitext(file.name)[-1].lower()

        if file_ext==".csv":
            df = pd.read_csv(file)
        elif file_ext ==".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # Display info about the file 
        st.write(f"**File Name:**{file.name}")
        st.write(f"**File Size:**{file.size/1024}") 

        #show 5 rows of our df
        st.write("Preview the Head of the DataFrame")
        st.dataframe(df.head())

        #options for dta cleaning 
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                 if st.button(f"Remove Duplicates from {file.name}"):
                     df.drop_duplicates(inplace=True)
                     st.write("Duplicates Removed!")

                     with col2:
                         if st.button(f"Fill Missing Values for {file.name}"):
                             numeric_cols = df.select_dtypes(include=["number"]).columns
                             df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                             st.write("Missing Values have been Filled!")

                             # choose specific colums to keep or convert    
                             st.subheader("Select Columns to Convert")  
                             columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
                             df = df [columns]

                             # create some visualizations   
                             st.subheader("data visualization")
                             if st.checkbox(f"show visualization for {file.name}"):
                                 st.br_char(df.select_dtypes(include="number").iloc[:,:2])

                                 # convert the file cvs to excel 
                                 st.subheader("conversion options ")
                                 conversion_type = st.radio (f"convert {file.name}to:", ["CVS","Excel"], key=file.name)
                                 if st.button(f"convert{file.name}"):
                                     if conversion_type=="CSV": 
                                         df.to_csv(buffer,index=False)
                                         file_name=file.name,replace(file_ext,".csv")
                                         mime_type= "text/csv"

                                     elif conversion_type== "Excel":
                                         df.to_excel(buffer, index =False)
                                         file_name= file.name.replace(file_ext,".xlsx") 
                                         mime_type= "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                         buffer.seek(0)

                                         #download_button 
                                         st.download_button(
                                         label=f"Download {file.name} as {conversion_type}",
                                         data=buffer,
                                         filename =file_name,
                                         mime=mime_type
                                         )

                                         st.success("All files processed!")
