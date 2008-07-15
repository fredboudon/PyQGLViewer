from PyQt4.Qt import *
from PyQGLViewer import *
import OpenGL.GL as ogl
from math import log

import sys,os
sys.path.append(os.path.join(os.getcwd(),os.pardir))
from qgllogo import *

helpstr = """<h2>T e x t u r e V i e w e r</h2>
This pedagogical example illustrates how to texture map a polygon.<br><br>
The Qt <i>QImage</i> class and its <i>convertToGLFormat()</i> function are used
to load an image in any format. The image is resized so that its dimensions 
are powers of two if needed. Feel free to cut and paste.<br><br>
Press <b>L</b>(oad) to load a new image."""

class Viewer(QGLViewer):
    def __init__(self,parent = None):
        QGLViewer.__init__(self,parent)
        self.setStateFileName('.textureViewer.xml')
        self.textureId = None
    def draw(self):
        # Display the quad
        ogl.glNormal3f(0.0, 0.0, 1.0)
        ogl.glBegin(ogl.GL_QUADS)
        ogl.glTexCoord2f(0.0,   1.0-self.v_max)
        ogl.glVertex2f(-self.u_max*self.ratio,-self.v_max)
        ogl.glTexCoord2f(0.0,   1.0)
        ogl.glVertex2f(-self.u_max*self.ratio, self.v_max)
        ogl.glTexCoord2f(self.u_max, 1.0)
        ogl.glVertex2f( self.u_max*self.ratio, self.v_max)
        ogl.glTexCoord2f(self.u_max, 1.0-self.v_max)
        ogl.glVertex2f( self.u_max*self.ratio,-self.v_max)
        ogl.glEnd()
    def init(self):
        self.restoreStateFromFile()
        # Enable GL textures
        ogl.glTexParameterf( ogl.GL_TEXTURE_2D, ogl.GL_TEXTURE_MAG_FILTER, ogl.GL_LINEAR )
        ogl.glTexParameterf( ogl.GL_TEXTURE_2D, ogl.GL_TEXTURE_MIN_FILTER, ogl.GL_LINEAR )
        ogl.glEnable(ogl.GL_TEXTURE_2D)

        # Nice texture coordinate interpolation
        ogl.glHint( ogl.GL_PERSPECTIVE_CORRECTION_HINT, ogl.GL_NICEST )

        self.u_max = 1.0
        self.v_max = 1.0
        self.ratio = 1.0

        self.setKeyDescription(Qt.Key_L, "Loads a new image")

        self.loadImage()
        self.help()
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
        else:
            QGLViewer.keyPressEvent(self,event)
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
