import os
from flask import Flask, jsonify, request, abort, make_response, render_template, send_file
from flask_cors import CORS, cross_origin
import datetime
import json
from bson.json_util import dumps
import io
import csv
import uuid
from lxml import etree
import traceback
import mysql.connector  

app = Flask(__name__)
CORS(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

connector = mysql.connector
mydb = connector.connect(
        connection_timeout = 5,
        port = "3306",
        host = "pbx.dynopii.com",
        user = "root",
        database = "asteriskcdrdb",
    )

@app.route("/fetch", methods=["POST"])
def fetch():
    data = request.get_json(silent = True)
    sql = data['sql']
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    row = mycursor.fetchone()
    response = {} 
    count = 0
    while row is not None:
        response[count] = list(row)
        count+=1 
        row = mycursor.fetchone()
    return jsonify(response) 

# Error Handler 404
@app.errorhandler(404)
def not_found(error):
    return send({'error': 'Not found'}, 404)

# Error Handler 405
@app.errorhandler(405)
def method_not_allowed(error):
    return send({'error': 'Method is not allowed'}, 405)

# Error Handler 500
@app.errorhandler(500)
def internal_server_error(error):
    print(traceback.format_exc())
    return send({'error': 'Internal Server Error'}, 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)

    