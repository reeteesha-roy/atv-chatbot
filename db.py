from pymongo import MongoClient

MONGO_URI = "mongodb+srv://rroy_atv:TOaDGWjtetGEzbbc@cluster1.ge4xvfu.mongodb.net/?appName=Cluster1"
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

try:
    client.admin.command("ping")
    print("✅ MongoDB connected successfully")
except Exception as e:
    print("❌ MongoDB connection failed:", e)
db = client["atv_chatbot"]
faq_collection = db["faq"]
