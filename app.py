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
        
        st.title("Top Statistics")

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

        # Monthly_TimeLine
        monthly_timeline = helper.monthly_timeline(selected_user,df)
        st.title("Monthly Timeline")
        fig , ax = plt.subplots()
        ax.plot(monthly_timeline['time'],monthly_timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily_timeline
        daily_timeline = helper.daily_timeline(selected_user,df)
        st.title("Daily Timeline")
        fig ,ax= plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        # Activity Map
        st.title("Activity Map")
        col1 , col2 = st.columns(2)

        with col1:
            st.header("Most Busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig ,ax= plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most Busy month")
            busy_month = helper.month_activity_map(selected_user,df)
            fig ,ax= plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

         
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # Finding the busiest person in group(Group level)
        if selected_user == "Overall":
            st.title("Most Busy Person")

            x , new_df = helper.most_busy_user(df)        
            fig , ax = plt.subplots()

            col1 , col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
               st.dataframe(new_df)

        #WordCloud
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig , ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Most Common Word
        st.header("Most common Word")
        most_common_df = helper.most_common_word(selected_user,df)
        fig1 , ax1 = plt.subplots()
        ax1.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig1)


        # Emoji
        emoji_df = helper.emoji_helper(selected_user,df)

        st.title("Emoji Analysis")

        col1 , col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig , ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct='%0.2f')
            st.pyplot(fig)