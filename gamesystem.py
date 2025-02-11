import pygame, pathlib, pickle, sys, os, random, entities, gui

pygame.font.init()
bigfont = pygame.font.SysFont('Comic Sans MS', 72)
medfont = pygame.font.SysFont('Comic Sans MS', 40)
smallfont = pygame.font.SysFont('Comic Sans MS', 20)
clock = pygame.time.Clock()

#   Constants
SIZE = WIDTH, HEIGHT, = 1280, 720
ACCELERATION = 1
FRICTION = -0.12
GRAVITY = 0.5
FPS = 60

class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode(SIZE)
        self.player = entities.Player()
        self.ground = entities.Platform(WIDTH, 30, WIDTH / 2, HEIGHT - 15)
        self.sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.sprites.add(self.player)
        self.sprites.add(self.ground)
        self.platforms.add(self.ground)
        self.amount_of_enemies = 3
        self.playing = True
        self.all_gui = {
            'HP' : gui.HPBar(20, HEIGHT - 120),
            'Score' : gui.Score(WIDTH / 2, 80)
        }

    def choose_enemy(self, enemy_type = None):
        if enemy_type == None:
            roll = random.randint(1, 3)
            if roll == 1:
                return entities.FlyingDemon(random.randint(WIDTH + 80, WIDTH + 800), random.randint(80, HEIGHT - 80))
            if roll > 1:
                return entities.WalkingDemon(random.randint(WIDTH + 80, WIDTH + 800), random.randint(80, HEIGHT - 80))
        else:
            if enemy_type == 1:
                return entities.WalkingDemon(1, 1)
            if enemy_type == 2:
                return entities.FlyingDemon(1, 1)

    def pack(self):
        self.screen = None
        for bullet in self.bullets:
            bullet.kill()
        sprite_list = []
        platform_list = []
        enemy_list = []
        self.player = self.player.pack()
        self.ground = self.ground.pack()
        sprite_list.append(self.player)
        sprite_list.append(self.ground)
        count = 0
        for platform in self.platforms:
            if count > 0:
                info = platform.pack()
                platform_list.append(info)
                sprite_list.append(info)
            count += 1
        for enemy in self.enemies:
            info = enemy.pack()
            enemy_list.append(info)
            sprite_list.append(info)
        self.sprites, self.platforms, self.enemies, self.bullets = sprite_list, platform_list, enemy_list, []
        self.all_gui = {}

    def unpack(self):
        self.screen = pygame.display.set_mode(SIZE)
        sprite_group = pygame.sprite.Group()
        platform_group = pygame.sprite.Group()
        enemy_group = pygame.sprite.Group()
        player = entities.Player()
        ground = entities.Platform(1, 1, 1, 1)
        player.unpack(self.player)
        ground.unpack(self.ground)
        self.player = player
        self.ground = ground
        sprite_group.add(self.player)
        sprite_group.add(self.ground)
        platform_group.add(self.ground)
        for info in self.platforms:
            platform = entities.Platform(1, 1, 1, 1)
            platform.unpack(info)
            platform_group.add(platform)
            sprite_group.add(platform)
        for info in self.enemies:
            enemy = self.choose_enemy(enemy_type = info[0])
            enemy.unpack(info)
            enemy_group.add(enemy)
            sprite_group.add(enemy)
        self.sprites, self.platforms, self.enemies, self.bullets = sprite_group, platform_group, enemy_group, pygame.sprite.Group()
        self.all_gui = {
            'HP' : gui.HPBar(20, HEIGHT - 120),
            'Score' : gui.Score(WIDTH / 2, 80)
        }

    def scroll(self):
        self.player.pos.x += -abs(self.player.velocity.x)
        for enemy in self.enemies:
            enemy.pos.x += -abs(self.player.velocity.x)
            if enemy.rect.right <= 0:
                enemy.kill()
        for platform in self.platforms:
            platform.rect.x += -abs(self.player.velocity.x)
            if platform.rect.right <= 0:
                platform.kill()
        for bullet in self.bullets:
            bullet.pos.x += -abs(self.player.velocity.x)
        self.player.acceleration.x = -1
        self.player.rect.right = WIDTH * 0.66 - 1
        self.ground.rect.x = 0

    def create_platform(self):
        width = random.randint(200, 400)
        collides = True
        while collides:
            platform = entities.Platform(width, 30, random.randint(WIDTH, WIDTH + 200), random.randint(80, HEIGHT - 80))
            platform.rect.center = (random.randrange(round(WIDTH + width / 2), WIDTH + 201), random.randrange(80, HEIGHT - 80))
            collides = platform.check(self.platforms)
        self.platforms.add(platform)
        self.sprites.add(platform)
        return platform

    def initialise_platforms(self):
        for x in range(random.randint(4, 5)):
            collides = True
            while collides:
                width = random.randint(200, 400)
                platform = entities.Platform(width, 30, random.randint(0, round(WIDTH - width / 2)), random.randint(80, HEIGHT - 80))
                collides = platform.check(self.platforms)
            self.platforms.add(platform)
            self.sprites.add(platform)

    def generate_platforms(self):
        while len(self.platforms) < 6:
            self.create_platform()

    def create_enemy(self):
        collides = True
        while collides:
            enemy = self.choose_enemy()
            collides = enemy.check(self.enemies)
        self.enemies.add(enemy)
        self.sprites.add(enemy)
        return enemy

    def initialise_enemies(self):
        for x in range(random.randint(1, 2)):
            collides = True
            while collides:
                enemy = entities.WalkingDemon(random.randint(round(WIDTH / 3), WIDTH), random.randint(80, HEIGHT - 80))
                collides = enemy.check(self.enemies)
            self.enemies.add(enemy)
            self.sprites.add(enemy)
        
    def generate_enemies(self):
        while len(self.enemies) < self.amount_of_enemies:
            self.create_enemy()
    
    def game_over(self):
        for entity in self.sprites:
            entity.kill()

        self.screen.fill((0,0,0))
        bigtext = bigfont.render("GAME OVER", False, (255, 50, 0))
        bigtext_rect = bigtext.get_rect(center = (WIDTH / 2, HEIGHT / 2 - 50))
        smalltext = smallfont.render("Press anything to exit.", False, (255, 50, 0))
        smalltext_rect = smalltext.get_rect(center = (WIDTH / 2, HEIGHT / 2 + 50))
        self.screen.blit(bigtext, bigtext_rect)
        self.screen.blit(smalltext, smalltext_rect)

        self.playing = False

    def update(self):
        if self.playing:
            self.player.move()
            self.player.update(self.platforms, self.enemies, self.bullets, self.sprites)
            self.generate_platforms()
            self.generate_enemies()
            if self.player.rect.right >= WIDTH * 0.66:
                self.scroll()
            for enemy in self.enemies:
                print(enemy)
                print(enemy.pos)
                print(enemy.direction)
                print(enemy.velocity)
                print(enemy.acceleration)
                enemy.move(self.player)
                enemy.update(self.platforms, self.player)
            for bullet in self.bullets:
                bullet.move()
                bullet.update(self.enemies)
            
            #   Drawing
            self.screen.fill((0, 0, 0))
            for entity in self.sprites:
                self.screen.blit(entity.surface, entity.rect)
            for enemy in self.enemies:
                enemy.display_health(self.screen)

            #   Drawing GUI
            self.all_gui['HP'].display(self.screen, self.player.max_hp, self.player.current_hp)
            self.all_gui['Score'].display(self.screen, self.player.score)

        #   Check for game over
        if self.player.current_hp <= 0:
            self.player.current_hp = 0
            self.game_over()

        pygame.display.update()
        clock.tick(FPS)

class Menu():
    def __init__(self):
        self.screen = pygame.display.set_mode(SIZE)
        self.title = pygame.image.load('logos/title.png')
        self.current_menu = 0
        self.menu_pointer = 0
        self.main_buttons = [
            gui.Button(self.screen, WIDTH / 2, 240, "Start Game", highlighted = True),
            gui.Button(self.screen, WIDTH / 2, 320, "Load Game"),
            gui.Button(self.screen, WIDTH / 2, 400, "Settings"),
            gui.Button(self.screen, WIDTH / 2, 480, "Leader Boards"),
            gui.Button(self.screen, WIDTH / 2, 560, "Quit Game")
        ]
        self.pause_buttons = [
            gui.Button(self.screen, WIDTH / 2, 240, "Resume Game", highlighted = True),
            gui.Button(self.screen, WIDTH / 2, 320, "Load Game"),
            gui.Button(self.screen, WIDTH / 2, 400, "Save Game"),
            gui.Button(self.screen, WIDTH / 2, 480, "Settings"),
            gui.Button(self.screen, WIDTH / 2, 560, "Exit Game")
        ]

    def _start(self):
        return 0

    def _resume(self):
        return 1

    def _load(self):
        if pathlib.Path("save.pickle").is_file():
            return 2
        else:
            gui.alert("There is no save file to load.")

    def _save(self):
        if pathlib.Path("save.pickle").is_file():
            if gui.confirm("Overwrite Save", "Are you sure you want to overwrite the current save?"):
                return 3
        else:
            return 3

    def _settings(self):
        pass

    def _leaderboard(self):
        pass

    def _quit_game(self):
        if gui.confirm("Quit Game", "Are you sure you want to quit?"):
            pygame.quit()
            sys.exit()
    
    def _exit_game(self):
        if gui.confirm("Exit Game", "Are you sure you want to exit? All unsaved progress will be lost"):
            return 4
    
    def _main(self):
        self.screen.blit(self.title, self.title.get_rect(center = (WIDTH / 2, 120)))
        for button in self.main_buttons:
            button.draw()

    def _pause(self):
        self.screen.blit(self.title, self.title.get_rect(center = (WIDTH / 2, 120)))
        for button in self.pause_buttons:
            button.draw()

    def up(self):
        if self.current_menu == 0:
            buttons = self.main_buttons
        if self.current_menu == 1:
            buttons = self.pause_buttons
        if self.menu_pointer > 0:
            buttons[self.menu_pointer].highlighted = False
            self.menu_pointer -= 1
            buttons[self.menu_pointer].highlighted = True

    def down(self):
        if self.current_menu == 0:
            buttons = self.main_buttons
        if self.current_menu == 1:
            buttons = self.pause_buttons
        if self.menu_pointer < len(buttons) - 1:
            buttons[self.menu_pointer].highlighted = False
            self.menu_pointer += 1
            buttons[self.menu_pointer].highlighted = True

    def press(self):
        if self.current_menu == 0:
            if self.menu_pointer == 0:
                return self._start()
            if self.menu_pointer == 1:
                return self._load()
            if self.menu_pointer == 2:
                self._settings()
            if self.menu_pointer == 3:
                self._leaderboard()
            if self.menu_pointer == 4:
                self._quit_game()
        if self.current_menu == 1:
            if self.menu_pointer == 0:
                return self._resume()
            if self.menu_pointer == 1:
                return self._load()
            if self.menu_pointer == 2:
                return self._save()
            if self.menu_pointer == 3:
                self._settings()
            if self.menu_pointer == 4:
                return self._exit_game()

    def update(self):
        self.screen.fill((0, 0, 0))
        if self.current_menu == 0:
            self._main()
        if self.current_menu == 1:
            self._pause()
        pygame.display.update()
        clock.tick(FPS)