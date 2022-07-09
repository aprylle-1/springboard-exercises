from flask import Flask, request

app = Flask(__name__)

@app.route('/welcome')
def welcome():
    return 'welcome'

@app.route('/welcome/<greet>')
def welcome_with_greet(greet):
    if greet == 'home' or greet == 'back':
        return f'welcome {greet}'
    return 'not found'