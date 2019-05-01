# exchange-rate-loader
This project fetches exchange rate data from an API  for a provided base currency and displays its exchange rate for a specified duration. It also calculates the avergae value of each currency during that time period.

# Assumptions

I will be pushing fresh data everytime the API is called.

# Architecture
The architecture is pretty straightforward. I am runnning the app to fetch exchange rate  data from an API. This data is then cleansed and pushed into an SQL table. This data could then be used to query all the exchange rates from the past. This would be a single source of truth for the exchange rates

The Architecture involves the following libraries:

- Python 3.7
- Pandas
- sqlalchemy('in memory sql database')
- built in request library
- built in unittest library for testing

# What can be done better

1. Dockerise the entire application
2. Schedule it as part of a daily cron to fetch legacy data
3. Better handling of sensitive credentials.

# How to run this application

```sh
### Python Application to do fetch legacy exchange rate data
### Clone the repository [https://github.com/ashshetty90/exchange-rate-loader.git]

### First things First . Create a virtual environment and run the tests to make sure we are all set

$ virtualenv exchange-rate-loader -p /usr/local/bin/python3.7
    
### and then activate the virtual environment
$ exchange-rate-loader/bin/activate

### install dependecies from Pipfile
$ pipenv install

### run the tests
 python -m unittest tests/exchange_rate_loader_test.py
 
### run the app 
python main.py

# Screenshots

(https://github.com/ashshetty90/exchange-rate-loader/blob/master/images/pip-env-install.png)

![TEST CASES](https://github.com/ashshetty90/exchange-rate-loader/blob/master/images/test-cases.png)

![OUTPUT](https://github.com/ashshetty90/exchange-rate-loader/blob/master/images/output.png)


