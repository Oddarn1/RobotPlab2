from abc import abstractmethod

from reflectance_sensors import *
from ultrasonic import *
from camera import *


class Sensob:                                      # interface mellom en eller flere sensorer i bbcons 'behaviors'

    def __init__(self):
        self.sensors = []
        self.value = None

    def get_value(self):
        return self.value

    @abstractmethod
    def update(self):                             # tvinger sensorer til å få verdier en gang per iterasjon
        return

    def reset(self):
        for sensor in self.sensors:
            sensor.reset()


class ReflectanceSensob(Sensob):

    def __init__(self):
        super(ReflectanceSensob, self).__init__()
        self.sensor = ReflectanceSensors()
        self.sensors.append(self.sensor)

    def update(self):                             # returnerer list of values, [left, midleft, midright, right]
        self.sensor.update()
        self.value = self.sensor.get_value()
        return self.value

    def get_value(self):                          # returnerer list of values, [left, midleft, midright, right]
        return self.value


class UltrasonicSensob(Sensob):

    def __init__(self):
        super(UltrasonicSensob, self).__init__()
        self.sensor = Ultrasonic()
        self.sensors.append(self.sensor)
        # print("US-sensob created.")

    def update(self):
        self.sensor.update()
        self.value = self.sensor.get_value()
        return self.value

    def get_value(self):
        return self.value                         # returnerer value som distanse i cm


class CameraSensob(Sensob):
    def __init__(self):
        super(CameraSensob, self).__init__()
        self.sensor = Camera()
        self.sensors.append(self.sensor)
        self.value = None

    def update(self):
        self.sensor.update()
        self.value = self.sensor.get_value()
        return self.value

    def get_value(self):
        return self.value                         # returnerer value som en RGB-array
