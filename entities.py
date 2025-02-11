import pygame, random, gamesystem

vector = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = self.width, self.height = 40, 40
        self.color = (128, 255, 40)
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)
        self.rect = self.surface.get_rect()
        self.pos = vector((20, gamesystem.HEIGHT - 30))
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)
        self.grounded = False
        self.jumping = True
        self.shooting = False

        self.max_hp = 100
        self.current_hp = self.max_hp
        self.firing_time = 20
        self.time_since_fired = 0
        self.damage = 6
        self.score = 0

    def pack(self):
        self.surface = None
        self.rect = None
        self.pos = (self.pos.x, self.pos.y)
        self.velocity = (self.velocity.x, self.velocity.y)
        self.acceleration = (self.acceleration.x, self.acceleration.y)

        info = [
            self.size,
            self.color,
            self.surface,
            self.rect,
            self.pos,
            self.velocity,
            self.acceleration,
            self.grounded,
            self.jumping,
            self.shooting,
            self.max_hp,
            self.current_hp,
            self.firing_time,
            self.time_since_fired,
            self.damage,
            self.score
        ]
        return info

    def unpack(self, info):
        self.size = self.width, self.height = info[0]
        self.color = info[1]
        self.surface = info[2]
        self.rect = info[3]
        self.pos = info[4]
        self.velocity = info[5]
        self.acceleration = info[6]
        self.grounded = info[7]
        self.jumping = info[8]
        self.shooting = info[9]
        self.max_hp = info[10]
        self.current_hp = info[11]
        self.firing_time = info[12]
        self.time_since_fired = info[13]
        self.damage = info[14]
        self.score = info[15]

        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)
        self.rect = self.surface.get_rect()
        self.pos = vector(self.pos)
        self.velocity = vector(self.velocity)
        self.acceleration = vector(self.acceleration)

    def move(self):
        self.acceleration = vector(0, gamesystem.GRAVITY)
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[ord('a')]:
            self.acceleration.x = -gamesystem.ACCELERATION
        if pressed_keys[ord('d')]:
            self.acceleration.x = gamesystem.ACCELERATION
        
        self.acceleration.x += self.velocity.x * gamesystem.FRICTION
        self.velocity += self.acceleration
        self.pos += self.velocity + 0.5 * self.acceleration

        if self.pos.x + self.width / 2 > gamesystem.WIDTH:
            self.pos.x = gamesystem.WIDTH - self.width / 2
        if self.pos.x - self.width / 2 < 0:
            self.pos.x = 0 + self.width / 2
        
        self.rect.midbottom = self.pos

    def create_bullet(self, bullets, sprites):
        bullet = Bullet(self.pos, self.damage)
        bullets.add(bullet)
        sprites.add(bullet)

    def update(self, platforms, enemies, bullets, sprites):
        if self.rect.top > gamesystem.HEIGHT:
            self.pos.y = gamesystem.HEIGHT - 100
        collisions_with_platforms = pygame.sprite.spritecollide(self, platforms, False)
        if self.velocity.y > 0:
            if collisions_with_platforms:
                if self.pos.y + self.width / 3 < collisions_with_platforms[0].rect.bottom:
                    self.pos.y = collisions_with_platforms[0].rect.top + 1
                    self.velocity.y = 0
                    self.grounded = True
            if self.rect.bottom == gamesystem.HEIGHT - 30:
                self.pos.y = gamesystem.HEIGHT - self.height - 30
        else: self.grounded = False
        
        if self.shooting and self.time_since_fired >= self.firing_time:
            self.create_bullet(bullets, sprites)
            self.time_since_fired = 0
        else:
            self.time_since_fired += 1

    def jump(self):
        if self.grounded:
            self.jumping = True
            self.velocity.y = -15
    
    def stop_jump(self):
        if self.jumping:
            if self.velocity.y < -3:
                self.velocity.y = -3
    
    def shoot(self):
        if not self.shooting:
            self.shooting = True
            self.time_since_fired = self.firing_time

    def stop_shoot(self):
        if self.shooting:
            self.shooting = False

class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y):
        super().__init__()
        self.size = self.width, self.height = width, height
        self.pos = vector((x, y))
        self.color = (0, 100, 255)
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)
        self.rect = self.surface.get_rect(center = (x, y))

    def pack(self):
        self.surface = None
        self.rect = None
        self.pos = (self.pos.x, self.pos.y)

        info = [
            self.size,
            self.pos,
            self.color,
            self.surface,
            self.rect
        ]
        return info

    def unpack(self, info):
        self.size = self.width, self.height = info[0]
        self.pos = info[1]
        self.color = info[2]
        self.surface = info[3]
        self.rect = info[4]

        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)
        self.pos = vector(self.pos)
        self.rect = self.surface.get_rect(center = (self.pos.x, self.pos.y))

    def check(self, group):
        collides = False
        if pygame.sprite.spritecollideany(self, group):
            return True
        else:
            for entity in group:
                if entity == self:
                    continue
                if (abs(self.rect.top - entity.rect.bottom) < 50) or (abs(self.rect.bottom - entity.rect.top) < 50):
                    collides = True
            if not collides:
                return False
            else: return True

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.type = 0
        self.size = self.width, self.height = width, height
        self.color = (200, 50, 0)
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)
        self.rect = self.surface.get_rect(center = (x + width / 2, y + height / 2))
        self.pos = vector((x, y))
        self.velocity = vector((0, 0))
        self.acceleration = vector((0, 0))
        self.direction = vector((0, 0))
        self.speed = random.randint(2, 5) / 10
        self.grounded = True
        self.jumping = False

        self.max_hp = 100
        self.current_hp = self.max_hp
        self.damage = 0
        self.score = 0

    def pack(self):
        self.surface = None
        self.rect = None
        self.pos = (self.pos.x, self.pos.y)
        self.velocity = (self.velocity.x, self.velocity.y)
        self.acceleration = (self.acceleration.x, self.acceleration.y)
        self.direction = (self.direction.x, self.direction.y)

        info = [
            self.type,
            self.size,
            self.color,
            self.surface,
            self.rect,
            self.pos,
            self.velocity,
            self.acceleration,
            self.direction,
            self.speed,
            self.grounded,
            self.jumping,
            self.max_hp,
            self.current_hp,
            self.damage,
            self.score
        ]
        return info

    def unpack(self, info):
        self.type = info[0]
        self.size = self.width, self.height = info[1]
        self.color = info[2]
        self.surface = info[3]
        self.rect = info[4]
        self.pos = info[5]
        self.velocity = info[6]
        self.acceleration = info[7]
        self.direction = info[8]
        self.speed = info[9]
        self.grounded = info[10]
        self.jumping = info[11]
        self.max_hp = info[12]
        self.current_hp = info[13]
        self.damage = info[14]
        self.score = info[15]

        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)
        self.pos = vector(self.pos)
        self.rect = self.surface.get_rect(center = (self.pos.x + self.width / 2, self.pos.y - self.height / 2))
        self.velocity = vector(self.velocity)
        self.acceleration = vector(self.acceleration)
        self.direction = vector(self.direction)
    
    def _check_vector_to_player(self, player_pos):
        return (player_pos - self.pos).normalize()
    
    def display_health(self, screen):
        width = (self.width * 1.4) * (self.current_hp / self.max_hp)
        pygame.draw.rect(screen, (255, 0, 0),
        pygame.Rect((self.rect.left + self.width / 2) - self.width * 0.7, self.rect.top - 14, width, 6))

    def move(self, player):
        pass

    def update(self, platforms, player):
        pass
    
    def check(self, group):
        collides = False
        if pygame.sprite.spritecollideany(self, group):
            return True
        else:
            for entity in group:
                if entity == self:
                    continue
                if (abs(self.rect.top - entity.rect.bottom) < 20) or (abs(self.rect.bottom - entity.rect.top) < 20):
                    collides = True
                if (abs(self.rect.left - entity.rect.right) < 20) or (abs(self.rect.right - entity.rect.left) < 20):
                    collides = True
            if not collides:
                return False
            else: return True

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_pos, damage):
        super().__init__()
        self.size = self.width, self.height = 5, 5 
        self.color = (255, 255, 0)
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)
        self.rect = self.surface.get_rect(center = (player_pos.x + self.width / 2, player_pos.y + self.height / 2))
        self.pos = vector((player_pos.x, player_pos.y))
        mx, my = pygame.mouse.get_pos()
        self.direction = (vector((mx, my)) - player_pos).normalize()
        self.speed = 6
        self.damage = damage
    
    def move(self):
        self.pos += self.direction * self.speed
        self.rect.midbottom = self.pos
    
    def update(self, enemies):
        if self.rect.right < 0 or self.rect.left > gamesystem.WIDTH:
            self.kill()
        collisions_with_enemies = pygame.sprite.spritecollide(self, enemies, False)
        if collisions_with_enemies:
            collisions_with_enemies[0].current_hp -= self.damage
            self.kill()

#   TYPES OF ENEMIES

class WalkingDemon(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40)
        self.type = 1
        self.speed = random.randint(2, 6) / 10

        self.max_hp = 50
        self.current_hp = self.max_hp
        self.damage = 3
        self.score = 1
    
    def move(self, player):
        self.direction = self._check_vector_to_player(player.pos)
        self.acceleration = vector(0, gamesystem.GRAVITY)

        if self.pos.x + self.width / 2 < gamesystem.WIDTH:
            if self.direction.x < 0:
                self.acceleration.x = -self.speed
            if self.direction.x > 0:
                self.acceleration.x = self.speed
            if abs(self.direction.y / self.direction.x) >= 2 and self.direction.y < 0:
                self.jump()
        
            self.acceleration.x += self.velocity.x * gamesystem.FRICTION
            self.velocity += self.acceleration
            self.pos += self.velocity + 0.5 * self.acceleration
        
        self.rect.midbottom = self.pos

    def update(self, platforms, player):
        collisions_with_platforms = pygame.sprite.spritecollide(self, platforms, False)
        if self.velocity.y > 0:
            if collisions_with_platforms:
                if self.pos.y + self.width / 3 < collisions_with_platforms[0].rect.bottom:
                    self.pos.y = collisions_with_platforms[0].rect.top + 1
                    self.velocity.y = 0
                    self.grounded = True
            if self.rect.bottom == gamesystem.HEIGHT - 30:
                self.pos.y = gamesystem.HEIGHT - self.height - 30
        else: self.grounded = False

        if pygame.sprite.collide_rect(self, player):
            player.current_hp -= self.damage
            self.velocity.x = -self.direction.x * self.speed * 40
            self.velocity.y = -self.direction.y * self.speed

        if self.current_hp <= 0:
            player.score += self.score
            self.kill()
    
    def jump(self):
        if self.grounded:
            self.jumping = True
            self.velocity.y = -10
    
    def stop_jump(self):
        if self.jumping:
            if self.velocity.y < -3:
                self.velocity.y = -3

class FlyingDemon(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 30, 30)
        self.type = 2
        self.max_hp = 30
        self.current_hp = self.max_hp
        self.damage = 10
        self.score = 2

    def move(self, player):
        self.direction = self._check_vector_to_player(player.pos)
        self.acceleration = vector((0, 0))

        if self.pos.x + self.width / 2 < gamesystem.WIDTH:
            if self.direction.x < 0:
                self.acceleration.x = -self.speed
            if self.direction.x > 0:
                self.acceleration.x = self.speed
            if self.direction.y < 0:
                self.acceleration.y = -self.speed
            if self.direction.y > 0:
                self.acceleration.y = self.speed
        
            self.acceleration += self.velocity * gamesystem.FRICTION
            self.velocity += self.acceleration
            self.pos += self.velocity + 0.5 * self.acceleration
        
        self.rect.midbottom = self.pos

    def update(self, platforms, player):
        if pygame.sprite.collide_rect(self, player):
            player.current_hp -= self.damage
            self.velocity.x = -self.direction.x * self.speed * 40
            self.velocity.y = -abs(self.direction.y * self.speed * 60 + 20)

        if self.current_hp <= 0:
            player.score += self.score
            self.kill()