from main import app

v1_0_url_prefix = '/api/v1.0'
from src.apis.v1_0.auth_service import auth1
app.register_blueprint(auth1, url_prefix='')

from src.apis.v1_0.comment_service import comments
app.register_blueprint(comments, url_prefix=v1_0_url_prefix)

from src.apis.v1_0.get_file_service import get_file1
app.register_blueprint(get_file1, url_prefix='')

from src.apis.dashboard import app1
app.register_blueprint(app1, url_prefix='')

