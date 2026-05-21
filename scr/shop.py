import pygame
from scr.sprites import thing
from scr.eztimer import ezTimer
import math
import json
import random
import runpy
from scr.staticProp import staticProp
pygame.init()
running = True

jsonStats = []; 
with open(("scr/globalStats.json"), "r") as file: jsonStats = json.load(file) #Open stats from json file

#jsonStats["adjLev"] = [shoes, chair, coffee]
win = pygame.display.set_mode((9*75, 9*75))
pygame.display.set_caption("DAVE Shop")
pygame.display.set_icon(pygame.image.load("assets/appicon.ico"))
clock = pygame.time.Clock()

#Init sounds
sounds = {}

sounds["buy"] = pygame.mixer.Sound('assets/upgrade.wav')
sounds["enter"] = pygame.mixer.Sound('assets/ShopDoorBell.mp3')
sounds["click"] = pygame.mixer.Sound('assets/blipSelect.wav')
sounds["poor"] = pygame.mixer.Sound('assets/pause.wav')

music = pygame.mixer.music.load('assets/Cubby-Disorientated.mp3')
pygame.mixer.music.play(-1)


def loadFrames(anim, frames, scale):
    everything = []
    for i in range(frames):
        frame = pygame.image.load('assets/'+anim+str(i+1)+'.png')
        if scale[0] > 1: everything.append(pygame.transform.scale(frame, scale))
        else: everything.append(frame)
    return everything

bombb = thing(50,50,0,0, {"off": [pygame.image.load('assets/bomb-butt.png')],"on": [pygame.image.load('assets/bomb-butt-press.png')]})
telep = thing(50,150,0,0, {"off": [pygame.image.load('assets/tele-butt.png')],"on": [pygame.image.load('assets/tele-butt-press.png')]})
thirtyse = thing(50,250,0,0, {"off": [pygame.image.load('assets/30-sec-en-butt.png')],"on": [pygame.image.load('assets/30-sec-en-butt-press.png')]})
shoes = thing(50,350,0,0, {"off": [pygame.image.load('assets/shoes-butt.png')],"on": [pygame.image.load('assets/shoes-butt-press.png')]})
recliner = thing(50,450,0,0, {"off": [pygame.image.load('assets/recliner-butt.png')],"on": [pygame.image.load('assets/recliner-butt-press.png')]})
coff = thing(50,550,0,0, {"off": [pygame.image.load('assets/coffee-butt.png')],"on": [pygame.image.load('assets/coffee-butt-press.png')]})
upgrades = thing(325,550,0,0, {"off": [pygame.image.load('assets/upgrades.png')],"on": [pygame.image.load('assets/upgrades-press.png')]})

powerUps = [bombb, telep, thirtyse, shoes, recliner, coff]
statsInOrder = ["bombs", "telporters", "enegrys", "shoes", "chair", "coffee"]
prices = [0,0,0,0,0,0]
titles = ["Bomb", "Teleporter", "30 Second Enegry", "Shoes", "Recliner", "Coffee"]
explan = ["Blast yourself forward!\nSingle use item", "Teleporters will breifly\ndo the walking for you!\nSingle use item", "Give yourself the boost\nof enegry you need!\nSingel use item", "Get better shoes to\nwalk faster!", "Upgrade your recliner\nto have better launch\npower!", "Increase your caffine\ndosage to have more\nstamania!"]

def renderText(string, pos, color=(0,0,0), size=30):
    win.blit(pygame.font.Font("assets/Davium-Pixel.ttf", size).render(string, True, color), pos)

def draw():
    win.fill("#FFFFFF")

    for l in powerUps:
        l.draw(win)
    upgrades.draw(win)
    renderText("Press ENTER to Launch!", (425,10), (0,0,0), 20)
    renderText("Arrow keys to move up/down or LR to change a powerup\n   SPACE to buy", (275,30), (0,0,0), 15)
    renderText(str(jsonStats["bombs"]) + " Owned", (150,75), (0,0,0), 25)
    renderText(str(jsonStats["telporters"]) + " Owned", (150,175), (0,0,0), 25)
    renderText(str(jsonStats["enegrys"]) + " Owned", (150,275), (0,0,0), 25)
    renderText("Level " + str(jsonStats["adjLev"][0]) + "/" + str(jsonStats["shoes"]), (150,375), (0,0,0), 25)
    renderText("Level " + str(jsonStats["adjLev"][1]) + "/" + str(jsonStats["chair"]), (150,475), (0,0,0), 25)
    renderText("Level " + str(jsonStats["adjLev"][2]) + "/" + str(jsonStats["coffee"]), (150,575), (0,0,0), 25)

    renderText("Money: " +str(jsonStats["money"]), (20,10), (0,0,0), 35)
    renderText("Costs " +str(prices[curSelected]) + " money", (350,510), (0,0,0), 35)
    win.blit(pygame.image.load("assets/"+ ["bomb", "teleport", "30sec", "shoes", "recliner", "coffee"][curSelected] +"-card.png"), (350,50))
    renderText(titles[curSelected], (450-len(titles[curSelected])*7,390), (0,0,0), 35)
    renderText(explan[curSelected], (360,425), (0,0,0), 20)
    pygame.display.update()

wasKeys = []
curSelected = 0
holdingKey = [0,0]

while running:
    clock.tick(27)
    prices = [9,13,7, 5 + 5*jsonStats["shoes"], 10 + 5*jsonStats["chair"], 5+3*jsonStats["coffee"]]

    keys = pygame.key.get_pressed()
    for e in pygame.event.get(): 
        if (e.type == pygame.QUIT): 
            running = False; 
            with open(("scr/globalStats.json"), "w") as file: json.dump(jsonStats, file)
            pygame.quit()

    for l in powerUps:
         #resets all the buttons
        if powerUps.index(l) == curSelected:
            l.setAnim("off")
        else:
            l.setAnim("on")
    upgrades.setAnim("off")
        
    if (keys[pygame.K_DOWN] and not wasKeys[pygame.K_DOWN]):
        sounds["click"].play()
        curSelected = (curSelected + 1) % 6
    if (keys[pygame.K_UP] and not wasKeys[pygame.K_UP]):
        sounds["click"].play()
        curSelected = (curSelected - 1) % 6
    if (keys[pygame.K_SPACE] and not wasKeys[pygame.K_SPACE]):
        upgrades.setAnim("on")
        if (jsonStats["money"] >= prices[curSelected]):
            sounds["buy"].play()
            jsonStats[statsInOrder[curSelected]] += 1
            if (curSelected >= 3): 
                jsonStats["adjLev"][curSelected-3] += 1
            jsonStats["money"] -= prices[curSelected]
        else:
            sounds["poor"].play()


    if (keys[pygame.K_LEFT] and not (holdingKey[0] < 10 and holdingKey[0] > 0)) and curSelected >= 3 and jsonStats["adjLev"][curSelected-3] > 1:
        sounds["click"].play()
        jsonStats["adjLev"][curSelected-3] -= 1
    if (keys[pygame.K_RIGHT] and not (holdingKey[1] < 10 and holdingKey[1] > 0)) and curSelected >= 3 and jsonStats["adjLev"][curSelected-3] < jsonStats[statsInOrder[curSelected]]:
        sounds["click"].play()
        jsonStats["adjLev"][curSelected-3] += 1


    if keys[pygame.K_RIGHT]: holdingKey[1] += 1
    else: holdingKey[1] = 0
    if keys[pygame.K_LEFT]: holdingKey[0] += 1
    else: holdingKey[0] = 0


    if (keys[pygame.K_RETURN] and not wasKeys[pygame.K_RETURN]):
        running = False
        with open(("scr/globalStats.json"), "w") as file: json.dump(jsonStats, file)
        pygame.quit()
        runpy.run_module("scr.main")

    wasKeys = keys
    try: draw()
    except: print("")
    

# Dumps the updated JSON data to the file
#with open(("globalStats.json"), "w") as file: json.dump(jsonStats, file)
print("Shop Closed")