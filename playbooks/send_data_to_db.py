from pymongo import MongoClient
import json
from vault_file import mongodb_password

client = MongoClient(f"mongodb+srv://wleong:{mongodb_password}@cluster0.kt74jjh.mongodb.net/")
database = client["StockTracker"]
collection = database["Companies"]

def send_data():
   with open("missing_data.json", "r") as file:
      new_data = json.load(file)
   # print(new_data)
   # for _ in range(30):
   #    collection.update_one({"name": "AAPL"}, {"$pop": {"price": -1}})
   collection.update_one({
      "name": "AAPL" 
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
    send_data()
