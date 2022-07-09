# Put your app in here.
from flask import Flask, request
from operations import add, sub, mult, div
app = Flask(__name__)

@app.route("/add")
def add_route():
    a,b = int(request.args['a']), int(request.args['b'])
    return str(add(a,b))

@app.route("/sub")
def sub_route():
    a,b = int(request.args['a']), int(request.args['b'])
    return str(sub(a,b))


@app.route("/mult")
def mult_route():
    a,b = int(request.args['a']), int(request.args['b'])
    return str(mult(a,b))

@app.route("/div")
def div_route():
    a,b = int(request.args['a']), int(request.args['b'])
    return str(div(a,b))

@app.route("/math/<operation>")
#all operatios in 1 route
def math_operation(operation):
    if operation == 'add':
        a,b = int(request.args['a']), int(request.args['b'])
        return str(add(a,b))
    elif operation == 'sub':
        a,b = int(request.args['a']), int(request.args['b'])
        return str(sub(a,b))
    elif operation == 'mult':
        a,b = int(request.args['a']), int(request.args['b'])
        return str(mult(a,b))
    elif operation == 'div':
        a,b = int(request.args['a']), int(request.args['b'])
        return str(div(a,b))

 
