from PyQt4.Qt import *
from PyQGLViewer import *
import OpenGL.GL as ogl
from math import log

import sys,os
sys.path.append(os.path.join(os.getcwd(),os.pardir))
from qgllogo import *

helpstr = """<h2>B a c k g r o u n d I m a g e</h2>
This example is derivated from textureViewer.<br><br>
It displays a background image in the viewer using a texture.<br><br>
Press <b>L</b> to load a new image, and <b>B</b> to toggle the background display."""

class Viewer(QGLViewer):
    def __init__(self,parent = None):
        QGLViewer.__init__(self,parent)
        self.setStateFileName('.backgroundImage.xml')
        self.textureId = None
    def draw(self):
        self.drawBackground()
        draw_qgl_logo()
    def init(self):
        self.restoreStateFromFile()
        # Enable GL textures
        ogl.glTexParameterf( ogl.GL_TEXTURE_2D, ogl.GL_TEXTURE_MAG_FILTER, ogl.GL_LINEAR )
        ogl.glTexParameterf( ogl.GL_TEXTURE_2D, ogl.GL_TEXTURE_MIN_FILTER, ogl.GL_LINEAR )

        # Nice texture coordinate interpolation
        ogl.glHint( ogl.GL_PERSPECTIVE_CORRECTION_HINT, ogl.GL_NICEST )

        self.u_max = 1.0
        self.v_max = 1.0
        self.ratio = 1.0
        self.background_ = True

        self.setKeyDescription(Qt.Key_L, "Loads a new background image")
        self.setKeyDescription(Qt.Key_B, "Toggles background display")

        self.loadImage()
        self.help()
        qWarning("fin init")
    def helpString(self):
        return helpstr
    def closeEvent(self,event):
        if self.textureId:
            self.deleteTexture(self.textureId)
            self.textureId = None
        helpwidget = self.helpWidget()
        if not helpwidget is None and helpwidget.isVisible() :
            helpwidget.hide()
        QGLViewer.closeEvent(self,event)
    def keyPressEvent(self,event):
        if event.key() == Qt.Key_L :
            self.loadImage()
        elif event.key() == Qt.Key_B :
            self.background_ = not self.background_
            self.updateGL()
        else:
            QGLViewer.keyPressEvent(self,event)
    def drawBackground(self):
        if not self.background_:
            return

        ogl.glDisable(ogl.GL_LIGHTING)
        ogl.glEnable(ogl.GL_TEXTURE_2D)
        ogl.glColor3f(1,1,1)

        self.startScreenCoordinatesSystem(True)

        # Draws the background quad
        ogl.glNormal3f(0.0, 0.0, 1.0)
        ogl.glBegin(ogl.GL_QUADS)
        ogl.glTexCoord2f(0.0,   1.0-self.v_max)
        ogl.glVertex2i(0,0)
        ogl.glTexCoord2f(0.0,   1.0)
        ogl.glVertex2i(0,self.height())
        ogl.glTexCoord2f(self.u_max, 1.0)
        ogl.glVertex2i(self.width(),self.height())
        ogl.glTexCoord2f(self.u_max, 1.0-self.v_max)
        ogl.glVertex2i(self.width(),0)
        ogl.glEnd()

        self.stopScreenCoordinatesSystem()

        # Depth clear is not absolutely needed. An other option would have been to draw the
        # QUAD with a 0.999 z value (z ranges in [0, 1[ with startScreenCoordinatesSystem()).
        ogl.glClear(ogl.GL_DEPTH_BUFFER_BIT)
        ogl.glDisable(ogl.GL_TEXTURE_2D)
        ogl.glEnable(ogl.GL_LIGHTING)
    def loadImage(self):
        if self.textureId:
            self.deleteTexture(self.textureId)
            self.textureId = None
        name = QFileDialog.getOpenFileName(self, "Select an image", ".", "Images (*.png *.xpm *.jpg)");

        # In case of Cancel
        if name.isEmpty() :  return

        img = QImage(name)

        if img.isNull():
            qWarning("Unable to load file, unsupported file format")
            return

        qWarning("Loading %s, %dx%d pixels" % (name.toLatin1(), img.width(), img.height()))

        # 1E-3 needed. Just try with width=128 and see !
        newWidth  = int (1<<(int)(1+log(img.width() -1+1E-3) / log(2.0)))
        newHeight = int (1<<(int)(1+log(img.height()-1+1E-3) / log(2.0)))

        self.u_max = img.width()  / float(newWidth)
        self.v_max = img.height() / float(newHeight)

        if (img.width()!=newWidth) or (img.height()!=newHeight) :
            qWarning("Image size set to %dx%d pixels" % (newWidth, newHeight))
            img = img.copy(0, 0, newWidth, newHeight)

        self.ratio = newWidth / float(newHeight)

        # Bind the img texture...
        self.textureId = self.bindTexture(img,ogl.GL_TEXTURE_2D,ogl.GL_RGBA)
        if self.textureId :
            ogl.glBindTexture(ogl.GL_TEXTURE_2D, self.textureId)
        

def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.setWindowTitle("backgroundImage")
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()
