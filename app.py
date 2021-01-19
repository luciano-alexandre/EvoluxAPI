from flask import Flask
from models.NumberModel import db
from controllers.NumberController import app as numberController
from controllers.AuthenticationController import app as authenticationController


app_web = Flask(__name__)
app_web.secret_key = "secret_key_evolux"
app_web.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.sqlite3'


app_web.register_blueprint(numberController, url_prefix="/number")
app_web.register_blueprint(authenticationController, url_prefix="/authentication")

if __name__ == '__main__':
    db.init_app(app=app_web)
    with app_web.test_request_context():
        db.create_all()
    app_web.run(debug=True, host='0.0.0.0')
