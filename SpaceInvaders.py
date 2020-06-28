"""This is the game SpaceInvaders.
The player stands on the bottom of the screen. He can move left and right.
There are enemies in a group. They move left and right and down as a group in a pattern.
You can shoot the enemies by pressing arrow key up. They shoot randomly down. If you are shot, the game is over.
Each time you defeat a group of enemies, a new group appears and they move faster than the previous one.
The highest score is kept and changes if a new highscore is reached.

Pygame was used for the graphics."""
import pygame
import random


# Standard settings
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)


# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('imgs/Speler.png').convert()
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.x = 160
        self.rect.y = 281
        self.change_x = 0
        self.walls = None
    def changespeed(self, x):
        self.change_x += x
    def setwalls(self, walls):
        self.walls = walls
    def givex(self):
        return self.rect.x
    def givey(self):
        return self.rect.y
    def update(self):
        self.rect.x += self.change_x
        hits = pygame.sprite.spritecollide(self, self.walls, False)
        for block in hits:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, hight):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, hight])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([4, 10])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        self.rect.y -= 5

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('imgs/Vijand1.png').convert()
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.changex = 0
        self.changey = 0
        self.dir = -1
    def changecoor(self, x, y):
        self.changex = x
        self.changey = y
    def givex(self):
        return self.rect.x
    def givey(self):
        return self.rect.y
    def givedir(self):
        return self.dir
    def changedir(self):
        if self.dir > 0:
            self.dir = -1
        else:
            self.dir = 1
    def update(self):
        self.rect.x += self.changex
        self.rect.y += self.changey
        self.changex, self.changey = 0, 0

class BulletEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([4, 10])
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        self.rect.y += 4

# Game mechanics
    # Initialiazing
def init(xdisplay, ydisplay, name):
    pygame.init()
    display = pygame.display.set_mode([xdisplay, ydisplay])
    pygame.display.set_caption(name)
    return display

    # Add walls
def addwalls(walls, allblocks):
    wall1 = Wall(0, 0, 10, 316)
    walls.add(wall1)
    allblocks.add(wall1)
    wall2 = Wall(342, 0, 10, 316)
    walls.add(wall2)
    allblocks.add(wall2)
    return (walls, allblocks)

    # Add enemies
def addenemies(enemies, allblocks):
    for i in range(56, 276, 22):
        for j in range(50, 138, 22):
            enemy = Enemy(i, j)
            enemies.add(enemy)
            allblocks.add(enemy)
    return (enemies, allblocks)

    # Enemies shoot bullets random
def enemiesshoot(allblocks, enemies, time, bulletsenemies):
    if time%75 == 0:
        bulletsenemies = pygame.sprite.Group()
        listxenemies = []
        for i in enemies:
            listxenemies.append((i.givex(), i.givey()))
        randomenemy = random.choice(listxenemies)
        bulletenemy = BulletEnemy(randomenemy[0] + 8, randomenemy[1] + 8)
        allblocks.add(bulletenemy)
        bulletsenemies.add(bulletenemy)
    return (allblocks, bulletsenemies)

    # Bullet hit enemy
def hitenemy(bullets, enemies, score, allblocks):
    for i in bullets:
        hits = pygame.sprite.spritecollide(i, enemies, True)
        if len(hits) > 0:
            score += len(hits)
            i.remove(allblocks)
            i.remove(bullets)
    return (bullets, enemies, score, allblocks)

    # Move enemies
def enemiesmove(time, accel, enemies):
    if time%(50 - accel) == 0:
        enemydown = False
        for i in enemies:
            if i.givedir() < 0 and i.givex() == 12:
                enemydown = True
            elif i.givedir() > 0 and i.givex() == 320:
                enemydown = True
        if enemydown is True:
            for i in enemies:
                i.changedir()
                i.changecoor(0, 22)
            enemydown = False
        else:
            for i in enemies:
                i.changecoor(i.givedir()*22, 0)
    return enemies

    # Remove bullets that didn't hit
def removebullets(bullets, allblocks):
    for bullet in bullets:
        if bullet.rect.y < -10:
            bullets.remove(bullet)
            allblocks.remove(bullet)
    return bullets, allblocks

    # New enemies
def newenemies(enemies, allblocks, accel):
    if len(enemies) == 0:
        for i in range(56, 276, 22):
            for j in range(50, 138, 22):
                enemy = Enemy(i, j)
                enemies.add(enemy)
                allblocks.add(enemy)
        accel += 2
    return enemies, allblocks, accel

    # Write text
def write(font, text, color, display, place):
    txt = font.render(text, True, color)
    display.blit(txt, place)

    # Read highscore
def readhigh(name):
    with open(name, 'r') as file:
        z = file.read()
        try:
            highscore = int(z)
        except:
            highscore = 0
    return highscore

    # Improve highscore
def improvehigh(name, newhighscore, highscore, score):
    with open(name, 'w') as file:
        if score > highscore:
            file.write(str(score))
            newhighscore = True
        else:
            file.write(str(highscore))
    return newhighscore

# User moves
def usermoves(done, done2, player, state, bullets, allblocks, display):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
            done2 = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-3)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(3)
            elif event.key == pygame.K_SPACE:
                if state == 1:
                    state = 0
                else:
                    state = 1
            elif event.key == pygame.K_UP:
                if len(bullets) < 2:
                    bullet = Bullet(player.givex() + 15, player.givey() - 9)
                    allblocks.add(bullet)
                    bullets.add(bullet)
            elif event.key == pygame.K_r:
                done = False
                done2 = False
                play(display)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(3)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(-3)
    return done, done2, player, state, bullets, allblocks


# Game loop
def play(display):
    # Names
    font = pygame.font.Font("C:/Windows/Fonts/FORTE.TTF", 20)
    font2 = pygame.font.Font("C:/Windows/Fonts/STENCIL.TTF", 40)
    allblocks = pygame.sprite.Group()
    player = Player()
    allblocks.add(player)
    walls = pygame.sprite.Group()
    walls, allblocks = addwalls(walls, allblocks)
    player.setwalls(walls)
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    enemies, allblocks = addenemies(enemies, allblocks)
    newhighscore = False
    accel = 0
    bulletsenemies = pygame.sprite.Group()
    clock = pygame.time.Clock()
    time = 0
    done = True
    done2 = True
    score = 0
    state = 1
    # Game
    while done:
        # User moves
        done, done2, player, state, bullets, allblocks = usermoves(done, done2, player, state, bullets, allblocks, display)
        
        # When game plays
        if state == 1:
                
            time += 1

            # Main game mechanics
            allblocks, bulletsenemies = enemiesshoot(allblocks, enemies, time, bulletsenemies)
            bullets, enemies, score, allblocks = hitenemy(bullets, enemies, score, allblocks)
            enemies = enemiesmove(time, accel, enemies)
            bullets, allblocks = removebullets(bullets, allblocks)
            enemies, allblocks, accel = newenemies(enemies, allblocks, accel)

            # Die
            for i in enemies:
                if i.givey() > 260:
                    done = False
            hits = pygame.sprite.spritecollide(player, bulletsenemies, True)
            if len(hits) > 0:
                done = False
                    
            # Display
            display.fill(black)
            allblocks.update()
            allblocks.draw(display)
            write(font, 'Score: ' + str(score), green, display, [10, 10])
            write(font, 'Arrow up to shoot', white, display, [10, 30])

            # Time between loops
            clock.tick(60)

        # When pause
        else:
            
            # Display
            display.fill(black)
            write(font2, 'Pause', white, display, [50, 50])
            write(font, 'Press r to restart', white, display, [10, 170])

        # Flip display
        pygame.display.flip()

    # Highscore
    highscore = readhigh('HighscoreSpaceInvaders.txt')
    newhighscore = improvehigh('HighscoreSpaceInvaders.txt', newhighscore, highscore, score)

    # End display
    while done2:
        # User moves
        done, done2, player, state, bullets, allblocks = usermoves(done, done2, player, state, bullets, allblocks, display)

        # Display
        display.fill(black)
        write(font2, 'Score: ', blue, display, [10, 50])
        write(font2, str(score), blue, display, [100, 150])
        write(font, 'Press r to restart', white, display, [10, 250])
        write(font, 'Highscore: ' + str(highscore), white, display, [10, 10])
        if newhighscore is True:
            write(font, 'New Highscore', green, display, [10, 30])

        # Flip display
        pygame.display.flip()


# Main loop        
def main():
    display = init(352, 316, 'Space Invaders')
    play(display)
    pygame.quit()


# Start game
if __name__ == '__main__':
    main()
