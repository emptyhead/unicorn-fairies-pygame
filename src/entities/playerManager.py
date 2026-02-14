from playerData import PlayerData 

class PlayerManager:
    def __init__(self, data: PlayerData):
        self.data = data

    def handle_icon_click(self, icon_id: str, cost: int, effect_value: int):
        """
        Processes the logic when the user clicks a game icon.
        """
        if self.data.can_afford(cost):
            self._apply_decision(icon_id, cost, effect_value)
            print(f"Action '{icon_id}' successful!")
        else:
            print("Insufficient funds for this choice.")

    def _apply_decision(self, icon_id: str, cost: int, effect_value: int):
        # Internal method to update the state
        self.data.currency -= cost
        self.data.reputation += effect_value
        self.data.decision_history.append(icon_id)
        
        # In a real game, you'd trigger a UI update or scene change here
        self._check_progression()

    def _check_progression(self):
        if self.data.reputation > 10:
            self.data.level += 1
            print(f"Level Up! You are now level {self.data.level}")