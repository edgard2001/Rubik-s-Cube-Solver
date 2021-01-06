import numpy as np
import math

class CubePiece:
    def __init__(self,Position,Colours):
        self._Position = Position
        self._Surfaces = Colours
        self.set_vertices()
        self.set_borders()
        
    def set_vertices(self):
        self._Vertices = []
        for x in [-0.5,0.5]:
            self._Vertices.append(np.array(self._Position)+np.array([x,0.5,0.5]))
            self._Vertices.append(np.array(self._Position)+np.array([x,0.5,-0.5]))
            self._Vertices.append(np.array(self._Position)+np.array([x,-0.5,-0.5]))
            self._Vertices.append(np.array(self._Position)+np.array([x,-0.5,0.5]))
        for y in [-0.5,0.5]:
            self._Vertices.append(np.array(self._Position)+np.array([0.5,y,0.5]))
            self._Vertices.append(np.array(self._Position)+np.array([0.5,y,-0.5]))
            self._Vertices.append(np.array(self._Position)+np.array([-0.5,y,-0.5]))
            self._Vertices.append(np.array(self._Position)+np.array([-0.5,y,0.5]))
        for z in [-0.5,0.5]:
            self._Vertices.append(np.array(self._Position)+np.array([0.5,0.5,z]))
            self._Vertices.append(np.array(self._Position)+np.array([0.5,-0.5,z]))
            self._Vertices.append(np.array(self._Position)+np.array([-0.5,-0.5,z]))
            self._Vertices.append(np.array(self._Position)+np.array([-0.5,0.5,z]))

    def set_borders(self):
        self._Borders = []
        for i, Surface in enumerate(self._Surfaces):
            if Surface != 6:
                for (j,k) in [(0,1),(1,2),(2,3),(3,0)]:
                    if (i*4+j,i*4+k) not in self._Borders and (i*4+k,i*4+j) not in self._Borders:
                        self._Borders.append((i*4+j,i*4+k))

    def get_position(self):
        return self._Position

    def get_vertices(self):
        return self._Vertices 
        
    def get_surfaces(self):
        return self._Surfaces

    def get_borders(self):
        return self._Borders

    def rotate_cube_piece(self, Axis, Angle):
        self._Position = rotate_vector_about_given_axis(np.array(self._Position),np.array(Axis),Angle)
        for i in range(24):
            self._Vertices[i] = rotate_vector_about_given_axis(np.array(self._Vertices[i]),np.array(Axis),Angle)

    def round_vertices_and_position(self):
        self._Position = np.array([round(self._Position[0],1),round(self._Position[1],1),round(self._Position[2],1)])
        for i in range(24):
            self._Vertices[i] = np.array([round(self._Vertices[i][0],2),round(self._Vertices[i][1],2),round(self._Vertices[i][2],2)])

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
