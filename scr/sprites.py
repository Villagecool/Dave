import random
import math
import pygame

class thing(object):
    #walkRight = [pygame.image.load('assets/R1E.png'), pygame.image.load('assets/R2E.png'), pygame.image.load('assets/R3E.png'), pygame.image.load('assets/R4E.png'), pygame.image.load('assets/R5E.png'), pygame.image.load('assets/R6E.png'), pygame.image.load('assets/R7E.png'), pygame.image.load('assets/R8E.png'), pygame.image.load('assets/R9E.png'), pygame.image.load('assets/R10E.png'), pygame.image.load('assets/R11E.png')]
    #walkLeft = [pygame.image.load('assets/L1E.png'), pygame.image.load('assets/L2E.png'), pygame.image.load('assets/L3E.png'), pygame.image.load('assets/L4E.png'), pygame.image.load('assets/L5E.png'), pygame.image.load('assets/L6E.png'), pygame.image.load('assets/L7E.png'), pygame.image.load('assets/L8E.png'), pygame.image.load('assets/L9E.png'), pygame.image.load('assets/L10E.png'), pygame.image.load('assets/L11E.png')]
    
    def __init__(self, x, y, width, height, anims):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.anims = anims #{"run": [pygame.image.load('path')], "walk": [pygame.yeah.you.get.the.point]}
        self.frames = list(anims.values())[0]
        self.frame = [0, len(self.frames)]
        self.curAnim = anims.values()
        self.visible = True
        self.hitbox = (1,1,1,1)

    def setAnim(self, anim):
        self.frames = self.anims[anim]
        self.frame = [0, len(self.frames)]
        self.curAnim = anim
        
    def draw(self, win):
        if not self.visible: return
        self.frame[0] = (self.frame[0] + 1) % self.frame[1]
        win.blit(self.frames[self.frame[0]], (self.x,self.y))
        self.hitbox = (self.x, self.y, self.width, self.height)

    def moveVec(self, steps, angle):
        self.x += math.cos(math.radians(angle)) * steps
        self.y += math.sin(math.radians(angle)) * steps
        
    def move(self, x, y):
        self.x += x
        self.y += y
        
    def moveTo(self, x, y):
        self.x = x
        self.y = y