import pygame
import random
import copy

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1024, 768))
pygame.display.set_caption('Mancala')
clock = pygame.time.Clock()
running = True
turn = True
won = False
mouse_active = True
extra_turn = False
ai_player = False
decided = False
scoreSpace = 6

font = pygame.font.Font('freesansbold.ttf', 32)

length = 75
board_pos = pygame.Vector2(screen.get_width() / 2 - length, screen.get_height() / 2 - 3 * length)

space_marbles = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
space_locs = []
temp_locs = []

for i in range(6):
    space_locs.append(pygame.Rect(board_pos.x, board_pos.y + length * i, length, length))
    temp_locs.append(pygame.Rect(board_pos.x + length, board_pos.y + length * 5 - length * i, length, length))
space_locs.append(pygame.Rect(0,0,0,0))
space_locs.extend(temp_locs)
space_locs.append(pygame.Rect(0,0,0,0))

def drawSquare(xoffset, yoffset, xmult, ymult):
    pygame.draw.line(screen, "black", (board_pos.x + xoffset, board_pos.y + yoffset), 
                     (board_pos.x + xoffset, board_pos.y + ymult * length + yoffset), 2)
    pygame.draw.line(screen, "black", (board_pos.x + xoffset, board_pos.y + yoffset), 
                     (board_pos.x + xmult * length + xoffset, board_pos.y + yoffset), 2)
    pygame.draw.line(screen, "black", (board_pos.x + xmult * length + xoffset, board_pos.y + yoffset), 
                     (board_pos.x + xmult * length + xoffset, board_pos.y + ymult * length + yoffset), 2)
    pygame.draw.line(screen, "black", (board_pos.x + xoffset, board_pos.y + + ymult * length + yoffset), 
                     (board_pos.x + xmult * length + xoffset, board_pos.y + ymult * length + yoffset), 2)
    
def drawText(xoffset, yoffset, text):
    text = font.render(text, True, (0,0,0), (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (board_pos.x + .5 * length + xoffset, board_pos.y + .5 * length + yoffset)
    screen.blit(text, textRect)

def moveMarbles(moved_marbles, i):
    global extra_turn
    global turn
    global mouse_active
    global marbles
    
    if moved_marbles[i] != 0 and i < scoreSpace and i > scoreSpace - 7:
        extra_turn = False
        marbles = moved_marbles[i]
        moved_marbles[i] = 0
        for j in range(marbles):
            if (turn):
                if ((i + j + 1) % 14 != scoreSpace + 7):
                    moved_marbles[(i + j + 1) % 14] += 1
                    if (j == marbles - 1 and (i+j+1) % 14 < scoreSpace and (1+j+1) % scoreSpace - 7 and space_marbles[(1+i+j) % 14] == 1 and space_marbles[12 - ((i+j+1) % 14)] != 0):
                        moved_marbles[scoreSpace] += moved_marbles[12 - ((i + j + 1) % 14)] + 1
                        moved_marbles[12 - ((i + j + 1) % 14)] = 0
                        moved_marbles[(i + j + 1) % 14] = 0
                else:
                    moved_marbles[(i + j + 2) % 14] += 1
            else:
                if ((i + j + 1) % 14 != scoreSpace - 7):
                    moved_marbles[(i + j + 1) % 14] += 1
                    if (j == marbles - 1 and (i+j+1) % 14 < scoreSpace and (1+j+1) % scoreSpace - 7 and space_marbles[(1+i+j) % 14] == 1 and space_marbles[12 - ((i+j+1) % 14)] != 0):
                        moved_marbles[scoreSpace] += moved_marbles[12 - ((i + j + 1) % 14)] + 1
                        moved_marbles[12 - ((i + j + 1) % 14)] = 0
                        moved_marbles[(i + j + 1) % 14] = 0
                else:
                    moved_marbles[(i + j + 2) % 14] += 1
        if (i + j + 1) % 14 == scoreSpace:
            turn = turn
            extra_turn = True
        elif (i + j + 1) % 14 != scoreSpace:
            turn = not turn
        mouse_active = True
    else:
        mouse_active = True
    return moved_marbles

def testWinCondition(moved_marbles):
    isWon = False
    global won
        
    if sum(moved_marbles[0:6]) == 0 and won == False:
        moved_marbles[13] += sum(moved_marbles[7:13])
        for i in range(7, 13):
            moved_marbles[i] = 0
        isWon = True
    elif sum(moved_marbles[7:13]) == 0 and won == False:
        moved_marbles[6] += sum(moved_marbles[0:6])
        for i in range(0, 6):
            moved_marbles[i] = 0
        isWon = True
    
    return isWon
        
# def miniMax(depth, marble_list, whoseTurn, moveMade):
#     global extra_turn
    
#     if (depth <= 0 or testWinCondition(marble_list)):
#         return [marble_list[13] - marble_list[6], moveMade]

#     if (whoseTurn):
#         best = [-10000, -1]
#         for i in range(7, 13):
#             if (marble_list[i] != 0):
#                 temp_list = copy.deepcopy(marble_list)
#                 temp_list = moveMarbles(temp_list, i)
                
#                 if extra_turn:
#                     points = miniMax(depth, temp_list, True, i)[0]
#                 else:
#                     points = miniMax(depth - 1, temp_list, False, i)[0]
                
#                 if (points > best[0]):
#                     best = [points, i]
    
#     if not whoseTurn:
#         best = [-10000, -1]
#         for i in range(1, 6):
#             if (marble_list[i] != 0):
#                 temp_list = copy.deepcopy(marble_list)
#                 temp_list = moveMarbles(temp_list, i)
                
#                 if extra_turn:
#                     points = miniMax(depth, temp_list, False, i)[0]
#                 else:
#                     points = miniMax(depth - 1, temp_list, True, i)[0]
                
#                 if (points < best[0]):
#                     best = [points, i]
#     print(best)
#     return best

def validMoves(board):
    valid_moves = []
    for i in range(13):
        if board[i] != 0:
            valid_moves.append(i)
    return valid_moves          

def miniMax(depth, board, maximizing_player):
    if depth == 0 or testWinCondition(board):
        return board[13] - board[6], None

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None

        for move in validMoves(board):
            temp_board = copy.deepcopy(board)
            new_board = moveMarbles(temp_board, move)
            eval = miniMax(depth - 1, new_board, False)[0]

            if eval > max_eval:
                max_eval = eval
                best_move = move

        return max_eval, best_move

    else:
        min_eval = float('inf')
        best_move = None

        for move in validMoves(board):
            temp_board = copy.deepcopy(board)
            new_board = moveMarbles(temp_board, move)
            eval = miniMax(depth - 1, new_board, True)[0]

            if eval < min_eval:
                min_eval = eval
                best_move = move

        return min_eval, best_move

# Example usage:
initial_board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
result = miniMax(3, initial_board, True)
print("Best move:", result[1])  
        
        
while running:
    while(not decided):
        screen.fill("white")
        drawText(0, -150, "Welcome to Mancala!")
        drawText(0, -50, "Would you like to play against a friend or the computer?")
        drawText(0, 50, "Press 1 for a friend")
        drawText(0, 150, "Press 2 for the computer")
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                decided = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    decided = True
                if event.key == pygame.K_2:
                    decided = True
                    ai_player = True
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # RENDER YOUR GAME HERE
    font = pygame.font.Font('freesansbold.ttf', 50)
    for i in range(6):
        drawSquare(0, 0 + length * i, 1, 1)
        drawSquare(length, 0 + length * i, 1, 1)
        drawText(0, 0 + length * i, str(space_marbles[i]))
        drawText(length, length * 5 - length * i, str(space_marbles[i+7]))
    drawSquare(0, -(length + .25 * length), 2, 1.25)
    drawSquare(0, 6 * length, 2, 1.25)

    font = pygame.font.Font('freesansbold.ttf', 64)

    drawText(.5 * length, -(length), str(space_marbles[13]))
    drawText(.5 * length, 6 * length + .25 * length, str(space_marbles[6]))

    if turn:
        scoreSpace = 6
    else:
        scoreSpace = 13

    font = pygame.font.Font('freesansbold.ttf', 50)

    if(not won):
        drawText(-250, 0, "Player " + str(scoreSpace % 2 + 1) + "'s turn")
        if extra_turn:
            drawText(-250, 100, "Extra Turn!")

    if ai_player == True and turn == False:
        mouse_active = False
        newBest = miniMax(1, space_marbles, True)
        print(newBest[1])
        space_marbles = moveMarbles(space_marbles, newBest[1])
        if (not extra_turn):
            turn = True
            mouse_active = True

    if event.type == pygame.MOUSEBUTTONDOWN and mouse_active and won == False:
        pos = pygame.mouse.get_pos()
        mouse_active = False
        for i in range(14):
            if(space_locs[i].collidepoint(pos)):
                space_marbles = moveMarbles(space_marbles, i)
    won = testWinCondition(space_marbles)
    if won:
        if space_marbles[6] > space_marbles[13]:
            drawText(-250, 0, "Player 1 wins!")
        elif space_marbles[6] < space_marbles[13]:
            drawText(-250, 0, "Player 2 wins!")
        else:
            drawText(-250, 0, "Tie!")
        mouse_active = False
    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()