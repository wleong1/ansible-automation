from pymongo import MongoClient
import requests, argparse
# from vault_file import mongodb_password, alphavantage_api_key

ALPHA_VANTAGE_ENDPOINT = "https://www.alphavantage.co/query"
class DatabaseConnection:
    
    def get_curr_points(self, company, mongodb_connection, alphavantage_api_key) -> list:
        client = MongoClient(mongodb_connection)
        database = client.StockTracker
        collection = database.Companies
        projection = {"_id": 1, "price": 1}
        cursor = collection.find({"_id": company}, projection)
        for doc in cursor:
            curr_points = doc["price"]
            latest_date = curr_points[0]["date"]
        
        price_params: dict = {
        "apikey": alphavantage_api_key,
        "function": "TIME_SERIES_DAILY",
        "symbol": company,
        "outputsize": "full"
        }
        raw_company_data = requests.get(ALPHA_VANTAGE_ENDPOINT, params=price_params).json()
        company_data = [{"date": date, "close": raw_company_data["Time Series (Daily)"][date]["4. close"]} for date in raw_company_data["Time Series (Daily)"]]
        if latest_date:
            curr_idx = self.calculate_missing_points(latest_date, company_data)
            return company_data[:curr_idx]
        else:
            return company_data
           
    def calculate_missing_points(self, latest_date: str, curr_points: list) -> int:
        start, end = 0, len(curr_points) - 1
        while start <= end:
            mid = (start + end) // 2
            date = curr_points[mid]["date"]
            if latest_date == date:
                return start
            elif latest_date > date:
                end = mid - 1
            else:
                start = mid + 1
        return start


if __name__ == "__main__":
    db_connection = DatabaseConnection()

    parser = argparse.ArgumentParser(description='Gather missing data from Alpha Vantage')
    parser.add_argument('company_name', help='Company for which to gather data')
    parser.add_argument('mongodb_connection', help='MongoDB connection link')
    parser.add_argument('alphavantage_api_key', help='AlphaVantage API Key')
    args = parser.parse_args()

    result = db_connection.get_curr_points(args.company_name, args.mongodb_connection, args.alphavantage_api_key)
    print(result)
