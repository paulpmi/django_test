from pymongo import MongoClient
import gridfs

mongo_client = MongoClient('localhost', 27017)
mongo_db = mongo_client.youtube_clone
fs = gridfs.GridFS(mongo_db)
fs_bucket = gridfs.GridFSBucket(mongo_db)
