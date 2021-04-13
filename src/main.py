from os import environ
if 'PYGAME_HIDE_SUPPORT_PROMPT' not in environ:
    environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hidden'
del environ
import pygame
from snake import Snake, Apple
from os.path import normpath
import json
class Game:
    def __init__(self):
        self.config()
    def config(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        self.SCREEN_W = 500
        self.SCREEN_H = 500
        pygame.display.set_caption('SnakeGame v0.1')
        self.display = pygame.display.set_mode((self.SCREEN_W,self.SCREEN_H))
        self.background = None
        self.clock = pygame.time.Clock()
        self.score = 0
        self.max_score = self.loadScore()
        self.openSoundConfig()

    def backgroundInit(self, xmax, ymax, size):
        self.background = pygame.Surface((xmax*size,ymax*size))
        self.background.fill((120,120,120))
        for i in range(xmax+1):
            for j in range(ymax+1):
                pygame.draw.rect(self.background, (142,142,142), (i*size+1,j*size+1,size-2,size-2),1)
                pygame.draw.rect(self.background, (142,142,142), (i*size+4,j*size+4,size-8,size-8))
        pygame.draw.rect(self.background, (0), (0,(j+1)*size,(xmax+1)*size,80))

    def runLoop(self):
        
        def updateTextScore():
            text_score = font.render(f'score: {self.score}', True, (255,255,255))
            text_max_score = font.render(f'max score: {self.max_score}', True, (255,255,255))
            return text_score,text_max_score
        FPS = 2
        FPS_ACCUMULATOR = FPS
        FPS_INCREMENT = 0.125
        SIZE = 20
        XMAX, YMAX = 23,20
        OFFSETX = SIZE
        OFFSETY = SIZE*4
        RECT_SCORE = (0,0,500,80)

        ticks = 0
        game = True
        game_quit = False
        key_pressed = False
        self.score = 0
        valid_keys = ['left','right','down','up']

        snake = Snake(0,0,440,380,size=SIZE)
        apple = Apple(XMAX-1,YMAX-1,size=SIZE)
        apple.choosePosition(snake)

        self.backgroundInit(XMAX,YMAX,SIZE)
        font = pygame.font.SysFont('Verdana', 20)
        font.set_bold(True)
        
        (text_score,text_max_score) = updateTextScore()
        while game:
            self.clock.tick(FPS)
            FPS = FPS_ACCUMULATOR
            self.display.blit(self.background,(OFFSETX,OFFSETY))

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    game = False
                    game_quit = True
                    break
                elif e.type == pygame.KEYDOWN:
                    key = pygame.key.name(e.key)
                    if key == 'escape':
                        game = False
                        game_quit = True
                        break
                    elif key in valid_keys:
                        ticks = pygame.time.get_ticks()
                        key_pressed = True
                        snake.dir = key
                elif e.type == pygame.KEYUP:
                    key_pressed = False

            if key_pressed and (pygame.time.get_ticks()-ticks)>50:
                FPS = FPS_ACCUMULATOR+30

            if game:

                if snake.colideBody():

                    self.playGameOverSound()
                    self.max_score = self.saveScore()
                    game = self.gameOver()
                    if not game:
                        break
                    self.score = 0
                    FPS = 2
                    snake.reset(0,0)
                    apple.choosePosition(snake)
                    (text_score,text_max_score) = updateTextScore()
                    continue

                if snake.colideApple(apple):
                    FPS_ACCUMULATOR+=FPS_INCREMENT
                    self.playAppleSound()
                    snake.increaseSize()
                    apple.choosePosition(snake)
                    self.score += 10
                    if self.score>self.max_score:
                        self.max_score = self.score
                    (text_score,text_max_score) = updateTextScore()
                else:
                    snake.move()
                pygame.draw.rect(self.display, (0),RECT_SCORE)
                snake.draw(self.display,OFFSETX,OFFSETY)
                apple.draw(self.display,OFFSETX,OFFSETY)
                self.display.blit(text_max_score,(20,10))
                self.display.blit(text_score,(78,40))
                pygame.display.flip()

        self.quitGame()

    def gameOver(self):
        font = pygame.font.SysFont('Arial black', 60)
        font.set_bold(True)
        text = font.render('GAME OVER', True, (255,255,255))

        info = pygame.font.SysFont('default', 25)
        info.set_bold(True)
        text_info = info.render('press Enter to continue or ESC to quit.', True, (255,255,255))

        game = True
        next_game = False
        ticks = 0
        while game:
            ticks += self.clock.tick(30)
            
            self.display.fill((0))

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    game = False
                    break
                elif e.type == pygame.KEYDOWN:
                    key = pygame.key.name(e.key)
                    if key == 'escape':
                        game = False
                        break
                    elif key == 'return':
                        next_game = True
                        game = False
                        break
            if game:

                if 300<ticks<600:
                    self.display.blit(text,(20,180))
                if ticks>600:
                    ticks=0
                self.display.blit(text_info,(70,420))
                pygame.display.flip()
        return next_game
    def quitGame(self):
        pygame.quit()
    def loadScore(self):
        try:
            file = open('score.txt')
        except FileNotFoundError:
            with open('score.txt','w') as file:
                for _ in range(5):
                    file.write('0\n')
            file = open('score.txt')
        with file:
            max_score = file.readline().strip()
        return int(max_score)
    def saveScore(self):
        scores = []
        with open('score.txt') as file:
            for _ in range(5):
                scores += [int(file.readline().strip())]
        with open('score.txt','w') as file:
            scores += [self.score]
            scores.sort(reverse=True)
            scores.pop()
            self.max_score = scores[0]
            for score in scores:
                file.writelines(f'{score}\n')
        return self.max_score
    def playAppleSound(self):
        if self.effect is not None:
            self.effect.play()
    def playGameOverSound(self):
        if self.game_over is not None:
            self.game_over.play()
    def openSoundConfig(self):
        self.effect = None
        self.game_over = None
        try:
            with open('sound.json','r') as file:
                data = json.load(file)
                path = data['music'].strip()
                if path!="":
                    pygame.mixer.music.load(normpath(path))
                    pygame.mixer.music.play(-1)
                path = data['apple'].strip()
                if path!="":
                    self.effect = pygame.mixer.Sound(normpath(path))
                path = data['game-over'].strip()
                if path!="":
                    self.game_over = pygame.mixer.Sound(normpath(path))
        except:
            pygame.mixer.music.stop()
            self.effect = None
            self.game_over = None

game = Game()
game.runLoop()
