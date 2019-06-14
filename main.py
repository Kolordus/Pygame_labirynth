import pygame
import bil
import sys
import mazes
import random
import time
import maze_solver

mazze = mazes.mazes[0]
mazzecopy = mazes.mazes[0]

ramka = pygame.display.set_mode((1920 , 1080))
pygame.display.set_caption('The Game')
pygame.display.toggle_fullscreen()


class Text:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont("comicsansms", 72)

    def draw(self, ramka, tekst):
        text = self.font.render(tekst, True, (255, 0, 0))
        ramka.blit(text, ((1920/2 - text.get_width() / 2), 1080/2 - 36))
        pygame.display.update()
        time.sleep(2)

class Plate(pygame.sprite.Sprite):
    def __init__(self, mazze):
        super().__init__()
        self.mazze = mazze

    def draw(self, ramka):
        ramka.blit(bil.maze, (0, 0))
        counter2 = 180
        for line in range(0,10): # was 10
            counter = 420
            for index in range(0,18): # was 18

                pos = (line,index)

                if pos in player.surr:
                    if self.mazze[line][index] == 0:
                        ramka.blit(bil.black, (counter, counter2))
                    elif self.mazze[line][index] == 1 or self.mazze[line][index] == 9 or self.mazze[line][index] == 8:
                        ramka.blit(bil.yellow, (counter, counter2)) # yellow
                    else:
                        ramka.blit(bil.rock, (counter, counter2)) # rock
                else:
                    ramka.blit(bil.black, (counter, counter2))
                counter += 60 # new piece every 60 px
            counter2 += 60 # same as above
    #

class Player(pygame.sprite.Sprite):
    def __init__(self, mazze):
        super().__init__()
        self.mazze = mazze
        self.pos_x = 425                                                # position on screen - animation purpous
        self.pos_y = 250                                                # position on screen - aniation purpous

        self.a = 1                                                      # position on board - movement purpous
        self.b = 0                                                      # position on board - movement purpous
        self.pos = self.mazze[self.a][self.b]

        self.direction = ""                                             # needed to draw() function
        self.surr = []                                                  # needed for printing 8 neighouring tiles

        self.cross = []                                                 # 4 points around the player
        self.checkpoint = (1,0)                                         # where is the last checkpoint


    def move_right(self):
        self.direction = "right"
        if self.pos_x < 1445:
            self.pos_x += 60
            player.b += 1

    def move_left(self):
        self.direction = "left"
        if self.pos_x > 425:
            self.pos_x -= 60
            player.b -= 1

    def move_down(self):
        if self.pos_y < 730:
            self.direction = "down"
            self.pos_y += 60
            player.a += 1

    def move_up(self):
        if self.pos_y > 190:
            self.direction = "up"
            self.pos_y -= 60
            player.a -= 1
#####
    def surrounding(self):
        self.surr.append((self.a-1,self.b-1))       #0 top left
        self.surr.append((self.a-1,self.b))         #1 top center #checkpoint
        self.surr.append((self.a-1,self.b+1))       #2 top right

        self.surr.append((self.a, self.b - 1))      #3 middle left #checkpoint
        self.surr.append((self.a, self.b))          #4 middle centre
        self.surr.append((self.a, self.b + 1))      #5 middle right #checkpoint

        self.surr.append((self.a + 1, self.b - 1))  #6 bottom left
        self.surr.append((self.a + 1, self.b))      #7 bottom center #checkpoint
        self.surr.append((self.a + 1, self.b + 1))  #8 bottom right

    def proper_move(self):
        #sprawdzamy czy idzie po sciezce
        if self.direction == "right":
            if (player.b + 1, player.a) not in game.path:
                text.draw(ramka,"Wrong move?")

    def draw(self, ramka):
        if self.direction == "":
            ramka.blit(bil.player[0], (self.pos_x, self.pos_y))
        elif self.direction == "right":
            ramka.blit(bil.player[3], (self.pos_x, self.pos_y))
        elif self.direction == "left":
            ramka.blit(bil.player[1], (self.pos_x, self.pos_y))
        elif self.direction == "up":
            ramka.blit(bil.player[2], (self.pos_x, self.pos_y))
        elif self.direction == "down":
            ramka.blit(bil.player[4], (self.pos_x, self.pos_y))

class Game:
    def __init__(self, ramka):
        pygame.init()
        self.width = 1920
        self.height = 1080
        self.ramka = ramka
        self.clock = pygame.time.Clock()
        self.path = []
        maze_solver.search(mazzecopy, player.a, player.b, self.path)
        print(maze_solver.Path)

        music = pygame.mixer.music.load('muza.mp3')  # muzyka
        pygame.mixer.music.play(-1)  # muzyka w pętli

    def draw(self):
        plate.draw(ramka)
        player.draw(ramka)

    def update(self):
        self.clock.tick(30)
        pygame.display.update()
        player.surrounding()
        ##########wydarzenia
        for event in pygame.event.get():

            if player.a == 8 and player.b == 16:  # win condition
                text.draw(ramka, "ZWYCIESTWO")
                player.surr = []
                sys.exit()
                pygame.quit()

            ###########################
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RIGHT:
                    if plate.mazze[player.a][player.b + 1] == 1 or plate.mazze[player.a][player.b + 1] == 8:
                        player.move_right()

                elif event.key == pygame.K_LEFT:
                    if plate.mazze[player.a][player.b - 1] == 1 or plate.mazze[player.a][player.b - 1] == 8:
                        player.move_left()

                elif event.key == pygame.K_UP:
                    if plate.mazze[player.a - 1][player.b] == 1 or plate.mazze[player.a - 1][player.b] == 8:
                        player.move_up()

                elif event.key == pygame.K_DOWN:
                    if plate.mazze[player.a + 1][player.b] == 1 or player.mazze[player.a + 1][player.b] == 9 or \
                            player.mazze[player.a + 1][player.b] == 8:
                        player.move_down()
                # elif event.key == pygame.K_f:
                #         player.a, player.b = player.checkpoint  # new position on board
                #         player.pos_x -= player.b * 60  # new position on screen
                #         player.pos_y -= player.a * 60
                #         player.surr = []
        else:
                player.draw(game.ramka)


player = Player(mazze)
game = Game(ramka)
plate = Plate(mazze)
text = Text()

while True:
    game.update()
    game.draw()
    # player.proper_move()

