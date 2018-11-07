from bbcon import Bbcon
from behavior import *
from zumo_button import ZumoButton

def main():

    bbcon = Bbcon()
    lineRider = FollowLine(bbcon)
    obstruction = Obstruction(bbcon)
    photo = Photo(bbcon)

    bbcon.add_behavior(lineRider)
    bbcon.add_behavior(obstruction)
    bbcon.add_behavior(photo)

    ZumoButton().wait_for_press()

    while True:
        bbcon.run_one_timestep()


if __name__ == "__main__":
    main()