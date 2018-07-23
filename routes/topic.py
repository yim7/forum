from flask import (
    render_template,
    Blueprint,
)

from routes import *

from models.topic import Topic
from models.board import Board
from models.cache import update_created_topic_cache

main = Blueprint('topic', __name__)


@main.route('/<int:id>')
def detail(id):
    m = Topic.get(id)
    u = User.one(id=m.user_id)
    b = m.board()
    token = new_csrf_token()
    return render_template("topic/detail.html", topic=m, user=u, board=b, csrf_token=token)


@main.route("/delete")
@csrf_required
@admin_required
def delete():
    id = int(request.args.get('id'))
    Topic.delete(id)

    return redirect(url_for('.index'))


@main.route("/new")
def new():
    board_id = int(request.args.get('board_id', -1))
    bs = Board.all()
    token = new_csrf_token()
    return render_template("topic/new.html", bs=bs, csrf_token=token, bid=board_id)


@main.route("/add", methods=["POST"])
@csrf_required
def add():
    form = request.form.to_dict()
    u = current_user()
    Topic.new(form, user_id=u.id)
    update_created_topic_cache(u.id)
    return redirect(url_for('.index'))
