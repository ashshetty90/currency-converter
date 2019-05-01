import yaml,requests,json
import pandas as pd
from sqlalchemy import create_engine
from pandas.io.json import json_normalize

class ExchangeRateLoader():

    """
    This method does the API call to fetch the currency exchange rate data with respect to the base currency

    """
    def fetch_exchange_rate_data(self,config_yaml_path):

        try:
            with open(config_yaml_path,'r') as stream:
                """
                Fetching configuration params required to make API call 
                """
                config_file =  yaml.load(stream)
                api_url = config_file['api_url']
                access_key = config_file['access_key']
                base_currency = config_file['base_currency']
                start_date = config_file['start_date']
                end_date = config_file['end_date']
                query_string = {}
                query_string['access_key'] = access_key
                query_string['base'] = base_currency
                query_string['start_date'] = start_date
                query_string['end_date'] = end_date
                headers = {}
                headers['cache-control'] = 'no-cache'
                headers['access_key'] = access_key
                payload = ""
                """
                Making a request to the API
                """
                response = requests.request("GET", api_url, data=payload, headers=headers, params=query_string)
                """
                Converting the data into json and returning only if the status code is 200
                """
                if response.status_code == 200:
                    return json.loads(response.text)
                else:
                    """
                    Raising Connection Error in case of non 200 status codes
                    """
                    response.raise_for_status()
        except Exception as e:
            print("Error while fetching data from the API ",e)
        return

    """
    This method accepts the response data and does basic cleaning of the data
    """
    def process_exchange_rate_data(self,response_data):
        try:
            response_dataframe = pd.DataFrame.from_dict(response_data)
            response_dataframe.rename(columns={'base': 'base_code'})
            # removing unwanted columns from the dataframe
            response_dataframe = response_dataframe.drop(columns=['timestamp','success'])

            """
            doing below manipulation as exchange currency is getting pushed into the index of the dataframe
            """
            response_dataframe.index.names = ['currency_code']
        except Exception as e:
            print("Error while processing API Data",e)
        return response_dataframe

    """
    using sql lite to build tables on top of the pandas dataframe and returning the query results
    """
    def populate_db_table(self,clean_df,query):
        try:
            engine = create_engine('sqlite://', echo=False)
            table_name = "exchange_rate_lookup"
            clean_df.to_sql(table_name, con=engine)
        except Exception as e:
            print("Error while populating database table",e)
        return engine.execute(query.format(table_name)).fetchall()



    def calculte_average_currency_value(self):

        """
        Using hardcoded json string as the API key is for the free trial and does not allow fetching legacy data
        """
        json_string = """{
    "success": true,
    "timeseries": true,
    "start_date": "2012-05-01",
    "end_date": "2012-05-03",
    "base": "EUR",
    "rates": {
        "2012-05-01":{
          "USD": 1.322891,
          "AUD": 1.278047,
          "CAD": 1.302303
        },
        "2012-05-02": {
          "USD": 1.315066,
          "AUD": 1.274202,
          "CAD": 1.299083
        },
        "2012-05-03": {
          "USD": 1.314491,
          "AUD": 1.280135,
          "CAD": 1.296868
        }
    }
}"""
        response_dataframe = pd.DataFrame.from_dict(json.loads(json_string))
        rates = json_normalize(response_dataframe['rates'])
        return rates.mean(axis=0, skipna=True)




