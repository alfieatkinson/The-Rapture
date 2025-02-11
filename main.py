import pygame, asyncio, pickle, sys, os, gamesystem, entities, gui

#   Initialisation
pygame.init()
pygame.display.set_caption("The Rapture")
game = gamesystem.Game()
menu = gamesystem.Menu()

#   Save and Load
def save():
    game.pack()
    file = open("save.pickle", "wb")
    pickle.dump(game, file)
    file.close()

def load():
    global game
    file = open("save.pickle", "rb")
    game = pickle.load(file)
    file.close()
    game.unpack()

#   Game functions
def initialise_game():
    game.__init__()
    game.initialise_platforms()
    game.initialise_enemies()

def game_loop():
    in_game = True
    while in_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game.playing:
                    menu.current_menu = 0
                    in_game = False
                if not game.player.shooting:
                    game.player.shoot()
            if event.type == pygame.MOUSEBUTTONUP:
                if game.player.shooting:
                    game.player.stop_shoot()
            if event.type == pygame.KEYDOWN:
                if not game.playing:
                    menu.current_menu = 0
                    in_game = False
                if event.key == pygame.K_SPACE:
                    game.player.jump()
                if event.key == pygame.K_ESCAPE:
                    menu.current_menu = 1
                    in_game = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    game.player.stop_jump()
        game.update()
        
def menu_loop():
    in_menu = True
    menu.menu_pointer = 0
    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu.up()
                if event.key == pygame.K_DOWN:
                    menu.down()
                if event.key == pygame.K_RETURN:
                    value = menu.press()
                    if value == 0:  #    Start Game
                        initialise_game()
                        in_menu = False
                        menu.menu_pointer = 0
                    if value == 1:  #   Resume Game
                        in_menu = False
                        menu.menu_pointer = 0
                    if value == 2:  #   Load Game
                        load()
                        in_menu = False
                        menu.menu_pointer = 0
                    if value == 3:  #   Save Game
                        save()
                        menu.menu_pointer = 0
                        menu.current_menu = 0
                    if value == 4:  #   Exit Game
                        menu.menu_pointer = 0
                        menu.current_menu = 0
        menu.update()
    
async def main():
    run = True
    while run:
        if not game.playing:
            menu_loop()
        else:
            game_loop()
        await asyncio.sleep(0)

if __name__ == '__main__':
    asyncio.run(main())
