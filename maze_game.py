import pygame
import random
print ("Hello, world")
# Initialize pygame
pygame.init()

# Set up game window
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Maze Game")

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up font
FONT = pygame.font.SysFont(None, 40)

class Maze:
    def __init__(self, rows, columns, cell_size, wall_color, path_color):
        self.rows = rows
        self.columns = columns
        self.cell_size = cell_size
        self.wall_color = wall_color
        self.path_color = path_color
        self.maze = self.generate_maze()
    def get_size (self):
        return self.cell_size
    def draw(self):
        for row in range(self.rows):
            for col in range(self.columns):
                if self.maze[row][col] == 1:
                    pygame.draw.rect(game_window, self.wall_color, (col*self.cell_size, row*self.cell_size, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(game_window, self.path_color, (col*self.cell_size, row*self.cell_size, self.cell_size, self.cell_size))

    def generate_maze(self):
        maze = [[1 for col in range(self.columns)] for row in range(self.rows)]
        for row in range(1, self.rows-1):
            for col in range(1, self.columns-1):
                if row % 2 == 0 or col % 2 == 0:
                    maze[row][col] = 0

        start_row = random.randint(1, self.rows-2)
        start_col = random.randint(1, self.columns-2)
        maze[start_row][start_col] = 2

        goal_row = random.randint(1, self.rows-2)
        goal_col = random.randint(1, self.columns-2)
        maze[goal_row][goal_col] = 3

        return maze

class Player:
    def __init__(self, x, y, color, player_size):
        self.x = x
        self.y = y
        self.color = color
        self.player_size = player_size

    def draw(self):
        pygame.draw.rect(game_window, self.color, (self.x, self.y, self.player_size, self.player_size))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def collide(self, maze):
        if maze.maze[self.y//maze.get_size()][self.x//maze.get_size()] == 1:
            return True
        return False

    def is_at_goal(self, goal):
        if self.x == goal[0] and self.y == goal[1]:
            return True
        return False

# Set up game loop
def game_loop():
    maze = Maze(rows=21, columns=21, cell_size=20, wall_color=BLACK, path_color=WHITE)
    player = Player(x=0, y=0, color=GREEN, player_size=maze.cell_size)

    dx = 0
    dy = 0

    # Set up timer
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    elapsed_time = 0

    # Game loop
    game_over = False
    while not game_over:
            goal_col = 5
            goal_row = 5
    # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        dx = -maze.cell_size
                    elif event.key == pygame.K_RIGHT:
                        dx = maze.cell_size
                    elif event.key == pygame.K_UP:
                        dy = -maze.cell_size
                    elif event.key == pygame.K_DOWN:
                        dy = maze.cell_size

            # Move player
            player.move(dx, dy)
            dx = 0
            dy = 0

            # Check for collision with walls
            if player.collide(maze):
                game_over = True

            # Check for goal
            if player.is_at_goal((maze.cell_size*goal_col, maze.cell_size*goal_row)):
                game_over = True

                # Clear screen
                game_window.fill(BLACK)

    # Draw maze and player
    maze.draw()
    player.draw()

    # Update screen
    pygame.display.update()

    # Update timer
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    timer_text = FONT.render(f"Time: {elapsed_time}", True, BLUE)
    game_window.blit(timer_text, (WINDOW_WIDTH - 150, 10))

    # Set game FPS
    clock.tick(30)
game_loop()
# Quit pygame
pygame.quit()