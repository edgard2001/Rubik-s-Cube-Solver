import tkinter as tk

class HelpWindow:
    def __init__(self):
        self._LabelTexts = [
                      "U+   Turn top face (U - Up) clockwise (+)",
                      "U-   Turn top face (U - Up) anticlockwise (-)",
                      "U2   Turn top face (U - Up) twice (2)",
                      "D+   Turn bottom face (D - Down) clockwise (+)",
                      "D-   Turn bottom face (D - Down) anticlockwise (-)",
                      "D2   Turn bottom face (D - Down) twice (2)",
                      "L+   Turn left face (L - Left) clockwise (+)",
                      "L-   Turn left face (L - Left) anticlockwise (-)",
                      "L2   Turn left face (L - Left) twice (2)",
                      "R+   Turn right face (R - Right) clockwise (+)",
                      "R-   Turn right face (R - Right) anticlockwise (-)",
                      "R2   Turn right face (R - Right) twice (2)",
                      "F+   Turn front face (F - Front) clockwise (+)",
                      "F-   Turn front face (F - Front) anticlockwise (-)",
                      "F2   Turn front face (F - Front) twice (2)",
                      "B+   Turn back face (B - Back) clockwise (+)",
                      "B-   Turn back face (B - Back) anticlockwise (-)",
                      "B2   Turn back face (B - Back) twice (2)"]

    def display_window(self):
        self._Window = tk.Tk()
        self._Window.title("Notation")
        self._Window.geometry("349x467")
        self._Window.resizable(0,0)
        self.create_interface()

    def create_interface(self):
        for i in range(len(self._LabelTexts)):
            Label = tk.Label(self._Window, text = self._LabelTexts[i],\
                             font = (None, 11))
            Label.grid(row = i, column = 0, sticky = tk.W)
        ButtonBack = tk.Button(self._Window, text = "Back", bg = "#CCCCCC", fg = "#000044",\
                               font = (None, 11), width = 12, command = self.close_window)
        ButtonBack.grid(row = 18, column = 0, sticky = tk.S)
    
    def close_window(self):
        self._Window.destroy()
