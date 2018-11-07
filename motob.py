from motors import Motors
from sensob import CameraSensob
from time import sleep


class Motob:

    def __init__(self, bbcon):
        self.bbcon = bbcon
        self.values = []
        self.motor = Motors()
        self.photograph = False
        self.camera=CameraSensob()

    def update(self, motor_recommendation):
        # Mottar en anbefaling fra bbcon og behaviors

        self.values = motor_recommendation
        self.operationlize()

    def operationlize(self):
        # Henter ut første verdi fra anbefalinger, antall grader gis som andre vektor i self.values dersom anbefaling er
        # 'l' eller 'r'

        value=self.values[0]
        print("Motor Recommendation = ", value)
        if value == "f":
            print("Forward")
            self.motor.set_value([0.5, 0.5],0.15)
        elif value == "l":
            print("Left")
            self.motor.set_value([-1,1], self.turn_n_degrees(self.values[1]))
        elif value == "r":
            print("Right")
            self.motor.set_value([1,-1], self.turn_n_degrees(self.values[1]))
        elif value == 'fl':
            print('Left and forward')
            self.motor.set_value([0.05, 0.35],0.15)
        elif value == 'fr':
            print('Right and forward')
            self.motor.set_value([0.35, 0.05],0.15)
        elif value == 't':
            self.motor.set_value([-0.5, 0.5], 0.25)
            self.motor.set_value([0.5, -0.5], 0.25)
            print("Found red!")
            self.motor.set_value([-1, 1], self.turn_n_degrees(180))
            self.bbcon.photo_taken()
        elif value == "s":
            print("Stop")
            self.motor.stop()
            self.photograph = True
            sleep(1)
        elif value == 'p':
            self.camera.update()

    @staticmethod
    def turn_n_degrees(deg):
        # Returnerer antall sekunder motorene må kjøres på full speed, henholdsvis frem og bak for å tilsvare grader
        return 0.0028 * deg
