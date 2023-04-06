import os
import pygame
import random
from pygame.constants import RLEACCEL
# variables locals per a veure quina tecla es presionada
from pygame.locals import(
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_SPACE,
    K_p,
    K_q
)
# definim constants per al tamany de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,150)
BLUE_LIGHT = (135, 206, 250)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)
GREY = (211, 211, 211)
color = BLUE_LIGHT

#nom del joc en la finestra
pygame.display.set_caption('DI_Avionets')
    

#ruta relativa
image_player_path = "resources/jet.png"
image_enemy_path = "resources/missile.png"
image_cloud_path = "resources/cloud.png"

#fonts
consolas = pygame.font.match_font('consolas')
tahoma = pygame.font.match_font('tahoma')
arial = pygame.font.match_font('arial')
courier = pygame.font.match_font('courier')

#canvi fons
dia = True

#puntuació
score = 0

#nivells
level = 1
puntuacio_limit = 500

#classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load(image_player_path).convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            move_up_sound.play()
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            move_down_sound.play()
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if pressed_keys[K_SPACE]:
            laser_sound.play()
            player.disparar()
    
    def disparar(self):
        shot = Disparar(self.rect.centerx, self.rect.top+15)
        laser.add(shot)
        

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load(image_enemy_path).convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(random.randint(SCREEN_WIDTH+20, SCREEN_WIDTH+100),
                    random.randint(0, SCREEN_HEIGHT)
                    )
        )
        self.speed = random.randint((2*level), (10+(3*level)))

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill() 

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load(image_cloud_path).convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(random.randint(SCREEN_WIDTH+20, SCREEN_WIDTH+100),
                    random.randint(0, SCREEN_HEIGHT)
                    )
        )
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
            
class Disparar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("resources/shot.png").convert(),(20,10))
        self.image.set_colorkey(BLACK, RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y

    def update(self):
        self.rect.x += 25
        if self.rect.left < 0:
            self.kill()

#mostrar score en la pantalla
def showMessage(screen, font, text, color, dimensionsPx, x, y):
    letter_type = pygame.font.Font(font, dimensionsPx)
    superficie = letter_type.render(text, True, color)
    rectangle = superficie.get_rect()
    rectangle.center = (x, y)
    screen.blit(superficie,rectangle)


#pausar el joc
def pausar():
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pause = False
            if event.type == QUIT:
                pause = False
                running = False
        showMessage(screen, arial, "Pause", RED, 50, (SCREEN_WIDTH/2), (SCREEN_HEIGHT/2))
        pygame.display.update()
        pygame.mixer.music.stop()
        clock.tick(5)

#intro
def start_game():
    intro = True
    while intro:
        menu_sound.play()
        screen.fill(GREY)
        showMessage(screen, arial, "Welcome to", BLACK, 60, 400, 100)
        showMessage(screen, arial, "AirPlanes Game", BLACK, 55, 400, 200)
        readFile()
        showMessage(screen, arial, "Press 'P' to start the game", RED, 35, 400, 400)
        pygame.display.update()
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_p:
                    menu_sound.stop()
                    running = False
                    intro = False

#llegir i escriure en un fitxer     
def readFile():
    filename = "punt_max.txt"
    try:
        if os.path.exists(filename):
            highscore = open(filename,'r', encoding='UTF-8')
            score = highscore.read()
            showMessage(screen, arial, "The HighScore is:"+str(score), BLACK, 32, 400, 300)
        else:
            highscore = open(filename, 'w')
            showMessage(screen, arial, "The HighScore is: 0", BLACK, 32, 400, 300)
    except:
        print("Error de lectura")
    finally:
        highscore.close()

def writeFile(score):
    try:
        filename = "punt_max.txt"
        highscore = open(filename, 'w')
        highscore.write(score)
    except:
        print("Error de escritura")
    finally:
        highscore.close


#inicialitza la musica
pygame.mixer.init()

#inicialitza el joc
pygame.init()



#efectes de música
move_up_sound = pygame.mixer.Sound("resources/Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("resources/Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("resources/Collision.ogg")
gameover_sound = pygame.mixer.Sound("resources/8_Bit_Nostalgia_gameover.mp3")
new_enemy_sound = pygame.mixer.Sound("resources/01 golpes.mp3")
menu_sound = pygame.mixer.Sound("resources/8_Bit_Menu.mp3")
laser_sound = pygame.mixer.Sound("resources/laser_sound.wav")
explosion_missile = pygame.mixer.Sound("resources/explosion_sound.wav")
newlevel = pygame.mixer.Sound("resources/newLevel_sound.wav")


#velocitats dels frames
clock = pygame.time.Clock()

# assignem el tamany de la pantalla utilitzant les constants
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#velocitat d'eixida de enemics
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, (100+(450-(50*level))))

#velocitat d'eixida de núvols
ADDCLOUD = ADDENEMY + 1
pygame.time.set_timer(ADDCLOUD, 1000)

#canviar color de fons
CANVIAR_FONS = ADDCLOUD + 1
pygame.time.set_timer(CANVIAR_FONS, 20000)


# instanciem la classe
player = Player()
enemy = Enemy()
cloud = Cloud()

#Sprites i all_sprites
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

clouds = pygame.sprite.Group()
all_sprites.add(clouds)

laser = pygame.sprite.Group()
all_sprites.add(laser)

running = True
game_over = False

start_game()

#llegim el fitxer de la puntuació màxima
file_highscore = open("punt_max.txt", 'r')
highscore = file_highscore.read()

#musica del joc
pygame.mixer.music.load("resources/Apoxode_-_Electric_1.ogg")
pygame.mixer.music.play(loops=-1)

# bucle principal
while running:
    
    #gameover
    while game_over:
        pygame.mixer.music.stop()
        pygame.mixer.music.play(loops=-1)
        gameover_sound.play()
        gameover_sound.set_volume(0.2)
        screen.fill(BLACK)
        showMessage(screen, consolas, "GAME OVER", RED, 50, 400, 150)
        showMessage(screen, consolas, "Level:"+str(level)+" "+"SCORE:"+str(score), GREEN, 30, 400, 250)
        if highscore != '':
            if int(score) > int(highscore):
                writeFile(str(score))
                showMessage(screen, consolas, "FELICITATS!!", YELLOW, 25, 400, 300)
                showMessage(screen, consolas, "HAS CONSEGUIT UN NOU RECORD", YELLOW, 25, 400, 350)
        else: 
            writeFile(str(score))
        showMessage(screen, consolas, "Press 'Q' to quit game", BLUE, 25, 400, 450)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                game_over = True
            if event.type == KEYDOWN:
                if event.key == K_q:
                    running = False
                    game_over = False
            
       
    # bucle d'events de les tecles
    for event in pygame.event.get():
        
        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:  # Pausem el joc si presionem la tecla "ESC"
                pausar()
                pygame.mixer.music.play(loops=-1)

        elif event.type == QUIT:  # Eixida del joc si tanquem la finestra amb el boto de la "X"
            running = False
        elif event.type == ADDENEMY:# anyadeix enemics cada 2,5 segons
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == ADDCLOUD:# anyadeix nuvols cada 1 segon
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
        
        elif event.type == CANVIAR_FONS: # canvia el color de fons cada 20 segons
            if dia == True:#"dia"
                color = BLUE_LIGHT
                dia = False
            else:#"nit"
                color = BLACK
                dia = True
        

    #detecta les tecles que s'apreten        
    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)
    enemies.update()
    clouds.update()
    laser.update()

    screen.fill(color)#color del fondo durant el inici del joc
    pygame.display.update()
          
    #mostra la puntuació en la part dreta superior de la pantalla
    #NOTA: si la font "consolas" NO funciona també estàn disponibles: [tahoma, arial, courier]
    showMessage(screen, consolas, str(score).zfill(6), RED, 30, 720, 30)#.zfill() -> cantitat de 0 en la pantalla
    
    #missatge de level
    showMessage(screen, consolas, "Level:"+(str(level)), RED, 25, 530, 30)
    
    #puntuacio +10 quan un objecte missil passa per la part esquerre de la pantalla
    for e in enemies:
        if e.rect.right < 10:
            score += 10 

    
    #augmentar level en +1 cada vegada que el score siga multiple de 500
    if (score%500 == 0) and puntuacio_limit == score:
        level += 1
        newlevel.play()
        showMessage(screen, consolas, "Level:"+(str(level)), RED, 25, 530, 30)
        puntuacio_limit += 500
        

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    #colisió entre Player i un Enemy
    if pygame.sprite.spritecollideany(player, enemies):
        collision_sound.play()
        player.kill()
        game_over = True
        #running = False
    
    #colisió entre el dispar del Player i un enemic
    if pygame.sprite.groupcollide(laser, enemies, True, True):
        explosion_missile.play()
        score += 20

    #screen.blit(player.surf, player.rect)
    #screen.blit(enemy.surf, enemy.rect)
    #screen.blit(cloud.surf, cloud.rect)
    laser.draw(screen) 

    pygame.display.flip()

    #velocitat del joc
    clock.tick(30)

#finalitza la música 
pygame.mixer.music.stop()
pygame.mixer.quit()

#finalitza el joc
pygame.quit()