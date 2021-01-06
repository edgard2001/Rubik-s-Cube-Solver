from Net import *

class Solver:
    EdgeTileCoords = (
    (0,1), (0,4), (0,7), (0,10), (0,13), (0,16),
    (1,0), (1,2), (1,3), (1,5), (1,6), (1,8),
    (1,9), (1,11), (1,12), (1,14), (1,15), (1,17),
    (2,1), (2,4), (2,7), (2,10), (2,13), (2,16)
    )
    
    AdjancentEdgeTiles = {
    0:(2,16), 1:(1,0), 2:(2,1), 3:(1,2),
    4:(2,7), 5:(2,13), 6:(0,4), 7:(0,10),
    8:(1,15), 9:(1,6), 10:(1,5), 11:(1,9),
    12:(1,8), 13:(1,17), 14:(2,4), 15:(2,10),
    16:(1,3), 17:(1,11), 18:(0,7), 19:(1,12),
    20:(0,13), 21:(1,14), 22:(0,16), 23:(0,1)
    }

    CornerTileCoords = (
    (0,0), (0,2), (0,3), (0,5), (0,6), (0,8),
    (0,9), (0,11), (0,12), (0,14), (0,15), (0,17),
    (2,0), (2,2), (2,3), (2,5), (2,6), (2,8),
    (2,9), (2,11), (2,12), (2,14), (2,15), (2,17)
    )
    
    AdjacentCornerTiles = (
    (3,4,12), (5,6,13), (8,15,16), (9,17,18),
    (10,14,20), (11,19,21), (0,2,22), (1,7,23)
    )
    
    def __init__(self, Net):
        self._Net = set_net(Net)
        
    def find_edge_position(self, Colour1, Colour2):
        for CoordIndex, Colour1Coord in enumerate(Solver.EdgeTileCoords):
            Row = Colour1Coord[0]
            Column = Colour1Coord[1]
            if self._Net[Row][Column] == Colour1:
                Colour2Coord = Solver.AdjancentEdgeTiles[CoordIndex]
                Row = Colour2Coord[0]
                Column = Colour2Coord[1]       
                if self._Net[Row][Column] == Colour2:
                    return Colour1Coord, Colour2Coord
                
    def find_corner_position(self, Colour1, Colour2, Colour3):
        for CoordIndex, Colour1Coord in enumerate(Solver.CornerTileCoords):
            Row = Colour1Coord[0]
            Column = Colour1Coord[1]
            if self._Net[Row][Column] == Colour1:
                for TileIndexesTuple in Solver.AdjacentCornerTiles:
                    if CoordIndex in TileIndexesTuple:
                        Remaining2Tiles = list(TileIndexesTuple)
                        Remaining2Tiles.remove(CoordIndex)
                        Colour2Coord = Solver.CornerTileCoords[Remaining2Tiles[0]]
                        Colour3Coord = Solver.CornerTileCoords[Remaining2Tiles[1]]
                        Row = Colour2Coord[0]
                        Column = Colour2Coord[1]
                        if self._Net[Row][Column] == Colour2:
                            Row = Colour3Coord[0]
                            Column = Colour3Coord[1]
                            if self._Net[Row][Column] == Colour3:
                                return Colour1Coord, Colour2Coord, Colour3Coord
                        Colour2Coord = Solver.CornerTileCoords[Remaining2Tiles[1]]
                        Colour3Coord = Solver.CornerTileCoords[Remaining2Tiles[0]]
                        Row = Colour2Coord[0]
                        Column = Colour2Coord[1]
                        if self._Net[Row][Column] == Colour2:
                            Row = Colour3Coord[0]
                            Column = Colour3Coord[1]
                            if self._Net[Row][Column] == Colour3:
                                return Colour1Coord, Colour2Coord, Colour3Coord
                            
    def solve_one_upper_edge(self):
        Colour1 = self._Net[1][1]
        Colour2 = self._Net[1][7]
        Colour1Coord, Colour2Coord = self.find_edge_position(Colour1,Colour2)
        
        if Colour1Coord[1] in (0,1,2):
            if Colour1Coord[1] == 0:
                Algorithm = ["L2","D+","F2"]
            elif Colour1Coord[1] == 1:
                if Colour1Coord[0] == 0:
                    Algorithm = ["B2","D2","F2"]
                else:
                    Algorithm = []
            else:
                Algorithm = ["R2","D-","F2"]
                    
        elif Colour1Coord[1] in (3,4,5):
            if Colour1Coord[1] == 3:
                Algorithm = ["L2","F+","L2"]
            elif Colour1Coord[1] == 4:
                if Colour1Coord[0] == 0:
                    Algorithm = ["L+","F+"]
                else:
                    Algorithm = ["L-","F+","L+"]
            else:
                Algorithm = ["F+"]

        elif Colour1Coord[1] in (6,7,8):
            if Colour1Coord[1] == 6:
                Algorithm = ["U+","L-","U-"]
            elif Colour1Coord[1] == 7:
                if Colour1Coord[0] == 0:
                    Algorithm = ["F+","U-","R+","U+"]
                else:
                    Algorithm = ["F-","U-","R+","U+"]
            else:
                Algorithm = ["U-","R+","U+"]
                
        elif Colour1Coord[1] in (9,10,11):
            if Colour1Coord[1] == 9:
                Algorithm = ["F-"]
            elif Colour1Coord[1] == 10:
                if Colour1Coord[0] == 0:
                    Algorithm = ["R-","F-"]
                else:
                    Algorithm = ["R+","F-","R-"]
            else:
                Algorithm = ["R2","F-","R2"]

        elif Colour1Coord[1] in (12,13,14):
            if Colour1Coord[1] == 12:
                Algorithm = ["D+","F2"]
            elif Colour1Coord[1] == 13:
                if Colour1Coord[0] == 0:
                    Algorithm = ["F2"]
                else:
                    Algorithm = ["D2","F2"]
            else:
                Algorithm = ["D-","F2"] 
        else:
            if Colour1Coord[1] == 15:
                Algorithm = ["U+","L+","U-"]
            elif Colour1Coord[1] == 16:
                if Colour1Coord[0] == 0:
                    Algorithm = ["D-","R+","F-","R-"]
                else:
                    Algorithm = ["B-","U-","R-","U+"]
            else:
                Algorithm = ["R+","D-","R-","F2"]
        for Move in Algorithm:
            self._Net = apply_move_to_net(self._Net, Move)
        return Algorithm

    def solve_upper_cross(self):
        Algorithm = []
        Algorithm += self.solve_one_upper_edge()
        for Edge in range(3):
            Algorithm.append("Y+")
            self._Net = apply_move_to_net(self._Net, "Y+")
            Algorithm += self.solve_one_upper_edge()
        return Algorithm

    def solve_one_upper_corner(self):
        Colour1 = self._Net[1][1]
        Colour2 = self._Net[1][7]
        Colour3 = self._Net[1][10]
        Colour1Coord,Colour2Coord,Colour3Coord = self.find_corner_position(Colour1,Colour2,Colour3)
        if Colour1Coord[1] in (0,2):
            if Colour1Coord[1] == 0:
                if Colour1Coord[0] == 0:
                    Algorithm = ["L-","D2","L+","F+","D+","F-"]
                else:
                    Algorithm = ["L+","D+","L-","R-","D-","R+"]
            else:
                if Colour1Coord[0] == 0:
                    Algorithm = ["B-","D-","B+","F+","D+","F-"]
                else:
                    Algorithm = []
        elif Colour1Coord[1] in (3,5):
            if Colour1Coord[1] == 3:
                if Colour1Coord[0] == 0:
                    Algorithm = ["L-","D2","L+","R-","D-","R+"]
                else:
                    Algorithm = ["D2","R-","D-","R+"]
            else:
                if Colour1Coord[0] == 0:
                    Algorithm = ["L+","D+","L-","F+","D+","F-"]
                else:
                    Algorithm = ["D+","F+","D+","F-"]
        elif Colour1Coord[1] in (6,8):
            if Colour1Coord[1] == 6:
                if Colour1Coord[0] == 0:
                    Algorithm = ["F-","D-","F2","D2","F-"]
                else:
                    Algorithm = ["D+","R-","D-","R+"]
            else:
                if Colour1Coord[0] == 0:
                    Algorithm = ["F+","D+","F-","D-","F+","D+","F-"]
                else:
                    Algorithm = ["F+","D+","F-"]
        elif Colour1Coord[1] in (9,11):
            if Colour1Coord[1] == 9:
                if Colour1Coord[0] == 0:
                    Algorithm = ["R-","D-","R+","D+","R-","D-","R+"]
                else:
                    Algorithm = ["R-","D-","R+"]
            else:
                if Colour1Coord[0] == 0:
                    Algorithm = ["R+","D+","R2","D2","R+"]
                else:
                    Algorithm = ["D-","F+","D+","F-"]
        elif Colour1Coord[1] in (12,14):
            if Colour1Coord[1] == 12:
                if Colour1Coord[0] == 0:
                    Algorithm = ["D+","R-","D2","R+","D+","R-","D-","R+"]
                else:
                    Algorithm = ["D2","R-","D2","R+","D+","R-","D-","R+"]
            else:
                if Colour1Coord[0] == 0:
                    Algorithm = ["R-","D2","R+","D+","R-","D-","R+"]
                else:
                    Algorithm = ["D-","R-","D2","R+","D+","R-","D-","R+"]
        else:
            if Colour1Coord[1] == 15:
                if Colour1Coord[0] == 0:
                    Algorithm = ["D2","F+","D+","F-"]
                else:
                    Algorithm = ["B+","D2","B-","F+","D+","F-"]
            else:
                if Colour1Coord[0] == 0:
                    Algorithm = ["D-","R-","D-","R+"]
                else:
                    Algorithm = ["B-","D-","B+","R-","D-","R+"]
        for Move in Algorithm:
            self._Net = apply_move_to_net(self._Net, Move)
        return Algorithm

    def solve_all_upper_corners(self):
        Algorithm = []
        Algorithm += self.solve_one_upper_corner()
        for Corner in range(3):
            Algorithm.append("Y+")
            self._Net = apply_move_to_net(self._Net, "Y+")
            Algorithm += self.solve_one_upper_corner()
        return Algorithm

    def solve_one_middle_edge(self):
        Colour1 = self._Net[1][7]
        Colour2 = self._Net[1][10]
        
        Colour1Coord, Colour2Coord = self.find_edge_position(Colour1,Colour2)
        
        if Colour1Coord[1] in (3,5):
            if Colour1Coord[1] == 3:
                AlgorithmPart1 = ["B+","D-","B-","D-","L-","D+","L+"]
            else:
                AlgorithmPart1 = ["L+","D-","L-","D-","F-","D+","F+"]
        elif Colour1Coord[1] in (6,8):
            if Colour1Coord[1] == 6:
                AlgorithmPart1 = ["L+","D-","L-","D-","F-","D+","F+"]
            else:
                AlgorithmPart1 = []
        elif Colour1Coord[1] in (9,11):
            if Colour1Coord[1] == 9:
                AlgorithmPart1 = ["R-","D+","R+","D+","F+","D-","F-"]
            else:
                AlgorithmPart1 = ["B-","D+","B+","D+","R+","D-","R-"]
        elif Colour1Coord[1] in (15,17):
            if Colour1Coord[1] == 15:
                AlgorithmPart1 = ["B+","D-","B-","D-","L-","D+","L+"]
            else:
                AlgorithmPart1 = ["B-","D+","B+","D+","R+","D-","R-"]
        else:
            AlgorithmPart1 = []
        
        for Move in AlgorithmPart1:
            self._Net = apply_move_to_net(self._Net, Move)
        
        Colour1Coord, Colour2Coord = self.find_edge_position(Colour1,Colour2)
        
        if Colour1Coord[1] in (4,7,10,16):
            if Colour1Coord[1] == 4:
                AlgorithmPart2 = ["R-","D+","R+","D+","F+","D-","F-"]
            elif Colour1Coord[1] == 7:
                AlgorithmPart2 = ["D-","R-","D+","R+","D+","F+","D-","F-"]
            elif Colour1Coord[1] == 10:
                AlgorithmPart2 = ["D2","R-","D+","R+","D+","F+","D-","F-"]
            else:
                AlgorithmPart2 = ["D+","R-","D+","R+","D+","F+","D-","F-"]
        elif Colour1Coord[1] in (12,13,14):
            if Colour1Coord[1] == 12:
                AlgorithmPart2 = ["D-","F+","D-","F-","D-","R-","D+","R+"]
            elif Colour1Coord[1] == 13:
                if Colour1Coord[0] == 0:
                    AlgorithmPart2 = ["D2","F+","D-","F-","D-","R-","D+","R+"]
                else:
                    AlgorithmPart2 = ["F+","D-","F-","D-","R-","D+","R+"]
            else:
                AlgorithmPart2 = ["D+","F+","D-","F-","D-","R-","D+","R+"]
        else:
            AlgorithmPart2 = []
                
        for Move in AlgorithmPart2:
            self._Net = apply_move_to_net(self._Net, Move)

        return AlgorithmPart1 + AlgorithmPart2
        
    def solve_middle_edges(self):
        Algorithm = []
        Algorithm += self.solve_one_middle_edge()
        for Corner in range(3):
            Algorithm.append("Y+")
            self._Net = apply_move_to_net(self._Net, "Y+")
            Algorithm += self.solve_one_middle_edge()
        return Algorithm

    def dot_on_bottom(self):
        return ( (self._Net[0][4] == self._Net[1][1]) and \
               (self._Net[0][7] == self._Net[1][1]) and \
               (self._Net[0][10] == self._Net[1][1]) and \
               (self._Net[2][16] == self._Net[1][1]) )
    
    def L_on_bottom(self):
        return ( (self._Net[0][1] == self._Net[1][1]) and \
               (self._Net[1][0] == self._Net[1][1]) and \
               (self._Net[0][7] == self._Net[1][1]) and \
               (self._Net[0][10] == self._Net[1][1]) )
    
    def line_on_bottom(self):
        return ( (self._Net[1][0] == self._Net[1][1]) and \
               (self._Net[1][2] == self._Net[1][1]) and \
               (self._Net[0][7] == self._Net[1][1]) and \
               (self._Net[2][16] == self._Net[1][1]) )
    
    def cross_on_bottom(self):
        return ( (self._Net[0][1] == self._Net[1][1]) and \
               (self._Net[1][0] == self._Net[1][1]) and \
               (self._Net[1][2] == self._Net[1][1]) and \
               (self._Net[2][1] == self._Net[1][1]) )

    def solve_bottom_cross(self):
        Algorithm = []
        Algorithm.append("X2")
        self._Net = apply_move_to_net(self._Net, "X2")
        while self.cross_on_bottom() != True:
            if self.dot_on_bottom() == True:
                AlgorithmPart = ["F+","U+","R+","U-","R-","F-"]
                Algorithm += AlgorithmPart
                for Move in AlgorithmPart:
                    self._Net = apply_move_to_net(self._Net, Move)
            elif self.L_on_bottom() == True:
                AlgorithmPart = ["F+","U+","R+","U-","R-","F-"]
                Algorithm += AlgorithmPart
                for Move in AlgorithmPart:
                    self._Net = apply_move_to_net(self._Net, Move)
            elif self.line_on_bottom():
                AlgorithmPart = ["F+","R+","U+","R-","U-","F-"]
                Algorithm += AlgorithmPart
                for Move in AlgorithmPart:
                    self._Net = apply_move_to_net(self._Net, Move)
            else:
                Algorithm.append("Y+")
                self._Net = apply_move_to_net(self._Net, "Y+")
        return Algorithm 

    def bottom_edges_permuted(self):
        LeftEdgeTileColour = self._Net[0][4]
        FrontEdgeTileColour = self._Net[0][7]
        RightEdgeTileColour = self._Net[0][10]
        BackEdgeTileColour = self._Net[2][16]

        EdgeCombination = (LeftEdgeTileColour,
                           FrontEdgeTileColour,
                           RightEdgeTileColour,
                           BackEdgeTileColour)
        
        LeftCentreColour = self._Net[1][4]
        FrontCentreColour = self._Net[1][7]
        RightCentreColour = self._Net[1][10]
        BackCentreColour = self._Net[1][16]
        
        PossibleEdgeCombinations = ( (LeftCentreColour,
                                    FrontCentreColour,
                                    RightCentreColour,
                                    BackCentreColour),
                                           
                                    (FrontCentreColour,
                                    RightCentreColour,
                                    BackCentreColour,
                                    LeftCentreColour),
                                           
                                    (RightCentreColour,
                                    BackCentreColour,
                                    LeftCentreColour,
                                    FrontCentreColour),
                                           
                                    (BackCentreColour,
                                    LeftCentreColour,
                                    FrontCentreColour,
                                    RightCentreColour) )
        
        return (EdgeCombination in PossibleEdgeCombinations)

    def swap_opposite_bottom_edges(self):
        LeftEdgeTileColour = self._Net[0][4]
        FrontEdgeTileColour = self._Net[0][7]
        RightEdgeTileColour = self._Net[0][10]
        BackEdgeTileColour = self._Net[2][16]

        EdgeCombination = (LeftEdgeTileColour,
                           FrontEdgeTileColour,
                           RightEdgeTileColour,
                           BackEdgeTileColour)

        LeftCentreColour = self._Net[1][4]
        FrontCentreColour = self._Net[1][7]
        RightCentreColour = self._Net[1][10]
        BackCentreColour = self._Net[1][16]
        
        PossibleEdgeCombinations = ( (RightCentreColour,
                                    FrontCentreColour,
                                    LeftCentreColour,
                                    BackCentreColour),
                                           
                                    (FrontCentreColour,
                                    LeftCentreColour,
                                    BackCentreColour,
                                    RightCentreColour),
                                           
                                    (LeftCentreColour,
                                    BackCentreColour,
                                    RightCentreColour,
                                    FrontCentreColour),
                                           
                                    (BackCentreColour,
                                    RightCentreColour,
                                    FrontCentreColour,
                                    LeftCentreColour) )
        
        return (EdgeCombination in PossibleEdgeCombinations)

    def swap_adjacent_bottom_edges(self):
        LeftEdgeTileColour = self._Net[0][4]
        FrontEdgeTileColour = self._Net[0][7]
        RightEdgeTileColour = self._Net[0][10]
        BackEdgeTileColour = self._Net[2][16]

        EdgeCombination = (LeftEdgeTileColour,
                           FrontEdgeTileColour,
                           RightEdgeTileColour,
                           BackEdgeTileColour)

        LeftCentreColour = self._Net[1][4]
        FrontCentreColour = self._Net[1][7]
        RightCentreColour = self._Net[1][10]
        BackCentreColour = self._Net[1][16]
        
        PossibleEdgeCombinations = ( (FrontCentreColour,
                                    LeftCentreColour,
                                    RightCentreColour,
                                    BackCentreColour),
                                           
                                    (LeftCentreColour,
                                    RightCentreColour,
                                    BackCentreColour,
                                    FrontCentreColour),
                                           
                                    (RightCentreColour,
                                    BackCentreColour,
                                    FrontCentreColour,
                                    LeftCentreColour),
                                           
                                    (BackCentreColour,
                                    FrontCentreColour,
                                    LeftCentreColour,
                                    RightCentreColour) )
        
        return (EdgeCombination in PossibleEdgeCombinations)

    def bottom_edges_solved(self):
        LeftEdgeTileColour = self._Net[0][4]
        FrontEdgeTileColour = self._Net[0][7]
        RightEdgeTileColour = self._Net[0][10]
        BackEdgeTileColour = self._Net[2][16]

        EdgeCombination = (LeftEdgeTileColour,
                           FrontEdgeTileColour,
                           RightEdgeTileColour,
                           BackEdgeTileColour)
        
        LeftCentreColour = self._Net[1][4]
        FrontCentreColour = self._Net[1][7]
        RightCentreColour = self._Net[1][10]
        BackCentreColour = self._Net[1][16]
        
        RequiredEdgeCombination = (LeftCentreColour,
                                    FrontCentreColour,
                                    RightCentreColour,
                                    BackCentreColour)
        
        return (EdgeCombination == RequiredEdgeCombination)
    
    def permute_bottom_edges(self):
        Algorithm = []
        while self.bottom_edges_permuted() != True:
            if self.swap_adjacent_bottom_edges() == True:
                AlgorithmPart = ["R+","U+","R-","U+","R+","U2","R-","U+"]
                Algorithm += AlgorithmPart
                for Move in AlgorithmPart:
                    self._Net = apply_move_to_net(self._Net, Move)
            elif self.swap_opposite_bottom_edges() == True:
                AlgorithmPart = ["U+","R+","U+","R-","U+","R+","U2","R-","U+",
                                 "Y2","R+","U+","R-","U+","R+","U2","R-","U+"]
                Algorithm += AlgorithmPart
                for Move in AlgorithmPart:
                    self._Net = apply_move_to_net(self._Net, Move)
            else:
                Algorithm.append("Y+")
                self._Net = apply_move_to_net(self._Net, "Y+")
        while self.bottom_edges_solved() != True:
            Algorithm.append("U+")
            self._Net = apply_move_to_net(self._Net, "U+")
        return Algorithm

    def bottom_corners_permuted(self):
        Colour1 = self._Net[1][1]
        MiddleLayerCentreColours = (self._Net[1][7],
                                    self._Net[1][10],
                                    self._Net[1][16],
                                    self._Net[1][4])
        CornersPermuted = 0
        Row = ((2,0,0),#1
               (0,0,2),#2
               (0,2,0),#3
               (2,0,0))#4
        Column = ((2,8,9),#1
                  (2,11,17),#2
                  (0,15,3),#3
                  (0,5,6))#4
        Index = 0
        for Colour2Pointer, Colour3Pointer in ( (0,1),(1,2),(2,3),(3,0) ):
            Colour2 = MiddleLayerCentreColours[Colour2Pointer]
            Colour3 = MiddleLayerCentreColours[Colour3Pointer]
            CornerColours = (Colour1,
                             Colour2,
                             Colour3)
            for (i,j,k) in ((0,1,2),(2,0,1),(1,2,0)):
                if (self._Net[Row[Index][0]][Column[Index][0]] == CornerColours[i]) and \
                   (self._Net[Row[Index][1]][Column[Index][1]] == CornerColours[j]) and \
                   (self._Net[Row[Index][2]][Column[Index][2]] == CornerColours[k]):
                    CornersPermuted += 1
            Index += 1
        return (CornersPermuted == 4)
        
        
        
    def clockwise_bottom_corner_swap(self):
        Colour1 = self._Net[1][1]
        MiddleLayerCentreColours = (self._Net[1][7],
                                    self._Net[1][10],
                                    self._Net[1][16],
                                    self._Net[1][4])
        CornersPermuted = 0
        Row = ((2,0,0),#1
               (0,0,2),#2
               (0,2,0),#3
               (2,0,0))#4
        Column = ((2,8,9),#1
                  (2,11,17),#2
                  (0,15,3),#3
                  (0,5,6))#4
        Index = 0
        for Colour2Pointer, Colour3Pointer in ( (0,1),(3,0),(1,2),(2,3) ):
            Colour2 = MiddleLayerCentreColours[Colour2Pointer]
            Colour3 = MiddleLayerCentreColours[Colour3Pointer]
            CornerColours = (Colour1,
                             Colour2,
                             Colour3)

            for (i,j,k) in ((0,1,2),(2,0,1),(1,2,0)):
                if (self._Net[Row[Index][0]][Column[Index][0]] == CornerColours[i]) and \
                   (self._Net[Row[Index][1]][Column[Index][1]] == CornerColours[j]) and \
                   (self._Net[Row[Index][2]][Column[Index][2]] == CornerColours[k]):
                    CornersPermuted += 1
            Index += 1
        return (CornersPermuted == 4)
    
    def anticlockwise_bottom_corner_swap(self):
        Colour1 = self._Net[1][1]
        MiddleLayerCentreColours = (self._Net[1][7],
                                    self._Net[1][10],
                                    self._Net[1][16],
                                    self._Net[1][4])
        CornersPermuted = 0
        Row = ((2,0,0),#1
               (0,0,2),#2
               (0,2,0),#3
               (2,0,0))#4
        Column = ((2,8,9),#1
                  (2,11,17),#2
                  (0,15,3),#3
                  (0,5,6))#4
        Index = 0
        for Colour2Pointer, Colour3Pointer in ( (0,1),(2,3),(3,0),(1,2) ):
            Colour2 = MiddleLayerCentreColours[Colour2Pointer]
            Colour3 = MiddleLayerCentreColours[Colour3Pointer]
            CornerColours = (Colour1,
                             Colour2,
                             Colour3)
            for (i,j,k) in ((0,1,2),(2,0,1),(1,2,0)):
                if (self._Net[Row[Index][0]][Column[Index][0]] == CornerColours[i]) and \
                   (self._Net[Row[Index][1]][Column[Index][1]] == CornerColours[j]) and \
                   (self._Net[Row[Index][2]][Column[Index][2]] == CornerColours[k]):
                    CornersPermuted += 1
            Index += 1
        return (CornersPermuted == 4)

    def permute_bottom_corners(self):
        Algorithm = []
        if self.bottom_corners_permuted() != True:
            
            if self.clockwise_bottom_corner_swap() != True and \
               self.anticlockwise_bottom_corner_swap() != True:
                Algorithm.append("Y+")
                self._Net = apply_move_to_net(self._Net, "Y+")
            if self.clockwise_bottom_corner_swap() != True and \
               self.anticlockwise_bottom_corner_swap() != True:
                Algorithm.append("Y+")
                self._Net = apply_move_to_net(self._Net, "Y+")
            if self.clockwise_bottom_corner_swap() != True and \
               self.anticlockwise_bottom_corner_swap() != True:
                Algorithm.append("Y+")
                self._Net = apply_move_to_net(self._Net, "Y+")
                
            if self.clockwise_bottom_corner_swap() != True and \
               self.anticlockwise_bottom_corner_swap() != True:
                AlgorithmPart = ["U+","R+","U-","L-","U+","R-","U-","L+"]
                Algorithm += AlgorithmPart
                for Move in AlgorithmPart:
                    self._Net = apply_move_to_net(self._Net, Move)
                    
            if self.clockwise_bottom_corner_swap() != True and \
               self.anticlockwise_bottom_corner_swap() != True:
                Algorithm.append("Y+")
                self._Net = apply_move_to_net(self._Net, "Y+")
            if self.clockwise_bottom_corner_swap() != True and \
               self.anticlockwise_bottom_corner_swap() != True:
                Algorithm.append("Y+")
                self._Net = apply_move_to_net(self._Net, "Y+")
            if self.clockwise_bottom_corner_swap() != True and \
               self.anticlockwise_bottom_corner_swap() != True:
                Algorithm.append("Y+")
                self._Net = apply_move_to_net(self._Net, "Y+")
                
            if self.clockwise_bottom_corner_swap() == True:
                AlgorithmPart = ["L-","U+","R+","U-","L+","U+","R-","U-"]
                Algorithm += AlgorithmPart
                for Move in AlgorithmPart:
                    self._Net = apply_move_to_net(self._Net, Move)
            elif self.anticlockwise_bottom_corner_swap() == True:
                AlgorithmPart = ["U+","R+","U-","L-","U+","R-","U-","L+"]
                Algorithm += AlgorithmPart
                for Move in AlgorithmPart:
                    self._Net = apply_move_to_net(self._Net, Move)
                    
        return Algorithm

    def last_layer_solved(self):
        return ( (self._Net[0][0] == self._Net[1][1]) and \
               (self._Net[0][2] == self._Net[1][1]) and \
               (self._Net[2][0] == self._Net[1][1]) and \
               (self._Net[2][2] == self._Net[1][1]) and \
               (self._Net[0][3] == self._Net[1][4]) )
    
    def orientate_bottom_corners(self):
        Algorithm = []
        while self.last_layer_solved() != True:
            if self._Net[2][2] == self._Net[1][1]:
                Algorithm.append("U+")
                self._Net = apply_move_to_net(self._Net, "U+")
            else:
                if self._Net[0][8] == self._Net[1][1]:
                    AlgorithmPart = ["R+","F-","R-","F+","R+","F-","R-","F+","U+"]
                    Algorithm += AlgorithmPart
                    for Move in AlgorithmPart:
                        self._Net = apply_move_to_net(self._Net, Move)
                else:
                    AlgorithmPart = ["F-","R+","F+","R-","F-","R+","F+","R-","U+"]
                    Algorithm += AlgorithmPart
                    for Move in AlgorithmPart:
                        self._Net = apply_move_to_net(self._Net, Move)
        return Algorithm

    def remove_adjacent_inverse_moves(self, SolutionString):
        SolutionString = SolutionString.replace("U+U-","")
        SolutionString = SolutionString.replace("U-U+","")
        SolutionString = SolutionString.replace("D+D-","")
        SolutionString = SolutionString.replace("D-D+","")
        SolutionString = SolutionString.replace("L+L-","")
        SolutionString = SolutionString.replace("L-L+","")
        SolutionString = SolutionString.replace("R+R-","")
        SolutionString = SolutionString.replace("R-R+","")
        SolutionString = SolutionString.replace("F+F-","")
        SolutionString = SolutionString.replace("F-F+","")
        SolutionString = SolutionString.replace("B+B-","")
        SolutionString = SolutionString.replace("B-B+","")
        return SolutionString
        
    def replace_consequent_single_turns(self, SolutionString):
        SolutionString = SolutionString.replace("Y+Y+Y+","Y-")
        SolutionString = SolutionString.replace("Y+Y+","Y2")
        SolutionString = SolutionString.replace("U+U+U+","U-")
        SolutionString = SolutionString.replace("U+U+","U2")
        SolutionString = SolutionString.replace("D+D+D+","D-")
        SolutionString = SolutionString.replace("D+D+","D2")
        SolutionString = SolutionString.replace("L+L+L+","L-")
        SolutionString = SolutionString.replace("L+L+","L2")
        SolutionString = SolutionString.replace("R+R+R+","R-")
        SolutionString = SolutionString.replace("R+R+","R2")
        SolutionString = SolutionString.replace("F+F+F+","F-")
        SolutionString = SolutionString.replace("F+F+","F2")
        SolutionString = SolutionString.replace("B+B+B+","B-")
        SolutionString = SolutionString.replace("B+B+","B2")
        
        SolutionString = SolutionString.replace("U-U-U-","U+")
        SolutionString = SolutionString.replace("U-U-","U2")
        SolutionString = SolutionString.replace("D-D-D-","D+")
        SolutionString = SolutionString.replace("D-D-","D2")
        SolutionString = SolutionString.replace("L-L-L-","L+")
        SolutionString = SolutionString.replace("L-L-","L2")
        SolutionString = SolutionString.replace("R-R-R-","R+")
        SolutionString = SolutionString.replace("R-R-","R2")
        SolutionString = SolutionString.replace("F-F-F-","F+")
        SolutionString = SolutionString.replace("F-F-","F2")
        SolutionString = SolutionString.replace("B-B-B-","B+")
        SolutionString = SolutionString.replace("B-B-","B2")

        
        return SolutionString

    def remove_cube_rotations(self, SolutionString):
        Index = 1
        ReversedSolution = SolutionString[::-1]
        while ( ReversedSolution.count("X") != 0 or \
              ReversedSolution.count("Y") != 0 or \
              ReversedSolution.count("Z") != 0 ) and\
              Index < len(SolutionString):
            if ReversedSolution[Index-1:Index+1] == "+Y":
                for CharIndex, Char in enumerate(ReversedSolution[0:Index-1]):
                    if Char == "L":
                        ReversedSolution = ReversedSolution[:CharIndex] + "F" + ReversedSolution[CharIndex+1:]
                    elif Char == "R":
                        ReversedSolution = ReversedSolution[:CharIndex] + "B" + ReversedSolution[CharIndex+1:]
                    elif Char == "F":
                        ReversedSolution = ReversedSolution[:CharIndex] + "R" + ReversedSolution[CharIndex+1:]
                    elif Char == "B":
                        ReversedSolution = ReversedSolution[:CharIndex] + "L" + ReversedSolution[CharIndex+1:]
                ReversedSolution = ReversedSolution[:Index-1] + ReversedSolution[Index+1:]
            elif ReversedSolution[Index-1:Index+1] == "-Y":
                for CharIndex, Char in enumerate(ReversedSolution[0:Index-1]):
                    if Char == "L":
                        ReversedSolution = ReversedSolution[:CharIndex] + "B" + ReversedSolution[CharIndex+1:]
                    elif Char == "R":
                        ReversedSolution = ReversedSolution[:CharIndex] + "F" + ReversedSolution[CharIndex+1:]
                    elif Char == "F":
                        ReversedSolution = ReversedSolution[:CharIndex] + "L" + ReversedSolution[CharIndex+1:]
                    elif Char == "B":
                        ReversedSolution = ReversedSolution[:CharIndex] + "R" + ReversedSolution[CharIndex+1:]
                ReversedSolution = ReversedSolution[:Index-1] + ReversedSolution[Index+1:]
            elif ReversedSolution[Index-1:Index+1] == "2Y":
                for CharIndex, Char in enumerate(ReversedSolution[0:Index-1]):
                    if Char == "L":
                        ReversedSolution = ReversedSolution[:CharIndex] + "R" + ReversedSolution[CharIndex+1:]
                    elif Char == "R":
                        ReversedSolution = ReversedSolution[:CharIndex] + "L" + ReversedSolution[CharIndex+1:]
                    elif Char == "F":
                        ReversedSolution = ReversedSolution[:CharIndex] + "B" + ReversedSolution[CharIndex+1:]
                    elif Char == "B":
                        ReversedSolution = ReversedSolution[:CharIndex] + "F" + ReversedSolution[CharIndex+1:]
                ReversedSolution = ReversedSolution[:Index-1] + ReversedSolution[Index+1:]
            elif ReversedSolution[Index-1:Index+1] == "2X":
                for CharIndex, Char in enumerate(ReversedSolution[0:Index-1]):
                    if Char == "U":
                        ReversedSolution = ReversedSolution[:CharIndex] + "D" + ReversedSolution[CharIndex+1:]
                    elif Char == "D":
                        ReversedSolution = ReversedSolution[:CharIndex] + "U" + ReversedSolution[CharIndex+1:]
                    elif Char == "F":
                        ReversedSolution = ReversedSolution[:CharIndex] + "B" + ReversedSolution[CharIndex+1:]
                    elif Char == "B":
                        ReversedSolution = ReversedSolution[:CharIndex] + "F" + ReversedSolution[CharIndex+1:]
                ReversedSolution = ReversedSolution[:Index-1] + ReversedSolution[Index+1:]
            elif ReversedSolution[Index-1:Index+1] == "+X":
                for CharIndex, Char in enumerate(ReversedSolution[0:Index-1]):
                    if Char == "U":
                        ReversedSolution = ReversedSolution[:CharIndex] + "F" + ReversedSolution[CharIndex+1:]
                    elif Char == "D":
                        ReversedSolution = ReversedSolution[:CharIndex] + "B" + ReversedSolution[CharIndex+1:]
                    elif Char == "F":
                        ReversedSolution = ReversedSolution[:CharIndex] + "D" + ReversedSolution[CharIndex+1:]
                    elif Char == "B":
                        ReversedSolution = ReversedSolution[:CharIndex] + "U" + ReversedSolution[CharIndex+1:]
                ReversedSolution = ReversedSolution[:Index-1] + ReversedSolution[Index+1:]
            elif ReversedSolution[Index-1:Index+1] == "+Z":
                for CharIndex, Char in enumerate(ReversedSolution[0:Index-1]):
                    if Char == "U":
                        ReversedSolution = ReversedSolution[:CharIndex] + "L" + ReversedSolution[CharIndex+1:]
                    elif Char == "D":
                        ReversedSolution = ReversedSolution[:CharIndex] + "R" + ReversedSolution[CharIndex+1:]
                    elif Char == "R":
                        ReversedSolution = ReversedSolution[:CharIndex] + "U" + ReversedSolution[CharIndex+1:]
                    elif Char == "L":
                        ReversedSolution = ReversedSolution[:CharIndex] + "D" + ReversedSolution[CharIndex+1:]
                ReversedSolution = ReversedSolution[:Index-1] + ReversedSolution[Index+1:]
            else:
                Index += 2 #skipping direction signs
        SolutionString = ReversedSolution[::-1]
        return SolutionString

    def optimise_solution(self, Solution):
        SolutionString = ""
        for Move in Solution:
            SolutionString += Move
        SolutionString = self.replace_consequent_single_turns(SolutionString)
        SolutionString = self.remove_cube_rotations(SolutionString)
        NewSolution = []
        for Index in range(len(SolutionString)//2):
            NewSolution.append(SolutionString[Index*2:Index*2+2])
        return NewSolution
    
    def cross_on_top(self):
        return ( (self._Net[0][1] == self._Net[1][1]) and\
               (self._Net[1][0] == self._Net[1][1]) and\
               (self._Net[2][1] == self._Net[1][1]) and\
               (self._Net[1][2] == self._Net[1][1]) and\
               (self._Net[1][4] == self._Net[1][4]) and\
               (self._Net[1][7] == self._Net[1][7]) and\
               (self._Net[1][10] == self._Net[1][10]) and\
               (self._Net[2][16] == self._Net[1][16]) )
    
    def top_layer_solved(self):
        return ( (self._Net[0][0] == self._Net[1][1]) and\
               (self._Net[0][2] == self._Net[1][1]) and\
               (self._Net[2][0] == self._Net[1][1]) and\
               (self._Net[2][2] == self._Net[1][1]) and\
               (self._Net[0][3] == self._Net[1][4]) and\
               (self._Net[0][5] == self._Net[1][4]) and\
               (self._Net[0][6] == self._Net[1][7]) and\
               (self._Net[0][8] == self._Net[1][7]) and\
               (self._Net[0][9] == self._Net[1][10]) and\
               (self._Net[0][11] == self._Net[1][10]) and\
               (self._Net[2][15] == self._Net[1][16]) and\
               (self._Net[2][17] == self._Net[1][16]))
    
    def middle_layer_solved(self):
        return ( (self._Net[1][3] == self._Net[1][4]) and\
               (self._Net[1][5] == self._Net[1][4]) and\
               (self._Net[1][6] == self._Net[1][7]) and\
               (self._Net[1][8] == self._Net[1][7]) and\
               (self._Net[1][9] == self._Net[1][10]) and\
               (self._Net[1][11] == self._Net[1][10]) and\
               (self._Net[1][15] == self._Net[1][16]) and\
               (self._Net[1][17] == self._Net[1][16]) )
    
    def solve_cube(self):
        Solution = []
        Solution += self.solve_upper_cross()
        Solution += self.solve_all_upper_corners()
        Solution += self.solve_middle_edges()
        Solution += self.solve_bottom_cross()
        Solution += self.permute_bottom_edges()
        Solution += self.permute_bottom_corners()
        Solution += self.orientate_bottom_corners()
        Solution = self.optimise_solution(Solution)
        return Solution
