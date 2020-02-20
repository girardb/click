from Client import Client
import tkinter as tk


class Interface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.wm_title("Click")

        self.frame_whole_window = tk.Frame(self.root)
        self.frame_whole_window.grid()
        self.frame_whole_window.config(background="#C0C0C0")

        self.client = Client()
        self.client.start_sockets()

        # input field for player name

        login_button = tk.Button(master=self.frame_whole_window,
                                 text="login",
                                 command=self.client.send_login)
        login_button.grid()
        start_game_button = tk.Button(master=self.frame_whole_window,
                                      text="start game",
                                      command=self.client.start_game)
        start_game_button.grid()
        click_button = tk.Button(master=self.frame_whole_window,
                                 text="click",
                                 command=self.client.send_click)
        click_button.grid()
        self.root.mainloop()

if __name__ == '__main__':
    app = Interface()
