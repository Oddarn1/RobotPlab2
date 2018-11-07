class Arbitrator:

    # Denne klassen velger en winning-behavior som returneres.

    def choose_action(self, behaviors):
        winning_behavior = None
        max_weight = -1

        for behavior in behaviors:

            # Hvis behavioren skal stoppe returnerer vi umiddelbart denne
            if behavior.halt_request:
                print(behavior.name, " will be recommended")
                return behavior.motor_recommendations

            # Hvis den ikke skal stoppe velger behavior med høyest weight
            elif behavior.weight > max_weight:
                max_weight = behavior.weight
                winning_behavior = behavior

        # Kjører bare fremover hvis ingen behavior ble funnet,
        if winning_behavior is None:
            print("Found no behavior, driving forwards")
            return ["f"]
        print(winning_behavior.name, " will be recommended")
        return winning_behavior.motor_recommendations
