import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a File")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    df = preprocessor.processor(data)

    st.dataframe(df)

    #. fetch unique user
    user_list = df['user'].unique().tolist()

    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show anylysis wrt ",user_list)


    if st.sidebar.button("Show Analysis"):

        num_mssg = helper.fetch_stats(selected_user,df)

        col1 ,col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_mssg)
