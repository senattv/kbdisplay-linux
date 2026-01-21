#!/usr/bin/env python3
import subprocess, json, sys
import tkinter as tk

try:
    layout = json.load(open(sys.argv[1]))
except Exception as e:
    print('no layout file supplied', file=sys.stderr)
    print(e)
    exit(1)

buttons = {}
bg_press = {}
bg_rel = {}
BACKGROUND_COLOR = '#000066'
if "background" in layout:
    BACKGROUND_COLOR = layout["background"]

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master,
                          width=layout['width'],
                          height=layout['height'])
        self['bg'] = BACKGROUND_COLOR
        self.pack()
        self.create_widgets()
        self.update()
        proc = subprocess.Popen(['sudo', 'showmethekey-cli'],
                        stdout=subprocess.PIPE)

        inkeypressevent = False
        inkeyrelevent = False

        while True:
            line = json.loads(proc.stdout.readline())
            if line:
                if line['state_name'] == "PRESSED":
                    inkeypressevent = True
                elif line['state_name'] == "RELEASED":
                    inkeyrelevent = True
            if inkeypressevent or inkeyrelevent:
                code = int(line['key_code'])
                try:
                    if inkeypressevent:
                        buttons[code]['image'] = bg_press[code]
                    elif inkeyrelevent:
                        buttons[code]['image'] = bg_rel[code]
                except KeyError:
                    pass
            inkeypressevent = False
            inkeyrelevent = False
            self.update()


    def create_widgets(self):
        default_press = tk.PhotoImage(file=layout['pressed']) if 'pressed' in layout else None
        default_rel = tk.PhotoImage(file=layout['unpressed']) if 'unpressed' in layout else None
        for button in layout['buttons']:
            code = button['keycode']

            # background image
            img_press = tk.PhotoImage(file=button['pressed']) if 'pressed' in button else default_press
            img_rel = tk.PhotoImage(file=button['unpressed']) if 'unpressed' in button else default_rel

            # button parameters
            w, h, x, y = button['width'], button['height'], button['x'], button['y']

            # button widget
            btn = tk.Label()
            btn.place(width=w, height=h, x=x, y=y)
            btn['bg'] = BACKGROUND_COLOR
            btn['image'] = img_rel
            btn['text'] = button['text']
            btn['font'] = ('Roboto Mono', 14)
            btn['fg'] = 'black'
            btn['compound'] = 'center'

            buttons[code] = btn
            bg_press[code] = img_press
            bg_rel[code] = img_rel


root = tk.Tk()
root.wm_attributes('-alpha', 0.0)
app = Application(master=root)
