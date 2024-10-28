from pymongo import MongoClient

client = MongoClient("mongodb+srv://pandunagella05:pandunagella05@cluster0.ubrgp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client.todo

collection_name = db['todo']
users_collection = db['users']  # New users collection