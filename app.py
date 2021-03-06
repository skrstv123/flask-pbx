import os
from flask import Flask, jsonify, request, abort, make_response, render_template, send_file
from flask_cors import CORS, cross_origin
import traceback
import json
from flask_mysqldb import MySQL

app = Flask(__name__)
CORS(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'asteriskcdrdb'

mysql = MySQL(app)

def send(data, status_code):
    return make_response(jsonify(data), status_code)

@app.route("/fetch", methods=["GET"])
def fetch():
    sql = "select * from cdr"
    mycursor = mysql.connection.cursor()
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

