import pygame
#Start PyGame
pygame.init()
#Create a window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#Display the window name
pygame.display.set_caption("PyGame Test")

#Create a player rectangle
player = pygame.Rect((300,250,50,50))

#Create a clock to control the frame rate
clock = pygame.time.Clock()

#speed variable for the player movement
speed = 5

#Detects if running
run = True

#Game loop
while run:
    #Set the frame rate to 60 frames per second
    clock.tick(60)

    #Check for events
    for event in pygame.event.get():
        #Check if the user wants to quit
        if event.type == pygame.QUIT:
            run = False
            
    #Get the keys being pressed
    key = pygame.key.get_pressed()
    #Get the movement of the player/rectangle
    if key[pygame.K_a]:
        player.x -= speed
    if key[pygame.K_d]:
        player.x += speed
    if key[pygame.K_w]:
        player.y -= speed
    if key[pygame.K_s]:
        player.y += speed

    #Fill the screen with black
    screen.fill((0,0,0))
    
    #Screen Name, Color, and Player Variable
    pygame.draw.rect(screen, (255,0,0), player)

    #Update the display
    pygame.display.update()
#Quit PyGame
pygame.quit()