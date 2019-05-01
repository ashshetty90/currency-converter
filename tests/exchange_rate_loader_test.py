import unittest,requests
import pandas as pd
from exchangerateloader.exchange_rate_loader import ExchangeRateLoader

class ExchangeRateLoaderTest(unittest.TestCase):

    def setUp(self):
        self.exchange_rate_loader = ExchangeRateLoader()
        self.response_data = self.exchange_rate_loader.fetch_exchange_rate_data("tests/config_test.yaml")
        self.pandas_df = self.exchange_rate_loader.process_exchange_rate_data(self.response_data)

    def test_fetch_exchange_rate_data(self):
        self.assertIsInstance(self.response_data,dict)

    @unittest.skip("skipped test_invalid_fetch_exchange_rate_data for now but test case can be verified by manipulating the api url in config_test.yaml")
    def test_invalid_fetch_exchange_rate_data(self):
        with self.assertRaises(requests.exceptions.ConnectionError):
            self.exchange_rate_loader.fetch_exchange_rate_data("tests/config_test.yaml")

    def test_process_exchange_rate_data(self):
        self.assertIsInstance(self.pandas_df,pd.DataFrame)

    def test_populate_db_table(self):
        response_sql_data = self.exchange_rate_loader.populate_db_table(self.pandas_df,"SELECT * FROM {} where currency_code = 'AOA'")
        self.assertIsInstance(response_sql_data,list)


if __name__ == '__main__':
    unittest.main()
