from flask import Blueprint, jsonify,request
from BL import IFBL

IfRoute = Blueprint('IfRoute', __name__)

@IfRoute.route('/if/all' , methods=['GET'])
def getAllIfs():
    try:
        allIfs = IFBL.getAllIfs()
        return jsonify(allIfs),200
    except Exception as ex:
        print(ex)
        return 400

@IfRoute.route('/if/<id>' , methods=['GET'])
def getIf(id):
    try:
        newIf = IFBL.getIf(id)
        print(newIf)
        return jsonify(newIf),200
    except Exception as ex:
        print(ex)
        return 400

@IfRoute.route('/if',methods=['POST'])
def createIf():
    try:
        data = request.get_json()
        if 'url' not in data:
            transaction = IFBL.createIf(data["name"],data["properties"])
        else:
            transaction = IFBL.createIf(data["name"], data["properties"],data["url"])

        return jsonify(transaction),200
    except Exception as ex:
        print(ex)
        return 400

@IfRoute.route('/if/<name>/execute',methods=['POST'])
def execIf(name):
    try:
        param = request.get_json()
        result = IFBL.execIf(name,param)
        return jsonify(result),200
    except Exception as ex:
        print(ex)
        return 400