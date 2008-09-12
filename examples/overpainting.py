from PyQt4.Qt import *
from PyQGLViewer import *
from qgllogo import *
from OpenGL.GL import *

helpstr = """<h2>O v e r p a i n t</h2>"""

class Viewer(QGLViewer):
    def __init__(self,parent = None):
        QGLViewer.__init__(self,QGLFormat(QGL.SampleBuffers),parent)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setStateFileName('.overpainting.xml')
    def draw(self):
        draw_qgl_logo()
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
    def drawOverpaint(self,painter):
        painter.save()
        painter.translate(self.width()/2, self.height()/2)
        radialGrad = QRadialGradient(QPointF(-40, -40), 100)
        radialGrad.setColorAt(0, QColor(255, 255, 255, 100))
        radialGrad.setColorAt(1, QColor(200, 200, 0, 100))
        painter.setBrush(QBrush(radialGrad))
        painter.drawRoundRect(-100, -100, 200, 200)
        painter.restore()
    def paintEvent(self,event):
        #Q_UNUSED(event)
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Save current OpenGL state
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

        # Reset OpenGL parameters
        glShadeModel(GL_SMOOTH)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_MULTISAMPLE)
        lightPosition = [ 1.0, 5.0, 5.0, 1.0 ]
        glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)
        self.qglClearColor(self.backgroundColor())
    
        # Classical 3D drawing, usually performed by paintGL().
        self.preDraw()
        self.draw()
        self.postDraw()
        
        # Restore OpenGL state
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glPopAttrib()
        
        self.drawOverpaint(painter)
        painter.end()

def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.setWindowTitle("Overpaint")
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()
