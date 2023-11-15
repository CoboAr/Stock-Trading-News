import os
import requests
from twilio.rest import Client

# TARGET COMPANY
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
# Twilio account sid and authentification token
TWILIO_ACCOUNT_SID= os.environ.get("ACCOUNT_SID_TWILIO")
TWILIO_AUTH_TOKEN=os.environ.get("AUTH_TOKEN_TWILIO")

# Virtual Twilio Number and Verified Twilio Number Environmental Variables
VIRTUAL_TWILIO_NUMBER = os.environ.get("VIRTUAL_TWILIO_NUMBER")
VERIFIED_TWILIO_NUMBER = os.environ.get("VERIFIED_NUMBER")

# Use https://www.alphavantage.co
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCKS_API_KEY= os.environ.get("API_KEY_STOCKS")

# Use https://newsapi.org
NEWS_ENDPOINT="https://newsapi.org/v2/everything"
NEWS_API_KEY=os.environ.get("NEWS_API_KEY")

stock_parameters = {
    # "function":"TIME_SERIES_DAILY" availability might differ over time
    # It is advised that the other functions provided in the https://www.alphavantage.com should be checked for free use.
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK_NAME,
    "apikey":STOCKS_API_KEY,
}

# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
response_stocks=requests.get(STOCK_ENDPOINT,params=stock_parameters)
response_stocks.raise_for_status()
stock_data=response_stocks.json()
# Get the stocks price of yesterday
yesterday_closing_price=float(stock_data["Time Series (Daily)"]["2023-11-10"]["4. close"])
# Get the stocks price of the day before yesterday
day_before_yesterday_closing_price=float(stock_data["Time Series (Daily)"]["2023-11-09"]["4. close"])
print(yesterday_closing_price)
print(day_before_yesterday_closing_price)

#Find  difference between yesterday and the day before yesterday and assign up_down accordingly depending on the result
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

#Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percentage_change=round(abs(((yesterday_closing_price-day_before_yesterday_closing_price)/day_before_yesterday_closing_price)*100))
print(percentage_change)

#If difference percentage is greater than
# 1 then send a request to the newsapi and get the first three articles related to the company we are interested
if (percentage_change>1):
    news_parameters = {
        "qInTitle": "tesla",
        "apiKey": NEWS_API_KEY
    }
    response_news_articles = requests.get (NEWS_ENDPOINT, params=news_parameters)
    response_news_articles.raise_for_status ()
    articles_data = response_news_articles.json ()["articles"]
    # Get the first 3 news pieces for the COMPANY_NAME.
    three_articles = articles_data[0:3]

# Use Twilio to send a seperate message with each article's title and description to your phone number.
# Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles = [f"{STOCK_NAME}: {up_down}{percentage_change}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for
     article in three_articles]

    client = Client (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages \
            .create (
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_TWILIO_NUMBER
        )
        print (message.status)

#Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

