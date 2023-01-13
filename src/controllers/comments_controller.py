from tkinter.messagebox import NO
from flask import request
import traceback,json
from src.models.comments_model import Comments
from src.models.comments_log_model import Commentslog
from src.models.reacts_model import Reacts
from src.models.files_attach_model import FilesAttach
from src.models.posts_model import POST
from src.commons.jsonencoder import JSONEncoder
from src.commons.file import File
import uuid
from datetime import datetime
from bson import ObjectId
import pymongo
# from mobio.libs.kafka_lib.helpers.kafka_producer_manager import KafkaProducerManager
import string
import random
from mobio.libs.validator import HttpValidator,InstanceOf,Required,VALIDATION_RESULT
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
class Comment:
    def add_comment(comment_id,current_user,post_id):
        try:
            comments_model=Comments()
            content=request.form.get('content')
            rules = {
                'post_id': [Required, InstanceOf(str)],
                'content': [Required, InstanceOf(str)]
            }
            valid = HttpValidator(rules)
            val_result = valid.validate_object({'content':content,'post_id':post_id})
            if not val_result[VALIDATION_RESULT.VALID]:
                valid = val_result[VALIDATION_RESULT.VALID]
                errors = val_result[VALIDATION_RESULT.ERRORS]
                return {'code':0 ,"msg":errors}
            if comment_id==None:
                path=[]
                parent=None
            else:
                path=[]
                parent=str(comment_id)
                parent_detail=comments_model.get_comment_details({"_id":ObjectId(comment_id)})
                path2=parent_detail.get('path')
                path.append(comment_id)
                path=path+path2
            created_time=datetime.now().timestamp()
            insert_data={
            'post_id':post_id,
            'user_id':str(current_user.get('_id')),
            'updated_by':str(current_user.get('_id')),
            'content':content,
            'parent':parent,
            'path':path,
            'files_detail':[],
            'update_time':created_time,
            'created_time':created_time,
            }
            comments_model=Comments()
            x=comments_model.append_topic_comments(insert_data)
            cmt_id=str(x.inserted_id)
            return {'code':200,'data':{'comment_id':cmt_id}}
        except Exception as e:
            e = traceback.format_exc()
            return json.dumps({'code':0,'data':e})

    def get_list_comments():
        page_size=20
        comments_model=Comments()
        reacts_model=Reacts()
        posts_model=POST()
        post_id = request.args.get('post_id')
        post_exist=posts_model.get_post_detail({'_id':ObjectId(post_id)},{'_id':1})
        if post_exist==None:
            return {'code':0,'msg':'bai viet khong ton tai'}
        # page = int(request.args.get('page',1))
        last_id = request.args.get('last_id',None)
        parent= request.args.get('parent',None)
        if parent==None:
            if last_id is None:
                cursor = comments_model.get_all_comments({'parent':parent,'post_id':post_id}).sort("_id", pymongo.DESCENDING).limit(page_size)
            else:
                cursor = list(comments_model.get_all_comments({'_id': {'$lt': ObjectId(last_id)},'parent':parent,'post_id':post_id}).sort("_id", pymongo.DESCENDING).limit(page_size))  
        else:
            if last_id is None:
                cursor = comments_model.get_all_comments({'parent':parent}).sort("_id", pymongo.DESCENDING).limit(page_size)
            else:
                cursor = list(comments_model.get_all_comments({'_id': {'$lt': ObjectId(last_id)},'parent':parent}).sort("_id", pymongo.DESCENDING).limit(page_size))
        data=[] 
        for i in cursor:
            comment_id=str(i.get('_id'))
            reacts_count=reacts_model.count_doc({'comment_id':comment_id})
            i['reacts_count']=reacts_count
            data.append(i)
        list_comments1=JSONEncoder().parse_json(data)
        try:
            last_id=list_comments1[-1].get("_id").get('$oid')
        except:
            last_id=None
        return {'code':200,'data':list_comments1,'last_id':last_id}

    def reaction(comment_id,current_user,type):
        reacts_model=Reacts()
        user_id=str(current_user.get('_id'))
        try:
            exist_react=reacts_model.get_react_detail({'comment_id':comment_id,'user_id':user_id})
            if exist_react == None:
                insert_data={
                    "comment_id":comment_id,
                    "user_id":user_id,
                    "type":type,
                    "created_time":datetime.now().timestamp()
                }
                reacts_model.add_react_document(insert_data)
                return {"code":200,'data':{'comment_id':comment_id,"user_id":user_id,"type":type,"created_time":datetime.now().timestamp()}}
            if type==exist_react.get('type'):
                reacts_model.delete({"comment_id":comment_id,"user_id":user_id})
                return {"code":200}
            reacts_model.update_react({ "_id": ObjectId(comment_id) },{ "$set": { "type": type} })
            return {"code":200,'data':{'comment_id':comment_id,"user_id":user_id,"type":type,"updated_time":datetime.now().timestamp()}}
        except Exception as e:
            e = traceback.format_exc()
            return json.dumps({'code':0,'data':e})

    def edit(comment_id,current_user):
        comments_model=Comments()
        log_model=Commentslog()
        try:
            current_id=str(current_user.get("_id"))
            content=request.form.get('content')
            rules = {
                'comment_id': [Required, InstanceOf(str)],
                'content': [Required, InstanceOf(str)]
            }
            valid = HttpValidator(rules)
            val_result = valid.validate_object({'content':content,'comment_id':comment_id})
            if not val_result[VALIDATION_RESULT.VALID]:
                valid = val_result[VALIDATION_RESULT.VALID]
                errors = val_result[VALIDATION_RESULT.ERRORS]
                return {'code':0 ,"msg":errors}
            last_data=comments_model.get_comment_details({ "_id": ObjectId(comment_id) })
            comments_model.update_comment({ "_id": ObjectId(comment_id) },{ "$set": { "content": content,"updated_by":current_id,"update_time": datetime.now().timestamp()} })
            log_model.save_comment_log(last_data)
            return {'code':200,'data':{'msg':f"{comment_id} edited"}}
        except Exception as e:
            e = traceback.format_exc()
            return json.dumps({'code':0,'data':e})

    def delete(comment_id,current_user):
        comments_model=Comments()
        attach_files_model=FilesAttach()
        reacts_model=Reacts()
        try:
            detail_comment=comments_model.get_comment_details({"_id":ObjectId(comment_id)},{"files_detail":1})
            if detail_comment != None:
                files_detail=detail_comment.get('files_detail',[])
                children_files_detail=list(comments_model.get_all_comments({ 'path': { '$in': [comment_id] } },{'files_detail':1,'_id':0}))
                filenames=[]
                for i in children_files_detail:
                    children_file_detail=i.get('files_detail')
                    files_detail=files_detail+children_file_detail
                for file_detail in files_detail:
                    File().delete(file_detail.get('filename'))
                    filenames.append(file_detail.get('filename'))
                comments_model.delete_comment({'$or':[{ 'path': { '$in': [comment_id] } },{'_id':ObjectId(comment_id)}]})
                reacts_model.delete_reacts_documents({"comment_id":comment_id})
                attach_files_model.delete_many_attach_files_documents({ 'file_name': { '$in': filenames }})
                return {'code':200,'deleted':comment_id}
            return {'code':0,'data':{'msg':'comment khong ton tai'}}
        except Exception as e:
            e = traceback.format_exc()
            return json.dumps({'code':0,'data':e})

    def delete_file(file_name,current_user,comment_id):
        attach_files_model=FilesAttach()
        try:
            file_id=str(attach_files_model.get_files_details({"file_name":file_name},{'_id':1}).get('_id'))
            comments_model=Comments()
            comment_detail=comments_model.get_comment_details({"_id":ObjectId(comment_id)},{'_id':0,'files_id':1})
            files_id=comment_detail.get('files_id')
            if file_id not in files_id:
                return {'code':0}
            files_id.remove(file_id)
            comments_model.update_comment({ "_id": ObjectId(comment_id) },{ "$set": { "files_id": files_id} })
            File().delete(file_name)
            attach_files_model.delete_attach_files_documents({"file_name":file_name})
            return {'code':200,'deleted':file_name}
        except Exception as e:
            e = traceback.format_exc()
            return json.dumps({'code':0,'data':e})

    def upload_file(current_user,comment_id):
        attach_files_model=FilesAttach()
        comments_model=Comments()
        user_id=str(current_user.get('_id'))
        try:
            files = request.files.getlist('attach_files')
            comment_detail=comments_model.get_comment_details({"_id":ObjectId(comment_id)},{'_id':0,'files_detail':1})
            files_detail=comment_detail.get('files_detail')
            for file in files:
                file_extend=file.filename.split('.')[-1]
                if file_extend not in ['png','jpg','docx']:
                    pass
                else:
                    uid=str(uuid.uuid4())
                    filename=uid+'.'+file_extend
                    origin_filename=file.filename
                    file_location = f"file/{filename}"
                    File().upload(file_location,file)
                    file_url=f'{request.host_url}file/{filename}'
                    attach_files_data={
                    'file_url':file_url,
                    'file_name':filename,
                    'origin_filename':origin_filename,
                    'user_id':user_id,
                    'created_time':datetime.now().timestamp()
                    }
                    attach_files_model.add_attach_files(attach_files_data)
                    files_detail.append({'url':file_url,'filename':filename,'origin_filename':origin_filename})
            comments_model.update_comment({ "_id": ObjectId(comment_id) },{ "$set": { "files_detail": files_detail} })
            return {'code':200,'data':{'user_id':user_id,'files_detail':files_detail}}
        except Exception as e:
            e = traceback.format_exc()
            return json.dumps({'code':0,'data':e})