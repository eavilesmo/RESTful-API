# -------------------------
# IMPORTS
# -------------------------
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import RadioField, IntegerField
from wtforms.validators import InputRequired

# Creating an instance of Flask
app = Flask(__name__)
app.config["SECRET_KEY"] = "22_this_is_a_flask_test_22"

# -------------------------
# CONSTANTS
# -------------------------

MSG_ATTACKER_DEAD = 0
MSG_ATTACKED_DEAD = 1
MSG_ATTACK_PERFORMED = 2
MSG_ATTACK_FAILED = 3

# -------------------------
# VARIABLES
# -------------------------
radio_bt = [("Option 1", "Create a new spaceship"), 
            ("Option 2", "See all spaceships created"),
            ("Option 3", "Attack a spaceship")]
redirect_message = """<h2>Welcome to FTC!</h2><button type="button" onclick="window.location.href='/home'">Home</button>"""

attack_dict = {MSG_ATTACKER_DEAD: "The attacker spaceship has no life left!", 
               MSG_ATTACKED_DEAD: "The spaceship you are trying to attack has no life left!", 
               MSG_ATTACK_PERFORMED: "Spaceship {} was attacked by spaceship {}!",
               MSG_ATTACK_FAILED: "The spaceship ID is not correct. Please make sure the spaceship is created or that you introduced the number correctly."}

# -------------------------
# CLASSES
# -------------------------
class Spaceship():
    def __init__(self, spaceship_life, ship_list:list):
        self.health = spaceship_life
        self.is_alive = True
        self.id = len(ship_list)
        ship_list.append(self)
        self.weapon = Weapon()
    
    def attack(self, spaceship_id, weapon):
        if self.health <= 0:
            return MSG_ATTACKER_DEAD
        if Game.ship_list[spaceship_id].health <= 0:
            return MSG_ATTACKED_DEAD
        else:
            Game.ship_list[spaceship_id].health -= weapon.weapon_damage
            return MSG_ATTACK_PERFORMED

class Game():
    ship_list = []

class Weapon():
    def __init__(self):
        self.weapon_damage = 1
    
def get_components(ship_list):
    elements = []
    for elem in ship_list:
        elements.append("Spaceship " + str(elem.id))
    return elements

class HomePage(FlaskForm):
    radio_buttons = RadioField(choices = radio_bt)

class CreatePage(FlaskForm):
    spaceship_life = IntegerField("Spaceship life: ", validators=[InputRequired()])

class AttackPage(FlaskForm):
    attacker_ship = IntegerField("Attacker spaceship: ", validators=[InputRequired()])
    attacked_ship = IntegerField("Attacked spaceship: ", validators=[InputRequired()])

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
            return redirect(url_for("create_ship"))
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

@app.route("/create-ship", methods=["GET", "POST"])
def create_ship():
    form = CreatePage()
    if form.validate_on_submit():
        print(form.spaceship_life.data)
        spaceship_life = int(form.spaceship_life.data)
        
        if spaceship_life > 0 and spaceship_life < 100:
            Spaceship(spaceship_life, Game.ship_list)
            message = "The spaceship has been created! Life: {}".format(spaceship_life)
            return render_template("create-ship.html", form=form, message = message)
        else:
            message = "The life of the spaceship must be a number between 1 and 100. Please try again."
            return render_template("create-ship.html", form=form, message = message)
    return render_template("create-ship.html", form=form)

@app.route("/attack", methods=["GET", "POST"])
def attack():
    form = AttackPage()
    if form.validate_on_submit():
        try:
            attacker_id = int(form.attacker_ship.data)
            attacked_id = int(form.attacked_ship.data)
            attacker = Game.ship_list[attacker_id]
            result = attacker.attack(attacked_id, attacker.weapon)
            if result == MSG_ATTACKER_DEAD:
                message = attack_dict[MSG_ATTACKER_DEAD]
                return render_template("attack.html", form=form, message = message)
            elif result == MSG_ATTACKED_DEAD:
                message = message = attack_dict[MSG_ATTACKED_DEAD]
                return render_template("attack.html", form=form, message = message)
            elif result == MSG_ATTACK_PERFORMED:
                message = message = attack_dict[MSG_ATTACK_PERFORMED].format(attacked_id, attacker_id)
                return render_template("attack.html", form=form, message = message)
        except IndexError:
            message = attack_dict[MSG_ATTACK_FAILED]
            return render_template("attack.html", form=form, message = message)
    return render_template("attack.html", form=form)

# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
