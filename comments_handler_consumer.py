from src.consumers.comments_handler_consumer import TestConsumer
from time import sleep
import os
from pymongo import MongoClient
if __name__ == "__main__":
    url_connection = os.getenv('TEST_MONGO_URI')
    client_mongo = MongoClient(url_connection, connect=False)
    TestConsumer(topic_name="comments_handler", group_id="test", client_mongo=client_mongo, retryable=False)
    sleep(1000)
