from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from models.reply import Reply
from routes import *

from models.topic import Topic
from models.board import Board

main = Blueprint('topic', __name__)


@main.route("/")
def index():
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.all(board_id=board_id)
    # token = new_csrf_token()
    bs = Board.all()
    u = current_user()
    return render_template("topic/index.html", user=u, ms=ms, bs=bs, bid=board_id)


@main.route('/<int:id>')
def detail(id):
    m = Topic.get(id)
    # 传递 topic 的所有 reply 到 页面中
    u = User.one(id=m.user_id)
    b = m.board()
    token = new_csrf_token()
    return render_template("topic/detail.html", topic=m, user=u, board=b, csrf_token=token)


@main.route("/delete")
@csrf_required
def delete():
    id = int(request.args.get('id'))
    u = current_user()
    print('删除 topic 用户是', u, id)
    Topic.delete(id)
    return redirect(url_for('.index'))


@main.route("/new")
def new():
    board_id = int(request.args.get('board_id', -1))
    bs = Board.all()
    # return render_template("topic/new.html", bs=bs, bid=board_id)
    token = new_csrf_token()
    return render_template("topic/new.html", bs=bs, csrf_token=token, bid=board_id)


@main.route("/add", methods=["POST"])
@csrf_required
def add():
    form = request.form.to_dict()
    u = current_user()
    Topic.new(form, user_id=u.id)
    return redirect(url_for('.index'))
