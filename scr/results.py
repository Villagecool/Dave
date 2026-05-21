import pygame
from scr.sprites import thing
from scr.eztimer import ezTimer
import math
import json
import random
import runpy
from playsound3 import playsound
from scr.staticProp import staticProp
def lerp(start, end, t): 
    return start * (1 - t) + end * t
def renderText(win,string, pos, color=(0,0,0), size=30):
    win.blit(pygame.font.Font("assets/Davium-Pixel.ttf", size).render(string, True, color), pos)

def showResults(json,dist,steps,money):
    pygame.init()
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((9*75, 6*75))
    pygame.display.set_caption("DAVE Results")
    pygame.display.set_icon(pygame.image.load("assets/appicon.ico"))
    run = True
    textx = 9*75
    davex = -200
    face = random.randint(1,5)
    shop = thing(450,300,0,0, {"off": [pygame.image.load('assets/toshop.png')],"on": [pygame.image.load('assets/toshop-press.png')]})
    quitt = thing(100,300,0,0, {"off": [pygame.image.load('assets/quit.png')],"on": [pygame.image.load('assets/quit-press.png')]})
    
    while run:
        keys = pygame.key.get_pressed()
        win.fill("#FFFFFF")
        textx = lerp(textx, 300, 0.2)
        davex = lerp(davex, 50, 0.2)
        win.blit(pygame.image.load("assets/dave-res/"+ str(face) +".png"), (davex,50))
        renderText(win,"Distance Traveled: "+str(dist)+"\nRecord Distance: "+str(json["recordDist"])+(json["recordDist"] == dist and " (NEW!)" or "")+"\n\nSteps Taken: "+str(steps)+"\n\nMoney Earned: "+str(money), (textx,100), (0,0,0), 25)
        shop.draw(win)
        quitt.draw(win)
        pygame.display.update()
        clock.tick(27)
        for e in pygame.event.get(): 
            if (e.type == pygame.QUIT): run = False; pygame.quit()
            if (keys[pygame.K_RIGHT] or keys[pygame.K_RETURN]):
                shop.setAnim("on")
                playsound("assets/ShopDoorBell.mp3", block=False)
                pygame.draw.rect(win,(255,255,255), (shop.x,shop.y,200,200))
                shop.draw(win)
                pygame.display.update()
                run = False
                pygame.quit()
                return True
            elif (keys[pygame.K_LEFT] or keys[pygame.K_ESCAPE] or keys[pygame.K_BACKSPACE]):
                run = False
                quitt.setAnim("on")
                pygame.draw.rect(win,(255,255,255), (quitt.x,quitt.y,200,200))
                quitt.draw(win)
                pygame.display.update()
                pygame.quit()
                return False
            elif (keys[pygame.K_SPACE]):
                run = False
                pygame.quit()
                runpy.run_module("scr.main")
                return False
        
#print(showResults({"recordDist":1},0,0,0))