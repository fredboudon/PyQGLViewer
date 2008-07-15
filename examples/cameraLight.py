from PyQt4.QtGui import *
from PyQGLViewer import *
from qgllogo import *
import OpenGL.GL as ogl

helpstr = """<h2>C a m e r a L i g h t</h2>
See the <b>Mouse</b> tab and the documentation web pages for details.<br><br>
Press <b>Escape</b> to exit the viewer."""

class Viewer(QGLViewer):
    def __init__(self,parent = None):
        QGLViewer.__init__(self,parent)
        self.setStateFileName('.cameraLight.xml')
    def draw(self):
        # Place light at camera position
        cameraPos = self.camera().position()
        pos = [cameraPos[0], cameraPos[1], cameraPos[2], 1.0]
        ogl.glLightfv(ogl.GL_LIGHT1, ogl.GL_POSITION, pos)

        # Orientate light along view direction
        ogl.glLightfv(ogl.GL_LIGHT1, ogl.GL_SPOT_DIRECTION, list(self.camera().viewDirection()))
        draw_qgl_logo()
    def init(self):
        # Light setup
        ogl.glDisable(ogl.GL_LIGHT0);
        ogl.glEnable(ogl.GL_LIGHT1);

        # Light default parameters
        light_ambient  = [1.0, 1.0, 1.0, 1.0]
        light_specular = [1.0, 1.0, 1.0, 1.0]
        light_diffuse  = [1.0, 1.0, 1.0, 1.0]

        ogl.glLightf( ogl.GL_LIGHT1, ogl.GL_SPOT_EXPONENT, 3.0)
        ogl.glLightf( ogl.GL_LIGHT1, ogl.GL_SPOT_CUTOFF,   10.0)
        ogl.glLightf( ogl.GL_LIGHT1, ogl.GL_CONSTANT_ATTENUATION,  0.1)
        ogl.glLightf( ogl.GL_LIGHT1, ogl.GL_LINEAR_ATTENUATION,    0.3)
        ogl.glLightf( ogl.GL_LIGHT1, ogl.GL_QUADRATIC_ATTENUATION, 0.3)
        ogl.glLightfv(ogl.GL_LIGHT1, ogl.GL_AMBIENT,  light_ambient)
        ogl.glLightfv(ogl.GL_LIGHT1, ogl.GL_SPECULAR, light_specular)
        ogl.glLightfv(ogl.GL_LIGHT1, ogl.GL_DIFFUSE,  light_diffuse)
        # Restore previous viewer state.
        self.restoreStateFromFile()
        # Opens help window
        self.help()
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
    viewer.setWindowTitle("cameraLight")
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()
