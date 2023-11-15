# Stock-Trading-News

## Requirements
pip install requests   
pip install twilio

## What is Stock Trading News?
It is an automated script implemented using twilio package; os and requests python modules.

## How does it work?
The script gets data from ALPHA VINTAGE API: https://www.alphavantage.co and NEWS API: https://newsapi.org.   
In order to use these API-s, the user needs to create an account respectively to each API and create 2 API Keys.
The API Keys are saved as environmental variables:  

ALPHA VINTAGE API KEY:    
STOCKS_API_KEY= os.environ.get("API_KEY_STOCKS") 

NEWS API KEY:    
NEWS_API_KEY=os.environ.get("NEWS_API_KEY")     

ALPHA VINTAGE API uses as required parameters:   
1. Required: function    
The time series of your choice. In this case, function=TIME_SERIES_DAILY. Sometimes the time series might become a premium feature, and the user need to find a new one that is free.    
2. Required: symbol    
The name of the equity of your choice. For example: symbol=TSLA    
3. Required: apikey.   
Your API key.      

NEWS API uses as required parameters:   
1. apiKey (required).      
Your API key.
2.  q (optional).    
Keywords or phrases to search for in the article title and body.

Step 1: The scrip calculates the difference in percentage between yesteday and the day before yesterday by using the data received from ALPHA VINTAGE API for a target compay.      
Step 2: If the difference in percentage between yesteday and the day before yesterday > 1, then the script searches for articles containing the target company in the title using NEWS API, and filter the first three ones.    
Step 3: Use Twilio to send 3 text messages with an article each.

## Twilio account setup
Create an account at: https://console.twilio.com/        
Note: Only the phone number used to register will serve as the phone number that will  get the text message rain alert.   
Upon registering and validating the Twilio account, the user has access to the 1) Account SID, 2) AUTH TOKEN, 3) The Twilio phone number assigned and a free trial credit of $15. 

![Screenshot 2023-11-11 at 2 52 28 PM](https://github.com/CoboAr/Rain-Alert-Automated-Script/assets/144629565/1d794533-bb8f-44c1-97b9-e20d8f49f3b4)    

This is an example how to use Twilio package in python:

![Screenshot 2023-11-11 at 2 59 34 PM](https://github.com/CoboAr/Rain-Alert-Automated-Script/assets/144629565/90d6bcde-4a11-430f-bf18-9de0c2a22ab5)

Account SID, AUTH TOKEN, Virtual Twilio number and Verified Twilio number are used in the script as environmental variables: 

TWILIO_ACCOUNT_SID= os.environ.get("ACCOUNT_SID_TWILIO")      
TWILIO_AUTH_TOKEN=os.environ.get("AUTH_TOKEN_TWILIO")      
VIRTUAL_TWILIO_NUMBER = os.environ.get("VIRTUAL_TWILIO_NUMBER")    
VERIFIED_TWILIO_NUMBER = os.environ.get("VERIFIED_NUMBER")

Enjoy! And please do let me know if you have any comments, constructive criticism, and/or bug reports.
## Author
## Arnold Cobo






