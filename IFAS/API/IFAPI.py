import json
from flask import request, render_template, make_response
from BL import IFBL
from flask_restful import Resource
from Constants import headers
from logger import logger

class homePage(Resource):
    def get(self):
        try:
            allIfs = IFBL.getAllIfs()
            return make_response(render_template('home.html', data=allIfs), 200 ,headers)
        except Exception as ex:
            logger.warning("Exception has occured:",ex)
            return 400

class getIf(Resource):
    def get(self,id):
        try:
            newIf = IFBL.getIf(id)
            return make_response(render_template('if.html',data=newIf), 200, headers)
        except Exception as ex:
            logger.warning("Exception has occured:",ex)
            return 400

class If(Resource):
    def post(self):
        try:
            form = request.form.to_dict()
            if 'url' not in form:
                transaction = IFBL.createIf(form["name"],form["condition"])
            else:
                transaction = IFBL.createIf(form["name"], form["condition"],form["url"])
            return make_response(render_template('status.html', data=json.loads(json.dumps(transaction)))
                                  ,200 ,headers)
        except Exception as ex:
            logger.warning("Exception has occured:",ex)
            return 400

class Execute(Resource):
    def post(self,name):
        try:
            param = request.get_json()
            result = IFBL.execIf(name,param)
            return json.loads(json.dumps(result)),200
        except Exception as ex:
            logger.warning("Exception has occured:",ex)
            return 400
