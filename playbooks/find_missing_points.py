from pymongo import MongoClient

class DatabaseConnection:
    
    def get_curr_points(self) -> list:
        client = MongoClient("mongodb+srv://wleong:Lwj970823@cluster0.kt74jjh.mongodb.net/")
        database = client.StockTracker
        collection = database.Companies
        projection = {"_id": 0, "name": 1, "price": 1}
        cursor = collection.find({"name": "MSFT"}, projection)
        for doc in cursor:
            curr_points = doc["price"]
        # return curr_points
        latest_date = "2023-10-10"
        curr_idx = self.calculate_missing_points(latest_date, curr_points)
        return curr_points[:curr_idx]
           
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
    
    # def filter_points(self, curr_idx: int, curr_points: list) -> list:
        # return curr_points[:curr_idx]
if __name__ == "__main__":
    # Create an instance of the DatabaseConnection class
    db_connection = DatabaseConnection()

    # Run the get_curr_points method
    result = db_connection.get_curr_points()
    print(result)
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="DatabaseConnection methods")
#     parser.add_argument("method", choices=["get_curr_points", "calculate_missing_points", "filter_points"])

#     args = parser.parse_args()

#     db_connection = DatabaseConnection()

#     if args.method == "get_curr_points":
#         result = db_connection.get_curr_points()
#     elif args.method == "calculate_missing_points":
#         parser.add_argument("--latest-date", required=True)
#         parser.add_argument("--curr-points", required=True)
#         args = parser.parse_args()
#         result = db_connection.calculate_missing_points(args.latest_date, args.curr_points)
#     elif args.method == "filter_points":
#         parser.add_argument("--curr-idx", required=True)
#         parser.add_argument("--curr-points", required=True)
#         args = parser.parse_args()
#         result = db_connection.filter_points(int(args.curr_idx), eval(args.curr_points))

#     print(result)
