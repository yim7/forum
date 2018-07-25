from flask import abort
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView

from models.base_model import db
from models.user import User
from models.topic import Topic
from models.reply import Reply
from models.board import Board

from routes import current_user, login_required


# Create customized model view class
class MyModelView(ModelView):

    def is_accessible(self):
        u = current_user()
        if u:
            return u.is_admin()
        else:
            return False


# Create customized index view class that handles login & registration
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    @login_required
    def index(self):
        u = current_user()
        if not u.is_admin():
            abort(401)
        return super(MyAdminIndexView, self).index()


admin = Admin(name='论坛后台', index_view=MyAdminIndexView(), template_mode='bootstrap3')

admin.add_view(MyModelView(User, db.session, name='用户', endpoint='用户'))
admin.add_view(MyModelView(Topic, db.session, name='主题', endpoint='主题'))
admin.add_view(MyModelView(Reply, db.session, name='评论', endpoint='评论'))
admin.add_view(MyModelView(Board, db.session, name='板块', endpoint='板块'))
