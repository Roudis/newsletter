import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import pandas as pd
import csv
import os
from datetime import datetime, timedelta

# Variables setup
emails_file = "emails.csv"
csv_file = "newsletter.csv"
subject = "CMMS-Boas Newsletter"
sender = "cmmsuse@gmail.com"
password = "ibhvkjwnnnclsnsx"
base_path = "./"
archive_path = os.path.join(base_path, "Archive")
source_file = os.path.join(base_path, csv_file)
utils = os.path.join(base_path, "Utils")

def make_sub_list():
    subscribers = []
    with open(os.path.join(utils, emails_file), newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        test = reader
        for row in reader:
            email = row[0]
            subscribers.append(email)
    return subscribers

def make_body(csv_file):
    body = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Newsletter</title>
        <style>
            /* Basic styling, you can modify as per your design */
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f2f2f2;
            }
            .container {
                width: 80%;
                max-width: 800px;
                margin: 20px auto;
                background-color: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            .banner {
                width: 100%;
                height: auto;
                border-radius: 10px;
            }
            .row {
                margin-top: 20px;
                border-bottom: 1px solid #ccc;
                padding-bottom: 20px;
            }
            .row:last-child {
                border-bottom: none;
                padding-bottom: 0;
            }
            .row img {
                max-width: 100px;
                height: auto;
                float: left;
                margin-right: 10px;
                border-radius: 5px;
            }
            .row-content {
                overflow: hidden;
            }
            .row-content h2 {
                margin-top: 0;
                font-size: 18px;
            }
            .row-content p {
                margin: 5px 0;
            }
            .row-content a {
                color: #007bff;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <img class="banner" src="cid:banner" alt="Banner">

    """

    news_df['cid'] = None
    # Iterrate over the csv rows for distinct items
    for index,row in news_df.iterrows():
        if pd.isna(row['Image']):
            row['Image'] = 'image.png'

        row['cid'] = "<image" + str(index) + ">"

        body +=  f"""
                <div class="row">
                    <div class="row-content">
                        <img src="cid:{row["cid"][1:-1]}" alt="{row['cid']}">
                        <h2>{row['Name']} </h2>
                        <p>Tag: <strong>#{row['Tag1'] }</strong> <strong>#{row['Tag2'] }</strong></p>
                        <p>Description: {row['Description'] }</p>
                        <p>Location: <em>{row['Location'] }</em></p>
                        <p>Date: {row['Expiration Date'] }</p>
                        <p><a href={row['Link'] }>Read more</a></p>
                    </div>
                </div>
                """
        
        news_df.loc[index] = row

    body += """
        </div>
    </body>
    </html>
    """
    return body, news_df

def attach_images(message,news_df):
    fp = open(os.path.join(utils, 'banner.jpg'), 'rb')
    image = MIMEImage(fp.read())
    fp.close()
    image.add_header('Content-ID', '<banner>')
    message.attach(image)
   
    for index, row in news_df.iterrows():
    # We assume that the image file is in the same directory that you run your Python script from
        try:
            fp = open(row['Image'], 'rb')
        except:
            fp = open(os.path.join(utils, "image.png"), 'rb')
        image = MIMEImage(fp.read())
        fp.close()

        # Specify the  ID according to the img src in the HTML part
        image.add_header('Content-ID', row['cid'])
        message.attach(image)
    return message


def send_email(subject, message, sender, subscribers, password):
    msg = message
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(subscribers)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, subscribers, msg.as_string())
    print("Message sent!")

# Initiate message
message_alt = MIMEMultipart("alternative")
message = MIMEMultipart('related')
message.attach(message_alt)

# Make list of emails to send to
subscribers = make_sub_list()
news_df = pd.read_csv(csv_file, delimiter=";")

# Make the body of the email
body, news_df = make_body(news_df)
body = MIMEText(body, "html")
message_alt.attach(body)

# Incert images in the body
message = attach_images(message,news_df)

send_email(subject, message, sender, subscribers, password)

# Get today's date and time in YYYY-MM-DD_HH-MM format
now = datetime.now()
start_of_week = now - timedelta(days=now.weekday() + 1)
formatted_datetime = start_of_week.strftime("%Y-%U_%b-%d")
rename_date = now.strftime("%Y%m%d%H%M%S")

# Define folder name and path
folder_name = f"{formatted_datetime}"
folder_path = os.path.join(archive_path, folder_name)
file_path = os.path.join(folder_path, 'newsletter' + rename_date + '.csv')


# Check if the folder already exists
if not os.path.exists(folder_path):
  # Create the folder
  os.makedirs(folder_path)
  print(f"Created folder: {folder_path}")


# Rename and move images in archive
for index,row in news_df.iterrows():
    image = row["Image"]
    try:
        os.rename(os.path.join(base_path, image), os.path.join(folder_path, image.split(".")[0] + rename_date + "." + image.split(".")[1]))
    except FileNotFoundError:
        print("Error: File not found or path is incorrect.")
    except Exception as e:
        print(f"Error occurred: {e}")


# Rename images for the current file 
news_df['Image'] = news_df['Image'].apply(lambda x: x.split(".")[0] + rename_date + "." + x.split(".")[1])
news_df = news_df.drop('cid', axis=1)

# Write the new file to the archive folder 
news_df.to_csv(file_path, index=False, sep=';')



# Define the header row with your desired tags
header = news_df.columns
next_newsletter = pd.DataFrame(columns=header)
next_newsletter.to_csv(os.path.join(base_path, csv_file),sep=";",index=False)

print("newsletter.csv file created with the header row.")
