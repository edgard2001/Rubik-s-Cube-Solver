import tkinter as tk

class ControlsWindow:
    def __init__(self):
        self._LabelTexts = [
                      "LSHIFT - reverse turn direction (hold)",
                      "C - reset cube",
                      "Q - scramble cube",
                      "V - solve cube (use X to apply solution)",
                      "Z - toggle undo move",
                      "X - toggle redo move",
                      "LCTRL + Z - single undo move ",
                      "LCTRL + X - single redo move ",
                      "SPACE - Pause",
                      "U - turn up layer clockwise",
                      "D - turn down layer clockwise",
                      "L - turn left layer clockwise",
                      "R - turn right layer clockwise",
                      "F - turn front layer clockwise",
                      "B - turn back layer clockwise",
                      "M - turn miidle layer clockwise",
                      "E - turn equatorial layer clockwise",
                      "S - turn standing layer clockwise",
                      "Numpad 4 - rotate cube left",
                      "Numpad 5 - rotate cube down",
                      "Numpad 6 - rotate cube right",
                      "Numpad 7 - roll cube left",
                      "Numpad 8 - rotate cube up",
                      "Numpad 9 - roll cube right",
		      "Left Mouse Button - press on",
		      "the cube and drag to turn",
		      "faces of the cube or press",
		      "outside of the cube and drag",
                      "to rotate the entire cube"]

    def display_window(self):
        self._Window = tk.Tk()
        self._Window.title("Controls")
        self._Window.geometry("485x435")
        self._Window.resizable(0,0)
        self.create_interface()

    def create_interface(self):
        for i in range(len(self._LabelTexts)):
            Row = i % 18
            Column = i // 18
            Label = tk.Label(self._Window, text = self._LabelTexts[i],\
                             font = (None, 11))
            Label.grid(row = Row, column = Column, sticky = tk.W)
        ButtonBack = tk.Button(self._Window, text = "Back", bg = "#CCCCCC", fg = "#000044",\
                               font = (None, 11), width = 12, command = self.close_window)
        ButtonBack.grid(row = 16, column = 1, rowspan = 2, sticky = tk.SE)
    
    def close_window(self):
        self._Window.destroy()
