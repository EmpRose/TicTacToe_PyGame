import pygame
import sys

# Pygame initialisieren
pygame.init()

# Fenstergröße und Einstellungen
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# Spielfeld
board = [""] * 9
current_player = "X"
running = True
game_over = False


def draw_grid():
    """Zeichnet das 3x3-Gitter."""
    # Linien (horizontal)
    pygame.draw.line(screen, BLACK, (0, HEIGHT // 3), (WIDTH, HEIGHT // 3), 5)
    pygame.draw.line(screen, BLACK, (0, 2 * HEIGHT // 3), (WIDTH, 2 * HEIGHT // 3), 5)
    # Linien (vertikal)
    pygame.draw.line(screen, BLACK, (WIDTH // 3, 0), (WIDTH // 3, HEIGHT), 5)
    pygame.draw.line(screen, BLACK, (2 * WIDTH // 3, 0), (2 * WIDTH // 3, HEIGHT), 5)


def draw_symbols():
    """Zeichnet X und O auf das Spielfeld."""
    for i, symbol in enumerate(board):
        x = (i % 3) * (WIDTH // 3) + (WIDTH // 6)
        y = (i // 3) * (HEIGHT // 3) + (HEIGHT // 6)
        if symbol == "X":
            pygame.draw.line(screen, RED, (x - 50, y - 50), (x + 50, y + 50), 5)
            pygame.draw.line(screen, RED, (x + 50, y - 50), (x - 50, y + 50), 5)
        elif symbol == "O":
            pygame.draw.circle(screen, BLACK, (x, y), 50, 5)


def get_cell(x, y):
    """Berechnet die Zelle, in die der Spieler geklickt hat."""
    row = y // (HEIGHT // 3)
    col = x // (WIDTH // 3)
    return row * 3 + col


def check_winner():
    """Prüft, ob es einen Gewinner gibt."""
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Zeilen
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Spalten
        (0, 4, 8), (2, 4, 6)              # Diagonalen
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != "":
            return board[combo[0]]  # Rückgabe: "X" oder "O"
    return None


def is_draw():
    """Prüft, ob das Spiel unentschieden ist."""
    return all(cell != "" for cell in board)


def display_message(text):
    """Zeigt eine Nachricht auf dem Bildschirm an."""
    font = pygame.font.Font(None, 74)
    message = font.render(text, True, BLACK)
    screen.blit(message, (WIDTH // 4, HEIGHT // 2))
    pygame.display.flip()


def draw_button():
    """Zeichnet den 'Neue Runde'-Button."""
    button_rect = pygame.Rect(WIDTH // 3, HEIGHT // 1.5, WIDTH // 3, 50)
    pygame.draw.rect(screen, GRAY, button_rect)
    font = pygame.font.Font(None, 36)
    text = font.render("Neue Runde", True, BLACK)
    screen.blit(text, (WIDTH // 3 + 20, HEIGHT // 1.5 + 10))
    return button_rect


def reset_game():
    """Setzt das Spiel zurück."""
    global board, current_player, game_over
    board = [""] * 9
    current_player = "X"
    game_over = False


# Hauptspiel-Schleife
while running:
    # Ereignisse prüfen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Wenn das Spiel vorbei ist, prüfe, ob der Button gedrückt wurde
            if game_over:
                button_rect = draw_button()
                if button_rect.collidepoint(mouse_x, mouse_y):
                    reset_game()

            # Wenn das Spiel läuft, mache den Zug
            elif not game_over:
                cell = get_cell(mouse_x, mouse_y)

                # Setze X oder O, wenn das Feld leer ist
                if board[cell] == "":
                    board[cell] = current_player
                    winner = check_winner()
                    if winner:
                        game_over = True
                        display_message(f"{winner} gewinnt!")
                    elif is_draw():
                        game_over = True
                        display_message("Unentschieden!")
                    else:
                        current_player = "O" if current_player == "X" else "X"

    # Bildschirm aktualisieren
    screen.fill(WHITE)
    draw_grid()
    draw_symbols()

    # Zeichne den Button, wenn das Spiel vorbei ist
    if game_over:
        draw_button()

    pygame.display.flip()

pygame.quit()
sys.exit()