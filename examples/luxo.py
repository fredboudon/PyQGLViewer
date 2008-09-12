# -*- python -*-
# -*- coding: latin-1 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQGLViewer import *
import OpenGL.GL as ogl
import OpenGL.GLU as glu

helpstr = """<h2>L u x o  ©</h2>
This example illustrates several functionnalities of QGLViewer,
showing how easy it is to create a moderately complex application.<br><br>
The famous luxo lamp (©Pixar) can interactively be manipulated
with the mouse. <b>Shift</b> left click on an a part of the lamp to select it,
and then move it with the mouse. Press the <b>Control</b> key or select the background 
to move the camera instead.<br><br>
A simpler object selection example is given in the <i>select</i> example. 
A simpler frame displacement example is available in <i>manipulatedFrame</i> and 
a simpler constrained frame example is illustrated in <i>constrainedFrame</i>. 
See <i>multiSelect</i> for a multi-object selection example.<br><br>
Feel free to use this code as the starting point of a multiple frame manipulation application."""

class Luxo :
    def __init__(self):
        # The four articulations of the lamp
        self.__frame = []
        # Used to draw the selected element in a different color
        self.__selected = 4
        for i in range(0,4):
          self.__frame.append(ManipulatedFrame())
          # Creates a hierarchy of frames.
          if i>0:
            self.frame(i).setReferenceFrame(self.frame(i-1))

        # Initialize frames
        self.frame(1).setTranslation(Vec(0.0, 0.0, 0.08)) # Base height
        self.frame(2).setTranslation(Vec(0.0, 0.0, 0.5))  # Arm length
        self.frame(3).setTranslation(Vec(0.0, 0.0, 0.5))  # Arm length

        self.frame(1).setRotation(Quaternion(Vec(1.0,0.0,0.0), 0.6))
        self.frame(2).setRotation(Quaternion(Vec(1.0,0.0,0.0), -2.0))
        self.frame(3).setRotation(Quaternion(Vec(1.0,-0.3,0.0), -1.7))

        # Set frame constraints
        baseConstraint = WorldConstraint()
        baseConstraint.setTranslationConstraint(AxisPlaneConstraint.PLANE, Vec(0.0,0.0,1.0))
        baseConstraint.setRotationConstraint(AxisPlaneConstraint.AXIS, Vec(0.0,0.0,1.0))
        self.frame(0).setConstraint(baseConstraint)

        XAxis = LocalConstraint()
        XAxis.setTranslationConstraint(AxisPlaneConstraint.FORBIDDEN,  Vec(0.0,0.0,0.0))
        XAxis.setRotationConstraint   (AxisPlaneConstraint.AXIS, Vec(1.0,0.0,0.0))
        self.frame(1).setConstraint(XAxis)
        self.frame(2).setConstraint(XAxis)

        headConstraint = LocalConstraint()
        headConstraint.setTranslationConstraint(AxisPlaneConstraint.FORBIDDEN, Vec(0.0,0.0,0.0))
        self.frame(3).setConstraint(headConstraint)

        # Means camera is selected.
        selected = 4
    def draw(self,names=False):
        # Luxo's local frame
        ogl.glPushMatrix()
        ogl.glMultMatrixd(self.frame(0).matrix())

        if names:
            ogl.glPushName(0)
        self.__setColor(0)
        self.__drawBase()
        if names:
            ogl.glPopName()
            ogl.glPushName(1)
        ogl.glMultMatrixd(self.frame(1).matrix())
        self.__setColor(1)
        self.__drawCylinder()
        self.__drawArm()
        if names:
            ogl.glPopName()
            ogl.glPushName(2)
        ogl.glMultMatrixd(self.frame(2).matrix())
        self.__setColor(2)
        self.__drawCylinder()
        self.__drawArm()
        if names:
            ogl.glPopName()
            ogl.glPushName(3)
        ogl.glMultMatrixd(self.frame(3).matrix())
        self.__setColor(3)
        self.__drawHead()
        if names:
            ogl.glPopName()

        # Add light
        pos = [0.0, 0.0, 0.0, 1.0]
        ogl.glLightfv(ogl.GL_LIGHT1, ogl.GL_POSITION, pos)
        spot_dir  = [0.0, 0.0, 1.0]
        ogl.glLightfv(ogl.GL_LIGHT1, ogl.GL_SPOT_DIRECTION, spot_dir)
        ogl.glPopMatrix()
    def frame(self,i):
        return self.__frame[i]
    def setSelectedFrameNumber(self,nb) :
        self.__selected = nb
    def __drawBase(self):
        self.__drawCone(0.0,0.03, 0.15, 0.15, 30)
        self.__drawCone(0.03,0.05, 0.15, 0.13, 30)
        self.__drawCone(0.05,0.07, 0.13, 0.01, 30)
        self.__drawCone(0.07,0.09, 0.01, 0.01, 10)
    def __drawArm(self):
        ogl.glTranslatef(0.02, 0.0, 0.0)
        self.__drawCone(0.0,0.5, 0.01, 0.01, 10)
        ogl.glTranslatef(-0.04, 0.0, 0.0)
        self.__drawCone(0.0,0.5, 0.01, 0.01, 10)
        ogl.glTranslatef(0.02, 0.0, 0.0)
    def __drawHead(self):
        self.__drawCone(-0.02,0.06, 0.04, 0.04, 30)
        self.__drawCone(0.06,0.15, 0.04, 0.17, 30)
        self.__drawCone(0.15,0.17, 0.17, 0.17, 30)
    def __drawCylinder(self):
        ogl.glPushMatrix()
        ogl.glRotatef(90, 0.0,1.0,0.0)
        self.__drawCone(-0.05,0.05, 0.02, 0.02, 20)
        ogl.glPopMatrix()
    def __drawCone(self,zMin, zMax, r1, r2, nbSub):
        quadric = glu.gluNewQuadric()
        ogl.glTranslatef(0.0, 0.0, zMin)
        glu.gluCylinder(quadric, r1, r2, zMax-zMin, nbSub, 1)
        ogl.glTranslatef(0.0, 0.0, -zMin)
    def __setColor(self,nb):
        if nb == self.__selected:
            ogl.glColor3f(0.9, 0.9, 0.0)
        else:
            ogl.glColor3f(0.9, 0.9, 0.9)


class Viewer(QGLViewer):
    def __init__(self):
        QGLViewer.__init__(self)
        self.setStateFileName('.luxo.xml')        
        self.luxo = Luxo()
    def init(self):
        self.restoreStateFromFile()
        self.setManipulatedFrame( self.camera().frame() )
        # Preserve CAMERA bindings, see setHandlerKeyboardModifiers documentation.
        self.setHandlerKeyboardModifiers(QGLViewer.CAMERA, Qt.AltModifier)
        # The frames can be move without any key pressed
        self.setHandlerKeyboardModifiers(QGLViewer.FRAME, Qt.NoModifier)
        # The camera can always be moved with the Control key.
        self.setHandlerKeyboardModifiers(QGLViewer.CAMERA, Qt.ControlModifier)        
        self.initSpotLight()
        self.help()
    def draw(self):
        self.luxo.draw()
        # Draw the ground
        ogl.glColor3f(.4,.4,.4)
        nbPatches = 100.
        ogl.glNormal3f(0.0,0.0,1.0)
        for j in range(0,int(nbPatches)) :
            ogl.glBegin(ogl.GL_QUAD_STRIP)
            for i in range(0,int(nbPatches)+1):
              ogl.glVertex2f((2*i/nbPatches-1.0), (2*j/nbPatches-1.0))
              ogl.glVertex2f((2*i/nbPatches-1.0), (2*(j+1)/nbPatches-1.0))
            ogl.glEnd()
    def drawWithNames(self):
        self.luxo.draw(True)
    def postSelection(self,point):
        if self.selectedName() == -1:
            # Camera will be the default frame is no object is selected.
            self.setManipulatedFrame( self.camera().frame() )
            self.luxo.setSelectedFrameNumber(4) # dummy value meaning camera
        else :
            self.setManipulatedFrame(self.luxo.frame(self.selectedName()))
            self.luxo.setSelectedFrameNumber(self.selectedName())
    def helpString(self):
        return helpstr
    def closeEvent(self,event):
        helpwidget = self.helpWidget()
        if helpwidget.isVisible() :
            helpwidget.hide()
        QGLViewer.closeEvent(self,event)
    def initSpotLight(self):
        ogl.glMatrixMode(ogl.GL_MODELVIEW)
        ogl.glEnable(ogl.GL_LIGHT1)
        ogl.glLoadIdentity()

        # Light default parameters
        spot_dir       = [0.0, 0.0, 1.0]
        light_ambient  = [0.5, 0.5, 0.5, 1.0]
        light_specular = [1.0, 1.0, 1.0, 1.0]
        light_diffuse  = [3.0, 3.0, 1.0, 1.0]

        ogl.glLightfv(ogl.GL_LIGHT1, ogl.GL_SPOT_DIRECTION, spot_dir)
        ogl.glLightf( ogl.GL_LIGHT1, ogl.GL_SPOT_EXPONENT,  3.0)
        ogl.glLightf( ogl.GL_LIGHT1, ogl.GL_SPOT_CUTOFF,    50.0)
        ogl.glLightf( ogl.GL_LIGHT1, ogl.GL_CONSTANT_ATTENUATION, 0.5)
        ogl.glLightf( ogl.GL_LIGHT1, ogl.GL_LINEAR_ATTENUATION, 1.0)
        ogl.glLightf( ogl.GL_LIGHT1, ogl.GL_QUADRATIC_ATTENUATION, 1.5)
        ogl.glLightfv(ogl.GL_LIGHT1, ogl.GL_AMBIENT,  light_ambient)
        ogl.glLightfv(ogl.GL_LIGHT1, ogl.GL_SPECULAR, light_specular)
        ogl.glLightfv(ogl.GL_LIGHT1, ogl.GL_DIFFUSE,  light_diffuse)

def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.setWindowTitle("luxo")
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()
