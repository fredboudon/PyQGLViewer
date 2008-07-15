from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQGLViewer import *
from qgllogo import *
import OpenGL.GL as ogl

helpstr = """<h2>M a n i p u l a t e d F r a m e</h2>
A <i>ManipulatedFrame</i> converts mouse gestures into <i>Frame</i> displacements.
In this example, such an object defines the position of the spiral that can hence be manipulated.<br><br>
Adding two lines of code will then allow you to move the objects of 
your scene using the mouse. The button bindings of the <i>ManipulatedFrame</i> 
are the same than for the camera. Spinning is possible.<br><br>
Default key bindings have been changed in this example : press <b>Control</b>
while moving the mouse to move the camera instead of the ManipulatedFrame."""

class Viewer(QGLViewer):
    def __init__(self):
        QGLViewer.__init__(self)
        self.setStateFileName('.manipulatedFrame.xml')        
    def draw(self):
        # Here we are in the world coordinate system.
        # Draw your scene here.

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
        self.setHandlerKeyboardModifiers(QGLViewer.CAMERA, Qt.AltModifier)
        self.setHandlerKeyboardModifiers(QGLViewer.FRAME,  Qt.NoModifier)
        self.setHandlerKeyboardModifiers(QGLViewer.CAMERA, Qt.ControlModifier)

        self.setMouseBinding(Qt.LeftButton, QGLViewer.FRAME, QGLViewer.DRIVE)
        ogl.glEnable(ogl.GL_RESCALE_NORMAL)
        
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
