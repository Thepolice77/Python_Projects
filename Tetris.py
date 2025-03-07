import pygame
import random
import time

# Konstanten für das Spielfeld
WIDTH, HEIGHT = 500, 1000
CELL_SIZE = 50
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Farben
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# Tetromino-Formen
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 1, 1], [0, 1, 1]]
]

# Farben der Tetrominos
COLORS = [CYAN, YELLOW, ORANGE, BLUE, GREEN, RED, PURPLE]

# Konstanten für Zeitverzögerung und Beschleunigung
INITIAL_DELAY = 1000
ACCELERATION = 10

# Anzahl der zu löschenden Linien pro Level
LINES_PER_LEVEL = 10

# Funktion zum Zeichnen des Spielfelds
def draw_grid(screen, grid):
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            color = grid[y][x]
            if color:
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)
            pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

# Funktion zum Erstellen eines zufälligen Tetrominos
def get_random_tetromino():
    shape = random.choice(SHAPES)
    color = random.choice(COLORS)
    return shape, color

# Funktion zum Überprüfen, ob ein Tetromino im Spielfeld platziert werden kann
def is_valid_move(grid, tetromino, tetromino_x, tetromino_y):
    for y in range(len(tetromino)):
        for x in range(len(tetromino[0])):
            if tetromino[y][x]:
                if (tetromino_x + x < 0 or tetromino_x + x >= GRID_WIDTH or
                        tetromino_y + y >= GRID_HEIGHT or grid[tetromino_y + y][tetromino_x + x]):
                    return False
    return True

# Funktion zum Überprüfen und Löschen vollständiger Linien
def check_lines(grid):
    lines_to_clear = []
    for y in range(GRID_HEIGHT):
        if all(grid[y]):
            lines_to_clear.append(y)

    for y in lines_to_clear:
        grid.pop(y)
        grid.insert(0, [0] * GRID_WIDTH)

# Funktion zum Anzeigen der Game-Over-Nachricht
def show_game_over(screen):
    font = pygame.font.Font(None, 30)
    text = font.render("Game Over,press r to restart the game", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    return True

# Funktion zum Neustarten des Spiels
def restart_game():
    global current_tetromino, current_color, current_x, current_y, game_over, grid
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            grid[y][x] = 0
    return get_random_tetromino(), GRID_WIDTH // 2 - len(current_tetromino[0]) // 2, 0, False

def  show_next_tetromino(screen):
    next_tetromino,next_color=get_random_tetromino()
    font=pygame.font.Font(None,36)
    text = font.render("Next Tetromino:", True, WHITE)
    screen.blit(text, (WIDTH + 50, 50))

    for y in range(len(next_tetromino)):
        for x in range(len(next_tetromino[0])):
            if next_tetromino[y][x]:
                pygame.draw.rect(screen, next_color, ((WIDTH + 50) + x * CELL_SIZE, (100 + y * CELL_SIZE), CELL_SIZE, CELL_SIZE), 0)
            pygame.draw.rect(screen, BLACK, ((WIDTH + 50) + x * CELL_SIZE, (100 + y * CELL_SIZE), CELL_SIZE, CELL_SIZE), 1)
    pygame.display.update()



#funktion um levels anzuzeigen
def draw_level(screen, level):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Level: {level}", True, WHITE)
    text_rect = text.get_rect()
    text_rect.topleft = (20, HEIGHT - 50)
    screen.blit(text, text_rect)
# Die main-Schleife, die das Spiel ausführt
def main():

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")

    clock = pygame.time.Clock()

    grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

    current_tetromino, current_color = get_random_tetromino()
    current_x = GRID_WIDTH // 2 - len(current_tetromino[0]) // 2
    current_y = 0

    game_over = False

    last_time = 0
    delay = INITIAL_DELAY
    lines_cleared = 0
    level = 1

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if current_x > 0 and is_valid_move(grid, current_tetromino, current_x - 1, current_y):
                current_x -= 1

        if keys[pygame.K_RIGHT]:
            if current_x < GRID_WIDTH - len(current_tetromino[0]) and is_valid_move(grid, current_tetromino, current_x + 1, current_y):
                current_x += 1

        if keys[pygame.K_DOWN]:
            if current_y < GRID_HEIGHT - len(current_tetromino) and is_valid_move(grid, current_tetromino, current_x, current_y + 1):
                current_y += 1

        if keys[pygame.K_UP]:
            new_tetromino = [[current_tetromino[y][x] for y in range(len(current_tetromino))] for x in range(len(current_tetromino[0])-1,-1,-1)]
            if current_x + len(new_tetromino[0]) <= GRID_WIDTH and is_valid_move(grid, new_tetromino, current_x, current_y):
                current_tetromino = new_tetromino

        current_time = time.time()
        if current_time - last_time > delay / 1000:
            if not is_valid_move(grid, current_tetromino, current_x, current_y + 1):
                for y in range(len(current_tetromino)):
                    for x in range(len(current_tetromino[0])):
                        if current_tetromino[y][x]:
                            grid[current_y + y][current_x + x] = current_color

                lines_cleared += 1

                if lines_cleared >= LINES_PER_LEVEL:
                    level += 1
                    lines_cleared = 0
                    if delay > ACCELERATION:
                        delay -= ACCELERATION

                check_lines(grid)

                current_tetromino, current_color = get_random_tetromino()
                current_x = GRID_WIDTH // 2 - len(current_tetromino[0]) // 2
                current_y = 0

                if not is_valid_move(grid, current_tetromino, current_x, current_y):
                    game_over = show_game_over(screen)

            current_y += 1
            last_time = current_time

        screen.fill(BLACK)
        draw_grid(screen, grid)
        draw_level(screen,level)
        show_next_tetromino(screen)# Zeichnen des Level-Felds

        for y in range(len(current_tetromino)):
            for x in range(len(current_tetromino[0])):
                if current_tetromino[y][x]:
                    pygame.draw.rect(screen, current_color, ((current_x + x) * CELL_SIZE, (current_y + y) * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)
                pygame.draw.rect(screen, BLACK, (
                    (current_x + x) * CELL_SIZE, (current_y + y) * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

        pygame.display.update()
        clock.tick(5)

    show_game_over(screen)
    pygame.display.update()

    restart = False
    while not restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart = True

    if restart:
        main()

if __name__ == "__main__":
    pygame.init()
    main()