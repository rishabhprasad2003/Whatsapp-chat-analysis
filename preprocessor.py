import re
import pandas as pd

def preprocess(data):
    #pattern = r'\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}[\u202f\s][AP]M - '
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}[\u202f\s](?:[APap][Mm]) - '

    messages = re.split(pattern, data)[1:]

    dates = re.findall(pattern, data)
    # Removing any extra non-breaking spaces for uniform output
    cleaned_dates = [date.replace('\u202f', ' ') for date in dates]

    df = pd.DataFrame({'user_message':messages, 'message_date':cleaned_dates})

    #convert message_date type
    try:
        df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p - ')
    except:
        df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M %p - ')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['day_name'] = df['date'].dt.day_name()
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour+1))
        else:
            period.append(str(hour) + '-' + str(hour+1))
    df['period'] = period

    df = df[df['message'] != 'null\n']
    
    return df