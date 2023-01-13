from dotenv import load_dotenv
load_dotenv()
from mobio.libs.kafka_lib.helpers.kafka_consumer_manager import BaseKafkaConsumer
from src.models.comments_model import Comments
class TestConsumer2(BaseKafkaConsumer):
    def message_handle(self, data):
        print('consumer 2')
        comments_model=Comments()
        comments_model.append_topic_comments(data)