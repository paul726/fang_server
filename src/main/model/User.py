from mongoengine import Document, StringField, DateTimeField, BooleanField
from passlib.apps import custom_app_context as pwd_context


def hash_password(password):
    return pwd_context.encrypt(password)


def verify_password(password_hash, password):
    return pwd_context.verify(password, password_hash)


class User(Document):
    name = StringField(max_length=10)
    company = StringField(max_length=30)
    phone_num = StringField(unique=True, max_length=11)
    hashPass = StringField()
    token = StringField(unique=True)
    time = DateTimeField()
    isBuy = BooleanField()
    orderNum = StringField()
    startDate = DateTimeField()
    endDate = DateTimeField()

