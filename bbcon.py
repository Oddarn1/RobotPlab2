from arbitrator import Arbitrator
from time import sleep
from motorob import Motob
from behavior import Photo

class Bbcon:

    def __init__(self):
        self.behaviors = []                     # behavior-listen, med både inaktive og aktive behaviors
        self.active_behaviors = []              # liste med aktive behaviors
        self.sensobs = []                       # liste med sensor-objekter
        self.motobs = Motob(self)               # list med motor-objekter
        self.arbitrator = Arbitrator()          # arbitrator-objektet, velger winning-behavior
        self.num_timesteps = 0                  # antall timesteps som er kjørt
        self.can_take_photo = False


    # Legger til behavior i listen
    def add_behavior(self, behavior):
        if behavior not in self.behaviors:
            self.behaviors.append(behavior)

    # Legger til sensor-objekt i listen
    def add_sensor(self, sensor):
        if sensor not in self.sensobs:
            self.sensobs.append(sensor)

    # Legger til behavior i listen over active-behaviors
    def activate_behavior(self, behavior):
        if behavior in self.behaviors:
            self.active_behaviors.append(behavior)

    # Fjerner aktive behaviors fra active-behaviors listen
    def deactive_behavior(self, behavior):
        if behavior in self.active_behaviors:
            self.active_behaviors.remove(behavior)

    # Resetter hvis foto er tatt
    def photo_taken(self):
        self.can_take_photo = False
        self.motobs.can_take_photo = False

    # "loopen" til klassen
    def run_one_timestep(self):

        # Oppdaterer behaviors
        for behaviour in self.behaviors:
            behaviour.update()

        # Henter ut motor-recommendations
        print("Active behaviors", self.active_behaviors)
        motor_recoms = self.arbitrator.choose_action(self.active_behaviors)

        # Oppdaterer motobs
        self.motobs.update(motor_recoms)

        if self.motobs.can_take_photo:
            self.can_take_photo = True

        # vent slik at motorene kan gjøre tingen sin
        sleep(0.15)

        # Reset sensorverdiene
        for sensor in self.sensobs:
            sensor.reset()
            
        self.active_behaviors=[]

        self.num_timesteps += 1
