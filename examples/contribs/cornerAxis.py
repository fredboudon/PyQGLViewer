from PyQt4.QtGui import *
from PyQGLViewer import *
import OpenGL.GL as ogl

import sys,os
sys.path.append(os.path.join(os.getcwd(),os.pardir))
from qgllogo import *

helpstr = """<h2>C o r n e r A x i s</h2>
A world axis representation is drawn in the lower left corner, so that one always sees how the scene is oriented.<br><br>
The axis is drawn in <code>postDraw()</code> with appropriate ortho camera parameters.
<code>glViewport</code> and <code>glScissor</code> are used to restrict the drawing area."""

class Viewer(QGLViewer):
    def __init__(self,parent = None):
        QGLViewer.__init__(self,parent)
        self.setStateFileName('.cornerAxis.xml')
    def draw(self):
        draw_qgl_logo()
    def postDraw(self):
        QGLViewer.postDraw(self)
        self.drawCornerAxis()
    def init(self):
        self.restoreStateFromFile()
        self.help()
    def helpString(self):
        return helpstr
    def closeEvent(self,event):
        helpwidget = self.helpWidget()
        if helpwidget.isVisible() :
            helpwidget.hide()
        QGLViewer.closeEvent(self,event)
    def drawCornerAxis(self):
        # The viewport and the scissor are changed to fit the lower left
        # corner. Original values are saved.
        viewport = ogl.glGetIntegerv(ogl.GL_VIEWPORT)
        scissor  = ogl.glGetIntegerv(ogl.GL_SCISSOR_BOX)

        # Axis viewport size, in pixels
        size = 150;
        ogl.glViewport(0,0,size,size)
        ogl.glScissor(0,0,size,size)

        # The Z-buffer is cleared to make the axis appear over the
        # original image.
        ogl.glClear(ogl.GL_DEPTH_BUFFER_BIT)

        # Tune for best line rendering
        ogl.glDisable(ogl.GL_LIGHTING)
        ogl.glLineWidth(3.0)

        ogl.glMatrixMode(ogl.GL_PROJECTION)
        ogl.glPushMatrix()
        ogl.glLoadIdentity()
        ogl.glOrtho(-1, 1, -1, 1, -1, 1)

        ogl.glMatrixMode(ogl.GL_MODELVIEW)
        ogl.glPushMatrix()
        ogl.glLoadIdentity()
        ogl.glMultMatrixd(self.camera().orientation().inverse().matrix())

        ogl.glBegin(ogl.GL_LINES)
        ogl.glColor3f(1.0, 0.0, 0.0)
        ogl.glVertex3f(0.0, 0.0, 0.0)
        ogl.glVertex3f(1.0, 0.0, 0.0)

        ogl.glColor3f(0.0, 1.0, 0.0)
        ogl.glVertex3f(0.0, 0.0, 0.0)
        ogl.glVertex3f(0.0, 1.0, 0.0)
    
        ogl.glColor3f(0.0, 0.0, 1.0)
        ogl.glVertex3f(0.0, 0.0, 0.0)
        ogl.glVertex3f(0.0, 0.0, 1.0)
        ogl.glEnd()

        ogl.glMatrixMode(ogl.GL_PROJECTION)
        ogl.glPopMatrix()

        ogl.glMatrixMode(ogl.GL_MODELVIEW)
        ogl.glPopMatrix()

        ogl.glEnable(ogl.GL_LIGHTING)

        # The viewport and the scissor are restored.
        ogl.glScissor(*scissor)
        ogl.glViewport(*viewport)
        

def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.setWindowTitle("cornerAxis")
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()
