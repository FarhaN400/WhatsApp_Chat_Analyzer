from urlextract import URLExtract
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
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'users':'name','count':'percent'})
    return x,df