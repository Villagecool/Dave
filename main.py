import runpy
import json
jsonStats = []; 
with open(("scr/globalStats.json"), "r") as file: jsonStats = json.load(file) #Open stats from json file

if (jsonStats["totalDistance"] < 1): runpy.run_module("scr.cutscene")
else: runpy.run_module("scr.shop")