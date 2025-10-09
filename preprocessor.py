import re
import pandas as pd

def processor(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s[ap]m)?\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    cleaned_dates = df['message_date'].str.strip().str.rstrip(' -')

    try:
        df['date'] = pd.to_datetime(cleaned_dates, dayfirst=True)
    except (ValueError, TypeError):
        df['date'] = pd.to_datetime(cleaned_dates, dayfirst=False)

    df.drop(columns=['message_date'], inplace=True)

    users = []
    message_list = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message, 1)
        if len(entry) > 1:
            users.append(entry[1])
            message_list.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            message_list.append(entry[0])

    df['user'] = users
    df['message'] = message_list
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['only_date'] = df['date'].dt.date
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    df.drop(columns=['date'], inplace=True)

    return df