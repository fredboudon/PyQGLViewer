from PyQt4.QtGui import *
from PyQGLViewer import *
import OpenGL.GL as ogl
import math

helpstr = """<h2>F a s t D r a w</h2>
The <code>fastDraw()</code> function is called instead of <code>draw()</code> when the camera 
is manipulated. Providing such a simplified version of <code>draw()</code> allows for interactive 
frame rates when the camera is moved, even for very complex scenes."""

def drawSpiral(simplified = False):
    nbSteps = 150
    nbSub = 20
    if simplified :
        nbSteps = 60
        nbSub = 2
    for n in range(0, nbSub):
        ogl.glBegin(ogl.GL_QUAD_STRIP)
        for i in range(0,int(nbSteps)):
            ratio = i/float(nbSteps)
            angle = 21.0*ratio
            c = math.cos(angle)
            s = math.sin(angle)
            radius = 1.0 - 0.5*ratio            
            center = Vec(radius*c, ratio-0.5, radius*s)

            for j in range(0,2):
                nj = float(n+j)
                delta = 3.0*nj/nbSub
                cdelta = math.cos(delta)
                shift = Vec(c*cdelta, math.sin(delta), s*cdelta)
                ogl.glColor3f(1-ratio, nj/nbSub , ratio)
                ogl.glNormal3fv(list(shift))
                ogl.glVertex3fv(list(center+shift*0.2))
        ogl.glEnd()

class Viewer(QGLViewer):
    def __init__(self):
        QGLViewer.__init__(self)
        self.setStateFileName('.fastDraw.xml')        
    def draw(self):
        drawSpiral()
    def fastDraw(self):
        drawSpiral(True)
    def init(self):
        ogl.glMaterialf(ogl.GL_FRONT_AND_BACK, ogl.GL_SHININESS, 50.0)
        specular_color = [ 0.8, 0.8, 0.8, 1.0 ]
        ogl.glMaterialfv(ogl.GL_FRONT_AND_BACK, ogl.GL_SPECULAR,  specular_color)
        self.restoreStateFromFile()
        # self.help()
    def helpString(self):
        return helpstr

def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.setWindowTitle("fastDraw")
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()
