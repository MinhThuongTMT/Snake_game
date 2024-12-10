from tkinter import *
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
OBSTACLE_COLOR = "#FFFFFF"

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def create_obstacles():
    obstacles = []
    for _ in range(5):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        obstacle = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=OBSTACLE_COLOR, tag="obstacle")
        obstacles.append([x, y])
    return obstacles


def next_turn(snake, food):
    global paused

    if paused:
        return

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label_score.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake) or check_obstacle_collision(snake, obstacles):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False


def check_obstacle_collision(snake, obstacles):
    x, y = snake.coordinates[0]
    for obstacle in obstacles:
        if x == obstacle[0] and y == obstacle[1]:
            return True
    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 50,
                       font=('consolas', 40), text="Press Enter to Restart", fill="white", tag="restart")
    window.bind('<Return>', restart_game)


def restart_game(event):
    global score, direction, SPEED, paused, snake, food, obstacles
    canvas.delete(ALL)
    score = 0
    direction = 'down'
    SPEED = 100
    paused = False
    label_score.config(text="Score:0")
    snake = Snake()
    food = Food()
    obstacles = create_obstacles()
    next_turn(snake, food)


def toggle_pause(event):
    global paused
    paused = not paused
    if not paused:
        next_turn(snake, food)


def start_game(event):
    canvas.delete("start")
    restart_game(None)


# Cài đặt cửa sổ game
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = 'down'
paused = False

label_score = Label(window, text="Score:{}".format(score), font=('consolas', 20))
label_score.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2,
                   font=('consolas', 40), text="Press Enter to Start", fill="white", tag="start")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<Return>', start_game)
window.bind('<p>', toggle_pause)

snake = None
food = None
obstacles = None

window.mainloop()
