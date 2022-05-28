# -------------------------
# IMPORTS
# -------------------------
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import RadioField, StringField
from wtforms.validators import InputRequired

# Creating an instance of Flask
app = Flask(__name__)
app.config["SECRET_KEY"] = "22_this_is_a_flask_test_22"

# -------------------------
# VARIABLES
# -------------------------
radio_bt = [("Option 1", "Create a new spaceship"), 
            ("Option 2", "See all spaceships created"),
            ("Option 3", "Attack a spaceship")]
redirect_message = """<h2>Welcome to FTC!</h2><button type="button" onclick="window.location.href='/home'">Home</button>"""
attack_error = "The spaceship ID is not correct. Please make sure the spaceship is created or that you introduced the number correctly."

# -------------------------
# CLASSES
# -------------------------
class Spaceship():
    def __init__(self, ship_list:list):
        self.health = 10
        self.is_alive = True
        self.id = len(ship_list)
        ship_list.append(self)

    def check_status(self):
        if self.health > 0:
            return True
        else:
            return False
    
    def attack(self, spaceship_id):
        Game.ship_list[spaceship_id].health -= 1

class Game():
    ship_list = []
    
def get_components(ship_list):
    elements = []
    for elem in ship_list:
        elements.append("Spaceship " + str(elem.id))
    return elements

class HomePage(FlaskForm):
    radio_buttons = RadioField(choices = radio_bt)

class AttackPage(FlaskForm):
    attacker_ship = StringField("Attacker spaceship: ", validators=[InputRequired()])
    attacked_ship = StringField("Attacked spaceship: ", validators=[InputRequired()])

# -------------------------
# FUNCTIONS
# -------------------------

# Creating welcome page
@app.route("/", methods=["GET", "POST"])
def welcome_page():
    return redirect_message

# Creating home page
@app.route("/home", methods=["GET", "POST"])
def home():
    form = HomePage()
    if form.validate_on_submit():
        if form.radio_buttons.data == "Option 1":
            Spaceship(Game.ship_list)
            message = "The spaceship has been created!"
            return render_template("home.html", form=form, message = message)
        if form.radio_buttons.data == "Option 2":
            all_elements = get_components(Game.ship_list)
            if len(all_elements) == 0:
                message = "There are no spaceships created yet!"
                return render_template("home.html", form=form, message = message)
            else:
                return render_template("home.html", form=form, elements = all_elements)
        if form.radio_buttons.data == "Option 3":
            return redirect(url_for("attack"))
    return render_template("home.html", form=form)

@app.route("/attack", methods=["GET", "POST"])
def attack():
    form = AttackPage()
    if form.validate_on_submit():
        try:
            attacker = int(form.attacker_ship.data)
            attacked = int(form.attacked_ship.data)
            Game.ship_list[attacker].attack(attacked)
            message = "Spaceship {} was attacked by spaceship {}!".format(attacked, attacker)
            return render_template("attack.html", form=form, message = message)
        except (ValueError, IndexError):
            message = attack_error
            return render_template("attack.html", form=form, message = message)
    return render_template("attack.html", form=form)

# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
