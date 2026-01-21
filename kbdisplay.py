#!/usr/bin/env python3
"""
A basic keyboard display for wayland that
allows inputs to be shown even when out of focus
"""
import subprocess, json, sys
import tkinter as tk


class Application(tk.Frame):
    def __init__(self, layout, master=None):
        self.background_color = "#000066"
        self.buttons = {}
        self.bg_press = {}
        self.bg_rel = {}

        if "background" in layout:
            self.background_color = layout["background"]

        tk.Frame.__init__(self, master, width=layout["width"], height=layout["height"])
        self["bg"] = self.background_color
        self.pack()
        self.create_widgets(layout)
        self.update()
        proc = subprocess.Popen(["sudo", "showmethekey-cli"], stdout=subprocess.PIPE)

        inkeypressevent = False
        inkeyrelevent = False

        while True:
            line = json.loads(proc.stdout.readline())
            if not line:
                continue
            if line["state_name"] == "PRESSED":
                inkeypressevent = True
            elif line["state_name"] == "RELEASED":
                inkeyrelevent = True
            if inkeypressevent or inkeyrelevent:
                code = int(line["key_code"])

                # button was not defined in layout
                if not code in self.buttons:
                    continue

                # update key image
                if inkeypressevent:
                    self.buttons[code]["image"] = self.bg_press[code]
                elif inkeyrelevent:
                    self.buttons[code]["image"] = self.bg_rel[code]
            inkeypressevent = inkeyrelevent = False
            self.update()

    def create_widgets(self, layout):
        default_press = (
            tk.PhotoImage(file=layout["pressed"]) if "pressed" in layout else None
        )
        default_rel = (
            tk.PhotoImage(file=layout["unpressed"]) if "unpressed" in layout else None
        )
        for button in layout["buttons"]:
            code = button["keycode"]

            img_press = (
                tk.PhotoImage(file=button["pressed"])
                if "pressed" in button
                else default_press
            )
            img_rel = (
                tk.PhotoImage(file=button["unpressed"])
                if "unpressed" in button
                else default_rel
            )

            # button parameters
            w, h, x, y = button["width"], button["height"], button["x"], button["y"]

            # button widget
            btn = tk.Label()
            btn.place(width=w, height=h, x=x, y=y)
            btn["bg"] = self.background_color
            btn["image"] = img_rel
            btn["text"] = button["text"]
            btn["font"] = ("Roboto Mono", 14)
            btn["fg"] = "black"
            btn["compound"] = "center"

            self.buttons[code] = btn
            self.bg_press[code] = img_press
            self.bg_rel[code] = img_rel


def main():
    def close():
        print("closing")
        root.destroy()

    try:
        layout = json.load(open(sys.argv[1]))
    except Exception as e:
        print("no layout file supplied", file=sys.stderr)
        print(e, file=sys.stderr)
        return 1

    root = tk.Tk()
    app = Application(layout, master=root)
    root.protocol("WM_DELETE_WINDOW", app.on_delete)

    return 0


if __name__ == "__main__":
    exit(main())
