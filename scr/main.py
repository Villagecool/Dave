import pygame
from scr.sprites import thing
from scr.eztimer import ezTimer
import math
import json
import random
import runpy
import scr.results
from scr.staticProp import staticProp
pygame.init()
running = True
curTick = 0
timer = ezTimer()

stats = {"steps": 0, "cooldown": 0, "maxCooldown": 30, "shoes": 1, "stam": 30, "maxStam": 30, "money": 0, "telepee": 0, "jumpCooldown": 0, "maxJumpCooldown": 30, "dist": 0}
jsonStats = []; 
with open(("scr/globalStats.json"), "r") as file: jsonStats = json.load(file) #Open stats from json file


win = pygame.display.set_mode((16*75, 9*75))
pygame.display.set_caption("DAVE")
pygame.display.set_icon(pygame.image.load("assets/appicon.ico"))
clock = pygame.time.Clock()
sped = 25 + (jsonStats["adjLev"][1] * 2)
accel = 1
stats["maxStam"] = 25+jsonStats["adjLev"][2]*5
stats["stam"] = 25+jsonStats["adjLev"][2]*5

#Init sounds
sounds = {}

sounds["step"] = pygame.mixer.Sound('assets/step.wav')
sounds["dies"] = pygame.mixer.Sound('assets/dies.wav')
sounds["collide"] = pygame.mixer.Sound('assets/collision.wav')
sounds["jump"] = pygame.mixer.Sound('assets/boing.wav')
sounds["bomb"] = pygame.mixer.Sound('assets/explosion.wav')
sounds["enegry"] = pygame.mixer.Sound('assets/enegry.wav')
sounds["teleport"] = pygame.mixer.Sound('assets/teleport.wav')
pygame.mixer.Sound('assets/launch.wav').play() #launch sound

music = pygame.mixer.music.load('assets/FIGHTER.mp3')
pygame.mixer.music.play(-1)


def loadFrames(anim, frames, scale):
    everything = []
    for i in range(frames):
        frame = pygame.image.load('assets/'+anim+str(i+1)+'.png')
        if scale[0] > 1: everything.append(pygame.transform.scale(frame, scale))
        else: everything.append(frame)
    return everything


skyline = [
    thing(0,100,0,0, {"": [pygame.image.load('assets/skyline_b.png')]}),
    thing(2000,100,0,0, {"": [pygame.image.load('assets/skyline_b.png')]}),
    thing(0,100,0,0, {"": [pygame.image.load('assets/skyline_a.png')]}),
    thing(2000,100,0,0, {"": [pygame.image.load('assets/skyline_a.png')]})
]
sidewalk = thing(0,400,0,0, {"": [pygame.image.load('assets/sidewalk.png')]})
dave = thing(300,360,32,32,
{
    "run": loadFrames("run", 4, (64,64)),
    "sprint": loadFrames("sprint", 4, (64,64)),
    "dies": loadFrames("fall", 9, (64,64)),
    "walk": loadFrames("walk", 4, (64,64))
    }
)

effect = thing(200,225,0,0, {
    "boom": loadFrames("boom", 2, (256,256)),
    "tele": loadFrames("tele", 2, (256,256)),
    "eneg": loadFrames("eneg", 2, (256,256))
})

dave.jump = 0
streetThings = []
obst = []


stepBut = thing(1050,500,0,0, {"off": [pygame.image.load('assets/step.png')],"on": [pygame.image.load('assets/step-press.png')]})
jumpBut = thing(950,500,0,0, {"off": [pygame.image.load('assets/jump-button.png')],"on": [pygame.image.load('assets/jump-button-press.png')]})

bombb = thing(50,500,0,0, {"off": [pygame.image.load('assets/bomb-butt.png')],"on": [pygame.image.load('assets/bomb-butt-press.png')]})
telep = thing(150,500,0,0, {"off": [pygame.image.load('assets/tele-butt.png')],"on": [pygame.image.load('assets/tele-butt-press.png')]})
thirtyse = thing(250,500,0,0, {"off": [pygame.image.load('assets/30-sec-en-butt.png')],"on": [pygame.image.load('assets/30-sec-en-butt-press.png')]})

powerUps = [jumpBut, stepBut, bombb, telep, thirtyse]

bar = [pygame.image.load('assets/bar-empty.png'),pygame.image.load('assets/bar-full.png')]

def renderText(string, pos, color=(0,0,0), size=30):
    win.blit(pygame.font.Font("assets/Davium-Pixel.ttf", size).render(string, True, color), pos)

def draw():
    win.fill("#FFFFFF")

    for l in skyline + streetThings:
        l.draw(win)
    sidewalk.draw(win)
    for l in obst:
        l.draw(win)
    
    win.blit(bar[0], (450,500))
    win.blit(bar[1], (450,500), (0,0,bar[1].get_width()*(stats["stam"] / stats["maxStam"]),bar[1].get_height()))

    if (invurn % 2 == 0): dave.draw(win)
    if (effectVis > 0): effect.draw(win)
    pygame.draw.rect(win,(255,255,255), (0,0,100,9*75))
    pygame.draw.rect(win,(255,255,255), ((16*75)-100,0,100,9*75))

    if (stats["dist"] >= annoyingDist - (5+(sped*0.2))): win.blit(pygame.image.load("assets/jumpwarn.png"), (600,200))
    
    for l in powerUps:
        l.draw(win)
#Hellow world!
    win.blit(pygame.font.Font("assets/Davium-Pixel.ttf", 30).render("Dave!\nSped: "+str(math.floor(sped))+" mph", True, (0,0,0)), (100,100))
    renderText("Staminma: "+str(math.floor(stats["stam"]))+"/"+str(stats["maxStam"]), (450,480), (0,0,0), 25)
    renderText("Distance: "+str(math.floor(stats["dist"]))+"   Steps:"+str(stats["steps"]), (450,520), (0,0,0), 25)
    renderText("Cash Found: "+str(math.floor(stats["money"])), (900,100), (0,0,0), 25)

    renderText(str(jsonStats["bombs"]), (75,600), (0,0,0), 25)
    renderText(str(jsonStats["telporters"]), (175,600), (0,0,0), 25)
    renderText(str(jsonStats["enegrys"]), (275,600), (0,0,0), 25)
    pygame.display.update()

speedBasedLoop = 0
wasKeys = []
effectVis = 0
annoyingDist = 50
lastFloorDist = 1
invurn = 0
while running:
    clock.tick(27)
    curTick += 1
    timer.update(curTick)
    try: draw()
    except: break
    if dave.jump == 0 and not (effectVis > 0 and effect.curAnim == "tele"):
        accel = accel < -1 and -1 or accel - 0.05
        sped += accel
    if stats["stam"] < stats["maxStam"]: stats["stam"] += 0.1

    if sped >= 50 and dave.curAnim != "sprint": dave.setAnim("sprint")
    if sped < 50 and sped > 25 and dave.curAnim != "run": dave.setAnim("run")
    if sped <= 25 and sped > 1 and dave.curAnim != "walk": dave.setAnim("walk")

    if sped < 1: 
        if dave.curAnim != "dies": 
            dave.setAnim("dies")
            sounds["dies"].play()
            timer.after(9, curTick, pygame.quit, repeat=False)
        sped = 0
        

    if math.floor((stats["dist"]+jsonStats["totalDistance"]) / 20) > lastFloorDist:
        lastFloorDist = math.floor((stats["dist"]+jsonStats["totalDistance"]) / 20)
        stats["money"] += 1

    for thin in obst:
        if (thin.x > 200 and thin.x < 400) and invurn <= 0 and dave.jump <= 0 and not (effectVis > 0 and effect.curAnim == "tele"):
            #print("owie")
            sounds["collide"].play()
            sped = sped * 0.25
            invurn = 30
    if invurn > 0: invurn -= 1

    stats["cooldown"] -= 1
    stats["jumpCooldown"] -= 1
    effectVis -= 1
    stats["dist"] += sped*0.01

    speedBasedLoop += sped
    sidewalk.x = (sidewalk.x - sped) % -105
    skyline[0].x = (skyline[0].x - sped*0.4) % -1000
    skyline[1].x = 1000 + (skyline[1].x - sped*0.4) % -1000
    skyline[2].x = (skyline[2].x - sped*0.5) % -1000
    skyline[3].x = 1000 + (skyline[3].x - sped*0.5) % -1000

    if (speedBasedLoop > random.randint(200,400)): speedBasedLoop = 0
    
    if (math.floor(speedBasedLoop) == 0): streetThings.append(staticProp(1000,200,("building/"+str(random.randint(1,6)))))
    if (stats["dist"] >= annoyingDist):
        obst.append(staticProp(1000,275,(random.choice(["homeless-guy", "hole", "cone"]))))
        annoyingDist += (random.randint(25,100) + (sped*random.uniform(0.01,0.05)))
    for th in streetThings + obst:
        th.x -= sped
        try:
            if (th.x < -200): streetThings.remove(th)
        except:
            if (th.x < -200): obst.remove(th)


    keys = pygame.key.get_pressed()
    for e in pygame.event.get(): 
        if (e.type == pygame.QUIT): running = False; pygame.quit()

    for l in powerUps:
        l.setAnim("off") #resets all the buttons
    #Step button
    if keys[pygame.K_SPACE] and stats["stam"] >= 1 and stats["cooldown"] < 1 and sped > 0:
        sounds["step"].play()
        sped += 1 + (jsonStats["adjLev"][0] / 10)
        accel = 0.1
        stats["stam"] += -5
        stats["steps"] += 1
        stats["cooldown"] = 3
        stepBut.setAnim("on")
        
    if (dave.jump > 0): #jump animation
        dave.y = 360 + [0,-9.5,-18,-25.5,-32,-37.5,-42,-45.5,-48,-49.5,-50,-49.5,-48,-45.5,-42,-37.5,-32,-25.5,-18,-9.5][math.floor(dave.jump)-1]*2
        dave.jump -= 1
    #Jump button
    if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] or keys[pygame.K_LCTRL] or keys[pygame.K_UP]) and sped > 0 and stats["jumpCooldown"] < 1:
        sounds["jump"].play()
        dave.jump = 20
        stats["stam"] += -15
        jumpBut.setAnim("on")
        stats["jumpCooldown"] = stats["maxJumpCooldown"]
    #Bomb
    if (keys[pygame.K_z] and not wasKeys[pygame.K_z]) and jsonStats["bombs"] > 0 and effectVis <= 5:
        bombb.setAnim("on")
        jsonStats["bombs"] -= 1
        sped += 20
        effectVis = 10
        effect.setAnim("boom")
        sounds["bomb"].play()
    #Teleport
    if (keys[pygame.K_x] and not wasKeys[pygame.K_x]) and jsonStats["telporters"] > 0 and effectVis <= 5:
        telep.setAnim("on")
        jsonStats["telporters"] -= 1
        effectVis = 60
        effect.setAnim("tele")
        sounds["teleport"].play()
    #30 second enegry
    if (keys[pygame.K_c] and not wasKeys[pygame.K_c]) and jsonStats["enegrys"] > 0 and effectVis <= 5:
        thirtyse.setAnim("on")
        jsonStats["enegrys"] -= 1
        effectVis = 10
        effect.setAnim("eneg")
        stats["stam"] += 30
        sounds["enegry"].play()


    wasKeys = keys

#Total stats saves
jsonStats["totalSteps"] += stats["steps"]
jsonStats["totalDistance"] += math.floor(stats["dist"])
if math.floor(stats["dist"]) > jsonStats["recordDist"]: jsonStats["recordDist"] = math.floor(stats["dist"])
jsonStats["money"] += math.floor(stats["money"])

# Dumps the updated JSON data to the file
with open(("scr/globalStats.json"), "w") as file: json.dump(jsonStats, file)
print("You Died!")


if scr.results.showResults(jsonStats, math.floor(stats["dist"]), stats["steps"], math.floor(stats["money"])):
    runpy.run_module("scr.shop")