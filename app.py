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

    #st.dataframe(df)

    #. fetch unique user
    user_list = df['user'].unique().tolist()

    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show anylysis wrt ",user_list)


    if st.sidebar.button("Show Analysis"):

        # Stats
        num_mssg , words , num_media_mssg ,num_links= helper.fetch_stats(selected_user,df)

        col1 ,col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown('<p style="text-align: center; font-size: 26px;">Total Messages</p>', unsafe_allow_html=True)
            st.markdown(f'<h1 style="text-align: center;">{num_mssg}</h1>', unsafe_allow_html=True)

        # Total Words
        with col2:
            st.markdown('<p style="text-align: center; font-size: 26px;">Total Words</p>', unsafe_allow_html=True)
            st.markdown(f'<h1 style="text-align: center;">{words}</h1>', unsafe_allow_html=True)

        # Media Shared
        with col3:
            st.markdown('<p style="text-align: center; font-size: 26px;">Media Shared</p>', unsafe_allow_html=True)
            st.markdown(f'<h1 style="text-align: center;">{num_media_mssg}</h1>', unsafe_allow_html=True)

        # Links Shared
        with col4:
            st.markdown('<p style="text-align: center; font-size: 26px;">Links Shared</p>', unsafe_allow_html=True)
            st.markdown(f'<h1 style="text-align: center;">{num_links}</h1>', unsafe_allow_html=True)


        
        # Finding the busiest person in group(Group level)
        if selected_user == "Overall":
            st.markdown('<p style="text-align: left; font-size: 26px;">Most Busy Person</p>', unsafe_allow_html=True)

            x , new_df = helper.most_busy_user(df)        
            fig , ax = plt.subplots()

            col1 , col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
               st.dataframe(new_df)


    
