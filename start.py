import os
from _sha1 import sha1

from flask import Flask, make_response, jsonify, request, abort
from mongoengine import connect
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

from src.main.model import User

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db':   'tongcheng',
    'host': '127.0.0.1',
    'port': 31231
}

app.config['SECRET_KEY'] = 'secret_key'

connect(host='localhost', port=31231)


def generate_auth_token():
    return sha1(os.urandom(24)).hexdigest()



@app.route('/')
def index():
    return 'hello,world'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/app/sign_in', methods=['POST'])
def sign_in(params):
    data = request.data
    pass


@app.route('/app/verifyCode')
def requestVerifyCode():
    pass


def verifyCode(msgId, code):
    return True


@app.route('/app/findPassWord', methods=['POST'])
def findPassword():
    pass


@app.route('/app/reset', methods=['POST'])
def reset_password():
    pass


@app.route('/app/register', methods=['POST'])
def sign():
    data = request.data
    phoneNum = request.json.get('phone_num')
    print(phoneNum)
    password = request.json.get('password')
    msgId = request.json.get('msgId')
    code = request.json.get('code')
    if not verifyCode(msgId, code):
        abort(400)
    if phoneNum is None or password is None:
        abort(400)  # missing arguments
    if User.Objects(phone_num=phoneNum).first() is not None:
        return jsonify({'error': True, 'errorMsg': '该手机号已注册', 'result': {}})
    hashPass = pwd_context.encrypt(data['password'])
    token = generate_auth_token()
    user = User(phone_num = phoneNum, hashPass = hashPass, token = token)
    user.save()
    return jsonify({'error': False, 'errorMsg': '该手机号已注册', 'result': {'token': token}})


@app.route('/app/login', methods=['POST'])
def login():
    token = request.json.get('token')
    userId = phoneNum = request.json.get('phone_num')
    password = request.json.get('password')
    hashPass = pwd_context.encrypt(password)
    if User.Objects(phone_num = phoneNum, hashPass = hashPass, token = token).first() is not None:
        return jsonify({'error': True, 'errorMsg': '该号码还未注册', 'result': {}})
    pass


if __name__ == '__main__':
    app.run(debug=True)