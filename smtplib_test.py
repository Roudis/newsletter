import smtplib
from email.mime.text import MIMEText
import csv
import os
from datetime import datetime

emails_file = "emails.csv"
subscribers = []
subject = "Email Subject"
sender = "cmmsuse@gmail.com"
password = "ibhvkjwnnnclsnsx"

with open(emails_file, newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    test = reader
    for row in reader:
        email = row[0]
        subscribers.append(email)


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
        <img class="banner" src="banner.jpg" alt="Banner">

"""
# for item in items:
body +=  """
        <div class="row">
            <div class="row-content">
                <img src="image1.jpg" alt="Image 1">
                <h2>News Title 1</h2>
                <p>Tag: <strong>#Tag1</strong></p>
                <p>Description: Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
                <p>Location: <em>City, Country</em></p>
                <p>Date: <time datetime="2024-04-01">April 1, 2024</time></p>
                <p><a href="#">Read more</a></p>
            </div>
        </div>
        
"""
body += """
    </div>
</body>
</html>
"""


def send_email(subject, body, sender, subscribers, password):
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(subscribers)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, subscribers, msg.as_string())
    print("Message sent!")



send_email(subject, body, sender, subscribers, password)

# Get today's date and time in YYYY-MM-DD_HH-MM format
now = datetime.now()
formatted_datetime = now.strftime("%Y-%m-%d_%H-%M")

# Define folder name and path
folder_name = f"Todays_Take_{formatted_datetime}"
folder_path = os.path.join("/Users/croudis/Documents/Projects/Mail-offer/Archive", folder_name)

# Define source file path
source_file = "/Users/croudis/Documents/Projects/Mail-offer/newsletter.csv"

# Check if the folder already exists
if not os.path.exists(folder_path):
  # Create the folder
  os.makedirs(folder_path)
  print(f"Created folder: {folder_path}")

# Check if the source file exists
if os.path.isfile(source_file):
  # Move the file to the created folder
  destination_file = os.path.join(folder_path, "newsletter.csv")
  os.replace(source_file, destination_file)
  print(f"Moved newsletter.csv to: {destination_file}")
else:
  print("newsletter.csv not found in the source location.")

# Define the header row with your desired tags
header = ["Tag1", "Tag2", "Name", "Description", "Location", "Expiration Date", "Link"]

# Open the CSV file in write mode
with open("newsletter.csv", "w", newline="") as csvfile:
  writer = csv.writer(csvfile, delimiter=";")

  # Write the header row
  writer.writerow(header)

print("newsletter.csv file created with the header row.")
