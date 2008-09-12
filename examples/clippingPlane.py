from PyQt4.QtGui import *
import PyQGLViewer as pq
from qgllogo import *
import OpenGL.GL as ogl

helpstr = """<h2>C l i p p i n g P l a n e</h2>
The standard OpenGL <i>GL_CLIP_PLANE</i> feature is used to add an additionnal clipping
plane in the scene, which position and orientation are set by a <b>ManipulatedFrame</b>.<br><br>
Hold the <b>Control</b> key pressed down while using the mouse to modify the plane orientation (left button)
and position (right button) and to interactively see the clipped result.<br><br>
Since the plane equation is defined with respect to the current modelView matrix, a constant equation (normal
along the Z axis) can be used since we transformed the coordinates system using the <b>matrix()</b> method."""

class Viewer(pq.QGLViewer):
    def __init__(self):
        pq.QGLViewer.__init__(self)
        self.setStateFileName('.clippingPlane.xml')        
    def draw(self):
        draw_qgl_logo()
        ogl.glPushMatrix()
        ogl.glMultMatrixd(self.manipulatedFrame().matrix())
        ogl.glClipPlane(ogl.GL_CLIP_PLANE0, [ 0.0, 0.0, 1.0, 0.0 ])
        ogl.glColor3f(0.8, 0.8, 0.8)
        self.drawArrow(0.4, 0.015)
        ogl.glBegin(ogl.GL_QUADS)
        ogl.glVertex3f(-1.0, -1.0, 0.001)
        ogl.glVertex3f(-1.0,  1.0, 0.001)
        ogl.glVertex3f( 1.0,  1.0, 0.001)
        ogl.glVertex3f( 1.0, -1.0, 0.001)
        ogl.glEnd()
        ogl.glPopMatrix()
    def init(self):
        self.restoreStateFromFile()
        self.help()
        self.setManipulatedFrame(pq.ManipulatedFrame())
        ogl.glEnable(ogl.GL_CLIP_PLANE0)
    def helpString(self):
        return helpstr

def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.setWindowTitle("clippingPlane")
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()

