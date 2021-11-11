from flask import Flask,render_template
from API import IFAPI
from API import TransactionsAPI

app = Flask(__name__)
app.register_blueprint(IFAPI.IfRoute)
app.register_blueprint(TransactionsAPI.transRoute)

@app.route("/")
def home():
    return "hello"

if __name__ == '__main__':
    app.run(debug=True)