from flask import Blueprint, jsonify
from BL import TransactionBL

def getTransaction(id):
    transaction = TransactionBL.getTransaction(id)
    return transaction

transRoute = Blueprint('transRoute', __name__)

@transRoute.route('/transaction/<id>')
def index(id):
    transaction = getTransaction(id)
    return jsonify(transaction),200