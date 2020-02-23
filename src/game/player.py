class Player:
    def __init__(self, name='unnamed'):
        self.hp = 100
        self.income = 1
        self.cookies = 0
        self.click_value = 1
        self.bleed_amount = 20
        self.name = name

    def is_alive(self):
        return self.hp > 0

    def income_tick(self):
        self.cookies += self.income

    def click(self):
        self.cookies += self.click_value

    def bleed(self):
        self.hp -= self.bleed_amount
