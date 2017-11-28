# Import basic packages
import os
from urllib.request import urlretrieve, urlopen
import time

# Import data science packages
import pandas as pd

# Import reddit related packages
import praw
import pdb
import re

# Import CNN
#from neuralnetwork import food_CNN

# Import helper functions
from helpers import create_log, download, submission_is_image, save_reply, send_reply

# Set download destinations
pic_dest = "C:/project/imgbot/pics/"
thumbnail_dest = "C:/project/imgbot/thumbnails/"

# Create csv file to save data
csv_file = 'replies.csv'
col_list = ['Post_ID', 'Post_title', 'Post_URL', 'Subreddit', 'Post_Date', 'Post_Score', 'Bot_Reply', 'Reply_Date', 'Classification', 'Calories', 'Reply_Score']
reply_log = create_log(csv_file, col_list)

# Set up reddit instance and subreddits
reddit = praw.Reddit('bot1')
subreddit_list = 'food+HealthyFood' # not in use
subreddit = reddit.subreddit('pythonforengineers')

########################################################################################
### Subreddit loop and reply function
### Scan through subreddits and classifies food images
########################################################################################

for submission in subreddit.hot(limit=5):

    if submission.id not in reply_log.Post_ID.values:  # Check that the bot hasn't already replied to this post
        if submission.stickied: # Ignore stickied posts e.g. rules
            continue

        # Download and save picture and thumbnail
        if submission_is_image:
            filename = submission.id + ".jpg"
            download(submission.url, filename, pic_dest)
            download(submission.thumbnail, filename, thumbnail_dest)

            # Call CNN to classify and estimate calories
            #classification, calories = food_CNN(pic_dest, filename)
            classification, calories = (None, None)

            # Reply to post and generate new log entry
            text = "Hi" # TODO: learn to format
            new_reply = send_reply(text, submission, classification, calories)

            # Save reply in dataframe and csv file
            save_reply(new_reply, reply_log, csv_file)

        else:
            print("Already replied to post")

########################################################################################
### Reply score update function
### Scan previous replies and records score for any reply made more than 24 hours ago
########################################################################################

for i in reply_log.index:

    elapsed_hours = (time.time() - reply_log['Reply_Date'][i]) / 3600 # 3600 seconds per hour
    saved_reply_score = reply_log['Reply_Score'][i]

    if saved_reply_score == None and elapsed_hours >= 24:
        reply = reddit.comment(reply_log['Bot_Reply'][i])
        score_update = reply.score
        reply_log['Reply_Score'][i] = score_update
        reply_log.to_csv(csv_file, encoding='utf-8', index=False) # Save dataframe as .csv file
