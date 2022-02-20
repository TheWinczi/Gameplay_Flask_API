import requests

from frontend.src import app
from frontend.config import GAMES_SERVER_URL, PLAYERS_SERVER_URL
from flask import Flask, render_template, Response
# app = Flask(None)


@app.route("/", methods=("GET",))
def main():
    return render_template("gameplay/main.html")


@app.route("/games", methods=("GET",))
def all_games():
    games = requests.get(f"{GAMES_SERVER_URL}api/games").json()
    if "games" in games.keys():
        games = games["games"]
    else:
        games = []
    return render_template("gameplay/games.html", games=games)


@app.route("/games/<int:id>", methods=("GET",))
def particular_game(id: int):
    game = requests.get(f"{GAMES_SERVER_URL}api/games/{id}")
    if game.status_code == 200:
        game = game.json()
    else:
        game = None
    return render_template("gameplay/game.html", game=game)


@app.route("/games/<int:game_id>/players")
def particular_game_players(game_id: int):
    game = requests.get(f"{GAMES_SERVER_URL}api/games/{game_id}")
    if game.status_code == 200:
        game = game.json()
    else:
        game = None

    players = requests.get(f"{GAMES_SERVER_URL}/api/games/{game_id}/players")
    if players.status_code == 200:
        players = players.json()
        if "players" in players.keys():
            players = players["players"]
        else:
            players = []
    else:
        players = []
    return render_template("gameplay/game_players.html", game=game, players=players)


@app.route("/games/<int:game_id>/edit")
def edit_game(game_id: int):
    return "<h1>Edit Game</h1>"


@app.route("/players", methods=("GET",))
def all_players():
    players = requests.get(f"{PLAYERS_SERVER_URL}api/players").json()
    if "players" in players.keys():
        players = players["players"]
    else:
        players = []
    return render_template("gameplay/players.html", players=players)


@app.route("/players/<int:id>", methods=("GET",))
def particular_player(id: int):
    player = requests.get(f"{PLAYERS_SERVER_URL}api/players/{id}")
    if player.status_code == 200:
        player = player.json()
    else:
        player = None
    return render_template("gameplay/player.html", player=player)


@app.route("/players/<int:player_id>/edit")
def edit_player(player_id: int):
    return "<h1>Edit Player</h1>"


@app.route("/about", methods=("GET",))
def about():
    return render_template("gameplay/about.html")
