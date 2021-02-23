import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np
import math
import random

import tkinter as tk

import os
import platform

try:
    from Net import *
    from CubePiece import CubePiece
    from Solver import Solver
    from Settings import SettingsWindow
    from Controls import ControlsWindow
    from Help import HelpWindow
except ImportError:
    quit()

def load_settings_from_file():
    global TileColourValues
    global BackgroundColourValues
    global CubeRotationSpeed
    global CustomRotationSpeed
    File = open("Settings.sav","r")
    TileColourValues = []
    for i in range(21):
        TileColourValues.append(float(File.readline().replace("\n","")))
    BackgroundColourValues = []
    for i in range(3):
        BackgroundColourValues.append(float(File.readline().replace("\n","")))
    CubeRotationSpeed = int(File.readline().replace("\n",""))
    CustomRotationSpeed = int(File.readline().replace("\n",""))
    File.close()

def save_settings_to_file():
    global TileColourValues
    global BackgroundColourValues
    global CubeRotationSpeed
    global CustomRotationSpeed
    File = open("Settings.sav","w")
    for Value in TileColourValues:
        File.write(str(Value)+"\n")
    for Value in BackgroundColourValues:
        File.write(str(Value)+"\n")
    File.write(str(CubeRotationSpeed)+"\n")
    File.write(str(CustomRotationSpeed)+"\n")
    File.close()
    
try:
    load_settings_from_file()
except:
    BackgroundColourValues = [178,178,178]
    TileColourValues = [255,255,255,
                        0,128,0,
                        178,0,0,
                        0,0,178,
                        230,205,0,
                        230,78,0,
                        0,0,0]
    CubeRotationSpeed = 6
    CustomRotationSpeed = 18 #must be a factor of 90
    save_settings_to_file()
    
BackgroundColour = [BackgroundColourValues[0]/250,
                    BackgroundColourValues[1]/250,
                    BackgroundColourValues[2]/250]
TileColours = [[TileColourValues[0]/250,TileColourValues[1]/250,TileColourValues[2]/250],
               [TileColourValues[3]/250,TileColourValues[4]/250,TileColourValues[5]/250],
               [TileColourValues[6]/250,TileColourValues[7]/250,TileColourValues[8]/250],
               [TileColourValues[9]/250,TileColourValues[10]/250,TileColourValues[11]/250],
               [TileColourValues[12]/250,TileColourValues[13]/250,TileColourValues[14]/250],
               [TileColourValues[15]/250,TileColourValues[16]/250,TileColourValues[17]/250],
               [TileColourValues[18]/250,TileColourValues[19]/250,TileColourValues[20]/250]]

Values = TileColourValues + BackgroundColourValues+[CubeRotationSpeed]+[CustomRotationSpeed]           
NewSettingsWindow = SettingsWindow(Values)
def display_settings_window():
    global TileColourValues
    global BackgroundColourValues
    global BackgroundColour
    global TileColours
    global CubeRotationSpeed
    global CustomRotationSpeed
    NewSettingsWindow.display_window()
    TileColourValues = NewSettingsWindow._SliderValues[0:21]
    BackgroundColourValues = NewSettingsWindow._SliderValues[21:24]
    CubeRotationSpeed = NewSettingsWindow._SliderValues[24]
    CustomRotationSpeed = NewSettingsWindow._SliderValues[25]
    BackgroundColour = [BackgroundColourValues[0]/250,
                    BackgroundColourValues[1]/250,
                    BackgroundColourValues[2]/250]
    glClearColor(*BackgroundColour,1)
    TileColours = [[TileColourValues[0]/250,TileColourValues[1]/250,TileColourValues[2]/250],
                   [TileColourValues[3]/250,TileColourValues[4]/250,TileColourValues[5]/250],
                   [TileColourValues[6]/250,TileColourValues[7]/250,TileColourValues[8]/250],
                   [TileColourValues[9]/250,TileColourValues[10]/250,TileColourValues[11]/250],
                   [TileColourValues[12]/250,TileColourValues[13]/250,TileColourValues[14]/250],
                   [TileColourValues[15]/250,TileColourValues[16]/250,TileColourValues[17]/250],
                   [TileColourValues[18]/250,TileColourValues[19]/250,TileColourValues[20]/250]]
    save_settings_to_file()

NewControlsWindow = ControlsWindow()
def display_controls_window():
    NewControlsWindow.display_window()

NewHelpWindow = HelpWindow()
def display_help_window():
    NewHelpWindow.display_window()

def reset_cube():
    global Net
    global Cube
    global AnimateTurn
    global Scramble
    global DisplaySolution
    global DisplayTutorial
    global UndoMoves
    global RedoMoves
    if not AnimateTurn and not Scramble:
        Net = set_default_net()
        Cube = create_cube_from_net(Net)
        UndoMoves = []
        RedoMoves = []
        DisplaySolution = False
        DisplayTutorial = False
        clear_solution_algorithm()

def scramble_cube():
    global ScramblingAlgorithm
    global UndoMoves
    global RedoMoves
    global Scramble
    global AnimateTurn
    global DisplaySolution
    global DisplayTutorial
    if not AnimateTurn and not Scramble:
        Moves = ["U","D","L","R","F","B","M","E","S"]
        ScramblingAlgorithm = []
        for TurnNumber in range(25):
            Move = random.choice(Moves)
            if len(ScramblingAlgorithm) >= 1:
                while ScramblingAlgorithm[len(ScramblingAlgorithm)-1][0] == Move:
                    Move = Moves[random.randint(0,len(Moves)-1)]
                Move = Moves[random.randint(0,len(Moves)-1)]
            RandInt = random.randint(0,2)
            if RandInt == 0:
                ScramblingAlgorithm.append(Move + "+")
            elif RandInt == 1:
                ScramblingAlgorithm.append(Move + "-")
            else:
                # Double moves [U2,D2,F2,B2,L2...] 
                ScramblingAlgorithm.append(Move + "2")
        Scramble = True
        UndoMoves = []
        RedoMoves = []
        DisplaySolution = False
        DisplayTutorial = False
        clear_solution_algorithm()

def solve_cube():
    global DisplaySolution
    global DisplayTutorial
    global RedoMoves
    global UndoMoves
    global Scramble
    global AnimateTurn
    if not AnimateTurn and not Scramble and \
       not DisplaySolution and not DisplayTutorial:
        NewSolver = Solver(Net)
        Solution = NewSolver.solve_cube()
        display_solution_algorithm(Solution)
        DisplaySolution = True
        DisplayTutorial = False
        RedoMoves = Solution[::-1]
        UndoMoves = []

def pause():
    global UndoMove
    global ToggleUndo
    global RedoMove
    global ToggleRedo
    UndoMove = False
    ToggleUndo = False
    RedoMove = False
    ToggleRedo = False

def single_undo():
    global UndoMove
    global UndoMoves
    global ToggleUndo
    if len(UndoMoves) >= 1:
        pause()
        UndoMove = True
        ToggleUndo = False
        
def single_redo():
    global RedoMove
    global RedoMoves
    global ToggleRedo
    if len(RedoMoves) >= 1:
        pause()
        RedoMove = True

def toggle_undo():
    global UndoMove
    global UndoMoves
    global ToggleUndo
    if len(UndoMoves) > 1:
        pause()
        UndoMove = True
        ToggleUndo = True
        
def toggle_redo():
    global RedoMove
    global RedoMoves
    global ToggleRedo
    if len(RedoMoves) > 1:
        pause()
        RedoMove = True
        ToggleRedo = True
    
# Tkinter user interface
WindowHeight = 400
WindowWidth = 400

MainWindow = tk.Tk()
MainWindow.title("Rubik's Cube Solver")
MainWindow.geometry("800x600")
MainWindow.resizable(0, 0)
MainWindow.configure(background = "#555555")

Frame1 = tk.Frame(MainWindow,height = WindowHeight,width = 800)
Frame1.grid(row = 0)

def display_solution_algorithm(Algorithm):
    global MoveLabels
    for Label in MoveLabels:
        Label.configure(text = "", fg = "white")
    for i in range(len(Algorithm)):
        MoveLabels[i].configure(text = Algorithm[i])

def change_moves_of_solution(Algorithm):
    global MoveLabels
    global TurnLayerCommands
    global SliceTurnLayerKeys
    global TurnLayerKeys
    global SliceTurnNotation
    global TurnNotation
    for i in range(len(Algorithm)):
        OriginalMove = Algorithm[i]
        AxisOfLayerRotation = TurnLayerCommands[OriginalMove[0]]
        if OriginalMove[0] in ["M","E","S"]:
            for Move in SliceTurnLayerKeys:
                Axis = (SliceTurnLayerKeys[Move])
                if AxisOfLayerRotation[0] == Axis[0]:
                    if AxisOfLayerRotation[1] == Axis[1]:
                        if AxisOfLayerRotation[2] == Axis[2]:
                            MoveLabels[i].configure(text = SliceTurnNotation[Move] + OriginalMove[1])
                    
        else:
            for Move in TurnLayerKeys:
                Axis = (TurnLayerKeys[Move])
                if AxisOfLayerRotation[0] == Axis[0]:
                    if AxisOfLayerRotation[1] == Axis[1]:
                        if AxisOfLayerRotation[2] == Axis[2]:
                            MoveLabels[i].configure(text = TurnNotation[Move] + OriginalMove[1])


def change_move_colour(CorrectMove):
    global MoveLabels
    global UndoMoves
    if len(UndoMoves) > 0:
        Index = len(UndoMoves) - 1
        if CorrectMove:
            if Index > 0:
                MoveLabels[Index-1].configure(fg = "White")
            MoveLabels[Index].configure(fg = "#00AA00")
            if Index < len(MoveLabels) - 1:
                MoveLabels[Index+1].configure(fg = "White")
        else:
            if Index > 0:
                MoveLabels[Index-1].configure(fg = "White")
            MoveLabels[Index].configure(fg = "#AA0000")
            if Index < len(MoveLabels) - 1:
                MoveLabels[Index+1].configure(fg = "White")
    else:
        MoveLabels[0].configure(fg = "white")

def clear_solution_algorithm():
    global MoveLabels
    for Label in MoveLabels:
        Label.configure(text = " ")

Frame2 = tk.Frame(MainWindow, height = 200, width = 800, bg = "#555555")
Frame2.grid(row = 1)

tk.Button(Frame2, text = "|<", bg = "#CCCCCC", fg = "#000044", font = (None, 11), \
width = 3, command = toggle_undo).grid(row = 0, column = 0, padx = 5, pady = 5)
tk.Button(Frame2, text = "<", bg = "#CCCCCC", fg = "#000044", font = (None, 11), \
width = 3, command = single_undo).grid(row = 0, column = 1, padx = 5, pady = 5)
tk.Button(Frame2, text = "||", bg = "#CCCCCC", fg = "#000044", font = (None, 11), \
width = 3, command = pause).grid(row = 0, column = 2, padx = 5, pady = 5)
tk.Button(Frame2, text = ">", bg = "#CCCCCC", fg = "#000044", font = (None, 11), \
width = 3, command = single_redo).grid(row = 0, column = 3, padx = 5, pady = 5)
tk.Button(Frame2, text = ">|", bg = "#CCCCCC", fg = "#000044", font = (None, 11), \
width = 3, command = toggle_redo).grid(row = 0, column = 4, padx = 5, pady = 5)

Frame3 = tk.Frame(MainWindow, height = 200, width = 800, bg = "#555555")
Frame3.grid(row = 2)

MoveLabels = []
for i in range(180):
    Row = (i // 36) + 1
    Column = i % 36
    Label = tk.Label(Frame3, text = "  ", bg = "#555555", fg = "White", width = 2)
    Label.grid(row = Row, column = Column)
    MoveLabels.append(Label)

MenuFrame = tk.Frame(Frame1,height = WindowHeight,width = 200,bg = "#282828")
MenuFrame.grid(row = 0, column = 0)

ButtonHeight = 35
ButtonPadY = 10
ButtonTexts = ["Reset",
               "Scramble",
               "Solve",
               "Controls",
               "Settings",
               "Help"]
ButtonCommands = [reset_cube,
                  scramble_cube,
                  solve_cube,
                  display_controls_window,
                  display_settings_window,
                  display_help_window,]
for i in range(len(ButtonTexts)):
    tk.Button(MenuFrame, text = ButtonTexts[i], bg = "#CCCCCC", fg = "#000044", font = (None, 11), \
        width = 12, command = ButtonCommands[i]).place(x=35,y=(ButtonHeight*i + ButtonPadY*(i+1)))

def load_tutorial(Tutorial):
    global NetBackup
    global Net
    global Cube
    global DisplayTutorial
    global DisplaySolution
    global Solution
    global UndoMoves
    global RedoMoves
    global UndoMove
    global ToggleUndo
    global RedoMove
    global ToggleRedo
    if Tutorial == 0:
        Net = set_net(NetBackup)
        Cube = create_cube_from_net(Net)
        UndoMoves = []
        RedoMoves = []
        Solution = []
        UndoMove = False
        ToggleUndo = False
        RedoMove = False
        ToggleRedo = False
        DisplayTutorial = False
        DisplaySolution = False
        clear_solution_algorithm()
    else:
        Moves = ["U","D","L","R","F","B","M","E","S"]
        PreviousMove = ""
        for TurnNumber in range(25):
            Move = random.choice(Moves)
            while Move == PreviousMove:
                Move = random.choice(Moves)
            Type = random.randint(0,2)
            if Type == 0:
                Net = apply_move_to_net(Net, Move + "+")
            elif Type == 1:
                Net = apply_move_to_net(Net, Move + "-")
            else:
                Net = apply_move_to_net(Net, Move + "2")
        UndoMoves = []
        RedoMoves = []
        clear_solution_algorithm()
        NewSolver = Solver(Net)
        Solution = []
        if Tutorial == 1:
            TutorialAlgorithm = NewSolver.solve_upper_cross()
        elif Tutorial == 2:
            Solution += NewSolver.solve_upper_cross()
            TutorialAlgorithm = NewSolver.solve_all_upper_corners()
        elif Tutorial == 3:
            Solution += NewSolver.solve_upper_cross()
            Solution += NewSolver.solve_all_upper_corners()
            TutorialAlgorithm = NewSolver.solve_middle_edges()
        elif Tutorial == 4:
            Solution += NewSolver.solve_upper_cross()
            Solution += NewSolver.solve_all_upper_corners()
            Solution += NewSolver.solve_middle_edges()
            TutorialAlgorithm = NewSolver.solve_bottom_cross()
        elif Tutorial == 5:
            Solution += NewSolver.solve_upper_cross()
            Solution += NewSolver.solve_all_upper_corners()
            Solution += NewSolver.solve_middle_edges()
            Solution += NewSolver.solve_bottom_cross()
            TutorialAlgorithm = NewSolver.permute_bottom_edges()
        elif Tutorial == 6:
            Solution += NewSolver.solve_upper_cross()
            Solution += NewSolver.solve_all_upper_corners()
            Solution += NewSolver.solve_middle_edges()
            Solution += NewSolver.solve_bottom_cross()
            Solution += NewSolver.permute_bottom_edges()
            TutorialAlgorithm = NewSolver.permute_bottom_corners()
        elif Tutorial == 7:
            Solution += NewSolver.solve_upper_cross()
            Solution += NewSolver.solve_all_upper_corners()
            Solution += NewSolver.solve_middle_edges()
            Solution += NewSolver.solve_bottom_cross()
            Solution += NewSolver.permute_bottom_edges()
            Solution += NewSolver.permute_bottom_corners()
            TutorialAlgorithm = NewSolver.orientate_bottom_corners()
        for Move in Solution:
            Net = apply_move_to_net(Net, Move)
        TutorialAlgorithm = NewSolver.optimise_solution(TutorialAlgorithm)
        i = 0
        while i != len(TutorialAlgorithm):
            if TutorialAlgorithm[i][1] == "2":
                TutorialAlgorithm = TutorialAlgorithm[:i] + [TutorialAlgorithm[i][0]+"+"]*2 + TutorialAlgorithm[i+1:]
            i += 1
        Solution = TutorialAlgorithm
        if Solution != []:
            Cube = create_cube_from_net(Net)
            display_solution_algorithm(Solution)
            DisplayTutorial = True
            DisplaySolution = False
        else:
            load_tutorial(Tutorial)
        
TutorialsFrame = tk.Frame(Frame1,height = WindowHeight,width = 200,bg = "#282828")
TutorialsFrame.grid(row = 0, column = 2)

TutorialsListBox = tk.Listbox(TutorialsFrame, width = 22, height = 18, bg = "#555555", fg = "White")
TutorialsListBox.yview()
TutorialsListBox.insert(0,"Back To Cube")
TutorialsListBox.insert(1,"Upper Cross Tutorial")
TutorialsListBox.insert(2,"Upper Corners Tutorial")
TutorialsListBox.insert(3,"Middle Edges Tutorial")
TutorialsListBox.insert(4,"Bottom Cross Tutorial")
TutorialsListBox.insert(5,"Bottom Edge Swap Tutorial")
TutorialsListBox.insert(6,"Bottom Corner Swap Tutorial")
TutorialsListBox.insert(7,"Bottom Corner Flip Tutorial")
TutorialsListBox.activate(0)
TutorialsListBox.place(x=11,y=13)

# Below is the code to embed the pygame window with into a tkinter window
# the code is no my own it is taken and implemented in to my system from the link below
# https://stackoverflow.com/questions/23319059/embedding-a-pygame-window-into-a-tkinter-or-wxpython-frame

DisplayFrame = tk.Frame(Frame1, width = WindowWidth, height = WindowHeight)
DisplayFrame.grid(row = 0, column = 1)
MainWindow.update()

os.environ['SDL_WINDOWID'] = str(DisplayFrame.winfo_id())
if platform.system == "Windows":
    os.environ['SDL_VIDEODRIVER'] = 'windib'

FieldOfView = 35

NearClippingPlane = 7
FarClippingPlane = 13
NearPlaneWidth = 2*NearClippingPlane*math.tan((FieldOfView/2)*math.pi/180)
NearPlaneHeight = NearPlaneWidth*WindowHeight/WindowWidth

def create_cube_from_net(Net):
    Cube = []
    PositionColours = []
    for x in range(-1,2):
        for y in range(-1,2):
            for z in range(-1,2):
                PositionColours.append( [ [x,y,z],[6,6,6,6,6,6] ] )
    for Row in range(3):
        for Face in range(6):
            for Column in range(3):
                Position = [0,0,0]
                # x coord
                if Face in (0,2,4,5):
                    Position[0] = Column-1
                elif Face == 1:
                    Position[0] = -1
                else:
                    Position[0] = 1
                # y coord
                if Face in (1,2,3):
                    Position[1] = 1-Row
                elif Face == 0:
                    Position[1] = 1
                elif Face == 4:
                    Position[1] = -1
                else:
                    Position[1] = Row-1
                # z coord     
                if Face == 0:
                    Position[2] = Row-1
                elif Face == 1:
                    Position[2] = Column-1
                elif Face == 2:
                    Position[2] = 1
                elif Face == 3:
                    Position[2] = 1-Column
                elif Face == 4:
                    Position[2] = 1-Row
                else:
                    Position[2] = -1
                    
                if Face in (0,4):
                    ImportantAxis = 1
                elif Face in (1,3):
                    ImportantAxis = 0
                else:
                    ImportantAxis = 2
                    
                Colour = Net[Row][Face*3+Column]
                PositionIndexInArray = (Position[0] + 1)*9 + (Position[1] + 1)*3 + (Position[2] + 1)

                if Position[ImportantAxis] == 1:
                    if ImportantAxis == 0:
                        PositionColours[PositionIndexInArray][1][1] = Colour
                    if ImportantAxis == 1:
                        PositionColours[PositionIndexInArray][1][3] = Colour
                    if ImportantAxis == 2:
                        PositionColours[PositionIndexInArray][1][5] = Colour
                elif Position[ImportantAxis] == -1:
                    if ImportantAxis == 0:
                        PositionColours[PositionIndexInArray][1][0] = Colour
                    if ImportantAxis == 1:
                        PositionColours[PositionIndexInArray][1][2] = Colour
                    if ImportantAxis == 2:
                        PositionColours[PositionIndexInArray][1][4] = Colour
                
    for x in range(-1,2):
        for y in range(-1,2):
            for z in range(-1,2):
                Position = (x,y,z)
                PositionIndexInArray = (Position[0] + 1)*9 + (Position[1] + 1)*3 + (Position[2] + 1)
                Colours = PositionColours[PositionIndexInArray][1]
                Cube.append(CubePiece(Position,Colours))
    return Cube     
    
def determine_cube_normal_vector(EyeNormalVector):
    EyeNormalVector = list(EyeNormalVector)
    CubeNormalVector = [0,0,0]
    if -1*min(EyeNormalVector) > max(EyeNormalVector):
        CubeNormalVector[EyeNormalVector.index(min(EyeNormalVector))] = -1
    else:
        CubeNormalVector[EyeNormalVector.index(max(EyeNormalVector))] = 1
    return np.array(CubeNormalVector)

def vector_magnitude(Vector):
    return math.sqrt(Vector[0]**2 + Vector[1]**2 + Vector[2]**2)

def normalise_vector(Vector):
    if vector_magnitude(Vector) != 0:
        NormalisedVector = np.array(Vector)/vector_magnitude(Vector)
        return NormalisedVector
    else:
        return Vector

def vector_dot_product(Vector1,Vector2):
    ScalarProduct = 0
    for i in range(3):
        ScalarProduct += Vector1[i] * Vector2[i]
    return ScalarProduct

def vector_cross_product(Vector1,Vector2):
    x = Vector1[1]*Vector2[2] - Vector1[2]*Vector2[1]
    y = Vector1[2]*Vector2[0] - Vector1[0]*Vector2[2]
    z = Vector1[0]*Vector2[1] - Vector1[1]*Vector2[0]
    CrossProduct = np.array([x,y,z])
    return CrossProduct

def rotate_vector_about_given_axis(Vector,Axis,Angle):
    v = Vector
    k = -Axis
    O = Angle*math.pi/180
    RotatedVector = v*math.cos(O) + vector_cross_product(k,v)*math.sin(O) + k*vector_dot_product(k,v)*(1 - math.cos(O))
    return RotatedVector

def get_ray_intersection_distance(MouseX,MouseY,EyeVertex,EyeRightNormal,EyeUpNormal,EyeFrontNormal):
    x = NearPlaneWidth*MouseX/WindowWidth
    y = NearPlaneHeight*MouseY/WindowHeight
    MousePositionOnNearPlane = EyeVertex+NearClippingPlane*EyeFrontNormal+x*EyeRightNormal+y*EyeUpNormal
    RayEntryPoint = EyeVertex
    RayDirection = normalise_vector(MousePositionOnNearPlane-EyeVertex)
    FaceNormals = [[0,1,0],[0,-1,0],[-1,0,0],[1,0,0],[0,0,1],[0,0,-1]]
    RayIntersectionDistances = [999,999,999,999,999,999]
    for Normal in FaceNormals:
        n = Normal
        o = [1.5*n[0],1.5*n[1],1.5*n[2]]
        if vector_dot_product(RayDirection,n) != 0: # avoids divide by zero error when ray is parallel to a plane
            t = vector_dot_product(np.array(o)-np.array(RayEntryPoint),n)/vector_dot_product(RayDirection,n)
            RayIntersectionPoint = RayEntryPoint + t*RayDirection
            Axes = [0,1,2]
            if max(n) == 1:
                Axes.pop(n.index(max(n)))
            else:
                Axes.pop(n.index(min(n)))
            if -1.5 < RayIntersectionPoint[Axes[0]] < 1.5:
                if -1.5 < RayIntersectionPoint[Axes[1]] < 1.5:
                    RayIntersectionDistances[FaceNormals.index(Normal)] = t
    return min(RayIntersectionDistances),RayDirection

def get_selected_tile_centre(Vertex):
    TileCentre = [0,0,0]
    Vertex = [round(Vertex[0],4),round(Vertex[1],4),round(Vertex[2],4)]
    Axes = [0,1,2]
    if max(Vertex) > -min(Vertex):
        TileCentre[Vertex.index(max(Vertex))] = 1.5
        Axes.pop(Vertex.index(max(Vertex)))
    else:
        TileCentre[Vertex.index(min(Vertex))] = -1.5
        Axes.pop(Vertex.index(min(Vertex)))
    if -1.5 < Vertex[Axes[0]] < -0.5:
        TileCentre[Axes[0]] = -1
    elif -0.5 < Vertex[Axes[0]] < 0.5:
        TileCentre[Axes[0]] = 0
    elif 0.5 < Vertex[Axes[0]] < 1.5:
        TileCentre[Axes[0]] = 1
    if -1.5 < Vertex[Axes[1]] < -0.5:
        TileCentre[Axes[1]] = -1
    elif -0.5 < Vertex[Axes[1]] < 0.5:
        TileCentre[Axes[1]] = 0 
    elif 0.5 < Vertex[Axes[1]] < 1.5:
        TileCentre[Axes[1]] = 1
    return np.array(TileCentre)

def draw(Cube):
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    for Cubelet in Cube:
        Vertices = Cubelet.get_vertices()
        Surfaces = Cubelet.get_surfaces()
        for i in range(0,len(Vertices),4):
            glColor3fv(TileColours[Surfaces[i//4]])
            glBegin(GL_QUADS)
            glVertex3fv(Vertices[i])
            glVertex3fv(Vertices[i+1])
            glVertex3fv(Vertices[i+2])
            glVertex3fv(Vertices[i+3])
            glEnd()
        # about 10 fps loss with lines on
        glColor3fv([0,0,0])
        glLineWidth(2.0)
        glBegin(GL_LINES)
        Borders = Cubelet.get_borders()
        for Border in Borders:
            glVertex3fv(Vertices[Border[0]])
            glVertex3fv(Vertices[Border[1]])
        glEnd()
    pygame.display.flip()

Display = pygame.display.set_mode((WindowWidth,WindowHeight),DOUBLEBUF|OPENGL)
pygame.display.init()
AspectRatio = WindowWidth / WindowHeight
gluPerspective(FieldOfView, AspectRatio, NearClippingPlane, FarClippingPlane)
glEnable(GL_DEPTH_TEST)
glClearColor(*BackgroundColour,1)

Net = set_default_net()
NetBackup = set_net(Net)
Cube = create_cube_from_net(Net)     

CubeUpFaceNormal = np.array([0,1,0])
CubeDownFaceNormal = np.array([0,-1,0])
CubeLeftFaceNormal = np.array([-1,0,0])
CubeRightFaceNormal = np.array([1,0,0])
CubeFrontFaceNormal = np.array([0,0,1])
CubeBackFaceNormal = np.array([0,0,-1])

EyeVertex = np.array([0,0,10])
glTranslatef(-EyeVertex[0],-EyeVertex[1],-EyeVertex[2])

EyeUpNormal = CubeUpFaceNormal
EyeRightNormal = CubeRightFaceNormal
EyeFrontNormal = -normalise_vector(EyeVertex)

TurnNotation = {K_u:"U",
                K_d:"D",
                K_l:"L",
                K_r:"R",
                K_f:"F",
                K_b:"B"}

SliceTurnNotation = {K_m:"M",
                     K_e:"E",
                     K_s:"S"}

ActionKeys = {K_z:"Undo",
              K_x:"Redo",
              K_SPACE:"Pause",
              K_c:"Reset",
              K_q:"Scramble",
              K_v:"Solve"}
            
TurnLayerCommands = {"U":[0,1,0],
                    "D":[0,-1,0],
                    "L":[-1,0,0],
                    "R":[1,0,0],
                    "F":[0,0,1],
                    "B":[0,0,-1],
                    "M":[-1,0,0],
                    "E":[0,-1,0],
                    "S":[0,0,1]}

CurrentTutorial = 0
TurnDirection = 1
AnimateTurn = False
AngleTurned = 0
NewTileSelected = False
SliceRotation = True
DoubleRotation = False
Turned = False
UndoMove = False
RedoMove = False
Toggle = True
ToggleRedo = True
ToggleUndo = True
UndoMoves = []
RedoMoves = []
Solution = []
Scramble = False
DisplaySolution = False
DisplayTutorial = False
CubeSolved = True

while True:
    
    #previous_time = pygame.time.get_ticks()
    
    CubeUpFaceNormal = determine_cube_normal_vector(EyeUpNormal)
    CubeDownFaceNormal = determine_cube_normal_vector(-EyeUpNormal)
    CubeLeftFaceNormal = determine_cube_normal_vector(-EyeRightNormal)
    CubeRightFaceNormal = determine_cube_normal_vector(EyeRightNormal)
    CubeFrontFaceNormal = determine_cube_normal_vector(-EyeFrontNormal)
    CubeBackFaceNormal = determine_cube_normal_vector(EyeFrontNormal)

    TurnLayerKeys = {K_u:CubeUpFaceNormal,
                     K_d:CubeDownFaceNormal,
                     K_l:CubeLeftFaceNormal,
                     K_r:CubeRightFaceNormal,
                     K_f:CubeFrontFaceNormal,
                     K_b:CubeBackFaceNormal}
    
    SliceTurnLayerKeys = {K_m:CubeLeftFaceNormal,
                          K_e:CubeDownFaceNormal,
                          K_s:CubeFrontFaceNormal}

    CubeRotationKeys = {K_KP4:-EyeUpNormal,
                        K_KP5:EyeRightNormal,
                        K_KP6:EyeUpNormal,
                        K_KP7:-EyeFrontNormal,
                        K_KP8:-EyeRightNormal,
                        K_KP9:EyeFrontNormal}
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == K_LCTRL:
                Toggle = False
                
            elif event.key == K_LSHIFT:
                TurnDirection = -1
                
            elif event.key in ActionKeys:
                if ActionKeys[event.key] ==  "Pause":
                    pause()
                        
                elif ActionKeys[event.key] == "Reset":
                    reset_cube()

                elif ActionKeys[event.key] == "Solve":
                    solve_cube()
                    
                elif ActionKeys[event.key] == "Scramble":
                    scramble_cube()

                elif ActionKeys[event.key] == "Undo":
                    if Toggle:
                        toggle_undo()
                    else:
                        single_undo()

                elif ActionKeys[event.key] ==  "Redo":
                    if Toggle:
                        toggle_redo()
                    else:
                        single_redo()
            
            if not AnimateTurn and not Scramble and not DisplaySolution: # When a layer is being turned, controls are locked
                
                if event.key in TurnLayerKeys:
                    AxisOfLayerRotation = list(TurnLayerKeys[event.key])
                    AnimateTurn = True
                    AngleTurned = 0
                    Direction = TurnDirection
                    SliceRotation = False
                    for Move in ["U","D","L","R","F","B"]:
                        Axis = list(TurnLayerCommands[Move])
                        if AxisOfLayerRotation[0] == Axis[0]:
                            if AxisOfLayerRotation[1] == Axis[1]:
                                if AxisOfLayerRotation[2] == Axis[2]:
                                    if Direction == 1:
                                        UndoMoves.append(Move + "+")
                                        Net = apply_move_to_net(Net, Move + "+")
                                    else:
                                        UndoMoves.append(Move + "-")
                                        Net = apply_move_to_net(Net, Move + "-")
                    
                elif event.key in SliceTurnLayerKeys:
                    AxisOfLayerRotation = list(SliceTurnLayerKeys[event.key])
                    AnimateTurn = True
                    AngleTurned = 0
                    Direction = TurnDirection
                    SliceRotation = True
                    for Move in ["M","E","S"]:
                        Axis = list(TurnLayerCommands[Move])
                        if AxisOfLayerRotation[0] == Axis[0]:
                            if AxisOfLayerRotation[1] == Axis[1]:
                                if AxisOfLayerRotation[2] == Axis[2]:
                                    if Direction == 1:
                                        UndoMoves.append(Move + "+")
                                        Net = apply_move_to_net(Net, Move + "+")
                                    else:
                                        UndoMoves.append(Move + "-")
                                        Net = apply_move_to_net(Net, Move + "-")



        if event.type == pygame.KEYUP:
            if event.key == K_LSHIFT:
                TurnDirection = 1

            elif event.key == K_LCTRL:
                Toggle = True
                
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1: #mouse1,mwheel,mouse2,scrollup,scrolldown,mouse6,mouse7
                Turned = False
                MousePosition = pygame.mouse.get_pos()
                MouseX = MousePosition[0]-WindowWidth/2
                MouseY = -MousePosition[1]+WindowHeight/2
                MouseRayIntersectionDistance,RayDirection = get_ray_intersection_distance(MouseX,MouseY,EyeVertex,EyeRightNormal,EyeUpNormal,EyeFrontNormal)
                MouseCursorIsOnCube = False
                if MouseRayIntersectionDistance == 999:
                    MouseCursorIsOnCube = False
                else:
                    MouseCursorIsOnCube = True
                    RayIntersectionPoint = EyeVertex + MouseRayIntersectionDistance*RayDirection
                    CurrentTileCentre = get_selected_tile_centre(RayIntersectionPoint)
                    
    for Key in CubeRotationKeys:
        if pygame.key.get_pressed()[Key]:
            AxisOfCubeRotation = CubeRotationKeys[Key]
            glRotatef(CubeRotationSpeed*1.5,AxisOfCubeRotation[0],AxisOfCubeRotation[1],AxisOfCubeRotation[2])
            EyeRightNormal = normalise_vector(rotate_vector_about_given_axis(EyeRightNormal,AxisOfCubeRotation,CubeRotationSpeed*1.5))
            EyeFrontNormal = normalise_vector(rotate_vector_about_given_axis(EyeFrontNormal,AxisOfCubeRotation,CubeRotationSpeed*1.5))
            EyeUpNormal = normalise_vector(rotate_vector_about_given_axis(EyeUpNormal,AxisOfCubeRotation,CubeRotationSpeed*1.5))
            EyeVertex = -10*EyeFrontNormal
                
    if pygame.mouse.get_pressed()[0]:
        if MouseCursorIsOnCube == True:
            if not Turned and not Scramble and not AnimateTurn and not DisplaySolution:
                PreviousMouseX = MouseX
                PreviousMouseY = MouseY
                MousePosition = pygame.mouse.get_pos()
                MouseX = MousePosition[0]-WindowWidth/2
                MouseY = -MousePosition[1]+WindowHeight/2
                PreviousTileCentre = CurrentTileCentre
                MouseRayIntersectionDistance,RayDirection = get_ray_intersection_distance(MouseX,MouseY,EyeVertex,EyeRightNormal,EyeUpNormal,EyeFrontNormal)
                RayIntersectionPoint = EyeVertex + MouseRayIntersectionDistance*RayDirection
                CurrentTileCentre = get_selected_tile_centre(RayIntersectionPoint)
                if CurrentTileCentre[0] != PreviousTileCentre[0]:
                    if vector_magnitude(CurrentTileCentre - PreviousTileCentre) in [1,math.sqrt(0.5)]:
                        NewTileSelected = True
                if CurrentTileCentre[1] != PreviousTileCentre[1]:
                    if vector_magnitude(CurrentTileCentre - PreviousTileCentre) in [1,math.sqrt(0.5)]:
                        NewTileSelected = True
                if CurrentTileCentre[2] != PreviousTileCentre[2]:
                    if vector_magnitude(CurrentTileCentre - PreviousTileCentre) in [1,math.sqrt(0.5)]:
                        NewTileSelected = True
        else:
            PreviousMouseX = MouseX
            PreviousMouseY = MouseY
            MousePosition = pygame.mouse.get_pos()
            MouseX = MousePosition[0]-WindowWidth/2
            MouseY = -MousePosition[1]+WindowHeight/2
            MouseDisplacementX = MouseX - PreviousMouseX
            MouseDisplacementY = MouseY - PreviousMouseY
            
            glRotatef(MouseDisplacementX*CubeRotationSpeed/15,EyeUpNormal[0],EyeUpNormal[1],EyeUpNormal[2])
            EyeRightNormal = normalise_vector(rotate_vector_about_given_axis(EyeRightNormal,EyeUpNormal,MouseDisplacementX*CubeRotationSpeed/15))
            EyeFrontNormal = normalise_vector(rotate_vector_about_given_axis(EyeFrontNormal,EyeUpNormal,MouseDisplacementX*CubeRotationSpeed/15))
            EyeVertex = -10*EyeFrontNormal
            
            glRotatef(-MouseDisplacementY*CubeRotationSpeed/15,EyeRightNormal[0],EyeRightNormal[1],EyeRightNormal[2])
            EyeUpNormal = normalise_vector(rotate_vector_about_given_axis(EyeUpNormal,EyeRightNormal,-MouseDisplacementY*CubeRotationSpeed/15))
            EyeFrontNormal = normalise_vector(rotate_vector_about_given_axis(EyeFrontNormal,EyeRightNormal,-MouseDisplacementY*CubeRotationSpeed/15))
            EyeVertex = -10*EyeFrontNormal
        
    if NewTileSelected and not AnimateTurn and not Scramble and not DisplaySolution:
        Turned = True
        AxisOfLayerRotation = [0,0,0]
        NewTileSelected = False
        Point = np.array([0,0,0])
        for Axis in [0,1,2]:
            if CurrentTileCentre[Axis] == PreviousTileCentre[Axis] == 1:
                Point[Axis] = 1
            elif CurrentTileCentre[Axis] == PreviousTileCentre[Axis] == -1:
                Point[Axis] = -1
        CurrentDisplacementVectorFromPoint = CurrentTileCentre - Point
        PreviousDisplacementVectorFromPoint = PreviousTileCentre - Point
        AxisOfLayerRotation = vector_cross_product(CurrentDisplacementVectorFromPoint,PreviousDisplacementVectorFromPoint)
        AxisOfLayerRotation = normalise_vector(AxisOfLayerRotation)
        AxisOfLayerRotation = list(AxisOfLayerRotation)
        SliceRotation = False
        for Axis in [0,1,2]:
            if CurrentTileCentre[Axis] == PreviousTileCentre[Axis] == 0:
                SliceRotation = True
                
        if SliceRotation:
            for Move in ["M","E","S"]:
                Axis = list(TurnLayerCommands[Move])
                if AxisOfLayerRotation[0] == Axis[0]:
                    if AxisOfLayerRotation[1] == Axis[1]:
                        if AxisOfLayerRotation[2] == Axis[2]:
                            Direction = 1
                            UndoMoves.append(Move + "+")
                            Net = apply_move_to_net(Net, Move + "+")
                          
            for Move in ["M","E","S"]:
                Axis = list(-np.array(TurnLayerCommands[Move]))
                if AxisOfLayerRotation[0] == Axis[0]:
                    if AxisOfLayerRotation[1] == Axis[1]:
                        if AxisOfLayerRotation[2] == Axis[2]:
                            AxisOfLayerRotation = list(-np.array(AxisOfLayerRotation))
                            Direction = -1
                            UndoMoves.append(Move + "-")
                            Net = apply_move_to_net(Net, Move + "-")
                            
        else:
            if max(AxisOfLayerRotation) == max(Point) == 1:
                Direction = 1
            elif min(AxisOfLayerRotation) == min(Point) == -1:
                Direction = 1
            else:
                AxisOfLayerRotation = list(-np.array(AxisOfLayerRotation))
                Direction = -1
            for Move in ["U","D","L","R","F","B"]:
                Axis = list(TurnLayerCommands[Move])
                if AxisOfLayerRotation[0] == Axis[0]:
                    if AxisOfLayerRotation[1] == Axis[1]:
                        if AxisOfLayerRotation[2] == Axis[2]:
                            if Direction == 1:
                                UndoMoves.append(Move + "+")
                                Net = apply_move_to_net(Net, Move + "+")
                            else:
                                UndoMoves.append(Move + "-")
                                Net = apply_move_to_net(Net, Move + "-")
        RedoMoves = []
        DoubleRotation = False
        AnimateTurn = True
        AngleTurned = 0
        
    if UndoMove and not AnimateTurn and not Scramble:
        if len(UndoMoves) >= 1:
            DoubleRotation = False
            Move = UndoMoves.pop()
            RedoMoves.append(Move)
            # Reverse the direction of the move
            if Move[1] == "+":
                Direction = -1
                Net = apply_move_to_net(Net, Move.replace("+","-"))
            elif Move[1] == "-":
                Direction = 1
                Net = apply_move_to_net(Net, Move.replace("-","+"))
            else:
                DoubleRotation = True
                Direction = 1
                Net = apply_move_to_net(Net, Move)
            if Move[0] in ["M","E","S"]:
                SliceRotation = True
            else:
                SliceRotation = False
            AxisOfLayerRotation = list(TurnLayerCommands[Move[0]])
            AnimateTurn = True
            AngleTurned = 0
            if not ToggleUndo:
                UndoMove = False
            if not DisplayTutorial:
                change_move_colour(True)
        else:
            UndoMove = False
      
    if RedoMove and not AnimateTurn and not Scramble:
        if len(RedoMoves) >= 1:
            DoubleRotation = False
            Move = RedoMoves.pop()
            UndoMoves.append(Move)
            if Move[1] == "+":
                Direction = 1
            elif Move[1] == "-":
                Direction = -1
            else:
                DoubleRotation = True
                Direction = 1
            if Move[0] in ["M","E","S"]:
                SliceRotation = True
            else:
                SliceRotation = False
            AxisOfLayerRotation = list(TurnLayerCommands[Move[0]])
            Net = apply_move_to_net(Net, Move)
            AnimateTurn = True
            AngleTurned = 0
            if not ToggleRedo:
                RedoMove = False
            if not DisplayTutorial:
                change_move_colour(True)
        else:
            RedoMove = False
        
    if Scramble:
        LayerRotationSpeed = 90
        if len(ScramblingAlgorithm) >= 1:
            if not AnimateTurn:
                DoubleRotation = False
                Move = ScramblingAlgorithm.pop()
                if Move[1] == "+":
                    Direction = 1
                elif Move[1] == "-":
                    Direction = -1
                else:
                    Direction = 1
                    DoubleRotation = True
                if Move[0] in ["M","E","S"]:
                    SliceRotation = True
                else:
                    SliceRotation = False
                AxisOfLayerRotation = list(TurnLayerCommands[Move[0]])
                Net = apply_move_to_net(Net, Move)
                AnimateTurn = True
                AngleTurned = 0
        else:
            Scramble = False
    elif not AnimateTurn:
        LayerRotationSpeed = CustomRotationSpeed
    
    if not SliceRotation and AnimateTurn:
        if AngleTurned < 90:
            for Cubelet in Cube:
                for axis in [0,1,2]:
                    if Cubelet._Position[axis] == AxisOfLayerRotation[axis] == 1:
                        Cubelet.rotate_cube_piece(AxisOfLayerRotation, Direction*LayerRotationSpeed)
                    if Cubelet._Position[axis] == AxisOfLayerRotation[axis] == -1:
                        Cubelet.rotate_cube_piece(AxisOfLayerRotation, Direction*LayerRotationSpeed)
            if DoubleRotation:
                AngleTurned += LayerRotationSpeed*0.5
            else:
                AngleTurned += LayerRotationSpeed
            
        elif AngleTurned == 90:
            for axis in [0,1,2]:
                for Cubelet in Cube:
                    if Cubelet._Position[axis] == AxisOfLayerRotation[axis] == 1:
                        Cubelet.round_vertices_and_position()
                    if Cubelet._Position[axis] == AxisOfLayerRotation[axis] == -1:
                        Cubelet.round_vertices_and_position()
            AnimateTurn = False

    if SliceRotation and AnimateTurn:
        if max(AxisOfLayerRotation) == 1:
            axis = AxisOfLayerRotation.index(max(AxisOfLayerRotation))
        else:
            axis = AxisOfLayerRotation.index(min(AxisOfLayerRotation))
            
        if AngleTurned < 90:
            for Cubelet in Cube:
                if Cubelet._Position[axis] == 0:
                    Cubelet.rotate_cube_piece(AxisOfLayerRotation, Direction*LayerRotationSpeed)
            if DoubleRotation:
                AngleTurned += LayerRotationSpeed*0.5
            else:
                AngleTurned += LayerRotationSpeed
            
        elif AngleTurned == 90:
            for Cubelet in Cube:
                if Cubelet._Position[axis] == 0:
                    Cubelet.round_vertices_and_position()
            AnimateTurn = False
            SliceRotation = False
            
    CubeSolved = cube_solved(Net)
    if CubeSolved and not AnimateTurn:
        DisplaySolution = False

    if CurrentTutorial == 0:
        NetBackup = set_net(Net)
        
    if DisplayTutorial and not AnimateTurn and len(UndoMoves) > 0:
        if UndoMoves[len(UndoMoves)-1] == Solution[len(UndoMoves)-1]:
            CorrectMove = True
            change_move_colour(CorrectMove)
            if len(UndoMoves) == len(Solution):
                DisplayTutorial = False
        else:
            CorrectMove = False
            change_move_colour(CorrectMove)
            Move = UndoMoves.pop()
            if Move[1] == "+":
                Direction = -1
                Net = apply_move_to_net(Net, Move.replace("+","-"))
            elif Move[1] == "-":
                Direction = 1
                Net = apply_move_to_net(Net, Move.replace("-","+"))
            else:
                DoubleRotation = True
                Direction = 1
                Net = apply_move_to_net(Net, Move)
            if Move[0] in ["M","E","S"]:
                SliceRotation = True
            else:
                SliceRotation = False
            AxisOfLayerRotation = list(TurnLayerCommands[Move[0]])
            AnimateTurn = True
            AngleTurned = 0
        
    try:
        if DisplaySolution or DisplayTutorial:
            if DisplaySolution:
                Solution = UndoMoves + RedoMoves[::-1]
            change_moves_of_solution(Solution)
        TutorialSelected = TutorialsListBox.curselection()
        if TutorialSelected != () and not AnimateTurn and not Scramble:
            if CurrentTutorial != TutorialSelected[0]:
                CurrentTutorial = TutorialSelected[0]
                load_tutorial(TutorialSelected[0])
            elif CurrentTutorial == TutorialSelected[0] == 0:
                Net = set_net(NetBackup)
        draw(Cube) # Clear error if window closed
        MainWindow.update() # Update error if window closed
    except:
        quit()
    #print(1/(0.001*(pygame.time.get_ticks()-previous_time))) # show a rough estimate of frames drawn per second (fps)

