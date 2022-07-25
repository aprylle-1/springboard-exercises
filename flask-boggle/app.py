from os import times
from boggle import Boggle
from flask import Flask, render_template, redirect, request
from flask import session, jsonify

boggle_game = Boggle()
app = Flask(__name__)
app.config['SECRET_KEY'] = "fasdfsdhjfhjsdgfhsdfhkwe"

@app.route("/")
def initialize_board():
    """Initialize Boggle Board"""
    if session.get('board', None) != None:
        board = session['board']
    else:
        board = boggle_game.make_board() 
        session['board'] = board
    return render_template('index.html', board=board)


@app.route("/check-word")
def check_valid_word():
    """Check if word submitted is valid. Checks if board is initialize"""
    board = session.get("board", None)
    if board:
        word = request.args.get('word', 'nothing')
        result = boggle_game.check_valid_word(board, word)
        return jsonify({'result' : result})
    else:
        return redirect("/")

@app.route("/reset-board")
def reset_board():
    """Resets session board to none for reset"""
    session['board'] = None
    return redirect('/')

@app.route("/update-stats", methods=["POST"])
def update_stats():
    """Updates current high score and number of times played"""
    curr_high_score = session.get('high_score', 0)
    times_played = session.get('times_played', 0)
    score = int(request.json['params']['score'])
    if score > curr_high_score:
        session['high_score'] = score
    session['times_played'] = times_played + 1
    return jsonify({
        'high_score' : session['high_score'],
        'times_played' : session['times_played']
    })

@app.route("/get-stats")
def get_stats():
    """Gets values of current high schore and number of times played"""
    curr_high_score = session.get('high_score', 0)
    times_played = session.get('times_played', 0)
    return jsonify({
        'high_score' : curr_high_score ,
        'times_played' : times_played
    })
