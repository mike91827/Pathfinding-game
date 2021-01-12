import pygame


# this function displays the instructions when the user first runs the program.

def instructions():
    pygame.init()
    white = (255, 255, 255)
    black = (0, 0, 0)


    display_surface = pygame.display.set_mode((400, 400))

    # set the pygame window name
    pygame.display.set_caption("Instructions")

    # create a font object.
    # 1st parameter is the font file
    # which is present in pygame.
    # 2nd parameter is size of the font
    font = pygame.font.Font('freesansbold.ttf', 16)

    #all the instructions

    inst = font.render("Instructions: Go Through All Three Yellow Walls while avoiding the enemies to win the game",
                       True, black, white)
    character = font.render("Orange - Controlling Player. Control with arrow keys", True, black, white)
    walls = font.render("Black - Walls. No one can move through them", True, black, white)
    enemies = font.render("Blue - Enemies. If they reach you (orange) you lose", True, black, white)
    objectives = font.render("Yellow- Go through all 3 objectives to win. Once gone through, turns into a black tile",
                             True, black, white)
    portal = font.render("Purple- When stepped on, transport to a random empty tile, turns to black after use", True,
                         black, white)
    loading = font.render(
        "You may have to wait for the program to load. Once you see 3 blue tiles appear then you can start.", True,
        black, white)
    stuck = font.render(
        "If you ever reach a state where the enemy cannot reach you and you have not collected all yellow tiles, you lose",
        True, black, white)
    text = font.render("Play", True, black, white)

    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()
    textRect2 = text.get_rect()
    textRect3 = text.get_rect()
    textRect4 = text.get_rect()
    textRect5 = text.get_rect()
    textRect6 = text.get_rect()
    textRect7 = text.get_rect()
    textRect8 = text.get_rect()

    # set the center of the rectangular object.

    textRect.center = (50, 25)
    textRect2.center = (50, 100)
    textRect3.center = (50, 120)
    textRect4.center = (50, 140)
    textRect5.center = (50, 160)
    textRect6.center = (50, 180)
    textRect7.center = (50, 250)
    textRect8.center = (50, 270)

    res = (900, 720)
    screen = pygame.display.set_mode(res)




    # light shade of the button when you hover over it
    color_light = (170, 170, 170)

    # dark shade of the button when you do not hover over it
    color_dark = (100, 100, 100)


    # infinite loop
    while True:

        # completely fill the surface object
        # with white color
        display_surface.fill(white)

        # copying the text surface object
        # to the display surface object
        # at the center coordinate.
        display_surface.blit(inst, textRect)
        display_surface.blit(character, textRect2)
        display_surface.blit(walls, textRect3)
        display_surface.blit(enemies, textRect4)
        display_surface.blit(objectives, textRect5)
        display_surface.blit(portal, textRect6)
        display_surface.blit(loading, textRect7)
        display_surface.blit(stuck, textRect8)

        # iterate over the list of Event objects
        for event in pygame.event.get():

            # if event object type is QUIT
            # then quitting the pygame
            # and program both.
            if event.type == pygame.QUIT:
                # deactivates the pygame library
                pygame.quit()

                # quit the program.
                quit()

            mouse = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:

                # if the mouse is clicked on the
                # button the game starts
                if 250 <= mouse[0] <= 250 + 140 and 360 <= mouse[1] <= 360 + 40:
                    __import__("backtrackingalgo")

            # if mouse is hovered on a button it
            # changes to lighter shade
            if 250 <= mouse[0] <= 250 + 140 and 360 <= mouse[1] <= 360 + 40:
                pygame.draw.rect(screen, color_light, [250, 360, 140, 40])
                screen.blit(text, (300, 365))

            else:
                # displays the button normally
                pygame.draw.rect(screen, color_dark, [250, 360, 140, 40])
                screen.blit(text, (300, 365))

            pygame.display.update()


if __name__ == '__main__':
    instructions()

