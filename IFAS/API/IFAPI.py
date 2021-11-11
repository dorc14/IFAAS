import json

from flask import Blueprint, jsonify,request,render_template
from BL import IFBL

IfRoute = Blueprint('IfRoute', __name__)

@IfRoute.route('/' , methods=['GET'])
def getAllIfs():
    try:
        allIfs = IFBL.getAllIfs()
        return render_template('home.html',data=allIfs)
    except Exception as ex:
        print(ex)
        return 400

@IfRoute.route('/if/<string:id>' , methods=['GET'])
def getIf(id):
    try:
        newIf = IFBL.getIf(id)
        return render_template('if.html',data=newIf),200
    except Exception as ex:
        print(ex)
        return 400

@IfRoute.route('/if',methods=['POST'])
def createIf():
    try:
        form = request.form.to_dict()
        'data = request.get_json()'
        if 'url' not in form:
            transaction = IFBL.createIf(form["name"],form["condition"])
        else:
            transaction = IFBL.createIf(form["name"], form["condition"],form["url"])

        return render_template('status.html',data=json.loads(json.dumps(transaction)))
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