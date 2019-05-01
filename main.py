from exchangerateloader.exchange_rate_loader import ExchangeRateLoader

def start():
    config_file_path = "config/config.yaml"

    # just a sample query to test out the results
    sample_query = "SELECT * FROM {} where currency_code = 'AUD'"
    exchange_rate_loader = ExchangeRateLoader()

    """
    Fetching the data from the API
    """
    response_data = exchange_rate_loader.fetch_exchange_rate_data(config_file_path)
    """
    clean response data for further processing
    """
    clean_dataframe = exchange_rate_loader.process_exchange_rate_data(response_data)

    """
    Printing the  results from the sql query
    """
    print("The result for the sample query is   \n  ",exchange_rate_loader.populate_db_table(clean_dataframe,sample_query))
    print("Average value of all the currencies for the time period is \n ",exchange_rate_loader.calculte_average_currency_value())


"""
Entry point for the application
"""
if __name__ == "__main__":
    start()
