from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models.base_model import db
from models.user import User
from models.topic import Topic
from models.reply import Reply
from models.board import Board

admin = Admin(name='论坛后台', template_mode='bootstrap3')

admin.add_view(ModelView(User, db.session, name='用户', endpoint='用户'))
admin.add_view(ModelView(Topic, db.session, name='主题', endpoint='主题'))
admin.add_view(ModelView(Reply, db.session, name='评论', endpoint='评论'))
admin.add_view(ModelView(Board, db.session, name='板块', endpoint='板块'))
