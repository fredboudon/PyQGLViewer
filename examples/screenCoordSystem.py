from PyQt4.QtGui import *
from PyQGLViewer import *
from qgllogo import *
import OpenGL.GL as ogl
import OpenGL.GLU as glu
from random import *
from math import pi

helpstr = """<h2>S c r e e n C o o r d S y s t e m</h2>
This example illustrates the <i>startScreenCoordinatesSystem()</i> function
which enables a GL drawing directly into the screen coordinate system.<br><br>
The arrows are drawned using this method. The screen projection coordinates 
of the objects is determined using <code>camera()->projectedCoordinatesOf()</code>, 
thus <i>attaching</i> the 2D arrows to 3D objects."""

class Viewer(QGLViewer):
    def __init__(self):
        QGLViewer.__init__(self)
        self.setStateFileName('.screenCoordSystem.xml')        
        self.nbSaucers = 10
        self.saucerPos = [Frame() for i in range(self.nbSaucers)]
        self.saucerColor = [ QColor() for i in range(self.nbSaucers)]
    def draw(self):
        proj = [Vec() for i in range(self.nbSaucers)]
        # Draw 3D flying saucers
        for i in range(self.nbSaucers):
            ogl.glPushMatrix()
            ogl.glMultMatrixd(self.saucerPos[i].matrix())
            self.qglColor(self.saucerColor[i])
            self.__drawSaucer()
            ogl.glPopMatrix()

        # Draw the arrows
        self.qglColor(self.foregroundColor())
        self.startScreenCoordinatesSystem()
        for i in range(self.nbSaucers):
            ogl.glBegin(ogl.GL_POLYGON)
            proj[i] = self.camera().projectedCoordinatesOf(self.saucerPos[i].position())
            # The small z offset makes the arrow slightly above the saucer, so that it is always visible
            ogl.glVertex3fv(list(proj[i] + Vec(-55, 0, -0.001)))
            ogl.glVertex3fv(list(proj[i] + Vec(-17,-5, -0.001)))
            ogl.glVertex3fv(list(proj[i] + Vec( -5, 0, -0.001)))
            ogl.glVertex3fv(list(proj[i] + Vec(-17, 5, -0.001)))
            ogl.glEnd()
        self.stopScreenCoordinatesSystem()

        # Draw text id
        ogl.glDisable(ogl.GL_LIGHTING)
        for i in range(self.nbSaucers):
            self.drawText(int(proj[i].x)-60, int(proj[i].y)+4, str(i))
        ogl.glEnable(ogl.GL_LIGHTING)
    def init(self):
        for i in range(self.nbSaucers):
            pos = Vec(uniform(-0.5,0.5),uniform(-0.5,0.5),uniform(-0.5,0.5))
            ori = Quaternion (Vec(uniform(0,1),uniform(0,1),uniform(0,1)),pi*uniform(0,1))
            self.saucerPos[i].setPosition(pos)
            self.saucerPos[i].setOrientation(ori)
            self.saucerColor[i].setRgb(int(255.0 * uniform(0,1)),int(255.0 * uniform(0,1)),int(255.0 * uniform(0,1)))
            
        self.restoreStateFromFile()
        self.help()
    def helpString(self):
        return helpstr
    def closeEvent(self,event):
        helpwidget = self.helpWidget()
        if helpwidget.isVisible() :
            helpwidget.hide()
        QGLViewer.closeEvent(self,event)
    def __drawSaucer(self):
        quadric = glu.gluNewQuadric()
        ogl.glTranslatef(0.0, 0.0, -0.014)
        glu.gluCylinder(quadric, 0.015, 0.03, 0.004, 32, 1)
        ogl.glTranslatef(0.0, 0.0, 0.004)
        glu.gluCylinder(quadric, 0.03, 0.04, 0.01, 32, 1)
        ogl.glTranslatef(0.0, 0.0, 0.01)
        glu.gluCylinder(quadric, 0.05, 0.03, 0.02, 32, 1)
        ogl.glTranslatef(0.0, 0.0, 0.02)
        glu.gluCylinder(quadric, 0.03, 0.0, 0.003, 32, 1)
        ogl.glTranslatef(0.0, 0.0, -0.02)


def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.setWindowTitle("screenCoordSystem")
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()
