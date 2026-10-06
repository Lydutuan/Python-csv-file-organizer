import streamlit as st
import pandas as pd
import altair as alt
st.title("CSV Data Explorer")

file=st.file_uploader('Upload file here')
if file is not None:
    df = pd.read_csv(file)
    df = df.loc[:, ~df.columns.str.contains('Unnamed')]
    df = df.dropna()
    with st.expander('Preview'):
        st.dataframe(df.head())
    with st.expander("Info"):
        col1, col2 = st.columns(2)
        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
    with st.expander("Summary"):
        st.dataframe(df.describe())
    with st.expander("Missing Value"):
        null = df.isnull()
        st.dataframe(null.sum())
    with st.expander("Chart"):
        select_column = st.selectbox("Choose a column",df.columns)
        counts = df[select_column].value_counts().head(10).reset_index()
        counts.columns = ['Category', 'Count']
        chart = alt.Chart(counts).mark_bar().encode(
            y = alt.Y('Category',sort='-x',title=None,axis=alt.Axis(labelLimit=500)),
            x=alt.X('Count', title='Count')
            ).properties(
            width=700,
            height=500
            )
        st.altair_chart(chart, use_container_width= True)
    with st.expander("Histogram"):
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        
        if len(numeric_cols) > 0:
            selected_num = st.selectbox("Choose a numeric column", numeric_cols)
            
            chart = alt.Chart(df).mark_bar().encode(
                alt.X(selected_num, bin=True),
                y='count()'
            ).properties(width=700, height=400)
            
            st.altair_chart(chart, use_container_width=True)
        else:
            st.write("No numeric columns found.")
    csv=df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download cleaned CSV file",
        data=csv,
        file_name='cleaned_data.csv',
        mime='text_csv'
        )