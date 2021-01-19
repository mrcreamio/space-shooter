###########################
#Step 1
#Importing Libraries Needed
###########################
import pygame
import random
import os
from os import path

###########################
#Step 2
#Defining Constants
###########################

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100,100)##set position of game screen 


##Width and height of the screen
WIDTH = 600
HEIGHT = 600


# Defining Colors that would be used 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


###########################
#Step 3
#Initializng Pygame ,setting
#up screen size & title
###########################

pygame.init()
pygame.mixer.init()
#pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("QuestKids")
clock = pygame.time.Clock()     ## For syncing the FPS


###########################
#Step 4
#Defining path & variables for images & game SFX & font
###########################


##setting font
font_name = pygame.font.match_font('comicsansms')

##setting up the path for image assets and sfx of the game from their respective folders
ImagePath = path.join(path.dirname(__file__), 'ImageAssets')
SFXPath = path.join(path.dirname(__file__), 'SFX')

##defining variables for sound,loading them , setting up the volume
shooting_sound = pygame.mixer.Sound(path.join(SFXPath, 'laser.ogg'))
expl_sounds = pygame.mixer.Sound(path.join(SFXPath, 'explosion.wav'))
pygame.mixer.music.set_volume(0.2)     
PlayerShip_ReSpawn_sound = pygame.mixer.Sound(path.join(SFXPath, 'rumble1.ogg'))

##initializing images and loading them 
background = pygame.image.load(path.join(ImagePath, 'space background.png')).convert_alpha()
background_rect = background.get_rect()
PlayerShip_img = pygame.image.load(path.join(ImagePath, 'spaceship.png')).convert_alpha()
start_img = pygame.image.load(path.join(ImagePath, 'buttons - START.png')).convert()
exit_img = pygame.image.load(path.join(ImagePath, 'buttons - EXIT.png')).convert()

#PlayerShip_img.set_colorkey((255,0,255))

	
PlayerShipLifeImg = pygame.image.load(path.join(ImagePath, 'life icon.png')).convert_alpha()
#PlayerShipLifeImg = pygame.transform.scale(PlayerShipl_img, (25, 19))
#PlayerShipLifeImg.set_colorkey(BLACK)
PlayerHealthImage1 = pygame.image.load(path.join(ImagePath, 'life bar 1.png')).convert_alpha()
PlayerHealthImage2 = pygame.image.load(path.join(ImagePath, 'life bar 2.png')).convert_alpha()
PlayerHealthImage3 = pygame.image.load(path.join(ImagePath, 'life bar 3.png')).convert_alpha()
PlayerHealthImage4 = pygame.image.load(path.join(ImagePath, 'life bar 4.png')).convert_alpha()


bullet_img = pygame.image.load(path.join(ImagePath, 'lazer bullet.png')).convert_alpha()
ShipImages = []
AlienShipList = ['alien ship 1.png','alien ship 2.png','alien ship 3.png']

for image in AlienShipList:
    ShipImages.append(pygame.image.load(path.join(ImagePath, image)).convert_alpha())

#Dictionary for Explosion Effect
ExplosionEffect = {}
ExplosionEffect['explosion'] = []

##adding images related to explosion in explosion effect dictionary
for i in range(9):
    filename = 'explosion {}.png'.format(i)##getting filename , there are 9 image files for animation , getting name of each file
    img = pygame.image.load(path.join(ImagePath, filename)).convert_alpha()
    img.set_colorkey(BLACK)
    img_sm = pygame.transform.scale(img, (50, 50))##setting scale for images
    ExplosionEffect['explosion'].append(img_sm)##appending to list inside explosion effect dictionary


###################################
#Step 5
#Button class for main menu buttons
###################################

class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        # Display button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)

        # Set font for the button
        if self.text != '':
            font = pygame.font.SysFont('comicsansms', 30)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
    
    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False


###################################
#Step 6
#Displaying Main menu
###################################

def main_menu():
    global gameDisplay

    menu_song = pygame.mixer.music.load(path.join(SFXPath, "menu1.ogg"))##play menu music
    pygame.mixer.music.play(-1)#-- play music in loop

    title = pygame.image.load(path.join(ImagePath, "title-screen.png")).convert()##image for main menu
    title = pygame.transform.scale(title, (WIDTH, HEIGHT), gameDisplay)
    ##display title
    gameDisplay.blit(title, (0,0))

    ###initializing buttons start and exit
    btn=button(WHITE,WIDTH/2-140, HEIGHT/2+80,118,45,"Start")
    btn.draw(gameDisplay)
    gameDisplay.blit(start_img, (WIDTH/2-140, HEIGHT/2+80))

    btnExit=button(WHITE,WIDTH/2, HEIGHT/2+80,118,45,"Exit")
    btnExit.draw(gameDisplay)
    ##update display
    gameDisplay.blit(exit_img, (WIDTH/2, HEIGHT/2+80))

    pygame.display.update()
    ##loop to get any mouse movement and event 
    while True:
        ev = pygame.event.poll()
        pos=pygame.mouse.get_pos()

        ##checking if mouse button is clicked on any one of these buttons
        if ev.type == pygame.MOUSEBUTTONDOWN:
            if btn.isOver(pos):
                break

        if ev.type == pygame.MOUSEBUTTONDOWN:
            if btnExit.isOver(pos):
                pygame.quit()
                exit()
    
###################################
#Step 7
#creating class for PlayerShip
###################################

class PlayerShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        ## setting scale for PlayerShip image
        self.image = pygame.transform.scale(PlayerShip_img, (51, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()##setting image
        self.radius = 18##setting radius for PlayerShip
        self.speedx = 0 ##PlayerShip movement speed
        self.Health = 100##PlayerShip health
        self.shoot_delay = 230##shoot delay
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3##total lives
        self.visible = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_timer = pygame.time.get_ticks()
        self.rect.centerx = WIDTH / 2##setting PlayerShip position in centre
        self.rect.bottom = HEIGHT - 8##setting PlayerShip position from bottom
        
    def update(self):

        ##hiding playership after dying 


        
        if self.visible and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.visible = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 30

        self.speedx = 0     ## keep PlayerShip ship static at its position 

        ##getting keys pressed and moving ship accordingly on x axis
        keystate = pygame.key.get_pressed()     
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        elif keystate[pygame.K_RIGHT]:
            self.speedx = 5

        ##shooting laser bullets 
        if keystate[pygame.K_SPACE]:
            self.shoot()

        ##keeping player within defined boundaries of the screen
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        ##updating player ship position
        self.rect.x += self.speedx
        
  
    ##shoot method
    def shoot(self):
        ## to tell the bullet where to spawn
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:##checking if the delay between laser bullets shot is over
            self.last_shot = now
            if self.power == 1:
                bullet = Laser(self.rect.centerx, self.rect.top)##creating a bullet
                GameSprites.add(bullet)
                LaserBullets.add(bullet)##adding to the list of bullets
                shooting_sound.play()##playing sound

    ##add health bar on the screen
    def AddHealthBar(self,surf, x, y):
       pct = max(self.Health, 0)
       if self.Health>=80 and self.Health<=100:
           gameDisplay.blit(PlayerHealthImage1, (5,5))
  
       if self.Health<=80 and self.Health>60:
           gameDisplay.blit(PlayerHealthImage2, (5,5))
       if self.Health<=60 and self.Health>40:
           gameDisplay.blit(PlayerHealthImage3, (5,5))
           
       if self.Health<=40 and self.Health>0:
           gameDisplay.blit(PlayerHealthImage4, (5,5))
       
        
##        fill = (pct / 100) * 100##getting the fill area
##        outline_rect = pygame.Rect(x, y, 100, 10)##creating outline
##        fill_rect = pygame.Rect(x, y, fill, 10)##filling the health bar
##        gameDisplay.blit(PlayerHealthImage, (x,y))
##        
##        pygame.draw.rect(surf, RED, fill_rect)##setting the health bar fill color
##        pygame.draw.rect(surf, WHITE, outline_rect, 2)##settting health bar outline color

  
    ##respawn player ship
    def ReSpawn(self):
        self.visible = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)
    ##display lives of the player
    def DisplayLives(self,surf, x, y, lives, img):
        for i in range(lives):##getting number of lives set for player
            img_rect= img.get_rect()
            img_rect.x = x + 30 * i##displaying player image at +30 distance from current image on x axis
            img_rect.y = y##setting the same y axis
            surf.blit(img, img_rect)




###################################
#Step 8
#Defining class for laser bullet
###################################


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img##setting bullet image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        ##seeting bullet position according to the player ship position 
        self.rect.bottom = y 
        self.rect.centerx = x
        ##bullet speed
        self.speedy = -12

    def update(self):
        
        self.rect.y += self.speedy
        ##remove the object from game screen if it reaches the top moving from bottom 
        if self.rect.bottom < 0:
            self.kill()



###################################
#Step 9
#Defining class Alien Ships
###################################

class AlienShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(ShipImages)##choosing a random ship image from list we defined above
        ##setting up image
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        ##setting the radius of enemy ship
        self.radius = int(self.rect.width *.90 / 2)
        ##setting up random x axis movement speed 
        self.speedx = random.randrange(-2, 2)
        ##setting random y axis movement speed 
        self.speedy = random.randrange(6, 12)
        ##random x axis position
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        ##random y axis spawn position
        self.rect.y = random.randrange(-150, -100)
        self.last_update = pygame.time.get_ticks()  ## time when the rotation has to happen
        
    
    ##updating the alien position
    def update(self): 
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        ##random movement of enemies
        if (self.rect.top > HEIGHT + 10) or (self.rect.left < -25) or (self.rect.right > WIDTH + 20):
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)       



##########################################
#Step 10
#Defining class for animation of explosion
##########################################            

class Animation(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size##setting explosion size
        self.image = ExplosionEffect[self.size][0]##setting image
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0##setting first frame 
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1##setting next frame which is next image
            if self.frame == len(ExplosionEffect[self.size]):
                self.kill()##if all images are shown on screen remove from screen
            else:
                center = self.rect.center##else display next image of explosion series on screen
                self.image = ExplosionEffect[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
                


##########################################
#Step 11
#method to spawn aliens on screen
##########################################            


##spawn alien on the screen
def SpawnAlien():
    ship = AlienShip()
    GameSprites.add(ship)
    EnemyShips.add(ship)

###########################################
#Step 11
#Defining method to display score on screen
###########################################            

def DisplayScore(surf, text, size, x, y):
    # Display score on the screen
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)     
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y) # Setting on the top mid
    surf.blit(text_surface, text_rect)


##############################################################
#Step 12
#Playing the game using the classes and methods created above
##############################################################            

playing = True
showMenu = True
while playing:
    if showMenu:
        main_menu()
        pygame.time.wait(2000)

        #Stop menu music
        pygame.mixer.music.stop()
        #Play the gameplay music
        pygame.mixer.music.load(path.join(SFXPath, 'musicgame.ogg'))
        pygame.mixer.music.play(-1)     ## play game sound in a loop
        
        showMenu = False
        
        ## grouping all sprites together
        GameSprites = pygame.sprite.Group()
        Player = PlayerShip()
        GameSprites.add(Player)

        ##grouping laser bullets
        LaserBullets = pygame.sprite.Group()
      
        ## creating group of enemy ships
        EnemyShips = pygame.sprite.Group()
        for i in range(8): ##creating ships together    
            SpawnAlien()

        

        ## Score
        score = 0
        
    
    clock.tick(60)##setting fps
    for event in pygame.event.get():
        ##If the event is to quit game
        if event.type == pygame.QUIT:
            playing = False

        ## Press ESC to exit game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                playing = False

    #2 Update
    GameSprites.update()


    
    ##check all the 
    collisions = pygame.sprite.groupcollide(EnemyShips, LaserBullets, True, True)
    ##delete the enemy ship if it collides with the bullet and play explosion animation and sound
    for collision in collisions:
        score += 10        ##add score to the player score 
        expl_sounds.play()
       
        explosionAnim = Animation(collision.rect.center, 'explosion')
        GameSprites.add(explosionAnim)

        SpawnAlien()##spawn more aliens        

    
    ## check if the PlayerShip collides with alien ship
    collisions = pygame.sprite.spritecollide(Player, EnemyShips, True, pygame.sprite.collide_circle)        
    for collision in collisions:##checking for collisions 
        Player.Health -= 25##reducing player health 
        explosionAnim = Animation(collision.rect.center, 'explosion')
        GameSprites.add(explosionAnim)
        SpawnAlien()##spawn more alien
        if Player.Health <= 0: ##if health is 0 play explosion
            PlayerShip_ReSpawn_sound.play()
            EndExplosion = Animation(Player.rect.center, 'explosion')
            GameSprites.add(EndExplosion)
            Player.ReSpawn()
            Player.lives -= 1##reducing player lives
            Player.Health = 100

  

    ## end game
    if Player.lives == 0 and not EndExplosion.alive():
        showMenu = True

      
   
    gameDisplay.fill(BLACK)
    ##draw background image on screen
    gameDisplay.blit(background, background_rect)

    GameSprites.draw(gameDisplay)
    DisplayScore(gameDisplay, str(score), 24, WIDTH / 2, 10)## setting player score on the screen
    Player.AddHealthBar(gameDisplay, 5, 5)##setting health bar position

    ## draw the player lives on screen
    Player.DisplayLives(gameDisplay, WIDTH - 90, 5, Player.lives, PlayerShipLifeImg)

    ## update full display
    pygame.display.flip()       

pygame.quit()
