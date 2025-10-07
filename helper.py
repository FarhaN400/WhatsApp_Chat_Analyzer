from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

def fetch_stats(selected_user,df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    # fetch the no of mssg
    num_mssg = df.shape[0]

    # fetch the no of words
    words = []
    for mssg in df['message']:
            words.extend(mssg.split())  

    # fetch the no of media
    num_media_mssg = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch no of link
    extractor = URLExtract()
    links = []
    for mssg in df['message']:
        links.extend(extractor.find_urls(mssg))
    return num_mssg , len(words) , num_media_mssg , len(links)

def most_busy_user(df):
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    #temp = temp[temp['message'] != 'This message was deleted\n']
    x = temp['user'].value_counts().head()
    df = round((temp['user'].value_counts()/temp.shape[0])*100,2).reset_index().rename(columns={'users':'name','count':'percent'})
    return x,df

def create_wordcloud(selected_user,df):

    f = open('stop_hinglish.txt','r')
    stop_word = f.read()
     
    if selected_user != "Overall":
        df = df[df['user']==selected_user]

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'This message was deleted\n']

    def remove_stop_word(message):
        y=[]
        for words in message.lower().split():
            if words not in stop_word:
                y.append(words)
        return " ".join(y)
    
    temp['message'] = temp['message'].apply(remove_stop_word)

    df_wc = wc.generate(temp['message'].str.cat(sep=""))
    return df_wc

def most_common_word(selected_user,df):

    if selected_user != "Overall":
        df = df[df['user']==selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'This message was deleted\n']

    f = open('stop_hinglish.txt','r')
    stop_word = f.read()

    words=[]
    for mssg in temp['message']:
        for j in mssg.lower().split():
            if j not in stop_word:
                words.append(j)

    return pd.DataFrame(Counter(words).most_common(20))

def emoji_helper(selected_user,df):

    if selected_user != "Overall":
        df = df[df['user']==selected_user]

    emojis = []
    for mssg in df['message']:
        for c in mssg:
            if c in emoji.EMOJI_DATA:
                emojis.extend(c)
    
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df
    
def monthly_timeline(selected_user,df):

    if selected_user != "Overall":
        df = df[df['user']==selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + " - " + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != "Overall":
        df = df[df['user']==selected_user]
    
    daily_timeline = df.groupby(['only_date']).count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap
