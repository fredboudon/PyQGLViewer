from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQGLViewer import *
from qgllogo import *
import OpenGL.GL as ogl
import OpenGL.GLU as oglu

helpstr = """<h2>M a n i p u l a t e d F r a m e</h2>
A <i>ManipulatedFrame</i> converts mouse gestures into <i>Frame</i> displacements.
In this example, such an object defines the position of the spiral that can hence be manipulated.<br><br>
Adding two lines of code will then allow you to move the objects of 
your scene using the mouse. The button bindings of the <i>ManipulatedFrame</i> 
are the same than for the camera. Spinning is possible.<br><br>
Default key bindings have been changed in this example : press <b>Control</b>
while moving the mouse to move the camera instead of the ManipulatedFrame."""

def opengl_error_check():
    error = ogl.glGetError()
    if error != ogl.GL_NO_ERROR:
        print("OPENGL_ERROR: ", oglu.gluErrorString(error))

class Viewer(QGLViewer):
    def __init__(self):
        QGLViewer.__init__(self)
        self.setStateFileName('.manipulatedFrame.xml')        
    def draw(self):
        # Here we are in the world coordinate system.
        # Draw your scene here.
        self.drawAxis()

        # Save the current model view matrix (not needed here in fact)
        ogl.glPushMatrix()

        # Multiply matrix to get in the frame coordinate system.
        ogl.glMultMatrixd(self.manipulatedFrame().matrix())

        # Scale down the drawings
        ogl.glScalef(0.3, 0.3, 0.3)

        # Draw an axis using the QGLViewer static function
        self.drawAxis()

        # Draws a frame-related spiral.
        draw_qgl_logo()

        # Restore the original (world) coordinate system
        ogl.glPopMatrix()        
        
    def init(self):
        self.setMouseBinding(Qt.AltModifier, Qt.LeftButton, QGLViewer.CAMERA, QGLViewer.ROTATE)
        self.setMouseBinding(Qt.AltModifier, Qt.RightButton, QGLViewer.CAMERA, QGLViewer.TRANSLATE)
        self.setMouseBinding(Qt.AltModifier, Qt.MidButton, QGLViewer.CAMERA, QGLViewer.ZOOM)
        self.setWheelBinding(Qt.AltModifier, QGLViewer.CAMERA, QGLViewer.ZOOM)

        self.setMouseBinding(Qt.NoModifier, Qt.LeftButton, QGLViewer.FRAME, QGLViewer.ROTATE)
        self.setMouseBinding(Qt.NoModifier, Qt.RightButton, QGLViewer.FRAME, QGLViewer.TRANSLATE)
        self.setMouseBinding(Qt.NoModifier, Qt.MidButton, QGLViewer.FRAME, QGLViewer.ZOOM)
        self.setWheelBinding(Qt.NoModifier, QGLViewer.FRAME, QGLViewer.ZOOM)

        ogl.glEnable(ogl.GL_RESCALE_NORMAL)

        # Make sure the manipulatedFrame is not easily clipped by the zNear and zFar
        # planes
        self.setSceneRadius(30)
        self.camera().fitSphere(Vec(0, 0, 0), 1)

        # Add a manipulated frame to the viewer.
        self.setManipulatedFrame(ManipulatedFrame())

        self.restoreStateFromFile()
        self.help()
        
        # Make world axis visible
        self.setAxisIsDrawn()
    def helpString(self):
        return helpstr
    def closeEvent(self,event):
        helpwidget = self.helpWidget()
        if helpwidget.isVisible() :
            helpwidget.hide()
        QGLViewer.closeEvent(self,event)

def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.setWindowTitle("manipulatedFrame")
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()
