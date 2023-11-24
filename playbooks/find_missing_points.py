from pymongo import MongoClient
import requests
from vault_file import alphavantage_api_key, mongodb_password

class DatabaseConnection:
    
    def get_curr_points(self) -> list:
        ALPHA_VANTAGE_ENDPOINT = "https://www.alphavantage.co/query"
        client = MongoClient(f"mongodb+srv://wleong:{mongodb_password}@cluster0.kt74jjh.mongodb.net/")
        database = client.StockTracker
        collection = database.Companies
        projection = {"_id": 0, "name": 1, "price": 1}
        cursor = collection.find({"name": "AAPL"}, projection)
        for doc in cursor:
            curr_points = doc["price"]
        # return curr_points
        latest_date = curr_points[0]["date"]
        
        price_params: dict = {
        "apikey": alphavantage_api_key,
        "function": "TIME_SERIES_DAILY",
        "symbol": "AAPL",
        "outputsize": "full"
        }
        raw_company_data = requests.get(ALPHA_VANTAGE_ENDPOINT, params=price_params).json()
        company_data = [{"date": date, "close": raw_company_data["Time Series (Daily)"][date]["4. close"]} for date in raw_company_data["Time Series (Daily)"]]
        curr_idx = self.calculate_missing_points(latest_date, company_data)
        return company_data[:curr_idx]
           
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

    result = db_connection.get_curr_points()
    print(result)
