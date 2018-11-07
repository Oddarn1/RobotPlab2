from abc import abstractclassmethod
from sensob import *
from imager2 import Imager


class Behavior:

    def __init__(self, bbcon):

        self.bbcon = bbcon                                      # bbcon-controlleren hvor behavioren benyttes
        self.sensobs = []                                       # sensobs-objektene som benyttes
        self.motor_recommendations = ["none"]                   # motor-recommendation som skal sendes til Arbitrator
        self.active_flag = False                                # er behavior aktiv?
        self.halt_request = False                               # sender melding om at behavior skal stoppe.
        self.priority = 0                                       # prioriteten til behavior
        self.match_degree = 0                                   # Enten 0 eller 1. Brukes i samsvar med weight og priority.
        self.weight = self.match_degree * self.priority         # vektingen til behavioren når den benyttes av Arbitrator.
        self.name = ""

    # Tester om behavioren skal deaktiveres
    def consider_deactivation(self):
        pass

    # Tester om behavioren skal aktiveres
    def consider_activation(self):
        pass

    # Funksjon som kjøres for å oppdatere behavior
    def update(self):
        pass

    def sense_and_act(self):
        pass


# stopper roboten hvis sensoren detekterer et objekt
class Obstruction(Behavior):

    def __init__(self, bbcon):
        super(Obstruction,self).__init__(bbcon)
        self.name = "Obstruction"
        self.u_sensob = UltrasonicSensob()
        self.sensobs.append(self.u_sensob)

    # aktiver behavior hvis sensoren ser noe nærmere enn 10 centimeter
    def consider_activation(self):
        val=self.u_sensob.get_value()
        print(val)
        if val < 10:
            self.bbcon.activate_behavior(self)
            self.active_flag = True
            self.halt_request = True

    # DEaktiver behavior hvis sensoren IKKE ser noe nærmere enn 10 centimeter
    def consider_deactivation(self):
        val = self.u_sensob.get_value()
        print(val)
        if val > 10:
            self.bbcon.deactive_behavior(self)
            self.active_flag = False
            self.halt_request = False

    def update(self):

        for sensor in self.sensobs:
            sensor.update()

        if self.active_flag:
            self.consider_deactivation()
        else:
            self.consider_activation()

        # set vekting = 0 hvis ikke aktiv
        if not self.active_flag:
            self.weight = 0
            return

        self.sense_and_act()
        self.weight = self.priority * self.match_degree

    def sense_and_act(self):
        self.motor_recommendations = ["s"]
        self.priority = 1
        self.match_degree = 1

        
# Kjører bare fremover
class DriveForward(Behavior):

    def __init__(self, bbcon):
        super(DriveForward, self).__init__(bbcon)
        self.name = "DriveForward"
        self.active_flag = True
        self.r_sensob = ReflectanceSensob()
        self.sensobs.append(self.r_sensob)
        self.treshold = 0.5

    def consider_activation(self):
        if self.active_flag:
            self.bbcon.activate_behavior(self)

    def consider_deactivation(self):
        return

    def update(self):
        self.r_sensob.update()
        self.consider_activation()
        self.sense_and_act()
        self.weight = self.priority * self.match_degree

    def sense_and_act(self):
        self.motor_recommendations = ["s"]
        self.priority = 0.5
        self.match_degree = 0.5


class FollowLine(Behavior):

    def __init__(self, bbcon):
        super(FollowLine, self).__init__(bbcon)
        self.name = "FollowLine"
        self.r_sensob = ReflectanceSensob()
        self.sensobs.append(self.r_sensob)
        self.treshold = 0.3

    def consider_activation(self):

        for value in self.r_sensob.update():
            if value < self.treshold:
                self.bbcon.activate_behavior(self)
                self.active_flag = True
                return

        # Deaktiverer behavior
        self.weight = 0
        self.bbcon.deactive_behavior(self)
        self.active_flag = False

    def consider_deactivation(self):
        self.consider_activation()

    def update(self):

        self.consider_activation()
        self.sense_and_act()
        self.weight = self.priority * self.match_degree

    def sense_and_act(self):

        self.r_sensob.update()

        if self.r_sensob.get_value()[0] < self.treshold:
            self.motor_recommendations = ["l",30]
            self.match_degree = 0.8

        elif self.r_sensob.get_value()[5] < self.treshold:
            self.motor_recommendations = ["r",30]
            self.match_degree = 0.8

        elif self.r_sensob.get_value()[1] < self.treshold:
            self.motor_recommendations = ["l", 15]
            self.match_degree = 0.8

        elif self.r_sensob.get_value()[4] < self.treshold:
            self.motor_recommendations = ["r",15]
            self.match_degree = 0.8

        else:
            self.motor_recommendations = ["f"]
            self.match_degree = 0.5

        self.priority = 0.5


class Photo(Behavior):
    def __init__(self, bbcon):
        super(Photo, self).__init__(bbcon)
        self.name = "Photo"
        self.c_sensob = CameraSensob()
        self.sensobs.append(self.c_sensob)

    def consider_activation(self):

        if self.bbcon.can_take_photo:
            self.bbcon.activate_behavior(self)
            self.halt_request = True
            self.active_flag = True

    def consider_deactivation(self):

        if not self.bbcon.can_take_photo:
            self.bbcon.deactive_behavior(self)
            self.halt_request = False
            self.active_flag = False

    def update(self):

        if self.active_flag:
            self.consider_deactivation()
        else:
            self.consider_activation()

        self.sense_and_act()
        self.weight = self.priority * self.match_degree

    def sense_and_act(self):

        if self.bbcon.can_take_photo:
            print("Taking photo!")
            image_obj = self.c_sensob.update()
            img = Imager(image=image_obj)
            img.dump_image('/')

            self.match_degree = 0.9

            triple2 = [0] * 3
            for x in range(img.xmax):
                for y in range(img.ymax):
                    t = img.get_pixel(x, y)
                    for i in range(len(triple2)):
                        triple2[i] += t[i]

            print("RGB", triple2)
            print(triple2[0] > triple2[1] and triple2[0] > triple2[2])

            if triple2[0] > triple2[1] and triple2[0] > triple2[2]:
                self.motor_recommendations = ['t']

            else:
                self.motor_recommendations = ['f']
                self.bbcon.photo_taken()

            self.priority = 0.9
