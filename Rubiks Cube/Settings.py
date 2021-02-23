import tkinter as tk

class SettingsWindow:
    def __init__(self, Values):
        self._SliderLabelTexts = ["Top Red",
                                  "Top Green",
                                  "Top Blue",
                                  "Left Red",
                                  "Left Green",
                                  "Left Blue",
                                  "Front Red",
                                  "Front Green",
                                  "Front Blue",
                                  "Right Red",
                                  "Right Green",
                                  "Right Blue",
                                  "Bottom Red",
                                  "Bottom Green",
                                  "Bottom Blue",
                                  "Back Red",
                                  "Back Green",
                                  "Back Blue",
                                  "Inside Red",
                                  "Inside Green",
                                  "Inside Blue",
                                  "Background Red",
                                  "Background Green",
                                  "Background Blue",
                                  "Cube Rotation Speed",
                                  "Layer Rotation Speed"]
        self._SliderValues = Values
        self._DefaultSliderValues = [255,255,255,
                                     0,128,0,
                                     178,0,0,
                                     0,0,178,
                                     230,205,0,
                                     230,78,0,
                                     0,0,0,
                                     178,178,178,
                                     6,18]

    def display_window(self):
        self._Window = tk.Tk()
        self._Window.title("Settings")
        self._Window.geometry("780x420")
        self._Window.resizable(0,0)
        self.create_interface()
        while True:
            try:
                self.save_changes()
                self.change_button_colours()
                self._Window.update()
            except:
                break

    def create_interface(self):
        self._Sliders = []
        for i in range(len(self._SliderValues)-2):
            Row = (i % 6)*2
            Column = (i // 6)
            ColourLabel = tk.Label(self._Window, text = self._SliderLabelTexts[i])
            ColourLabel.grid(row = Row, column = Column, sticky = tk.W)
            Slider = tk.Scale(self._Window, from_ = 0, to = 255, orient = tk.HORIZONTAL, length = 150, width = 10)
            Slider.set(self._SliderValues[i])
            Slider.grid(row = Row + 1, column = Column, sticky = tk.W)
            self._Sliders.append(Slider)
        Row = (24 % 6)*2
        Column = (24 // 6)
        ColourLabel = tk.Label(self._Window, text = self._SliderLabelTexts[24])
        ColourLabel.grid(row = Row, column = Column, sticky = tk.W)
        Slider = tk.Scale(self._Window, from_ = 1, to = 15, orient = tk.HORIZONTAL, length = 150, width = 10)
        Slider.set(self._SliderValues[24])
        Slider.grid(row = Row + 1, column = Column, sticky = tk.W)
        self._Sliders.append(Slider)
        Row = (25 % 6)*2
        Column = (25 // 6)
        ColourLabel = tk.Label(self._Window, text = self._SliderLabelTexts[25])
        ColourLabel.grid(row = Row, column = Column, sticky = tk.W)
        Slider = tk.Scale(self._Window, from_ = 1, to = 100, orient = tk.HORIZONTAL, length = 150, width = 10)
        Slider.set(self._SliderValues[25])
        Slider.grid(row = Row + 1, column = Column, sticky = tk.W)
        self._Sliders.append(Slider)
            
        self._ColouredTileButtons = []
        for i in range(0,len(self._SliderValues)-2,3):
            Row = (i % 6)*2
            Column = (i // 6)
            RedAmount = self._SliderValues[i]
            GreenAmount = self._SliderValues[i+1]
            BlueAmount = self._SliderValues[i+2]
            RedHex = self.den_to_hex(RedAmount)
            GreenAmount = self.den_to_hex(GreenAmount)
            BlueAmount = self.den_to_hex(BlueAmount)
            Colour = "#"+RedHex+GreenAmount+BlueAmount
            ColouredTile = tk.Button(self._Window, width = 3, height = 1, bg = Colour)
            ColouredTile.grid(row = Row, column = Column, sticky = tk.E)
            self._ColouredTileButtons.append(ColouredTile)
        
        ButtonSetDefault = tk.Button(self._Window, text = "Set Default", bg = "#CCCCCC", fg = "#000044",\
                                     font = (None, 11), width = 12, command = self.set_default_values)
        ButtonSetDefault.grid(row = 9, column = 4, sticky = tk.S)
        ButtonBack = tk.Button(self._Window, text = "Back", bg = "#CCCCCC", fg = "#000044",\
                               font = (None, 11), width = 12, command = self.close_window)
        ButtonBack.grid(row = 11, column = 4, sticky = tk.S)

    def den_to_hex(self, Number):
        DenToHexDict = {0:"0",1:"1",2:"2",3:"3",
                        4:"4",5:"5",6:"6",7:"7",
                        8:"8",9:"9", 10:"A",11:"B",
                        12:"C",13:"D",14:"E",15:"F"}
        FirstHexChar = Number // 16
        FirstHexChar = DenToHexDict[FirstHexChar]
        SecondHexChar = Number % 16
        SecondHexChar = DenToHexDict[SecondHexChar]
        return FirstHexChar + SecondHexChar

    def change_button_colours(self):
        for i in range(0,len(self._SliderValues)-2,3):
            RedAmount = self._SliderValues[i]
            GreenAmount = self._SliderValues[i+1]
            BlueAmount = self._SliderValues[i+2]
            RedHex = self.den_to_hex(RedAmount)
            GreenAmount = self.den_to_hex(GreenAmount)
            BlueAmount = self.den_to_hex(BlueAmount)
            Colour = "#"+RedHex+GreenAmount+BlueAmount
            ColouredTile = self._ColouredTileButtons[int(i/3)]
            ColouredTile.configure(bg = Colour)
        
    def set_default_values(self):
        for i in range(len(self._Sliders)):
            self._Sliders[i].set(self._DefaultSliderValues[i])
        self.save_changes()
        self.change_button_colours()
        self._Window.update()

    def save_changes(self):
        for i in range(len(self._Sliders)):
            self._SliderValues[i] = self._Sliders[i].get()

    def close_window(self):
        self.save_changes()
        self.adjust_rotation_speed()
        self._Window.destroy()

    def adjust_rotation_speed(self):
        Value =  self._Sliders[25].get()
        PossibleValues = (1,2,3,5,6,9,10,15,18,30,45,90)
        if Value not in PossibleValues:
            if Value > 90:
                Value = 90
                self._Sliders[25].set(Value)
                self._SliderValues[25] = Value
            else:
                for (i,j) in ((0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9),(9,10),(10,11)):
                    LowerLimit = PossibleValues[i]
                    UpperLimit = PossibleValues[j]
                    if LowerLimit < Value < UpperLimit:
                        Range = UpperLimit - LowerLimit
                        DifferenceWithLowerLimit = Value - LowerLimit
                        DifferenceWithUpperLimit = UpperLimit - Value
                        if DifferenceWithLowerLimit < DifferenceWithUpperLimit:
                            Value = LowerLimit
                        else:
                            Value = UpperLimit
                        self._Sliders[25].set(Value)
                        self._SliderValues[25] = Value
                        break
