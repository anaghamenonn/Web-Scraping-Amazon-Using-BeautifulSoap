import requests
from bs4 import BeautifulSoup
import datetime
import csv
import smtplib
import time

def get_soup(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1"
    }
    page = requests.get(url, headers=headers)
    return BeautifulSoup(page.content, "html.parser")

def get_product_info(soup):
    title = soup.find(id='productTitle').get_text().strip()
    price = soup.find(id='priceblock_ourprice').get_text().strip()[1:]
    return title, price

def write_to_csv(data):
    header = ['Title', 'Price', 'Date']
    with open('AmazonWebScraperDataset.csv', 'a+', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow(header)
        writer.writerow(data)

def check_price():
    URL = 'https://www.amazon.com/Funny-Data-Systems-Business-Analyst/dp/B07FNW9FGJ/ref=sr_1_3?dchild=1&keywords=data%2Banalyst%2Btshirt&qid=1626655184&sr=8-3&customId=B0752XJYNL&th=1'
    soup = get_soup(URL)
    title, price = get_product_info(soup)
    today = datetime.date.today()
    data = [title, price, today]
    write_to_csv(data)

def send_mail():
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login('anagha@gmail.com', 'your_password_here')

    subject = "The Shirt you want is below $15! Now is your chance to buy!"
    body = "Alex, This is the moment we have been waiting for. Now is your chance to pick up the shirt of your dreams. Don't mess it up! Link here: https://www.amazon.com/Funny-Data-Systems-Business-Analyst/dp/B07FNW9FGJ/ref=sr_1_3?dchild=1&keywords=data+analyst+tshirt&qid=1626655184&sr=8-3"

    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail('AlexTheAnalyst95@gmail.com', 'your_email@example.com', msg)

# Run this only once to create the CSV file with header
write_to_csv([])

# Continuously check the price every day
while True:
    check_price()
    # Check if the price is below a certain threshold and send email if it is
    # if float(price) < 15:
    #     send_mail()
    time.sleep(86400)  # Wait for a day before checking again
