import tkinter as tk
import vlc
import runpy

root = tk.Tk()
root.geometry("1200x675+150+60")
root.title("DAVE the Cutscene")
root.iconbitmap("assets/appicon.ico")
coorl = tk.Label(text="Loading...")

instance = vlc.Instance()
player = instance.media_player_new()

media = instance.media_new("assets/intro.mp4")
player.set_media(media)

player.set_hwnd(root.winfo_id())

player.play()

def closee():
    player.stop()
    root.destroy()
    runpy.run_module("scr.main")

root.after(22700, closee)

root.mainloop()