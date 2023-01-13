from mobio.libs.schedule import BaseScheduler
import schedule
from src.models.comments_model import Comments
from src.models.files_attach_model import FilesAttach
from src.models.reacts_model import Reacts
from src.commons.file import File
from bson import ObjectId
class TestScheduler(BaseScheduler):
    def owner_do(self):
        exist_ids=[]
        comments_model=Comments()
        attach_files_model=FilesAttach()
        reacts_model=Reacts()
        exist_comments=list(comments_model.get_all_comments({},{'files_id':1,'_id':0}))
        for exist_comment in exist_comments:
            files_id=exist_comment.get('files_id')
            exist_ids=exist_ids+files_id
        file_ids=attach_files_model.get_files_ids()
        for i in file_ids:
            file_id = str(i.get('_id'))
            if file_id not in exist_ids:
                file_name=attach_files_model.get_files_details({'_id':ObjectId(file_id)},{'file_name':1,'_id':0}).get('file_name')
                File().delete(file_name)
                attach_files_model.delete_attach_files_documents({"file_name":file_name})
        pass

    def get_schedule(self):
        """
        hàm xác định thời điểm chạy của scheduler, bằng cách xử dụng thư viện schedule
        Các ví dụ hướng dẫn cách xác định thời gian chạy
        1. scheduler chỉ thực hiện công việc một lần duy nhất.
            return None
        2. scheduler sẽ thực hiện mỗi 10 phút một lần.
            return schedule.every(10).minutes
        3. scheduler sẽ thực hiện hàng ngày vào lúc 10h 30 phút.
            return schedule.every().day.at("10:30")
        4. scheduler sẽ thực hiện sau mỗi giờ.
            return schedule.every().hour
        5. scheduler sẽ thực hiện vào mỗi thứ 2 hàng tuần.
            return schedule.every().monday
        6. scheduler sẽ thực hiện vào mỗi thứ 5 hàng tuần và vào lúc 13h 15'.
            return schedule.every().wednesday.at("13:15")
        """
        return schedule.every(10).minutes

