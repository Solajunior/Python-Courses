import random
import tkinter as tk


class BombDodger2Player:
    def __init__(self, root):
        self.root = root
        self.root.title("Bomb Dodger 2 Player")
        self.root.resizable(False, False)

        self.width = 560
        self.height = 650
        self.root.geometry(f"{self.width}x{self.height}")

        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="#111827", highlightthickness=0)
        self.canvas.pack()

        self.player1 = self.canvas.create_rectangle(120, 590, 180, 630, fill="#38bdf8", outline="#0284c7")
        self.player2 = self.canvas.create_rectangle(340, 590, 400, 630, fill="#f59e0b", outline="#d97706")

        self.p1_x = 120
        self.p2_x = 340

        self.score1 = 0
        self.score2 = 0
        self.p1_alive = True
        self.p2_alive = True

        self.canvas.create_text(20, 10, anchor="nw", text="Player 1: A / D", fill="white", font=("Arial", 14, "bold"))
        self.canvas.create_text(self.width - 20, 10, anchor="ne", text="Player 2: ← / →", fill="white", font=("Arial", 14, "bold"))

        self.score_text = self.canvas.create_text(self.width // 2, 20, text=f"P1: {self.score1}   P2: {self.score2}", fill="white", font=("Arial", 16, "bold"))
        self.canvas.create_text(self.width // 2, 45, text="Dodge bombs without getting hit", fill="#cbd5e1", font=("Arial", 12))

        self.bombs = []
        self.keys = set()
        self.running = True

        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)
        self.root.focus_set()

        self.spawn_bomb()
        self.update_game()

    def on_key_press(self, event):
        if event.keysym in {"a", "A"}:
            self.keys.add("p1_left")
        elif event.keysym in {"d", "D"}:
            self.keys.add("p1_right")
        elif event.keysym == "Left":
            self.keys.add("p2_left")
        elif event.keysym == "Right":
            self.keys.add("p2_right")
        elif event.keysym == "Escape":
            self.root.destroy()

    def on_key_release(self, event):
        if event.keysym in {"a", "A"}:
            self.keys.discard("p1_left")
        elif event.keysym in {"d", "D"}:
            self.keys.discard("p1_right")
        elif event.keysym == "Left":
            self.keys.discard("p2_left")
        elif event.keysym == "Right":
            self.keys.discard("p2_right")

    def move_players(self):
        step = 10
        if self.p1_alive:
            if "p1_left" in self.keys and self.p1_x > 0:
                self.p1_x -= step
            if "p1_right" in self.keys and self.p1_x < self.width - 60:
                self.p1_x += step

        if self.p2_alive:
            if "p2_left" in self.keys and self.p2_x > 0:
                self.p2_x -= step
            if "p2_right" in self.keys and self.p2_x < self.width - 60:
                self.p2_x += step

        self.canvas.coords(self.player1, self.p1_x, 590, self.p1_x + 60, 630)
        self.canvas.coords(self.player2, self.p2_x, 590, self.p2_x + 60, 630)

    def spawn_bomb(self):
        if not self.running:
            return

        size = random.randint(16, 28)
        x = random.randint(0, self.width - size)
        bomb = self.canvas.create_oval(x, -size, x + size, 0, fill="#ef4444", outline="#b91c1c")
        speed = random.randint(6, 10)
        self.bombs.append([bomb, x, -size, size, speed])

        delay = random.randint(400, 700)
        self.root.after(delay, self.spawn_bomb)

    def update_game(self):
        if not self.running:
            return

        self.move_players()

        survivors = []
        for bomb, x, y, size, speed in self.bombs:
            new_y = y + speed
            self.canvas.move(bomb, 0, speed)

            if new_y + size >= self.height:
                self.canvas.delete(bomb)
                if self.p1_alive:
                    self.score1 += 1
                if self.p2_alive:
                    self.score2 += 1
                self.canvas.itemconfig(self.score_text, text=f"P1: {self.score1}   P2: {self.score2}")
                continue

            hit_player = self.check_collision(bomb, new_y, size)
            if hit_player == 1:
                self.p1_alive = False
                self.canvas.itemconfig(self.player1, fill="#64748b", outline="#475569")
                self.canvas.create_text(self.width // 2, self.height // 2, text="Player 1 was hit!", fill="white", font=("Arial", 20, "bold"))
            elif hit_player == 2:
                self.p2_alive = False
                self.canvas.itemconfig(self.player2, fill="#64748b", outline="#475569")
                self.canvas.create_text(self.width // 2, self.height // 2 + 30, text="Player 2 was hit!", fill="white", font=("Arial", 20, "bold"))

            if not self.p1_alive and not self.p2_alive:
                self.end_game()
                return

            survivors.append([bomb, x, new_y, size, speed])

        self.bombs = survivors
        self.root.after(16, self.update_game)

    def check_collision(self, bomb, y, size):
        p1_x1, p1_y1, p1_x2, p1_y2 = self.canvas.coords(self.player1)
        p2_x1, p2_y1, p2_x2, p2_y2 = self.canvas.coords(self.player2)
        bomb_x1, bomb_y1, bomb_x2, bomb_y2 = self.canvas.coords(bomb)

        if self.p1_alive and p1_x1 < bomb_x2 and p1_x2 > bomb_x1 and p1_y1 < bomb_y2 and p1_y2 > bomb_y1:
            return 1
        if self.p2_alive and p2_x1 < bomb_x2 and p2_x2 > bomb_x1 and p2_y1 < bomb_y2 and p2_y2 > bomb_y1:
            return 2
        return 0

    def end_game(self):
        self.running = False
        self.canvas.create_text(self.width // 2, self.height // 2 - 60, text="Game Over", fill="white", font=("Arial", 24, "bold"))
        self.canvas.create_text(self.width // 2, self.height // 2, text=f"Final Scores\nPlayer 1: {self.score1}\nPlayer 2: {self.score2}", fill="#f8fafc", font=("Arial", 18))
        self.canvas.create_text(self.width // 2, self.height // 2 + 90, text="Press Esc to close", fill="#cbd5e1", font=("Arial", 12))


if __name__ == "__main__":
    root = tk.Tk()
    BombDodger2Player(root)
    root.mainloop()
