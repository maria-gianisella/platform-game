import pgzrun
from pgzero.actor import Actor
from pgzero.keyboard import keyboard
from pgzero.loaders import sounds
from pgzero.builtins import music

WIDTH = 800
HEIGHT = 600

GRAVITY = 800
PLAYER_SPEED = 200
JUMP_STRENGTH = -500
ANIMATION_RATE = 0.1

class AnimatedActor(Actor):
    def __init__(self, animations, **kwargs):
        self.animations = animations
        self.direction = 'right'
        self.action = 'idle'
        initial_image = self.animations[f'{self.action}_{self.direction}'][0]
        super().__init__(initial_image, **kwargs)
        self.frame_index = 0
        self.animation_timer = 0

    def update_animation(self, dt):
        self.animation_timer += dt
        if self.animation_timer < ANIMATION_RATE:
            return
        self.animation_timer = 0
        animation_key = f'{self.action}_{self.direction}'
        current_animation = self.animations.get(animation_key)
        if current_animation:
            self.frame_index = (self.frame_index + 1) % len(current_animation)
            self.image = current_animation[self.frame_index]

    def set_action(self, new_action):
        if self.action != new_action:
            self.action = new_action
            self.frame_index = 0
            self.animation_timer = 0

class Player(AnimatedActor):
    def __init__(self, pos):
        animations = {
            'idle_right': ['alien_pink_stand'],
            'idle_left': ['alien_pink_stand_left'],
            'walk_right': ['alien_pink_walk1', 'alien_pink_walk2'],
            'walk_left':  ['alien_pink_walk1_left', 'alien_pink_walk2_left'],
        }
        super().__init__(animations, pos=pos)
        self.vy = 0
        self.on_ground = False
        self.cherries_collected = 0

    def move(self, dt, platforms):
        vx = 0
        if keyboard.left:
            vx = -PLAYER_SPEED
            self.direction = 'left'
        elif keyboard.right:
            vx = PLAYER_SPEED
            self.direction = 'right'

        if self.on_ground and keyboard.up:
            self.vy = JUMP_STRENGTH
            if music_on: sounds.jump.play()

        self.vy += GRAVITY * dt
        self.x += vx * dt
        self.y += self.vy * dt

        self.on_ground = False
        for p in platforms:
            if self.colliderect(p) and self.vy >= 0 and self.bottom < p.center[1]:
                self.bottom = p.top
                self.vy = 0
                self.on_ground = True

        if self.on_ground:
            self.set_action('idle' if vx == 0 else 'walk')
        
        self.update_animation(dt)

class Enemy(AnimatedActor):
    def __init__(self, pos, patrol_dist):
        animations = {
            'walk_left': ['bee_fly'],
            'walk_right': ['bee_fly_left'],
            'idle_left': ['bee'],
            'idle_right': ['bee_left'],
        }
        super().__init__(animations, pos=pos)
        self.start_x = pos[0]
        self.end_x = pos[0] + patrol_dist
        self.vx = -60
        self.set_action('walk')
        self.direction = 'left'

    def move(self, dt):
        self.x += self.vx * dt
        if (self.vx < 0 and self.x < self.start_x) or \
           (self.vx > 0 and self.x > self.end_x):
            self.vx *= -1
            self.direction = 'right' if self.vx > 0 else 'left'
        self.update_animation(dt)

game_state = 'menu'
music_on = True
player = None
enemies = []
platforms = []
cherries = []

def draw_menu():
    button_start.draw()
    button_music.draw()
    button_exit.draw()

def draw_game_elements():
    for p in platforms: p.draw()
    for c in cherries: c.draw()
    for e in enemies: e.draw()
    player.draw()
    screen.draw.text(f"Cerejas: {player.cherries_collected} / 3", (20, 20), fontsize=30)

button_restart = Actor('button_restart', center=(WIDTH / 2, 400))
button_menu = Actor('button_menu', center=(WIDTH / 2, 450))

def draw_win_screen():
    screen.draw.text("VOCÊ ESCAPOU!", center=(WIDTH/2, HEIGHT/2), fontsize=80, color="green")
    button_restart.draw()
    button_menu.draw()
    
def draw_lose_screen():
    screen.draw.text("VOCÊ FOI ATACADO!\nTENTE DE NOVO!", center=(WIDTH/2, HEIGHT/2), fontsize=80, color="black")
    button_restart.draw()
    button_menu.draw()

def setup_level():
    global player, enemies, platforms, cherries
    player = Player(pos=(100, 400))
    platforms = [Actor('platform_cake', topleft=(-100, HEIGHT - 40))]
    for i in range(15):
        platforms.append(Actor('platform_choco', topleft=(i * 64, HEIGHT - 40)))

    platforms.append(Actor('platform_cake', center=(400, 450)))
    platforms.append(Actor('platform_choco', center=(250, 350)))
    platforms.append(Actor('platform_choco', center=(550, 300)))
    platforms.append(Actor('platform_cake', center=(350, 200)))
    
    cherries = [
        Actor('cherry', center=(250, 310)),
        Actor('cherry', center=(550, 260)),
        Actor('cherry', center=(350, 160))
    ]
    enemies = [Enemy(pos=(550, 480), patrol_dist=200)]

def check_collisions():
    global game_state
    
    # Colisão com inimigos
    for e in enemies:
        if player.colliderect(e):
            if music_on: sounds.defeat.play()
            game_state = "lose"
            return

    # Coleta de cristais
    for c in cherries:
        if player.colliderect(c):
            if music_on: sounds.collect.play()
            player.cherries_collected += 1
            cherries.remove(c)
            if player.cherries_collected >= 3:
                game_state = "win"
                return
    
    # Cair do mapa
    if player.top > HEIGHT:
        if music_on: sounds.defeat.play()
        game_state = "lose"

def update_game_logic(dt):
    player.move(dt, platforms)
    for e in enemies:
        e.move(dt)
    check_collisions()

def draw():
    screen.blit('background_candy', (0, 0))
    if game_state == 'menu':
        draw_menu()
    elif game_state == 'playing':
        draw_game_elements()
    elif game_state == 'win':
        draw_game_elements() # Desenha o estado final do jogo
        draw_win_screen()
    elif game_state == 'lose':
        draw_game_elements() # Desenha o estado final do jogo
        draw_lose_screen()

def update(dt):
    if game_state == 'playing':
        update_game_logic(dt)

# Inicialização

current_level = 1
MAX_LEVEL = 3

def setup_level():
    global player, enemies, platforms, cherries, current_level
    player = Player(pos=(100, 400))
    platforms = []
    cherries = []
    enemies = []

    if current_level == 1:
        platforms = [Actor('platform_cake', topleft=(-100, HEIGHT - 40))]
        for i in range(15):
            platforms.append(Actor('platform_choco', topleft=(i * 64, HEIGHT - 40)))
        platforms.append(Actor('platform_cake', center=(400, 450)))
        platforms.append(Actor('platform_choco', center=(250, 350)))
        platforms.append(Actor('platform_choco', center=(550, 300)))
        platforms.append(Actor('platform_cake', center=(350, 200)))
        cherries = [
            Actor('cherry', center=(250, 310)),
            Actor('cherry', center=(550, 260)),
            Actor('cherry', center=(350, 160))
        ]
        enemies = [Enemy(pos=(550, 480), patrol_dist=200)]
    elif current_level == 2:
        platforms = [Actor('platform_cake', topleft=(-100, HEIGHT - 40))]
        for i in range(16):
            platforms.append(Actor('platform_choco', topleft=(i * 60, HEIGHT - 40)))
        platforms.append(Actor('platform_cake', center=(400, 500)))
        platforms.append(Actor('platform_choco', center=(200, 400)))
        platforms.append(Actor('platform_choco', center=(600, 350)))
        platforms.append(Actor('platform_cake', center=(300, 250)))
        platforms.append(Actor('platform_choco', center=(500, 180)))
        cherries = [
            Actor('cherry', center=(200, 360)),
            Actor('cherry', center=(600, 310)),
            Actor('cherry', center=(500, 140)),
            Actor('cherry', center=(300, 210))
        ]
        enemies = [
            Enemy(pos=(550, 480), patrol_dist=250),
            Enemy(pos=(250, 380), patrol_dist=120)
        ]
        # Deixa os inimigos mais rápidos
        for e in enemies:
            e.vx *= 1.3
    elif current_level == 3:
        platforms = [Actor('platform_cake', topleft=(-100, HEIGHT - 40))]
        for i in range(18):
            platforms.append(Actor('platform_choco', topleft=(i * 50, HEIGHT - 40)))
        platforms.append(Actor('platform_cake', center=(400, 520)))
        platforms.append(Actor('platform_choco', center=(150, 430)))
        platforms.append(Actor('platform_choco', center=(650, 400)))
        platforms.append(Actor('platform_cake', center=(300, 320)))
        platforms.append(Actor('platform_choco', center=(500, 270)))
        platforms.append(Actor('platform_cake', center=(200, 200)))
        platforms.append(Actor('platform_choco', center=(600, 150)))
        cherries = [
            Actor('cherry', center=(150, 390)),
            Actor('cherry', center=(650, 360)),
            Actor('cherry', center=(500, 230)),
            Actor('cherry', center=(200, 160)),
            Actor('cherry', center=(600, 110))
        ]
        enemies = [
            Enemy(pos=(550, 500), patrol_dist=300),
            Enemy(pos=(250, 420), patrol_dist=180),
            Enemy(pos=(500, 250), patrol_dist=150)
        ]
        # Inimigos ainda mais rápidos
        for e in enemies:
            e.vx *= 1.7

def check_collisions():
    global game_state, current_level

    # Colisão com inimigos
    for e in enemies:
        if player.colliderect(e):
            if music_on: sounds.defeat.play()
            game_state = "lose"
            return

    # Coleta de cristais
    for c in cherries[:]:
        if player.colliderect(c):
            if music_on: sounds.collect.play()
            player.cherries_collected += 1
            cherries.remove(c)
            if len(cherries) == 0:
                if current_level < MAX_LEVEL:
                    current_level += 1
                    setup_level()
                else:
                    game_state = "win"
                return

    # Cair do mapa
    if player.top > HEIGHT:
        if music_on: sounds.defeat.play()
        game_state = "lose"

def draw_game_elements():
    for p in platforms: p.draw()
    for c in cherries: c.draw()
    for e in enemies: e.draw()
    player.draw()
    screen.draw.text(f"Cerejas: {player.cherries_collected} / {len(cherries) + player.cherries_collected}", (20, 20), fontsize=30, color="blue")
    screen.draw.text(f"Fase: {current_level}", (WIDTH - 150, 20), fontsize=30, color="blue")

def on_mouse_down(pos):
    global game_state, music_on, current_level
    if game_state in ['menu', 'win', 'lose']:
        if button_start.collidepoint(pos):
            game_state = 'playing'
            current_level = 1
            setup_level()
        elif button_exit.collidepoint(pos):
            quit()
        elif button_music.collidepoint(pos):
            music_on = not music_on
            button_music.image = 'button_music_on' if music_on else 'button_music_off'
            if music_on: music.unpause()
            else: music.pause()
        elif game_state == 'win' and button_restart.collidepoint(pos):
            game_state = 'playing'
            current_level = 1
            setup_level()
        elif game_state == 'lose' and button_restart.collidepoint(pos):
            game_state = 'playing'
            current_level = 1
            setup_level()

button_start = Actor('button_start', center=(WIDTH / 2, 250))
button_music = Actor('button_music_on', center=(WIDTH / 2, 350))
button_exit = Actor('button_exit', center=(WIDTH / 2, 450))

if music_on:
    music.play('music')
    music.set_volume(0.3)

pgzrun.go()