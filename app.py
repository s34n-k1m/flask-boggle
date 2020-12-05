from flask import Flask, request, render_template, jsonify, session
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.route("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.route("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    return jsonify({"gameId": game_id, "board": game.board})


@app.route('/api/score-word', methods=["POST"])
def score_word():
    """ Checks if submitted word is valid and returns result in JSON """
    word = request.json['word']
    game_id = request.json['gameId']
    game = games[game_id]

    # TODO: Check if the word submitted is a dup

    if not game.is_word_in_word_list(word):
        return jsonify({'result': 'not-word', "wordScore": 0, "gameScore": game.score})
    elif not game.check_word_on_board(word):
        return jsonify({'result': 'not-on-board', "wordScore": 0, "gameScore": game.score})
    elif not game.is_word_not_a_dup(word):
        return jsonify({'result': 'word-already-used', "wordScore": 0, "gameScore": game.score}) 
    else:
        word_score = game.play_and_score_word(word)
        return jsonify({'result': 'ok', "wordScore": word_score, "gameScore": game.score})