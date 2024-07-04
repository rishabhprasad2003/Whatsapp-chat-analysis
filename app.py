import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm, rcParams
import seaborn as sns
import os


st.sidebar.title("Whatsapp chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    
    df = preprocessor.preprocess(data)

    st.dataframe(df)


    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages, num_calls = helper.fetch_stats(selected_user, df)

        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)
        
        with col3:
            st.header("Media shared")
            st.title(num_media_messages)
        
        with col4:
            st.header("Calls Made")
            st.title(num_calls)


        #Monthly Timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='g')
        plt.ylabel('Messages')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy week day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.ylabel('Messages')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        with col2:
            st.header("Most Busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.ylabel('Messages')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Activity heatmap
        st.title("Weekly activity map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        colorbar = ax.collections[0].colorbar
        colorbar.set_label('Number of Messages', rotation=270, labelpad=20)
        st.pyplot(fig)

        # Busiest users
        if selected_user == 'Overall':
            st.title("Most Busy Users")
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                plt.ylabel("Messages")
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # Wordcloud
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title("most common words")
        most_common_df = helper.most_common_words(selected_user, df)
        #st.dataframe(most_common_df) 

        fig, ax = plt.subplots()

        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Emoji analysis
        st.title("Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            # fig, ax = plt.subplots()
            # # Set font properties for the pie chart
            # plt.rcParams['font.family'] = 'NotoEmoji-VariableFont_wght.ttf'
            # plt.rcParams['font.sans-serif'] = 'NotoEmoji-VariableFont_wght.ttf'
            # ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            # st.pyplot(fig)

            fig, ax = plt.subplots()
            #fpath = os.path.join(rcParams['datapath'], r"NotoEmoji-VariableFont_wght.ttf")
            fpath = 'NotoEmoji-VariableFont_wght.ttf'
            prop = fm.FontProperties(fname=fpath)
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(), textprops={'fontproperties': prop})
            st.pyplot(fig)

