class Unicorn:
    def __init__(self, name: str, color: str):
        self.name = name
        self.color = color
        self.happiness = 100
    def feed(self, food: str):
        if food == "apple":
            self.happiness += 10
        elif food == "carrot":
            self.happiness += 5
        else:
            self.happiness -= 5
        print(f"{self.name} the {self.color} unicorn is now {self.happiness} happy!")
