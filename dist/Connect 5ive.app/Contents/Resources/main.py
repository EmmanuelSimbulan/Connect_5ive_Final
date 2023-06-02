import pygame
import sys
from button import Button
import numpy as np
import math
import random

pygame.init()

SCREEN = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Connect 5ive")

background_surface = pygame.Surface((1000, 700))
background_surface.fill('#101b27')

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def multiplayer_window():

    BLUE = ('#273849')
    BLACK = ('#101b27')
    RED = (255,0,0)
    YELLOW = (255,255,0)

    ROW_COUNT = 7
    COLUMN_COUNT = 8


    # For Buttons
    class Powerup:
        def __init__(self, x, y, image, scale):
            width = image.get_width()
            height = image.get_height()
            self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
            self.clicked = False

        def draw(self, surface ):
            btn_action = False
            # getting mouse position
            pos = pygame.mouse.get_pos()
            
            # checking mouseover and clicked conditions
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    btn_action = True

            # drawing button on screen
            surface.blit(self.image, (self.rect.x, self.rect.y))

            return btn_action

    # Creating board function
    def create_board():
        board = np.zeros((ROW_COUNT,COLUMN_COUNT))
        return board

    # Dropping piece function
    def drop_piece(board, row, col, piece):
        board[row][col] = piece

    # Valid location function
    def is_valid_location(board, col):
        return board[ROW_COUNT-1][col] == 0

    # Next open row function
    def get_next_open_row(board, col):
        for r in range(ROW_COUNT):
            if board[r][col] == 0:
                return r

    # Print board function
    def print_board(board):
        print(np.flip(board, 0))

    # Winning move function
    def winning_move(board, piece):

        # Check horizontal locations for win
        for c in range(COLUMN_COUNT - 4):
            for r in range(ROW_COUNT):
                if board[r][c] == piece and board[r][c+1] == piece and \
                board[r][c+2] == piece and board[r][c+3] == piece and \
                    board[r][c+4] == piece:
                    return True

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 4):
                if board[r][c] == piece and board[r+1][c] == piece and \
                board[r+2][c] == piece and board[r+3][c] == piece and \
                    board[r+4][c] == piece:
                    return True

        # Check positively sloped diagonals
        for c in range(COLUMN_COUNT - 4):
            for r in range(ROW_COUNT - 4):
                if board[r][c] == piece and board[r+1][c+1] == piece and \
                board[r+2][c+2] == piece and board[r+3][c+3] == piece and \
                    board[r+4][c+4] == piece:
                    return True

        # Check negatively sloped diagonals
        for c in range(COLUMN_COUNT - 4):
            for r in range(4, ROW_COUNT):
                if board[r][c] == piece and board[r-1][c+1] == piece and \
                board[r-2][c+2] == piece and board[r-3][c+3] == piece and \
                    board[r-4][c+4] == piece:
                    return True

    # Draw board function
    def draw_board(board):
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(screen, BLUE, (c*SQUARESIZE + 200, r*SQUARESIZE+SQUARESIZE + 80, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2 + 200), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2 + 80)), RADIUS)

        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                if board[r][c] == 1:
                    pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2 + 200), height-int(r*SQUARESIZE+SQUARESIZE/2 - 80 )), RADIUS)
                elif board[r][c] == 2:
                    pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2 + 200), height-int(r*SQUARESIZE+SQUARESIZE/2 - 80)), RADIUS)    
        pygame.display.update()


    board = create_board()
    print_board(board)
    game_over = False
    turn = 0

    pygame.init()

    pygame.display.set_caption("Connect 5ive - Multiplayer")

    SQUARESIZE = 75

    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT + 1) * SQUARESIZE

    size = (1000, 700)
    RADIUS = int(SQUARESIZE/2 - 5)

    screen = pygame.display.set_mode(size)

    # Board Surfaces
    background_surface = pygame.Surface((1000, 700))
    background_surface.fill('#101b27')

    # Block Surfaces
    block_surface = pygame.Surface((200, 700))
    block_surface.fill('#101b27')

    # Information Surfaces
    vs_surface = pygame.image.load('graphics/VS.png').convert_alpha()
    vs_rect = vs_surface.get_rect(center=(500, 25))
    pl_profile_surface = pygame.image.load('graphics/player_profile.png').convert_alpha()
    pl_profile_rect = pl_profile_surface.get_rect(center=(120, 45))
    pl_banner_surface = pygame.image.load('graphics/player_banner.png').convert_alpha()
    pl_banner_rect = pl_banner_surface.get_rect(center=(50, 28))
    pl_time_surface = pygame.image.load('graphics/player_time.png').convert_alpha()
    pl_time_rect = pl_time_surface.get_rect(center=(50, 55))
    ai_profile_surface = pygame.image.load('graphics/player_profile.png').convert_alpha()
    ai_profile_rect = ai_profile_surface.get_rect(center=(880, 45))
    ai_banner_surface = pygame.image.load('graphics/player_banner.png').convert_alpha()
    ai_banner_rect = ai_banner_surface.get_rect(center=(950, 28))
    ai_time_surface = pygame.image.load('graphics/ai_time.png').convert_alpha()
    ai_time_rect = ai_time_surface.get_rect(center=(950, 55))

    # Powerup Surfaces
    double_surface = pygame.image.load('graphics/double.png').convert_alpha()
    obstacle_surface = pygame.image.load('graphics/block.png').convert_alpha()
    gravity_surface = pygame.image.load('graphics/gravity.png').convert_alpha()

    # Powerup Objects
    start_btn1 = Powerup(50, 130, double_surface, 1)
    obstacle_btn1 = Powerup(50, 180, obstacle_surface, 1)
    gravity_btn1 = Powerup(47, 230, gravity_surface, 1)
    start_btn2 = Powerup(920, 130, double_surface, 1)
    obstacle_btn2 = Powerup(920, 180, obstacle_surface, 1)
    gravity_btn2 = Powerup(917, 230, gravity_surface, 1)

    screen.blit(background_surface, (0, 0))
    draw_board(board)
    screen.blit(vs_surface, vs_rect)
    screen.blit(pl_profile_surface, pl_profile_rect)
    screen.blit(pl_banner_surface, pl_banner_rect)
    screen.blit(pl_time_surface, pl_time_rect)
    screen.blit(ai_profile_surface, ai_profile_rect)
    screen.blit(ai_banner_surface, ai_banner_rect)
    screen.blit(ai_time_surface, ai_time_rect)
    start_btn1.draw(screen)
    obstacle_btn1.draw(screen)
    gravity_btn1.draw(screen)
    start_btn2.draw(screen)
    obstacle_btn2.draw(screen)
    gravity_btn2.draw(screen)


    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)


    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (200,80, 600, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2 + 80)), RADIUS)
                    screen.blit(block_surface, (0, 0))
                    screen.blit(block_surface, (800, 0))
                    start_btn1.draw(screen)
                    obstacle_btn1.draw(screen)
                    gravity_btn1.draw(screen)
                    start_btn2.draw(screen)
                    obstacle_btn2.draw(screen)
                    gravity_btn2.draw(screen)
                    screen.blit(pl_profile_surface, pl_profile_rect)
                    screen.blit(pl_banner_surface, pl_banner_rect)
                    screen.blit(pl_time_surface, pl_time_rect)
                    screen.blit(ai_profile_surface, ai_profile_rect)
                    screen.blit(ai_banner_surface, ai_banner_rect)
                    screen.blit(ai_time_surface, ai_time_rect)
                    
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2 + 80)), RADIUS)
                    screen.blit(block_surface, (0, 0))
                    screen.blit(block_surface, (800, 0))
                    start_btn1.draw(screen)
                    obstacle_btn1.draw(screen)
                    gravity_btn1.draw(screen) 
                    start_btn2.draw(screen)
                    obstacle_btn2.draw(screen)
                    gravity_btn2.draw(screen)
                    screen.blit(pl_profile_surface, pl_profile_rect)
                    screen.blit(pl_banner_surface, pl_banner_rect)
                    screen.blit(pl_time_surface, pl_time_rect)
                    screen.blit(ai_profile_surface, ai_profile_rect)
                    screen.blit(ai_banner_surface, ai_banner_rect)
                    screen.blit(ai_time_surface, ai_time_rect)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (200,80, 600, SQUARESIZE))
                #print(event.pos)
                # Ask for Player 1 Input
                if turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor((posx-200)/(SQUARESIZE)))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winning_move(board, 1):
                            label = myfont.render("Player 1 Wins!", 1, RED)
                            #abel_rect = label.surface.get_rect(center=(500, 45))
                            screen.blit(label, (200,50))
                            game_over = True

                # Ask for Player 2 Input
                else:
                    posx = event.pos[0]
                    col = int(math.floor((posx-200)/(SQUARESIZE)))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if winning_move(board, 2):
                            label = myfont.render("Player 2 Wins!", 1, YELLOW)
                            screen.blit(label, (200,50))
                            game_over = True
                
                print_board(board)
                draw_board(board)
                


                turn += 1    
                turn = turn % 2

                if game_over:
                    pygame.time.wait(3000)


def vs_ai():

    BLUE = ('#273849')
    BLACK = ('#101b27')
    RED = (255,0,0)
    YELLOW = (255,255,0)

    ROW_COUNT = 7
    COLUMN_COUNT = 8

    PLAYER = 0
    AI = 1

    EMPTY = 0
    PLAYER_PIECE = 1
    AI_PIECE = 2

    WINDOW_LENGTH = 5

    # For Buttons
    class Powerup:
        def __init__(self, x, y, image, scale):
            width = image.get_width()
            height = image.get_height()
            self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
            self.clicked = False

        def draw(self, surface ):
            btn_action = False
            # getting mouse position
            pos = pygame.mouse.get_pos()
            
            # checking mouseover and clicked conditions
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    btn_action = True

            # drawing button on screen
            surface.blit(self.image, (self.rect.x, self.rect.y))

            return btn_action

    # Creating board function
    def create_board():
        board = np.zeros((ROW_COUNT,COLUMN_COUNT))
        return board

    # Dropping piece function
    def drop_piece(board, row, col, piece):
        board[row][col] = piece

    # Valid location function
    def is_valid_location(board, col):
        return board[ROW_COUNT-1][col] == 0

    # Next open row function
    def get_next_open_row(board, col):
        for r in range(ROW_COUNT):
            if board[r][col] == 0:
                return r

    # Print board function
    def print_board(board):
        print(np.flip(board, 0))

    # Winning move function
    def winning_move(board, piece):

        # Check horizontal locations for win
        for c in range(COLUMN_COUNT - 4):
            for r in range(ROW_COUNT):
                if board[r][c] == piece and board[r][c+1] == piece and \
                board[r][c+2] == piece and board[r][c+3] == piece and \
                    board[r][c+4] == piece:
                    return True

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 4):
                if board[r][c] == piece and board[r+1][c] == piece and \
                board[r+2][c] == piece and board[r+3][c] == piece and \
                    board[r+4][c] == piece:
                    return True

        # Check positively sloped diagonals
        for c in range(COLUMN_COUNT - 4):
            for r in range(ROW_COUNT - 4):
                if board[r][c] == piece and board[r+1][c+1] == piece and \
                board[r+2][c+2] == piece and board[r+3][c+3] == piece and \
                    board[r+4][c+4] == piece:
                    return True

        # Check negatively sloped diagonals
        for c in range(COLUMN_COUNT - 4):
            for r in range(4, ROW_COUNT):
                if board[r][c] == piece and board[r-1][c+1] == piece and \
                board[r-2][c+2] == piece and board[r-3][c+3] == piece and \
                    board[r-4][c+4] == piece:
                    return True

    def evaluate_window(window, piece):
        score = 0
        opp_piece = PLAYER_PIECE
        if piece == PLAYER_PIECE:
            opp_piece = AI_PIECE

        if window.count(piece) == 5:
            score += 100
        elif window.count(piece) == 4 and window.count(EMPTY) == 1:
            score += 10
        elif window.count(piece) == 3 and window.count(EMPTY) == 2:
            score += 5

        if window.count(opp_piece) == 4 and window.count(EMPTY) == 1:
            score -= 80

        return score

    def score_position(board, piece):
        score = 0

        # Score center column
        center_array = [int(i) for i in list(board[:,COLUMN_COUNT//2])]
        center_count = center_array.count(piece)
        score += center_count * 6

        # Score Horizontal
        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(board[r,:])]
            for c in range(COLUMN_COUNT - 4):
                window = row_array[c:c+WINDOW_LENGTH]
                score += evaluate_window(window, piece)

        # Score Vertical
        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:,c])]
            for r in range(ROW_COUNT - 4):
                window = col_array[r:r+WINDOW_LENGTH]
                score += evaluate_window(window, piece)

        # Score Positive Slope Diagonal
        for r in range(ROW_COUNT - 4):
            for c in range(COLUMN_COUNT - 4):
                window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
                score += evaluate_window(window, piece)

        for r in range(ROW_COUNT - 4):
            for c in range(COLUMN_COUNT - 4):
                window = [board[r+4-i][c+i] for i in range(WINDOW_LENGTH)]
                score += evaluate_window(window, piece)
                
        return score

    def is_terminal_node(board):
        return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


    # Expectimax algorithm implementation
    def expectimax(board, depth, player):
        valid_locations = get_valid_locations(board)
        is_terminal = is_terminal_node(board)
        
        if depth == 0 or is_terminal:
            if is_terminal:
                if winning_move(board, AI_PIECE):
                    return (None, 100000000000000)
                elif winning_move(board, PLAYER_PIECE):
                    return (None, -10000000000000)
                else: # Game is over, no more valid moves
                    return (None, 0)
            else: # Depth is zero
                return (None, score_position(board, AI_PIECE))
        
        if player == AI_PIECE:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = get_next_open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, AI_PIECE)
                new_score = expectimax(b_copy, depth-1, PLAYER_PIECE)[1]
                if new_score > value:
                    value = new_score
                    column = col
            return column, value
        
        else: # Chance node
            value = 0
            column = random.choice(valid_locations)
            probability = 1 / len(valid_locations)
            for col in valid_locations:
                row = get_next_open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, PLAYER_PIECE)
                new_score = expectimax(b_copy, depth-1, AI_PIECE)[1]
                value += probability * new_score
            return column, value

        
    def get_valid_locations(board):
        valid_locations = []
        for col in range(COLUMN_COUNT):
            if is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations

    def pick_best_move(board, piece):
        valid_locations = get_valid_locations(board)
        best_score = -10000
        best_col = random.choice(get_valid_locations(board))
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, piece)
            score = score_position(temp_board, piece)
            if score > best_score:
                best_score = score
                best_col = col

        return best_col

    # Draw board function
    def draw_board(board):
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(screen, BLUE, (c*SQUARESIZE + 200, r*SQUARESIZE+SQUARESIZE + 80, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2 + 200), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2 + 80)), RADIUS)

        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                if board[r][c] == PLAYER_PIECE:
                    pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2 + 200), height-int(r*SQUARESIZE+SQUARESIZE/2 - 80 )), RADIUS)
                elif board[r][c] == AI_PIECE:
                    pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2 + 200), height-int(r*SQUARESIZE+SQUARESIZE/2 - 80)), RADIUS)    
        pygame.display.update()


    board = create_board()
    print_board(board)
    game_over = False

    pygame.init()

    SQUARESIZE = 75

    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT + 1) * SQUARESIZE

    size = (1000, 700)
    RADIUS = int(SQUARESIZE/2 - 5)

    screen = pygame.display.set_mode(size)

    # Board Surfaces
    background_surface = pygame.Surface((1000, 700))
    background_surface.fill('#101b27')

    # Block Surfaces
    block_surface = pygame.Surface((200, 700))
    block_surface.fill('#101b27')

    # Information Surfaces
    vs_surface = pygame.image.load('graphics/VS.png').convert_alpha()
    vs_rect = vs_surface.get_rect(center=(500, 25))
    pl_profile_surface = pygame.image.load('graphics/player_profile.png').convert_alpha()
    pl_profile_rect = pl_profile_surface.get_rect(center=(120, 45))
    pl_banner_surface = pygame.image.load('graphics/player_banner.png').convert_alpha()
    pl_banner_rect = pl_banner_surface.get_rect(center=(50, 28))
    pl_time_surface = pygame.image.load('graphics/player_time.png').convert_alpha()
    pl_time_rect = pl_time_surface.get_rect(center=(50, 55))
    ai_profile_surface = pygame.image.load('graphics/ai_profile.png').convert_alpha()
    ai_profile_rect = ai_profile_surface.get_rect(center=(880, 45))
    ai_banner_surface = pygame.image.load('graphics/ai_banner.png').convert_alpha()
    ai_banner_rect = ai_banner_surface.get_rect(center=(950, 28))
    ai_time_surface = pygame.image.load('graphics/ai_time.png').convert_alpha()
    ai_time_rect = ai_time_surface.get_rect(center=(950, 55))

    # Powerup Surfaces
    double_surface = pygame.image.load('graphics/double.png').convert_alpha()
    obstacle_surface = pygame.image.load('graphics/block.png').convert_alpha()
    gravity_surface = pygame.image.load('graphics/gravity.png').convert_alpha()

    # Powerup Objects
    start_btn1 = Powerup(50, 130, double_surface, 1)
    obstacle_btn1 = Powerup(50, 180, obstacle_surface, 1)
    gravity_btn1 = Powerup(47, 230, gravity_surface, 1)
    start_btn2 = Powerup(920, 130, double_surface, 1)
    obstacle_btn2 = Powerup(920, 180, obstacle_surface, 1)
    gravity_btn2 = Powerup(917, 230, gravity_surface, 1)

    screen.blit(background_surface, (0, 0))
    draw_board(board)
    screen.blit(vs_surface, vs_rect)
    screen.blit(pl_profile_surface, pl_profile_rect)
    screen.blit(pl_banner_surface, pl_banner_rect)
    screen.blit(pl_time_surface, pl_time_rect)
    screen.blit(ai_profile_surface, ai_profile_rect)
    screen.blit(ai_banner_surface, ai_banner_rect)
    screen.blit(ai_time_surface, ai_time_rect)
    start_btn1.draw(screen)
    obstacle_btn1.draw(screen)
    gravity_btn1.draw(screen)
    start_btn2.draw(screen)
    obstacle_btn2.draw(screen)
    gravity_btn2.draw(screen)

    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)

    turn = AI

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (200,80, 600, SQUARESIZE))
                posx = event.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2 + 80)), RADIUS)
                    screen.blit(block_surface, (0, 0))
                    screen.blit(block_surface, (800, 0))
                    start_btn1.draw(screen)
                    obstacle_btn1.draw(screen)
                    gravity_btn1.draw(screen)
                    start_btn2.draw(screen)
                    obstacle_btn2.draw(screen)
                    gravity_btn2.draw(screen)
                    screen.blit(pl_profile_surface, pl_profile_rect)
                    screen.blit(pl_banner_surface, pl_banner_rect)
                    screen.blit(pl_time_surface, pl_time_rect)
                    screen.blit(ai_profile_surface, ai_profile_rect)
                    screen.blit(ai_banner_surface, ai_banner_rect)
                    screen.blit(ai_time_surface, ai_time_rect)
                    
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (200,80, 600, SQUARESIZE))
                #print(event.pos)
                # Ask for Player 1 Input
                if turn == PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor((posx-200)/(SQUARESIZE)))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)

                        if winning_move(board, PLAYER_PIECE):
                            label = myfont.render("Player 1 Wins!", 1, RED)
                            #abel_rect = label.surface.get_rect(center=(500, 45))
                            screen.blit(label, (200,50))
                            game_over = True

                        turn += 1    
                        turn = turn % 2

                        print_board(board)
                        draw_board(board)

        # Ask for Player 2 Input
        if turn == AI and not game_over:
        
            col, expectimax_score = expectimax(board, 4, AI_PIECE)

            if is_valid_location(board, col):
                pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    label = myfont.render("AI Wins!", 1, YELLOW)
                    screen.blit(label, (350,50))
                    game_over = True
                
                print_board(board)
                draw_board(board)
                


                turn += 1    
                turn = turn % 2

        if game_over:
            pygame.time.wait(3000)

def main_menu():
    while True:
        SCREEN.blit(background_surface, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("Connect 5ive", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(500, 150))

        DESCRIPTION_TEXT = get_font(15).render("A game by: Simbulan & Mercado", True, "#3D7EBF")
        DESCRIPTION_RECT = DESCRIPTION_TEXT.get_rect(center=(500, 200))

        DATE_TEXT = get_font(12).render("May 2023 ©", True, "#3D7EBF")
        DATE_RECT = DATE_TEXT.get_rect(center=(500, 230))

        MULTIPLAYER_BUTTON = Button(image=pygame.image.load("assets/Rectangle.png"), pos=(270, 450), 
                            text_input="Multiplayer", font=get_font(30), base_color="Dark Green", hovering_color="White")
        VS_AI_BUTTON = Button(image=pygame.image.load("assets/Rectangle.png"), pos=(730, 450), 
                            text_input="VS AI", font=get_font(30), base_color="Dark Green", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit.png"), pos=(980, 680), 
                            text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(DESCRIPTION_TEXT, DESCRIPTION_RECT)
        SCREEN.blit(DATE_TEXT, DATE_RECT)

        for button in [MULTIPLAYER_BUTTON, VS_AI_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MULTIPLAYER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    multiplayer_window()
                if VS_AI_BUTTON.checkForInput(MENU_MOUSE_POS):
                    vs_ai()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()