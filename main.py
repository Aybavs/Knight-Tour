import tkinter as tk
from tkinter import messagebox

class Chessboard:
    def __init__(self, master):
        self.master = master
        self.size = 4
        self.score = 0
        self.selected_squares = []
        self.player_name = None
        self.create_name_window()

    def create_name_window(self):
        self.name_window = tk.Toplevel(self.master)
        self.name_window.title("Player Name")
        self.name_label = tk.Label(self.name_window, text="Enter your name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(self.name_window)
        self.name_entry.pack()
        self.name_button = tk.Button(self.name_window, text="Submit", command=self.save_name)
        self.name_button.pack()

    def save_name(self):
        self.player_name = self.name_entry.get()
        self.name_window.destroy()
        self.create_widgets()

    def create_widgets(self):
        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack(side=tk.LEFT, padx=10)

        self.score_label = tk.Label(self.master, text="Score: {}".format(self.score))
        self.score_label.pack(side=tk.TOP, pady=10)

        self.size_button_frame = tk.Frame(self.master)
        self.size_button_frame.pack(side=tk.TOP, padx=10)

        self.size_label = tk.Label(self.size_button_frame, text="Board Size:")
        self.size_label.pack(side=tk.LEFT)

        self.size_var = tk.StringVar(self.size_button_frame)
        self.size_var.set("4x4")
        self.size_option = tk.OptionMenu(self.size_button_frame, self.size_var, "4x4", "5x5", "6x6", "7x7", "8x8", command=self.change_size)
        self.size_option.pack(side=tk.LEFT)

        self.leaderboard_frame = tk.Frame(self.master)
        self.leaderboard_frame.pack(side=tk.BOTTOM, padx=10)

        self.leaderboard_button = tk.Button(self.leaderboard_frame, text="Leaderboard", fg="blue", cursor="hand2", command=self.open_leaderboard)
        self.leaderboard_button.pack()

        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset_game)
        self.reset_button.pack(side=tk.BOTTOM, pady=10)

        self.create_board()

    def create_board(self):
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        self.board = []

        for i in range(self.size):
            row = []
            for j in range(self.size):
                color = "black" if (i+j) % 2 == 0 else "white"
                button = tk.Button(self.board_frame, text="", width=2, height=1, bg=color, command=lambda i=i, j=j: self.select_square(i, j))
                button.grid(row=i, column=j)
                row.append(button)
            self.board.append(row)

    def change_size(self, value):
        self.size = int(value[0])
        self.create_board()
        self.reset_game()

    def open_leaderboard(self):
        leaderboard_filename = f"leaderboard_{self.size}x{self.size}.txt"
        leaderboard_window = tk.Toplevel(self.master)
        leaderboard_window.title(f"Leaderboard - {self.size}x{self.size}")

        try:
            with open(leaderboard_filename, "r") as file:
                leaderboard_data = file.readlines()

            scores = [(line.strip().split(":")[0], int(line.strip().split(":")[1])) for line in leaderboard_data]
            scores.sort(key=lambda x: (-x[1], x[0]))
    
            for i, (name, score) in enumerate(scores, start=1):
                tk.Label(leaderboard_window, text=f"{i}. {name}: {score}").pack()

        except FileNotFoundError:
            tk.Label(leaderboard_window, text="Leaderboard is empty.").pack()


    def reset_game(self):
        self.score = 0
        self.score_label.config(text="Score: {}".format(self.score))
        self.selected_squares = []
        self.create_board()

    def select_square(self, i, j):
        if (i, j) not in self.selected_squares:
            move_number = len(self.selected_squares) + 1
            self.selected_squares.append((i, j))
            self.board[i][j].config(state=tk.DISABLED, text=str(move_number))
            self.update_score()
            if move_number == self.size ** 2:
                self.place_horse(i, j)
                self.save_score()
                messagebox.showinfo("Game Over", "Congratulations! You won the game.")
            else:
                self.possible_moves(i, j)

    def possible_moves(self, i, j):
        valid_moves = []
        moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for dx, dy in moves:
            new_i, new_j = i + dx, j + dy
            if 0 <= new_i < self.size and 0 <= new_j < self.size and (new_i, new_j) not in self.selected_squares:
                valid_moves.append((new_i, new_j))

        for x in range(self.size):
            for y in range(self.size):
                if (x, y) not in self.selected_squares and self.check_move((i, j), (x, y)):
                    self.board[x][y].config(bg="red", state=tk.NORMAL)
                else:
                    color = "black" if (x + y) % 2 == 0 else "white"
                    self.board[x][y].config(bg=color, state=tk.DISABLED)

        if not valid_moves:
            self.save_score()

    def save_score(self):
        if self.player_name:
            leaderboard_filename = f"leaderboard_{self.size}x{self.size}.txt"
            with open(leaderboard_filename, "a") as file:
                file.write(f"{self.player_name}: {self.score}\n")
            messagebox.showinfo("Game Over", f"{self.player_name}, your score is {self.score}.")
        else:
            messagebox.showinfo("Game Over", f"Your score is {self.score}.")

    def check_move(self, start, end):
        x1, y1 = start
        x2, y2 = end
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        return (dx == 1 and dy == 2) or (dx == 2 and dy == 1)

    def update_score(self):
        self.score += 1
        self.score_label.config(text="Score: {}".format(self.score))
        if self.score == self.size**2:
            self.save_score()
            messagebox.showinfo("Game Over", "Congratulations! You won the game.")

root = tk.Tk()
root.title("Knight's Tour")

chessboard = Chessboard(root)

root.mainloop()
