import pygame
class ezTimer:
    def __init__(self):
        self.tasks = []

    def after(self, delay_ms, now, callback, repeat=False):
        print("doing thing after",delay_ms,"ticks!")
        self.tasks.append({
            "delay": delay_ms,
            "time": now + delay_ms,
            "callback": callback,
            "repeat": repeat
    })

    def update(self, now):

        for task in self.tasks[:]:
            if now >= task["time"]:
                task["callback"]()

                if task["repeat"]:
                    task["time"] = now + task["delay"]
                else:
                    self.tasks.remove(task)