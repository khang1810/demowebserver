from dotenv import load_dotenv
load_dotenv()
from mobio.libs.kafka_lib.helpers.kafka_consumer_manager import BaseKafkaConsumer
from src.models.comments_model import Comments
class TestConsumer(BaseKafkaConsumer):
    def message_handle(self, data):
        print('consumer 1')
        comments_model=Comments()
        x=comments_model.append_topic_comments(data)
        return x.inserted_id
 
