from motors import Motors
from sensob import CameraSensob
from time import sleep

class Motob:
    """

    """
    def __init__(self, bbcon):
        self.bbcon = bbcon
        # Most recent motor recommendation sent to the motob
        self.values = []
        # Objektet Motors
        self.motor = Motors()
        self.speedDic = {100: 1, 75: 0.75, 50: 0.5, 40: 0.4, 35: 0.35, 33: 0.33, 30: 0.3, 25: 0.25, 20: 0.2, 10: 0.1, 5: 0.05, 0: 0.0}
        self.can_take_photo = False

    def update(self, motor_recommandation):
        """
        receive a new motor recommendation, load it into the value slot, and operationalize it.
        :param motorvalue:
        :return: Nothing
        """
        self.values = motor_recommandation
        self.operationlize()

    def operationlize(self):
        """
        L - Left
        R - Right
        F - Forwards
        S - Stop
        B - Backwards
        FL - Turning left while driving forward
        FR - Turning right while driving forward
        The second vector elemnt is the degree og turning.
        Exp: rec
        :return:
        """
        value=self.values[0]
        print("Motor Req = ", value)
        if value == "f":
            print("Forward")
            self.motor.set_value([self.speedDic[50], self.speedDic[50]],0.15)
        elif value == "l":
            print("Left")
            self.motor.set_value([-1,1], self.turn_n_degrees(self.values[1]))
        elif value == "r":
            print("Right")
            self.motor.set_value([1,-1], self.turn_n_degrees(self.values[1]))
        elif value == 'fl':
            print('Left and forward')
            self.motor.set_value([self.speedDic[5], self.speedDic[35]],0.15)
        elif value == 'fr':
            print('Right and forward')
            self.motor.set_value([self.speedDic[35], self.speedDic[5]],0.15)
        elif value == 't':
            self.motor.set_value([-1, 1], 0.5)
            self.motor.set_value([1, -1], 0.5)
            print("Doing some sick tricks! #hardcore")
            self.bbcon.photo_taken()
        elif value == "s":
            print("Stop")
            self.motor.stop()
            self.can_take_photo = True
            sleep(1)
        elif value == 'p':
            print('CHEEEEESE!')
            CameraSensob().update()

    @staticmethod
    def turn_n_degrees(deg):
        """
        Takes in the desired turn degree and returns how long the motors have to turn at full speed.
        :param deg: Desired turn degree.
        :return: Time.
        """
        return 0.0028 * deg
