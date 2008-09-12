from PyQt4.QtGui import *
from PyQGLViewer import *
import OpenGL.GL as ogl
from math import sin,cos,pi

helpstr = """<h2>F r a m e T r a n s f o r m</h2>
This example illustrates how easy it is to switch between the camera and 
the world coordinate systems using the <i>camera()->cameraCoordinatesOf()</i> 
and <i>camera::worldCoordinatesOf()</i> functions.<br><br>
You can create your own hierarchy of local coordinates systems and each of 
them can be manipulated with the mouse (see the <i>manipulatedFrame</i> and <i>luxo</i> examples). 
Standard functions allow you to convert from any local frame to any other, 
the world/camera conversion presented here simply being an illustration.<br><br>
See <i>examples/frameTransform.html</i> for an explanation of the meaning of these weird lines."""

class Viewer(QGLViewer):
    def __init__(self):
        QGLViewer.__init__(self)
        self.setStateFileName('.frameTransform.xml')        
    def draw(self):
        nbLines = 50
        ogl.glBegin(ogl.GL_LINES)
        for i in range(0,nbLines):
            angle = 2.0*pi*i/nbLines
            ogl.glColor3f(.8,.2,.2)
            # These lines will never be seen as they are always aligned with the viewing direction.
            ogl.glVertex3fv(list(self.camera().position()))
            ogl.glVertex3f (cos(angle), sin(angle), 0.0)

            ogl.glColor3f(.2,.8,.2)
            # World Coordinates are infered from the camera, and seem to be immobile in the screen.
            ogl.glVertex3fv(list(self.camera().worldCoordinatesOf(Vec(.3*cos(angle), .3*sin(angle), -2.0))))
            ogl.glVertex3f (cos(angle), sin(angle), 0.0)

            ogl.glColor3f(.2,.2,.8)
            # These lines are defined in the world coordinate system and will move with the camera.
            ogl.glVertex3f(1.5*cos(angle), 1.5*sin(angle), -1.0)
            ogl.glVertex3f(cos(angle), sin(angle), 0.0)
        ogl.glEnd()
    def init(self):
        self.restoreStateFromFile()
        self.setSceneRadius(1.5)
        self.showEntireScene()
        self.setAxisIsDrawn()
        ogl.glDisable(ogl.GL_LIGHTING)
        self.help()
    def helpString(self):
        return helpstr

def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.setWindowTitle("frameTransform")
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()
