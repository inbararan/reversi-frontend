from tkinter import *
from tkinter.messagebox import showinfo

import protocol


class Window(Frame):
    def create_btn(self, board, x, y):
        frame = Frame(board, width=40, height=40)
        frame.place(x=x * 40, y=y * 40)
        btn = Button(
            frame,
            width=40,
            height=40,
            bg="#999999",
            command=lambda: self.requests_queue.put(protocol.request_do_turn(x, y))
        )
        btn.place(x=0, y=0)
        return btn

    def create_board(self, width, height):
        self.board_buttons = []
        board = Frame(self.master, width=40 * width, height=40 * height, bg="#bbbbbb")
        board.place(x=100, y=40)
        for i in range(width):
            row = []
            for j in range(height):
                row.append(self.create_btn(board, i, j))
            self.board_buttons.append(row)

    def __init__(self, responses_queue, requests_queue, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)
        self.responses_queue = responses_queue
        self.requests_queue = requests_queue

        Button(self.master, text="Start", command=self.start_game).place(x=10, y=40)
        self.master.after(1000, self.handle_resps)

    def start_game(self):
        self.create_board(10, 10)
        self.requests_queue.put(protocol.request_start())

    def handle_resp(self, resp):
        if resp.resp_type == "Error":
            showinfo("Error", resp.resp_info)
        elif resp.resp_type == "Update":
            for loc in resp.resp_info:
                self.board_buttons[loc.pos[0]][loc.pos[1]].config(bg=loc.color)

    def handle_resps(self):
        print('Handling tasks...')
        while not self.responses_queue.empty():
            resp = self.responses_queue.get()
            print("Handling task: %s" % resp)
            self.handle_resp(protocol.parse_response(resp))

        self.master.after(1000, self.handle_resps)  # called only once!


def start(responses_queue, requests_queue):
    root = Tk()
    root.geometry("720x480")
    root.title("Reversi")
    Window(master=root, responses_queue=responses_queue, requests_queue=requests_queue)

    root.mainloop()
