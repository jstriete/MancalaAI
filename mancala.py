import pygame
import random

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

    if event.type == pygame.MOUSEBUTTONDOWN and mouse_active and won == False:
        pos = pygame.mouse.get_pos()
        if ai_player == True and turn == False:
            pos = (0,0)
        mouse_active = False
        for i in range(14):
            if(space_locs[i].collidepoint(pos)):
                if space_marbles[i] != 0 and i < scoreSpace and i > scoreSpace - 7:
                    extra_turn = False
                    marbles = space_marbles[i]
                    space_marbles[i] = 0
                    for j in range(marbles):
                        if((i + j + 1) % 14 != scoreSpace + 7):
                            space_marbles[(i + j + 1) % 14] += 1
                            if(j == marbles - 1 and (i+j+1) % 14 < scoreSpace and (i+j+1) % 14 > scoreSpace - 7 and space_marbles[(i + j + 1) % 14] == 1 and space_marbles[12 - ((i + j + 1) % 14)] != 0):
                                space_marbles[scoreSpace] += space_marbles[12 - ((i + j + 1) % 14)] + 1
                                space_marbles[12 - ((i + j + 1) % 14)] = 0
                                space_marbles[(i + j + 1) % 14] = 0
                        else:
                            space_marbles[(i + j + 2) % 14] += 1
                    if (i + j + 1) % 14 == scoreSpace:
                        turn = turn
                        extra_turn = True
                    elif (i + j + 1) % 14 != scoreSpace:
                        turn = not turn
                    mouse_active = True
                    break
                else:
                    mouse_active = True
                    break
    if space_marbles[0] == 0 and space_marbles[1] == 0 and space_marbles[2] == 0 and space_marbles[3] == 0 and space_marbles[4] == 0 and space_marbles[5] == 0 and won == False:
        space_marbles[13] += space_marbles[7] + space_marbles[8] + space_marbles[9] + space_marbles[10] + space_marbles[11] + space_marbles[12]
        for i in range(7, 13):
            space_marbles[i] = 0
        won = True
    elif space_marbles[7] == 0 and space_marbles[8] == 0 and space_marbles[9] == 0 and space_marbles[10] == 0 and space_marbles[11] == 0 and space_marbles[12] == 0 and won == False:
        space_marbles[6] += space_marbles[0] + space_marbles[1] + space_marbles[2] + space_marbles[3] + space_marbles[4] + space_marbles[5]
        for i in range(0, 6):
            space_marbles[i] = 0
        won = True
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
