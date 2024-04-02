from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)
    admin = db.Column(db.Boolean)

    def __repr__(self) -> str:
        return f'<User {self.username}>'

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def add_user(username: str, password: str = "password!123") -> None:
        user = User()
        user.username = username
        user.set_password(password)
        user.set_admin(False)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def remove_user(username: str) -> None:
        user = User.query.filter_by(username=username).first()
        db.session.delete(user)
        db.session.commit()

    @staticmethod
    def get_by_username(username: str):
        return db.one_or_404(db.select(User).filter_by(username=username))


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    time = db.Column(db.Integer)
    image = db.Column(db.String)

    ingredients = db.relationship('Ingredient', backref='recipe', lazy=True)
    instructions = db.relationship('Instruction', backref='recipe', lazy=True)


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Ingredient name
    measurement = db.Column(db.String(100), nullable=False)  # Ingredient measurement
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)


class Instruction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    step = db.Column(db.Text, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
