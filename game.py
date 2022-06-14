import pygame
import time
import random
import os
from snake import *

#Instruction
text = "QUICK INSTRUCTION: "\
    "\nPress any arrow key to start the game. Direct the"\
        "\nsnake to eat fruit and don't let it touch the wall."

# Window size
wid = 300
hei = 460

# Create some colors for the GUI
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
dk_blue = pygame.Color(33, 38, 112)

#read and retrieve best score
f = open("hscore.txt", "r")
bscore = int(f.read())
f.close()

#quick instruction
print(' ')
print(text)
print(' ')
print('Select dificulty: \nE for easy, N for normal, H for hard')
a = str(input())
if a=='e' or a=='n' or a=='h':
    if a == 'e': spd = 10
    if a == 'n': spd = 20
    if a == 'h': spd = 30
else: 
    print('you have press the wrong key ('+a+')')
    os.system('pause')

# Run lib pygame and create setting for game window
pygame.init()
pygame.display.set_caption('Snakes Game')
window = pygame.display.set_mode((wid, hei))
fps = pygame.time.Clock() # For changing fps ingame (in this case: fps = snake speed)

# fruit random position within the game window
fruit_pos = [random.randrange(2,((wid//10)-1))*10, random.randrange(4,((hei//10)-1))*10]
fruit_appear = True # variable for checking if the fruit is on the window or not

# begining score
score = 0

#create snake
def draw_snake():
    for i in snbody:
        pygame.draw.rect(window, green, pygame.Rect(i[0], i[1], 10, 10))

#create fruit
def draw_fruit():
    pygame.draw.rect(window, red, pygame.Rect(fruit_pos[0], fruit_pos[1], 10, 10))

def draw_wall():
    for bl1 in range (0,hei-10):
        pygame.draw.rect(window, dk_blue, pygame.Rect(0, bl1, 10, 10))
        pygame.draw.rect(window, dk_blue, pygame.Rect(wid-10, bl1, 10, 10))
    for bl2 in range (0,wid-10):
        pygame.draw.rect(window, dk_blue, pygame.Rect(bl2, hei-10, 10, 10))
        pygame.draw.rect(window, dk_blue, pygame.Rect(bl2, 0, 30, 30))

# function that display the score
def show_score(choice, color, font, size):

	# creating font for the score text
	sfont = pygame.font.SysFont(font, size)

	# create the place for the text to display (surface + rectangular)
	splace = sfont.render(' Score: '+str(score)+'          Best score: '+str(bscore), True, color) #surface
	score_rect = splace.get_rect() # rect

	# displaying text
	window.blit(splace, score_rect)

# game over function
def game_over():
   
    # creating font object gofont
    gofont = pygame.font.SysFont('times new roman', 35)
     
    # create the place for the text to display (surface + rectangular)
    goplace = gofont.render('Your Score is : ' + str(score), True, red)
    gorect = goplace.get_rect()
    gorect.midtop = (wid/2, hei/3) # setting position of the text
    
    # blit will draw the text on screen
    window.blit(goplace, gorect)
    pygame.display.flip()

    #If > best score then replace the best score
    if score>bscore:
        f2 = open("hscore.txt", "w")
        f2.write(str(score))
        f2.close()

    # after 3 seconds quit the program
    time.sleep(3)
    pygame.quit()
    os.system('pause')

def start():# Main Function
    while True:
        
        global dir, dir_change, score
        global fruit_appear, fruit_pos

        # assign key binding
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    dir_change = 'UP'
                if event.key == pygame.K_DOWN:
                    dir_change = 'DOWN'
                if event.key == pygame.K_LEFT:
                    dir_change = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    dir_change = 'RIGHT'

        """
        Sometimes players press oposite direction of the snake currently,
        so we don't want the snake to go opositely
        """
        if dir_change == 'UP' and dir != 'DOWN': dir = 'UP'
        if dir_change == 'DOWN' and dir != 'UP': dir = 'DOWN'
        if dir_change == 'LEFT' and dir != 'RIGHT': dir = 'LEFT'
        if dir_change == 'RIGHT' and dir != 'LEFT': dir = 'RIGHT'

        # Moving the snake with the dir
        if dir == 'UP': snpos[1] -= 10
        if dir == 'DOWN': snpos[1] += 10
        if dir == 'LEFT': snpos[0] -= 10
        if dir == 'RIGHT': snpos[0] += 10

        """
        aglorithm of growing snake when it eats the fruit
        """
        snbody.insert(0, list(snpos))
        if snpos[0] == fruit_pos[0] and snpos[1] == fruit_pos[1]:
            score += 10
            fruit_appear = False
        else:
            snbody.pop()
            
        if not fruit_appear:
            fruit_pos = [random.randrange(2,((wid//10)-1))*10, random.randrange(4,((hei//10)-1))*10]
            
        fruit_appear = True #change to true afterward if not then the fruit will be continously randomly
        
        #further design the game window and draw snake & fruit
        window.fill(black)
        draw_snake();draw_fruit();draw_wall()
        
        """
        game over when snake touch wall or touch itself
        """
        # touch wall
        if snpos[0] < 10 or snpos[0] > wid-20: game_over()
        if snpos[1] < 30 or snpos[1] > hei-20: game_over()
        
        # touch itself
        if dir=='UP' or dir=='RIGHT' or dir=='DOWN' or dir=='LEFT':
            for x in snbody[1:]:
                if snpos[0] == x[0] and snpos[1] == x[1]: game_over()

        # display score
        show_score(1, white, 'times new roman', 20)

        # Refresh game screen
        pygame.display.update()

        # set the fps (snake speed in this case)
        fps.tick(spd)

if __name__ == '__main__': 
    start()
