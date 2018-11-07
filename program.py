from bbcon import Bbcon
from behavior import *
from zumo_button import ZumoButton


def main():
    """
    Runs the program
    """

    bbcon = Bbcon()
    follow_line = FollowLine(bbcon)
    obstruction = Obstruction(bbcon)
    ninja_geir = Reverse(bbcon)
    kikkert_stine = Photo(bbcon)

    bbcon.add_behavior(follow_line)
    bbcon.add_behavior(obstruction)
    bbcon.add_behavior(ninja_geir)
    bbcon.add_behavior(kikkert_stine)

    ZumoButton().wait_for_press()

    while True:
        bbcon.run_one_timestep()


if __name__ == "__main__":
    main()


