# Download helper that checks if file already exists
def download(url, filename, destination):
    """
    Download file from <url>
    :param url: URL to file
    :param filename: name that file is saved as (also checks for duplications)
    :param destination: Local file save path
    """
    full_destination = destination + filename

    if not url:
        return print("invalid URL. Skipping...")

    if not os.path.isfile(full_destination):
                urlretrieve(url, full_destination)

    return print("Downloaded ", url)


# Helper to check if submission is an image
def submission_is_image(url):
    """
    Check if the submission is an image. Returns boolean
    :param url: URL of Reddit submission
    """
    response = urlopen(url)
    type = response.headers.get_content_maintype()
    if type == 'image':
        return True
    else:
        return False


# Helper to save a new reply entry or update existing entry in dataframe and csv
def save_reply(data, save_dataframe, csv_file):
    """
    Save submission and reply data to reply_log dataframe and csv file
    :param data: list of data in same format/structure as reply_log
    :param save_dataframe: the target dataframe to update with new data
    :param csv_file: filename of the csv_file for saving
    """
    col_list = list(save_dataframe.columns.values)
    new_entry = pd.DataFrame([new_row], columns=col_list)
    new_entry.set_index('Post_ID', inplace=True)

    if new_entry.index[0] in save_dataframe.index:
        save_dataframe.update(new_entry)
    else:
        save_dataframe = save_dataframe.append(new_entry)

    save_dataframe.to_csv(csv_file, encoding='utf-8', index=False) # Save dataframe as .csv file
    return print("Reply added to dataframe and saved to {}".format(csv_file))


# Helper to reply to a submission with classification data, and return new entry to log
def send_reply(text, submission, classification=None, calories=None):
    """
    Save submission and reply data to reply_log dataframe and csv file
    :param text: list of data in same format/structure as reply_log
    :param submission: the target dataframe to update with new data
    :param classification: food type / classification to save in record
    :param calories: calories score to save in record. Should be same as posted in reply text
    """
    reply_date = time.time()
    reply_id = submission.reply(text)
    reply = reddit.comment(reply_id)
    reply_score = None
    new_row = [submission.id,
               submission.title,
               submission.url,
               submission.subreddit.name,
               submission.created_utc,
               submission.score,
               reply.id,
               reply_date,
               classification,
               calories,
               reply_score]
    return new_row
