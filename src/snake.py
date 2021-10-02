from os import environ
if 'PYGAME_HIDE_SUPPORT_PROMPT' not in environ:
    environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hidden'
del environ
import pygame
from pygame import Surface
from random import randint
from typing import Tuple


class Apple:
    def __init__(self, xmax:int, ymax:int, x:int=0, y:int=0, size:int=1):
        self.x = x
        self.y = y
        self.size = size
        self.xmax = xmax
        self.ymax = ymax
    def choosePosition(self, snake:int):
        get_number = lambda max_value: randint(0, max_value) * self.size
        x = get_number(self.xmax)
        y = get_number(self.ymax)
        while snake.colideBodyWithPoint((x,y)):
            x = get_number(self.xmax)
            y = get_number(self.ymax)
        self.x = x
        self.y = y

    def draw(self, screen:Surface, offsetx:int=0,offsety:int=0):
        (x,y) = (self.x + offsetx, self.y + offsety)
        pygame.draw.rect(screen, (0), (x, y, self.size, self.size), 1)
        pygame.draw.rect(screen, (0x0) , (x + 2, y + 2, self.size - 4, self.size - 4), 1)
        pygame.draw.rect(screen, (0x990000), (x + 3,y + 3, self.size - 6,self.size - 6))

    def __str__(self):
        return f'Apple:({self.x}, {self.y})'

class Snake:
    def __init__(self, x:int=0, y:int=0, xmax:int=25, ymax:int=25, size:int=1):
        self.x = x
        self.y = y
        self.dir = 'right'
        self.body = [(x,y)]
        self.xmax = xmax
        self.ymax = ymax
        self.size = size

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.dir = 'right'
        self.body = [(x,y)]

    def getIncrement(self):
        (x,y) = (0,0)
        if self.dir in ['up','w']:
            y = -self.size
        elif self.dir in ['down','z']:
            y = self.size
        elif self.dir in ['right','s']:
            x = self.size
        else:
            x = -self.size
        return (x, y)

    def nextPosition(self):

        (x,y) = self.getIncrement()
        next_x = self.x + x
        next_y = self.y + y
            
        if next_x > self.xmax:
            next_x = 0
        elif next_x < 0:
            next_x = self.xmax
        if next_y > self.ymax:
            next_y = 0
        elif next_y < 0:
            next_y = self.ymax
        return (next_x, next_y)
        
    def move(self):
        pos = self.nextPosition()
        self.body.pop()
        self.body.insert(0, pos)
        self.x,self.y = pos
        
    def colideBody(self):
        return self.nextPosition() in self.body[1:]
        
    def colideApple(self, apple:Apple):
        (x, y) = self.nextPosition()
        return x == apple.x and y == apple.y

    def colideBodyWithPoint(self, point: Tuple[int,int]):
        return point in self.body

    def increaseSize(self):
        x,y = self.nextPosition()
        self.x = x
        self.y = y
        self.body.insert(0, (self.x, self.y))
        
    def draw(self, screen:Surface, offsetx:int=0, offsety:int=0):
        head = True
        for body in self.body:
            (x,y) = body
            x += offsetx
            y += offsety
            pygame.draw.rect(screen, (0), (x, y, self.size, self.size), 1)
            pygame.draw.rect(screen, (0), (x + 2, y + 2, self.size - 4, self.size - 4))
            if head:
                pygame.draw.rect(screen, (0x008800), (x + 1, y + 1, self.size - 2, self.size - 2),1)
                head = False