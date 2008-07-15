from PyQt4.QtGui import *
from PyQGLViewer import *
import OpenGL.GL as ogl
import math

helpstr = """<h2>A n a g l y p h</h2>
The anaglyph stereo mode displays simultaneously two colored views of the scene.<br><br>
You need to wear glasses with colored lenses (here red and blue) to view the stereo image
Each eye then sees the associated view, creating the stereo illusion.<br><br>
Stereo is best perceived when viewer is full screen (<code>Alt+Enter</code>).<br><br>
Simply use the <i>loadModelViewMatrixStereo()</i> and
<i>loadProjectionMatrixStereo()</i> camera functions to set appropriate
<i>GL_MODELVIEW</i> and <i>GL_PROJECTION</i> stereo matrices."""

class Viewer(QGLViewer):
    def __init__(self,parent = None):
        QGLViewer.__init__(self,parent)
        self.setStateFileName('.anaglyph.xml')
    def draw(self):
        # Draw for left eye
        self.camera().loadProjectionMatrixStereo(True)
        self.camera().loadModelViewMatrixStereo(True)
        ogl.glColor3f(0.0, 0.0, 1.0)
        self.drawScene()

        # Draw for right eye
        self.camera().loadProjectionMatrixStereo(False)
        self.camera().loadModelViewMatrixStereo(False)
        ogl.glColor3f(1.0, 0.0, 0.0)
        self.drawScene()
    def drawScene(self):
        nbSteps = 200
        ogl.glBegin(ogl.GL_QUAD_STRIP);
        for i in range(0,int(nbSteps)):
            ratio = i/float(nbSteps)
            angle = 21.0*ratio
            c = math.cos(angle)
            s = math.sin(angle)
            r1 = 1.0 - 0.8*ratio
            r2 = 0.8 - 0.8*ratio
            alt = ratio - 0.5
            nor = 0.5
            up = math.sqrt(1.0-nor*nor)
            ogl.glNormal3f(nor*c, up, nor*s)
            ogl.glVertex3f(r1*c, alt, r1*s)
            ogl.glVertex3f(r2*c, alt+0.05, r2*s)
        ogl.glEnd()
    def init(self):
        ogl.glPolygonMode(ogl.GL_FRONT_AND_BACK, ogl.GL_LINE);
        self.restoreStateFromFile()
        self.help()
    def helpString(self):
        return helpstr
    def closeEvent(self,event):
        helpwidget = self.helpWidget()
        if not helpwidget is None and helpwidget.isVisible() :
            helpwidget.hide()
        QGLViewer.closeEvent(self,event)

def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.setWindowTitle("anaglyph")
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()
