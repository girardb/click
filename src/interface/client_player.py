class ClientPlayer:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.income = 1
        self.cookies = 0
        self.cookie_click_value = 1
        self.game_state = {}

    def update_game_state(self, game_state):
        self.game_state = game_state
        # update cookies
        # update hp
        # update ...

    def display_game_state(self):
        print(f"{self.game_state['cookies']} cookies, {self.game_state['income']} income")
