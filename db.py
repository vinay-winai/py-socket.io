from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.socket_persistent
soc_events = db.socket_events
latest_event = db.latest_event

def save_event(event):
    soc_events.insert_one({"event":event})
    latest_event.update_one({'_id':1},{"$set":{"latest":event}},upsert=True)
