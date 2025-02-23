from datetime import datetime
from database import db
import uuid

class Companion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    seed = db.Column(db.Text, nullable=False)
    src = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    category_id = db.Column(db.String(36), db.ForeignKey('category.id'), nullable=True)
    messages = db.relationship('Message', backref='companion', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Companion {self.name}>'


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'user', 'assistant', or 'system'
    companion_id = db.Column(db.Integer, db.ForeignKey('companion.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Message {self.role}: {self.content[:50]}...>'


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    companions = db.relationship('Companion', backref='category', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Category {self.name}>'


class UserSubscription(db.Model):
    __tablename__ = 'user_subscription'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), unique=True, nullable=False)
    stripe_customer_id = db.Column(db.String(100), unique=True, nullable=True)
    stripe_subscription_id = db.Column(db.String(100), unique=True, nullable=True)
    stripe_price_id = db.Column(db.String(100), unique=True, nullable=True)
    stripe_current_period_end = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<UserSubscription {self.user_id}>'