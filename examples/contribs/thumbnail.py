from PyQt4.Qt import *
from PyQGLViewer import *
import OpenGL.GL as ogl

import sys,os
sys.path.append(os.path.join(os.getcwd(),os.pardir))
from qgllogo import *

helpstr = """<h2>T h u m b n a i l</h2>
A thumbnailed view of the scene is displayed in the lower left corner.<br><br>
Such display may be useful for illustration (e.g. to show the data structure) or to debug your
application. It uses <code>glScissor</code> and <code>glViewport</code> to restrict the display area.<br><br>
Press <b>T</b> to toggle the thumbnail display"""

class Viewer(QGLViewer):
    def __init__(self,parent = None):
        QGLViewer.__init__(self,parent)
        self.setStateFileName('.thumbnail.xml')
    def draw(self):
        draw_qgl_logo()
    def postDraw(self):
        QGLViewer.postDraw(self)
        self.drawThumbnail()
    def init(self):
        self.restoreStateFromFile()
        self.thumbnail_ = True
        self.setKeyDescription(Qt.Key_T, "Toggles thumbnail display")
        self.help()
    def helpString(self):
        return helpstr
    def closeEvent(self,event):
        helpwidget = self.helpWidget()
        if not helpwidget is None and helpwidget.isVisible() :
            helpwidget.hide()
        QGLViewer.closeEvent(self,event)
    def keyPressEvent(self,event):
        if event.key() == Qt.Key_T :
            self.thumbnail_ = not self.thumbnail_
            self.updateGL()
        else:
            QGLViewer.keyPressEvent(self,event)
    def drawThumbnail(self):
        if self.thumbnail_:

            # The viewport and the scissor are changed to fit the lower left
            # corner. Original values are saved.
            viewport = ogl.glGetIntegerv(ogl.GL_VIEWPORT)
            scissor = ogl.glGetIntegerv(ogl.GL_SCISSOR_BOX)

            ogl.glViewport(0,0,self.width()/2,self.height()/2)
            ogl.glScissor(0,0,self.width()/2,self.height()/2)

            # The Z-buffer is cleared to make the thumbnail appear over the
            # original image.
            ogl.glClear(ogl.GL_DEPTH_BUFFER_BIT)

            # Here starts the drawing, with specific GL flags
            ogl.glPolygonMode(ogl.GL_FRONT_AND_BACK, ogl.GL_LINE)
            ogl.glDisable(ogl.GL_LIGHTING)
            draw_qgl_logo(50,True)
            ogl.glEnable(ogl.GL_LIGHTING)
            ogl.glPolygonMode(ogl.GL_FRONT_AND_BACK, ogl.GL_FILL)
            # Here ends the drawing. OpenGL state is restored.

            # The viewport and the scissor are restored.
            ogl.glScissor(*scissor)
            ogl.glViewport(*viewport)
        

def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.setWindowTitle("thumbnail")
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()
