import requests
from flask import Flask, render_template, Response, flash, redirect, url_for

from frontend.src import app
from frontend.config import GAMES_SERVER_URL, PLAYERS_SERVER_URL
from frontend.src.gameplay.forms import AddPlayerForm, EditPlayerForm, AddGameForm, EditGameForm
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


@app.route("/games/<int:game_id>/players/<int:player_id>/remove")
def remove_player_from_game(game_id: int, player_id: int):
    r = requests.put(f"{GAMES_SERVER_URL}api/players/{player_id}", json={
        "game_id": -1
    })
    if r.status_code == 202:
        flash("Removing from game succeed", 'success')
    else:
        flash("Removing from game failed", 'danger')
    return redirect(url_for("particular_game_players", game_id=game_id))


@app.route("/games/<int:game_id>/edit", methods=["GET", "POST"])
def edit_game(game_id: int):
    form = EditGameForm()

    if form.validate_on_submit():
        r = requests.put(f"{GAMES_SERVER_URL}api/games/{game_id}", json={
            "description": form.description.data
        })
        if r.status_code == 202:
            flash("Game Editing Succeed", 'success')
        else:
            flash("Game Editing Failed", 'danger')

        return redirect(url_for("all_games"))
    else:
        game = requests.get(f"{GAMES_SERVER_URL}api/games/{game_id}").json()
        form.description.data = game.get("description", "")
        return render_template("gameplay/game_edit.html", form=form, game=game)


@app.route("/games/create", methods=("GET", "POST"))
def create_game():
    form = AddGameForm()

    if form.validate_on_submit():
        r = requests.post(f"{GAMES_SERVER_URL}api/games", json={
            "description": form.description.data,
        })
        if r.status_code == 201:
            flash("Game Adding Succeed", 'success')
        else:
            flash("Game Adding Failed", 'danger')

        return redirect(url_for("all_games"))
    else:
        return render_template("gameplay/game_create.html", form=form)


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


@app.route("/players/create", methods=("GET", "POST"))
def create_player():
    form = AddPlayerForm()

    if form.validate_on_submit():
        r = requests.post(f"{PLAYERS_SERVER_URL}api/players", json={
            "username": form.username.data,
            "image_file": form.image_file.data
        })
        if r.status_code == 201:
            flash("Player Adding Succeed", 'success')
        else:
            flash("Player Adding Failed", 'danger')

        return redirect(url_for("all_players"))
    else:
        return render_template("gameplay/player_create.html", form=form)


@app.route("/players/<int:player_id>/edit", methods=["GET", "POST"])
def edit_player(player_id: int):
    form = EditPlayerForm()

    if form.validate_on_submit():
        r = requests.put(f"{PLAYERS_SERVER_URL}api/players/{player_id}", json={
            "username": form.username.data,
            "image_file": form.image_file.data
        })
        if r.status_code == 202:
            flash("Player Editing Succeed", 'success')
        else:
            flash("Player Editing Failed", 'danger')

        return redirect(url_for("all_players"))
    else:
        player = requests.get(f"{PLAYERS_SERVER_URL}api/players/{player_id}").json()
        return render_template("gameplay/player_edit.html", form=form, player=player)


@app.route("/about", methods=("GET",))
def about():
    return render_template("gameplay/about.html")
