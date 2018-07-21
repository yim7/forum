import os
import uuid

from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    abort,
    send_from_directory
)
from werkzeug.utils import secure_filename

from models.reply import Reply
from models.topic import Topic
from models.user import User
from routes import (
    current_user,
    new_csrf_token,
    csrf_required,
)
import json

import redis

cache = redis.StrictRedis()

from utils import log

main = Blueprint('index', __name__)

"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 /profile
"""


@main.route("/")
def index():
    return redirect(url_for('topic.index'))


@main.route("/about")
def about():
    u = current_user()
    return render_template('about.html', user=u)


@main.route("/register", methods=['POST'])
def register():
    form = request.form.to_dict()
    # 用类函数来判断
    u = User.register(form)
    if u is None:
        result = False
    else:
        result = True
    return redirect(url_for('.register_view', success=result))


@main.route("/register/view")
def register_view():
    # token = new_csrf_token()
    success = request.args.get('success')
    return render_template('sign/signup.html', success=success)


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        return redirect(url_for('.login_view', success=False))
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        # 设置 cookie 有效期为 永久
        session.permanent = True
        # 转到 topic.index 页面
        return redirect(url_for('topic.index'))


@main.route("/login/view")
def login_view():
    # token = new_csrf_token()
    success = request.args.get('success')
    return render_template('sign/signin.html', success=success)


@main.route("/signout")
def signout():
    session.pop('user_id')
    return redirect(url_for('topic.index'))


def dict_to_object(form):
    t = Topic()
    for name, value in form.items():
        setattr(t, name, value)
    # print('test dict to object',t.user().username)
    return t


def created_topic(user_id):
    # O(n)
    # ts = Topic.all(user_id=user_id)
    # return ts
    k = 'created_topic_{}'.format(user_id)
    if cache.exists(k):
        v = cache.get(k)
        ts = json.loads(v)
        ts = [dict_to_object(t) for t in ts]
        return ts
    else:
        ts = Topic.all(user_id=user_id)
        v = json.dumps([t.json() for t in ts])
        cache.set(k, v)
        return ts


def replied_topic(user_id):
    # O(m*n)
    # rs = Reply.all(user_id=user_id)
    # ts = []
    # for r in rs:
    #     t = Topic.one(id=r.topic_id)
    #     ts.append(t)
    # return ts

    k = 'replied_topic_{}'.format(user_id)
    if cache.exists(k):
        v = cache.get(k)
        ts = json.loads(v)
        ts = [dict_to_object(t) for t in ts]
        return ts
    else:
        rs = Reply.all(user_id=user_id)
        ts = []
        for r in rs:
            t = Topic.one(id=r.topic_id)
            ts.append(t)

        v = json.dumps([t.json() for t in ts])
        cache.set(k, v)

        return ts


@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        token = new_csrf_token()
        return render_template('user/profile.html', user=u, csrf_token=token)


@main.route('/setting', methods=['POST'])
@csrf_required
def setting():
    form = request.form.to_dict()
    u = current_user()
    if 'old_pass' in form:
        old = form['old_pass']
        new = form['new_pass']
        if u.password == User.salted_password(old):
            User.update(u.id, password=User.salted_password(new))
            print('修改密码成功')
        else:
            print('原密码错误')
    else:
        User.update(u.id, **form)
    return redirect(url_for('.profile'))


@main.route('/user/<int:id>')
def user_detail(id):
    u = User.one(id=id)
    if u is None:
        abort(404)
    else:
        created = Topic.created_topic(user_id=u.id)
        replied = Topic.replied_topic(user_id=u.id)
        # created = created_topic(u.id)
        # replied = replied_topic(u.id)
        return render_template(
            'user/index.html',
            user=u,
            created=created,
            replied=replied
        )


@main.route('/image/add', methods=['POST'])
def avatar_add():
    file = request.files['avatar']

    # ../../root/.ssh/authorized_keys
    # filename = secure_filename(file.filename)
    suffix = file.filename.split('.')[-1]
    filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
    path = os.path.join('images', filename)
    file.save(path)

    u = current_user()
    User.update(u.id, image='/images/{}'.format(filename))

    return redirect(url_for('.profile'))


@main.route('/images/<filename>')
def image(filename):
    # 不要直接拼接路由，不安全，比如
    # open(os.path.join('images', filename), 'rb').read()
    return send_from_directory('images', filename)
