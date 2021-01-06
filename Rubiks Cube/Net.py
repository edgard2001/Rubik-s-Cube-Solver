def set_default_net():
    Net = []
    for Row in range(3):
        Net.append([])
        for Face in range(6):
            for Cell in range(3):
                Net[Row].append(Face)
    return Net

def set_net(GivenNet):
    Net = []
    for Row in range(3):
        Net.append([])
        for Face in range(6):
            for Cell in range(3):
                Net[Row].append(GivenNet[Row][Cell + 3*Face])
    return Net

def cube_solved(Net):
    Solved = True
    for Face in range(6):
        Colour = Net[0][Face*3]
        for Row in range(3):
            for Column in range(3):
                if Net[Row][Column+Face*3] != Colour:
                    Solved = False
    return Solved

def apply_move_to_net(Net, Move):
    #Moves to rotate the layers 90 degrees (single/quarter rotations)
    if Move == "U+":
        Temp = Net[0][0]
        Net[0][0] = Net[2][0]
        Net[2][0] = Net[2][2]
        Net[2][2] = Net[0][2]
        Net[0][2] = Temp
        Temp = Net[0][1]
        Net[0][1] = Net[1][0]
        Net[1][0] = Net[2][1]
        Net[2][1] = Net[1][2]
        Net[1][2] = Temp
        Temp = Net[0][3]
        Net[0][3] = Net[0][6]
        Net[0][6] = Net[0][9]
        Net[0][9] = Net[2][17]
        Net[2][17] = Temp
        Temp = Net[0][4]
        Net[0][4] = Net[0][7]
        Net[0][7] = Net[0][10]
        Net[0][10] = Net[2][16]
        Net[2][16] = Temp
        Temp = Net[0][5]
        Net[0][5] = Net[0][8]
        Net[0][8] = Net[0][11]
        Net[0][11] = Net[2][15]
        Net[2][15] = Temp
    elif Move == "U-":
        Temp = Net[0][0]
        Net[0][0] = Net[0][2]
        Net[0][2] = Net[2][2]
        Net[2][2] = Net[2][0]
        Net[2][0] = Temp
        Temp = Net[0][1]
        Net[0][1] = Net[1][2]
        Net[1][2] = Net[2][1]
        Net[2][1] = Net[1][0]
        Net[1][0] = Temp
        Temp = Net[0][3]
        Net[0][3] = Net[2][17]
        Net[2][17] = Net[0][9]
        Net[0][9] = Net[0][6]
        Net[0][6] = Temp
        Temp = Net[0][4]
        Net[0][4] = Net[2][16]
        Net[2][16] = Net[0][10]
        Net[0][10] = Net[0][7]
        Net[0][7] = Temp
        Temp = Net[0][5]
        Net[0][5] = Net[2][15]
        Net[2][15] = Net[0][11]
        Net[0][11] = Net[0][8]
        Net[0][8] = Temp
    elif Move == "D+":
        Temp = Net[0][12]
        Net[0][12] = Net[2][12]
        Net[2][12] = Net[2][14]
        Net[2][14] = Net[0][14]
        Net[0][14] = Temp
        Temp = Net[0][13]
        Net[0][13] = Net[1][12]
        Net[1][12] = Net[2][13]
        Net[2][13] = Net[1][14]
        Net[1][14] = Temp
        Temp = Net[2][3]
        Net[2][3] = Net[0][17]
        Net[0][17] = Net[2][9]
        Net[2][9] = Net[2][6]
        Net[2][6] = Temp
        Temp = Net[2][4]
        Net[2][4] = Net[0][16]
        Net[0][16] = Net[2][10]
        Net[2][10] = Net[2][7]
        Net[2][7] = Temp
        Temp = Net[2][5]
        Net[2][5] = Net[0][15]
        Net[0][15] = Net[2][11]
        Net[2][11] = Net[2][8]
        Net[2][8] = Temp
    elif Move == "D-":
        Temp = Net[0][12]
        Net[0][12] = Net[0][14]
        Net[0][14] = Net[2][14]#found a mistake, changed Net[0][12] to Net[0][14]
        Net[2][14] = Net[2][12]
        Net[2][12] = Temp
        Temp = Net[0][13]
        Net[0][13] = Net[1][14]
        Net[1][14] = Net[2][13]
        Net[2][13] = Net[1][12]
        Net[1][12] = Temp
        Temp = Net[2][3]
        Net[2][3] = Net[2][6]
        Net[2][6] = Net[2][9]
        Net[2][9] = Net[0][17]
        Net[0][17] = Temp
        Temp = Net[2][4]
        Net[2][4] = Net[2][7]
        Net[2][7] = Net[2][10]
        Net[2][10] = Net[0][16]
        Net[0][16] = Temp
        Temp = Net[2][5]
        Net[2][5] = Net[2][8]
        Net[2][8] = Net[2][11]
        Net[2][11] = Net[0][15]
        Net[0][15] = Temp
    elif Move == "L+":
        Temp = Net[0][3]
        Net[0][3] = Net[2][3]
        Net[2][3] = Net[2][5]
        Net[2][5] = Net[0][5]
        Net[0][5] = Temp
        Temp = Net[0][4]
        Net[0][4] = Net[1][3]
        Net[1][3] = Net[2][4]
        Net[2][4] = Net[1][5]
        Net[1][5] = Temp
        Temp = Net[0][0]
        Net[0][0] = Net[0][15]
        Net[0][15] = Net[0][12]
        Net[0][12] = Net[0][6]
        Net[0][6] = Temp
        Temp = Net[1][0]
        Net[1][0] = Net[1][15]
        Net[1][15] = Net[1][12]
        Net[1][12] = Net[1][6]
        Net[1][6] = Temp
        Temp = Net[2][0]
        Net[2][0] = Net[2][15]
        Net[2][15] = Net[2][12]
        Net[2][12] = Net[2][6]
        Net[2][6] = Temp
    elif Move == "L-":
        Temp = Net[0][3]
        Net[0][3] = Net[0][5]
        Net[0][5] = Net[2][5]
        Net[2][5] = Net[2][3]
        Net[2][3] = Temp
        Temp = Net[0][4]
        Net[0][4] = Net[1][5]
        Net[1][5] = Net[2][4]
        Net[2][4] = Net[1][3]
        Net[1][3] = Temp
        Temp = Net[0][0]
        Net[0][0] = Net[0][6]
        Net[0][6] = Net[0][12]
        Net[0][12] = Net[0][15]
        Net[0][15] = Temp
        Temp = Net[1][0]
        Net[1][0] = Net[1][6]
        Net[1][6] = Net[1][12]
        Net[1][12] = Net[1][15]
        Net[1][15] = Temp
        Temp = Net[2][0]
        Net[2][0] = Net[2][6]
        Net[2][6] = Net[2][12]
        Net[2][12] = Net[2][15]
        Net[2][15] = Temp
    elif Move == "R+":
        Temp = Net[0][9]
        Net[0][9] = Net[2][9]
        Net[2][9] = Net[2][11]
        Net[2][11] = Net[0][11]
        Net[0][11] = Temp
        Temp = Net[0][10]
        Net[0][10] = Net[1][9]
        Net[1][9] = Net[2][10]
        Net[2][10] = Net[1][11]
        Net[1][11] = Temp
        Temp = Net[0][2]
        Net[0][2] = Net[0][8]
        Net[0][8] = Net[0][14]
        Net[0][14] = Net[0][17]
        Net[0][17] = Temp
        Temp = Net[1][2]
        Net[1][2] = Net[1][8]
        Net[1][8] = Net[1][14]
        Net[1][14] = Net[1][17]
        Net[1][17] = Temp
        Temp = Net[2][2]
        Net[2][2] = Net[2][8]
        Net[2][8] = Net[2][14]
        Net[2][14] = Net[2][17]
        Net[2][17] = Temp
    elif Move == "R-":
        Temp = Net[0][9]
        Net[0][9] = Net[0][11]
        Net[0][11] = Net[2][11]
        Net[2][11] = Net[2][9]
        Net[2][9] = Temp
        Temp = Net[0][10]
        Net[0][10] = Net[1][11]
        Net[1][11] = Net[2][10]
        Net[2][10] = Net[1][9]
        Net[1][9] = Temp
        Temp = Net[0][2]
        Net[0][2] = Net[0][17]
        Net[0][17] = Net[0][14]
        Net[0][14] = Net[0][8]
        Net[0][8] = Temp
        Temp = Net[1][2]
        Net[1][2] = Net[1][17]
        Net[1][17] = Net[1][14]
        Net[1][14] = Net[1][8]
        Net[1][8] = Temp
        Temp = Net[2][2]
        Net[2][2] = Net[2][17]
        Net[2][17] = Net[2][14]
        Net[2][14] = Net[2][8]
        Net[2][8] = Temp
    elif Move == "F+":
        Temp = Net[0][6]
        Net[0][6] = Net[2][6]
        Net[2][6] = Net[2][8]
        Net[2][8] = Net[0][8]
        Net[0][8] = Temp
        Temp = Net[0][7]
        Net[0][7] = Net[1][6]
        Net[1][6] = Net[2][7]
        Net[2][7] = Net[1][8]
        Net[1][8] = Temp
        Temp = Net[2][0]
        Net[2][0] = Net[2][5]
        Net[2][5] = Net[0][14]
        Net[0][14] = Net[0][9]
        Net[0][9] = Temp
        Temp = Net[2][1]
        Net[2][1] = Net[1][5]
        Net[1][5] = Net[0][13]
        Net[0][13] = Net[1][9]
        Net[1][9] = Temp
        Temp = Net[2][2]
        Net[2][2] = Net[0][5]
        Net[0][5] = Net[0][12]
        Net[0][12] = Net[2][9]
        Net[2][9] = Temp
    elif Move == "F-":
        Temp = Net[0][6]
        Net[0][6] = Net[0][8]
        Net[0][8] = Net[2][8]
        Net[2][8] = Net[2][6]
        Net[2][6] = Temp
        Temp = Net[0][7]
        Net[0][7] = Net[1][8]
        Net[1][8] = Net[2][7]
        Net[2][7] = Net[1][6]
        Net[1][6] = Temp
        Temp = Net[2][0]
        Net[2][0] = Net[0][9]
        Net[0][9] = Net[0][14]
        Net[0][14] = Net[2][5]
        Net[2][5] = Temp
        Temp = Net[2][1]
        Net[2][1] = Net[1][9]
        Net[1][9] = Net[0][13]
        Net[0][13] = Net[1][5]
        Net[1][5] = Temp
        Temp = Net[2][2]
        Net[2][2] = Net[2][9]
        Net[2][9] = Net[0][12]
        Net[0][12] = Net[0][5]
        Net[0][5] = Temp
    elif Move == "B+":
        Temp = Net[0][15]
        Net[0][15] = Net[2][15]
        Net[2][15] = Net[2][17]
        Net[2][17] = Net[0][17]
        Net[0][17] = Temp
        Temp = Net[0][16]
        Net[0][16] = Net[1][15]
        Net[1][15] = Net[2][16]
        Net[2][16] = Net[1][17]
        Net[1][17] = Temp
        Temp = Net[0][0]
        Net[0][0] = Net[0][11]
        Net[0][11] = Net[2][14]
        Net[2][14] = Net[2][3]
        Net[2][3] = Temp
        Temp = Net[0][1]
        Net[0][1] = Net[1][11]
        Net[1][11] = Net[2][13]
        Net[2][13] = Net[1][3]
        Net[1][3] = Temp
        Temp = Net[0][2]
        Net[0][2] = Net[2][11]
        Net[2][11] = Net[2][12]
        Net[2][12] = Net[0][3]
        Net[0][3] = Temp
    elif  Move == "B-":
        Temp = Net[0][15]
        Net[0][15] = Net[0][17]
        Net[0][17] = Net[2][17]
        Net[2][17] = Net[2][15]
        Net[2][15] = Temp
        Temp = Net[0][16]
        Net[0][16] = Net[1][17]
        Net[1][17] = Net[2][16]
        Net[2][16] = Net[1][15]
        Net[1][15] = Temp
        Temp = Net[0][0]
        Net[0][0] = Net[2][3]
        Net[2][3] = Net[2][14]
        Net[2][14] = Net[0][11]
        Net[0][11] = Temp
        Temp = Net[0][1]
        Net[0][1] = Net[1][3]
        Net[1][3] = Net[2][13]
        Net[2][13] = Net[1][11]
        Net[1][11] = Temp
        Temp = Net[0][2]
        Net[0][2] = Net[0][3]
        Net[0][3] = Net[2][12]
        Net[2][12] = Net[2][11]
        Net[2][11] = Temp
    elif Move == "M+":
        Temp = Net[0][1]
        Net[0][1] = Net[0][16]
        Net[0][16] = Net[0][13]
        Net[0][13] = Net[0][7]
        Net[0][7] = Temp
        Temp = Net[1][1]
        Net[1][1] = Net[1][16]
        Net[1][16] = Net[1][13]
        Net[1][13] = Net[1][7]
        Net[1][7] = Temp
        Temp = Net[2][1]
        Net[2][1] = Net[2][16]
        Net[2][16] = Net[2][13]
        Net[2][13] = Net[2][7]
        Net[2][7] = Temp
    elif Move == "M-":
        Temp = Net[0][1]
        Net[0][1] = Net[0][7]
        Net[0][7] = Net[0][13]
        Net[0][13] = Net[0][16]
        Net[0][16] = Temp
        Temp = Net[1][1]
        Net[1][1] = Net[1][7]
        Net[1][7] = Net[1][13]
        Net[1][13] = Net[1][16]
        Net[1][16] = Temp
        Temp = Net[2][1]
        Net[2][1] = Net[2][7]
        Net[2][7] = Net[2][13]
        Net[2][13] = Net[2][16]
        Net[2][16] = Temp
    elif Move == "E+":
        Temp = Net[1][3]
        Net[1][3] = Net[1][17]
        Net[1][17] = Net[1][9]
        Net[1][9] = Net[1][6]
        Net[1][6] = Temp
        Temp = Net[1][4]
        Net[1][4] = Net[1][16]
        Net[1][16] = Net[1][10]
        Net[1][10] = Net[1][7]
        Net[1][7] = Temp
        Temp = Net[1][5]
        Net[1][5] = Net[1][15]
        Net[1][15] = Net[1][11]
        Net[1][11] = Net[1][8]
        Net[1][8] = Temp
    elif Move == "E-":
        Temp = Net[1][3]
        Net[1][3] = Net[1][6]
        Net[1][6] = Net[1][9]
        Net[1][9] = Net[1][17]
        Net[1][17] = Temp
        Temp = Net[1][4]
        Net[1][4] = Net[1][7]
        Net[1][7] = Net[1][10]
        Net[1][10] = Net[1][16]
        Net[1][16] = Temp
        Temp = Net[1][5]
        Net[1][5] = Net[1][8]
        Net[1][8] = Net[1][11]
        Net[1][11] = Net[1][15]
        Net[1][15] = Temp
    elif Move == "S+":
        Temp = Net[1][0]
        Net[1][0] = Net[2][4]
        Net[2][4] = Net[1][14]
        Net[1][14] = Net[0][10]
        Net[0][10] = Temp
        Temp = Net[1][1]
        Net[1][1] = Net[1][4]
        Net[1][4] = Net[1][13]
        Net[1][13] = Net[1][10]
        Net[1][10] = Temp
        Temp = Net[1][2]
        Net[1][2] = Net[0][4]
        Net[0][4] = Net[1][12]
        Net[1][12] = Net[2][10]
        Net[2][10] = Temp
    elif Move == "S-":
        Temp = Net[1][0]
        Net[1][0] = Net[0][10]
        Net[0][10] = Net[1][14]
        Net[1][14] = Net[2][4]
        Net[2][4] = Temp
        Temp = Net[1][1]
        Net[1][1] = Net[1][10]
        Net[1][10] = Net[1][13]
        Net[1][13] = Net[1][4]
        Net[1][4] = Temp
        Temp = Net[1][2]
        Net[1][2] = Net[2][10]
        Net[2][10] = Net[1][12]
        Net[1][12] = Net[0][4]
        Net[0][4] = Temp
    #Moves to rotate layers 180 degrees (double/half rotations)
    elif Move == "U2":
        apply_move_to_net(Net, "U+")
        apply_move_to_net(Net, "U+")
    elif Move == "D2":
        apply_move_to_net(Net, "D+")
        apply_move_to_net(Net, "D+")
    elif Move == "L2":
        apply_move_to_net(Net, "L+")
        apply_move_to_net(Net, "L+")
    elif Move == "R2":
        apply_move_to_net(Net, "R+")
        apply_move_to_net(Net, "R+")
    elif Move == "F2":
        apply_move_to_net(Net, "F+")
        apply_move_to_net(Net, "F+")
    elif Move == "B2":
        apply_move_to_net(Net, "B+")
        apply_move_to_net(Net, "B+")
    elif Move == "M2":
        apply_move_to_net(Net, "M+")
        apply_move_to_net(Net, "M+")
    elif Move == "E2":
        apply_move_to_net(Net, "E+")
        apply_move_to_net(Net, "E+")
    elif Move == "S2":
        apply_move_to_net(Net, "S+")
        apply_move_to_net(Net, "S+")
    #Moves to rotate the whole cube 90 degrees about x,y,z axes
    elif Move == "X+":
        apply_move_to_net(Net, "R+")
        apply_move_to_net(Net, "M-")
        apply_move_to_net(Net, "L-")
    elif Move == "X-":
        apply_move_to_net(Net, "R-")
        apply_move_to_net(Net, "M+")
        apply_move_to_net(Net, "L+")
    elif Move == "Y+":
        apply_move_to_net(Net, "U+")
        apply_move_to_net(Net, "E-")
        apply_move_to_net(Net, "D-")
    elif Move == "Y-":
        apply_move_to_net(Net, "U-")
        apply_move_to_net(Net, "E+")
        apply_move_to_net(Net, "D+")
    elif Move == "Z+":
        apply_move_to_net(Net, "F+")
        apply_move_to_net(Net, "S+")
        apply_move_to_net(Net, "B-")
    elif Move == "Z-":
        apply_move_to_net(Net, "F-")
        apply_move_to_net(Net, "S-")
        apply_move_to_net(Net, "B+")
    elif Move == "X2":
        apply_move_to_net(Net, "R2")
        apply_move_to_net(Net, "M2")
        apply_move_to_net(Net, "L2")
    elif Move == "Y2":
        apply_move_to_net(Net, "U2")
        apply_move_to_net(Net, "E2")
        apply_move_to_net(Net, "D2")
    elif Move == "Z2":
        apply_move_to_net(Net, "F2")
        apply_move_to_net(Net, "S2")
        apply_move_to_net(Net, "B2")
    return Net
