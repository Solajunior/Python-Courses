import random
import tkinter as tk


class BombDodgerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Bomb Dodger")
        self.root.resizable(False, False)

        self.width = 500
        self.height = 650
        self.root.geometry(f"{self.width}x{self.height}")

        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="#0f172a", highlightthickness=0)
        self.canvas.pack()

        self.player = self.canvas.create_rectangle(220, 590, 280, 630, fill="#38bdf8", outline="#0ea5e9")
        self.player_x = 220

        self.score = 0
        self.score_text = self.canvas.create_text(10, 10, anchor="nw", text=f"Score: {self.score}", fill="white", font=("Arial", 16, "bold"))
        self.instructions = self.canvas.create_text(
            self.width // 2,
            30,
            text="Use ← → or A / D to dodge the bombs",
            fill="#cbd5e1",
            font=("Arial", 12),
        )

        self.bombs = []
        self.keys = set()
        self.running = True

        self.canvas.create_text(self.width // 2, self.height // 2 - 60, text="Bomb Dodger", fill="white", font=("Arial", 26, "bold"))
        self.canvas.create_text(self.width // 2, self.height // 2, text="Avoid the falling bombs!", fill="#93c5fd", font=("Arial", 16))
        self.canvas.create_text(self.width // 2, self.height // 2 + 40, text="Press Esc to quit", fill="#94a3b8", font=("Arial", 12))

        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)
        self.root.focus_set()

        self.spawn_bomb()
        self.update_game()

    def on_key_press(self, event):
        if event.keysym in {"Left", "a", "A"}:
            self.keys.add("left")
        elif event.keysym in {"Right", "d", "D"}:
            self.keys.add("right")
        elif event.keysym == "Escape":
            self.root.destroy()

    def on_key_release(self, event):
        if event.keysym in {"Left", "a", "A"}:
            self.keys.discard("left")
        elif event.keysym in {"Right", "d", "D"}:
            self.keys.discard("right")

    def move_player(self):
        step = 12
        if "left" in self.keys and self.player_x > 0:
            self.player_x -= step
        if "right" in self.keys and self.player_x < self.width - 60:
            self.player_x += step

        self.canvas.coords(self.player, self.player_x, 590, self.player_x + 60, 630)

    def spawn_bomb(self):
        if not self.running:
            return

        size = random.randint(16, 28)
        x = random.randint(0, self.width - size)
        bomb = self.canvas.create_oval(x, -size, x + size, 0, fill="#ef4444", outline="#b91c1c")
        speed = random.randint(6, 10) + (self.score // 5)
        self.bombs.append([bomb, x, -size, size, speed])

        delay = max(250, 800 - self.score * 12)
        self.root.after(delay, self.spawn_bomb)

    def update_game(self):
        if not self.running:
            return

        self.move_player()

        remaining_bombs = []
        for bomb, x, y, size, speed in self.bombs:
            new_y = y + speed
            self.canvas.move(bomb, 0, speed)

            if new_y + size >= self.height:
                self.canvas.delete(bomb)
                self.score += 1
                self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
                continue

            if self.check_collision(bomb, x, new_y, size):
                self.end_game()
                return

            remaining_bombs.append([bomb, x, new_y, size, speed])

        self.bombs = remaining_bombs
        self.root.after(16, self.update_game)

    def check_collision(self, bomb, x, y, size):
        player_x1, player_y1, player_x2, player_y2 = self.canvas.coords(self.player)
        bomb_x1, bomb_y1, bomb_x2, bomb_y2 = self.canvas.coords(bomb)

        return (
            player_x1 < bomb_x2
            and player_x2 > bomb_x1
            and player_y1 < bomb_y2
            and player_y2 > bomb_y1
        )

    def end_game(self):
        self.running = False
        self.canvas.create_text(
            self.width // 2,
            self.height // 2,
            text=f"Game Over\nScore: {self.score}",
            fill="white",
            font=("Arial", 24, "bold"),
        )
        self.canvas.create_text(
            self.width // 2,
            self.height // 2 + 50,
            text="Press Esc to close",
            fill="#cbd5e1",
            font=("Arial", 12),
        )


if __name__ == "__main__":
    root = tk.Tk()
    BombDodgerGame(root)
    root.mainloop()
