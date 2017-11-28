# Set download destinations
pic_dest = "C:/project/imgbot/pics/"
thumbnail_dest = "C:/project/imgbot/thumbnails/"

# Set up reddit instance
reddit = praw.Reddit('bot1')

# Check or create csv file to save data
csv_file = 'replies.csv'
col_list = ['Post_ID', 'Post_title', 'Post_URL', 'Subreddit', 'Post_Date', 'Post_Score', 'Bot_Reply', 'Reply_Date', 'Classification', 'Calories', 'Reply_Score']

if os.path.isfile('replies.csv'):
   # if there is a log, load it as a pandas dataframe
    reply_log = pd.read_csv(csv_file)
else:
    reply_log = pd.DataFrame(columns=col_list)

reply_log.set_index('Post_ID', inplace=True)

# Set up list of subreddits to monitor
subreddit_list = 'food+HealthyFood' # not in use
subreddit = reddit.subreddit('pythonforengineers')
