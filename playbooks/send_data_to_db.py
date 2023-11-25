from pymongo import MongoClient
import json, argparse

class DatabaseSender:

   def send_data(self, company_name, mongodb_password):
      client = MongoClient(f"mongodb+srv://wleong:{mongodb_password}@cluster0.kt74jjh.mongodb.net/")
      database = client["StockTracker"]
      collection = database["Companies"]
      with open("missing_data.json", "r") as file:
         new_data = json.load(file)
      # print(new_data)
      # for _ in range(30):
      #    collection.update_one({"_id": "AAPL"}, {"$pop": {"price": -1}})
      collection.update_one({
         "_id": company_name 
      },
      {
         "$push": { 
         "price": {  
            "$each": new_data,
            "$position": 0
         }
         }
      })


if __name__ == "__main__":
   db_sender = DatabaseSender()

   parser = argparse.ArgumentParser(description='Gather missing data from Alpha Vantage')
   parser.add_argument('company_name', help='Company for which to add data')
   parser.add_argument('mongodb_password', help='MongoDB password')
   args = parser.parse_args()

   db_sender.send_data(args.company_name, args.mongodb_password)
