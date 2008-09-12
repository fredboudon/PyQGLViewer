from PyQt4.QtGui import *
import PyQGLViewer as pq
from qgllogo import *
import OpenGL.GL as ogl

helpstr = """<h2>D r a w L i g h t</h2>
The <i>drawLight()</i> function displays a representation of the OpenGL lights 
of your scene. This is convenient for debugging your light setup.<br><br>
This scene features a directionnal ligth (arrow), a spot light (cone) and a point 
light source (sphere). The representation color, position and shape matches the light setup.<br><br>
Hover over the point light or the spot light to manipulate it using the mouse (right 
button translates and left button rotates)."""

class Viewer(pq.QGLViewer):
    def __init__(self):
        pq.QGLViewer.__init__(self)
        self.setStateFileName('.drawLight.xml')        
        self.light1 = pq.ManipulatedFrame()
        self.light2 = pq.ManipulatedFrame()
    def draw(self):
        pos = [1.0, 0.5, 1.0, 0.0]
        # Directionnal light
        ogl.glLightfv(ogl.GL_LIGHT0, ogl.GL_POSITION, pos)

        pos[3] = 1.0
        # Spot light
        pos2 = list(self.light1.getPosition()) + [1]
        ogl.glLightfv(ogl.GL_LIGHT1, ogl.GL_POSITION, pos2)
        v = self.light1.getInverseTransformOf((0,0,1))
        ogl.glLightfv(ogl.GL_LIGHT1, ogl.GL_SPOT_DIRECTION, v)

        # Point light
        pos3 = list(self.light2.getPosition())
        pos3.append(1.0)
        ogl.glLightfv(ogl.GL_LIGHT2, ogl.GL_POSITION, pos3)
        draw_qgl_logo()
        self.drawLight(ogl.GL_LIGHT0)

        if self.light1.grabsMouse() :
            self.drawLight(ogl.GL_LIGHT1, 1.2)
        else:
            self.drawLight(ogl.GL_LIGHT1)
        if self.light2.grabsMouse():
            self.drawLight(ogl.GL_LIGHT2, 1.2)
        else:
            self.drawLight(ogl.GL_LIGHT2)
    def init(self):
        ogl.glMatrixMode(ogl.GL_MODELVIEW)
        ogl.glLoadIdentity()
        # Light0 is the default ambient light
        ogl.glEnable(ogl.GL_LIGHT0)
        # Light1 is a spot light
        ogl.glEnable(ogl.GL_LIGHT1)
        light_ambient  = [0.8, 0.2, 0.2, 1.0]
        light_diffuse  = [1.0, 0.4, 0.4, 1.0]
        light_specular = [1.0, 0.0, 0.0, 1.0]
        
        ogl.glLightf( ogl.GL_LIGHT1, ogl.GL_SPOT_EXPONENT,  3.0)
        ogl.glLightf( ogl.GL_LIGHT1, ogl.GL_SPOT_CUTOFF,    20.0)
        ogl.glLightf( ogl.GL_LIGHT1, ogl.GL_CONSTANT_ATTENUATION, 0.5)
        ogl.glLightf( ogl.GL_LIGHT1, ogl.GL_LINEAR_ATTENUATION, 1.0)
        ogl.glLightf( ogl.GL_LIGHT1, ogl.GL_QUADRATIC_ATTENUATION, 1.5)
        ogl.glLightfv( ogl.GL_LIGHT1, ogl.GL_AMBIENT,  light_ambient)
        ogl.glLightfv( ogl.GL_LIGHT1, ogl.GL_SPECULAR, light_specular)
        ogl.glLightfv( ogl.GL_LIGHT1, ogl.GL_DIFFUSE,  light_diffuse)
        # Light2 is a classical directionnal light
        ogl.glEnable(ogl.GL_LIGHT2)
        
        light_ambient2  = [0.2, 0.2, 2.0, 1.0]
        light_diffuse2  = [0.8, 0.8, 1.0, 1.0]
        light_specular2 = [0.0, 0.0, 1.0, 1.0]
        
        ogl.glLightfv(ogl.GL_LIGHT2, ogl.GL_AMBIENT,  light_ambient2)
        ogl.glLightfv(ogl.GL_LIGHT2, ogl.GL_SPECULAR, light_specular2)
        ogl.glLightfv(ogl.GL_LIGHT2, ogl.GL_DIFFUSE,  light_diffuse2)
        
        self.setMouseTracking(True)
        
        self.light1.setPosition(0.5, 0.5, 0)
        # Align z axis with -position direction : look at scene center
        self.light1.setOrientation(pq.Quaternion(pq.Vec(0,0,1), -self.light1.position()))
        
        self.light2.setPosition(-0.5, 0.5, 0)
        self.restoreStateFromFile()
        # self.help()
    def helpString(self):
        return helpstr

def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.setWindowTitle("drawLight")
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()
