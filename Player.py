class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.income = 1
        self.cookies = 0
        self.cookie_click_value = 1
        self.bleed_amount = 20

    def is_alive(self):
        return self.hp > 0

    def income_tick(self):
        self.cookies += self.income

    def click_cookie(self):
        self.cookies += self.cookie_click_value

    def bleed(self):
        self.hp -= self.bleed_amount
