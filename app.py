from flask import Flask
from API import IFAPI
from API import TransactionsAPI


app = Flask(__name__)
app.register_blueprint(IFAPI.IfRoute)
app.register_blueprint(TransactionsAPI.transRoute)
app.config['CELERY_BROKER_URL'] = 'ADD BROKER'
app.config['CELERY_BACKEND'] = 'ADD BACKEND'


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    app.run(debug=True)