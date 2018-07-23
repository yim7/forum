import time

from sqlalchemy import String, Integer, Column, Text, UnicodeText, Unicode, desc

from models.base_model import SQLMixin, db
from models.board import Board
from models.user import User
from models.reply import Reply
from utils import log


class Topic(SQLMixin, db.Model):
    views = Column(Integer, nullable=False, default=0)
    title = Column(Unicode(50), nullable=False)
    content = Column(UnicodeText, nullable=False)
    user_id = Column(Integer, nullable=False)
    board_id = Column(Integer, nullable=False)

    @classmethod
    def new(cls, form, user_id):
        form['user_id'] = user_id
        m = super().new(form)
        return m

    @classmethod
    def get(cls, id):
        m = cls.one(id=id)
        m.views += 1
        m.save()
        return m

    @classmethod
    def delete(cls, id):
        super().delete(id=id)
        Reply.delete(topic_id=id)

    @classmethod
    def created_topic(cls, user_id):
        topics = cls.query.filter_by(user_id=user_id).order_by(desc(cls.created_time)).all()
        return topics

    @classmethod
    def replied_topic(cls, user_id):
        replies = Reply.query.filter_by(user_id=user_id).order_by(desc(Reply.created_time)).all()

        replied_topics = []
        for r in replies:
            t = cls.one(id=r.topic_id)
            if t not in replied_topics:
                replied_topics.append(t)

        return replied_topics

    def user(self):
        u = User.one(id=self.user_id)
        return u

    def board(self):
        b = Board.one(id=self.board_id)
        return b

    def replies(self):
        ms = Reply.all(topic_id=self.id)
        return ms

    def reply_count(self):
        count = len(self.replies())
        return count

    def last_reply(self):
        r = Reply.query.filter_by(topic_id=self.id).order_by(desc(Reply.created_time)).limit(1).first()
        return r
