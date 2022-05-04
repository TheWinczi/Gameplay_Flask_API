import requests

from flask_bcrypt import generate_password_hash
from flask import render_template, flash, redirect, url_for, abort, session

from frontend.src import app
from frontend.config import GAMES_SERVER_URL, PLAYERS_SERVER_URL, ACCOUNTS_SERVER_URL
from frontend.src.gameplay.forms import AddPlayerForm, EditPlayerForm, AddGameForm, EditGameForm, AccountSignInForm
from frontend.src.gameplay.validators import is_player_image_valid


@app.route("/", methods=("GET",))
def home():
    return render_template("gameplay/home.html")


@app.route("/about", methods=("GET",))
def about():
    return render_template("gameplay/about.html")


@app.route("/games", methods=("GET",))
def all_games():
    games = requests.get(f"{GAMES_SERVER_URL}api/games")
    if games.status_code != 200:
        abort(status=games.status_code)

    games = games.json()
    if "games" in games.keys():
        games = games["games"]
    else:
        games = []
    return render_template("gameplay/games/games.html", games=games)


@app.route("/games/<int:game_id>", methods=("GET",))
def particular_game(game_id: int):
    game = requests.get(f"{GAMES_SERVER_URL}api/games/{game_id}")
    if game.status_code != 200:
        abort(game.status_code)

    game = game.json()
    return render_template("gameplay/games/game.html", game=game)


@app.route("/games/<int:game_id>/players")
def particular_game_players(game_id: int):
    game = requests.get(f"{GAMES_SERVER_URL}api/games/{game_id}")
    if game.status_code != 200:
        abort(game.status_code)
    game = game.json()

    players = requests.get(f"{GAMES_SERVER_URL}api/players?in-game={game_id}")
    if players.status_code != 200:
        abort(players.status_code)
    players = players.json()

    if "players" in players.keys():
        players = players["players"]
    else:
        players = []
    return render_template("gameplay/games/game_players.html", game=game, players=players)


@app.route("/games/<int:game_id>/add-new-player", methods=("GET", "POST"))
def add_player_to_game(game_id: int):
    game = requests.get(f"{GAMES_SERVER_URL}api/games/{game_id}")
    if game.status_code != 200:
        abort(game.status_code)
    game = game.json()

    players_not_in_game = requests.get(f"{GAMES_SERVER_URL}api/players?not-in-game={game_id}")
    if players_not_in_game.status_code != 200:
        abort(players_not_in_game.status_code)
    players_not_in_game = players_not_in_game.json()

    if "players" in players_not_in_game.keys():
        players_not_in_game = players_not_in_game["players"]
    else:
        players_not_in_game = []
    return render_template("gameplay/games/game_add_player.html", players=players_not_in_game, game=game)


@app.route("/games/<int:game_id>/add-new-player/<int:player_id>")
def add_particular_player_to_game(game_id: int, player_id: int):
    r = requests.post(f"{GAMES_SERVER_URL}api/games/{game_id}/players/{player_id}")
    if r.status_code == 201:
        flash("Adding player succeed", 'success')
    else:
        flash("Adding player failed", 'danger')

    return redirect(url_for("particular_game_players", game_id=game_id))


@app.route("/games/<int:game_id>/players/<int:player_id>/remove")
def remove_player_from_game(game_id: int, player_id: int):
    r = requests.delete(f"{GAMES_SERVER_URL}api/games/{game_id}/players/{player_id}")
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
        return render_template("gameplay/games/game_edit.html", form=form, game=game)


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
        return render_template("gameplay/games/game_create.html", form=form)


@app.route("/games/<int:game_id>/players/<int:player_id>/points/add/<int:points>")
def add_player_points(game_id: int, player_id: int, points: int):
    player = requests.get(f"{GAMES_SERVER_URL}api/games/{game_id}/players/{player_id}")
    if player.status_code != 200:
        flash("Updating Player Points Failed", 'danger')
        return redirect(url_for("particular_game_players", game_id=game_id))

    r = requests.put(f"{GAMES_SERVER_URL}api/games/{game_id}/players/{player_id}", json={
        "score": player.json().get("score", 0) + points
    })

    if r.status_code == 202:
        flash("Updating Player Points Succeed", "success")
    else:
        flash("Updating Player Points Failed", 'danger')
    return redirect(url_for("particular_game_players", game_id=game_id))


@app.route("/games/<int:game_id>/players/<int:player_id>/points/subtract/<int:points>")
def subtract_player_points(game_id: int, player_id: int, points: int):
    player = requests.get(f"{GAMES_SERVER_URL}api/games/{game_id}/players/{player_id}")
    if player.status_code != 200:
        flash("Updating Player Points Failed", 'danger')
        return redirect(url_for("particular_game_players", game_id=game_id))

    r = requests.put(f"{GAMES_SERVER_URL}api/games/{game_id}/players/{player_id}", json={
        "score": player.json().get("score", 0) - points
    })

    if r.status_code == 202:
        flash("Updating Player Points Succeed", "success")
    else:
        flash("Updating Player Points Failed", 'danger')
    return redirect(url_for("particular_game_players", game_id=game_id))


@app.route("/players", methods=("GET",))
def all_players():
    players = requests.get(f"{PLAYERS_SERVER_URL}api/players")

    if players.status_code != 200:
        abort(players.status_code)
    players = players.json()

    if "players" in players.keys():
        players = players["players"]
    else:
        players = []
    return render_template("gameplay/players/players.html", players=players)


@app.route("/players/<int:player_id>", methods=("GET",))
def particular_player(player_id: int):
    player = requests.get(f"{PLAYERS_SERVER_URL}api/players/{player_id}")
    if player.status_code != 200:
        abort(player.status_code)
    player = player.json()
    player["image_url"] = f"{PLAYERS_SERVER_URL}{player['image_url']}"
    return render_template("gameplay/players/player.html", player=player)


@app.route("/players/create", methods=("GET", "POST"))
def create_player():
    form = AddPlayerForm()

    if form.validate_on_submit():
        if form.image_file.data:
            pass

        filename = form.image_file.data.filename
        image = form.image_file.data
        if not is_player_image_valid(image):
            flash('Invalid player image', 'danger')
            return redirect(url_for('create_player'))

        r = requests.post(f"{PLAYERS_SERVER_URL}api/players", data={
            "username": form.username.data,
            "image_file": filename
        }, files={"image": image})

        if r.status_code == 201:
            flash("Player Adding Succeed", 'success')
        else:
            flash("Player Adding Failed", 'danger')

        return redirect(url_for("all_players"))
    else:
        return render_template("gameplay/players/player_create.html", form=form)


@app.route("/players/<int:player_id>/edit", methods=["GET", "POST"])
def edit_player(player_id: int):
    form = EditPlayerForm()

    if form.validate_on_submit():
        files = {}

        if form.image_file.data is not None:
            image = form.image_file.data
            files = {"image": image}
            if not is_player_image_valid(image):
                flash('Invalid player image', 'danger')
                return redirect(url_for('edit_player', player_id=player_id))

        r = requests.put(f"{PLAYERS_SERVER_URL}api/players/{player_id}", json={
            "username": form.username.data
        }, files=files)

        if r.status_code == 202:
            flash("Player Editing Succeed", 'success')
        else:
            flash("Player Editing Failed", 'danger')

        return redirect(url_for("all_players"))
    else:
        player = requests.get(f"{PLAYERS_SERVER_URL}api/players/{player_id}")
        if player.status_code == 200:
            player = player.json()
            player["image_url"] = f"{PLAYERS_SERVER_URL}{player['image_url']}"
            return render_template("gameplay/players/player_edit.html", form=form, player=player)
        else:
            abort(player.status_code)


@app.route('/sign-in', methods=('POST', 'GET'))
def sign_in():
    form = AccountSignInForm()

    if form.validate_on_submit():
        login = form.login.data
        password = generate_password_hash(form.password.data)

        r = requests.post(f'{ACCOUNTS_SERVER_URL}api/accounts/authentication', data={
            'login': login,
            'password': password
        })
        if r.status_code != 200:
            flash('Invalid login or password', 'danger')
            return render_template('gameplay/signing/sign_in.html', form=form)

        role = r.json().get('role', '')
        if not isinstance(role, str):
            role = 'UNKNOWN'

        role = role.lower()
        session['guest'] = role == 'guest'
        session['admin'] = role == 'admin'
        session['user-signed-in'] = True

        flash(f'Signing in as {role} succeed', 'success')
        return redirect(url_for('home'))

    return render_template('gameplay/signing/sign_in.html', form=form)


@app.route('/sign-out', methods=('GET',))
def sign_out():
    session.clear()

    flash('Signing out succeed', 'success')
    return redirect(url_for('home'))
