import enum
from .. import db


class PostType(enum.Enum):
    News = 'News'
    Publication = 'Publication'
    Other = 'Other'


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=True)
    image_file = db.Column(db.String(20), nullable=False, default='postdefault.jpg')
    created = db.Column(db.DateTime, default=db.func.now())
    type = db.Column(db.Enum(PostType))
    enabled = db.Column(db.Boolean, default=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


def __repr__(self):
    return f"Posts('{self.id}', '{self.title}', '{self.type}')"