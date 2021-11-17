from flask import Flask
from API import IFAPI
from flask_restful import Api

app = Flask(__name__)

api = Api(app)
api.add_resource(IFAPI.homePage,'/')
api.add_resource(IFAPI.getIf,'/if/<string:id>')
api.add_resource(IFAPI.If,'/if')
api.add_resource(IFAPI.Execute,'/if/<name>/execute')

if __name__ == '__main__':
    app.run(debug=True)