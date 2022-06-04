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
MSG_POWER_MISMATCH = 4

# -------------------------
# VARIABLES
# -------------------------
radio_bt = [("Option 1", "Create a new spaceship"), 
            ("Option 2", "See all spaceships created"),
            ("Option 3", "Attack a spaceship")]

redirect_message = """<h2>Welcome to FTC!</h2><button type="button" onclick="window.location.href='/home'">Home</button>"""

all_spaceships = """<h2>List of all spaceships created: </h2>{}
                    <br><button type="button" onclick="window.location.href='/home'">Home</button>"""

attack_dict = {MSG_ATTACKER_DEAD: "The attacker spaceship has no life left!", 
               MSG_ATTACKED_DEAD: "The spaceship you are trying to attack has no life left!", 
               MSG_ATTACK_PERFORMED: "Spaceship {} was attacked by spaceship {}!",
               MSG_ATTACK_FAILED: "The spaceship ID is not correct. Please make sure the spaceship is created or that you introduced the number correctly.", 
               MSG_POWER_MISMATCH: "The power needed for this action is higher than the power available. Please check again."}

# -------------------------
# CLASSES
# -------------------------
class Spaceship():
    def __init__(self, spaceship_life, spaceship_total_power, ship_list:list):
        self.health = spaceship_life
        self.is_alive = True
        self.id = len(ship_list)
        ship_list.append(self)
        self.weapon = Weapon()
        self.generator = Generator(spaceship_total_power, self.weapon.weapon_power_needed)
    
    def attack(self, spaceship_id, weapon):
        if self.health <= 0:
            return MSG_ATTACKER_DEAD
        if Game.ship_list[spaceship_id].health <= 0:
            return MSG_ATTACKED_DEAD
        if self.generator.attack_is_possible() == True:
            Game.ship_list[spaceship_id].health -= weapon.weapon_damage
            return MSG_ATTACK_PERFORMED
        elif self.generator.attack_is_possible() == False:
            return MSG_POWER_MISMATCH

class Game():
    ship_list = []

class Weapon():
    def __init__(self):
        self.weapon_damage = 1
        self.weapon_power_needed = 3
    
class Generator():
    def __init__(self, spaceship_total_power, weapon_power_needed):
        self.total_power = spaceship_total_power
        self.power_not_in_use = self.total_power
        self.power_consumed_by_weapon = weapon_power_needed
    
    def attack_is_possible(self):
        if self.power_not_in_use >= self.power_consumed_by_weapon:
            self.power_not_in_use = self.total_power - self.power_consumed_by_weapon            
            return True
        else: 
            return False

def get_components(ship_list):
    elements = ""
    for elem in ship_list:
        elements += "Spaceship {}. Life: {}, total power: {}<br>".format(str(elem.id), str(elem.health), str(elem.generator.total_power))
    return elements

class HomePage(FlaskForm):
    radio_buttons = RadioField(choices = radio_bt)

class CreatePage(FlaskForm):
    spaceship_life = IntegerField("Life of the spaceship: ", validators=[InputRequired()])
    spaceship_total_power = IntegerField("Total power of the spaceship: ", validators=[InputRequired()])

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
                return all_spaceships.format(all_elements)
        if form.radio_buttons.data == "Option 3":
            return redirect(url_for("attack"))
    return render_template("home.html", form=form)

@app.route("/create-ship", methods=["GET", "POST"])
def create_ship():
    form = CreatePage()
    if form.validate_on_submit():
        spaceship_life = int(form.spaceship_life.data)
        spaceship_total_power = int(form.spaceship_total_power.data)
        if (spaceship_life > 0 and spaceship_life < 100) and (spaceship_total_power >= 0):
            Spaceship(spaceship_life, spaceship_total_power, Game.ship_list)
            message = "The spaceship has been created! Life: {}, total power: {}".format(spaceship_life, spaceship_total_power)
            return render_template("create-ship.html", form=form, message = message)
        else:
            message = "The life of the spaceship must be a number between 1 and 100 and the total power must be a positive number. Please try again."
            return render_template("create-ship.html", form=form, message = message)
    return render_template("create-ship.html", form=form)

@app.route("/attack", methods=["GET", "POST"])
def attack():
    form = AttackPage()
    if form.validate_on_submit():
        try:
            attacker_id = int(form.attacker_ship.data)
            attacked_id = int(form.attacked_ship.data)

            if attacker_id == attacked_id:
                message = "The attacker spaceship and the attacked spaceship cannot be the same!"
                return render_template("attack.html", form=form, message = message)

            attacker = Game.ship_list[attacker_id]
            result = attacker.attack(attacked_id, attacker.weapon)

            if result == MSG_ATTACKER_DEAD:
                message = attack_dict[MSG_ATTACKER_DEAD]
                return render_template("attack.html", form=form, message = message)
            elif result == MSG_ATTACKED_DEAD:
                message = attack_dict[MSG_ATTACKED_DEAD]
                return render_template("attack.html", form=form, message = message)
            elif result == MSG_ATTACK_PERFORMED:
                message = attack_dict[MSG_ATTACK_PERFORMED].format(attacked_id, attacker_id)
                return render_template("attack.html", form=form, message = message)
            elif result == MSG_POWER_MISMATCH:
                message = attack_dict[MSG_POWER_MISMATCH]
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
