from PyQt4.QtGui import *
from PyQGLViewer import *
from qgllogo import *
import OpenGL.GL as ogl

helpstr = """<h2>T e x t u r e 3 D</h2>
An example to show how to build a 3D texture and apply it on a dynamic pyramid."""

class Viewer(QGLViewer):
    def __init__(self,parent = None):
        QGLViewer.__init__(self,parent)
        self.center = [ 0.0,0.0,1.0 ]
        self.base = [[ -1.0, -1.0, 0.0 ], [-1.0, 1.0, 0.0], [1.0, 1.0, 0.0], [1.0, -1.0, 0.0]]
        self.time = 0.
    def animate(self):
        self.center[2] = math.sin(self.time / 15.0) * 2.0
        self.time += 1
    def draw(self):
        if self.texname > 0:
            ogl.glBindTexture(ogl.GL_TEXTURE_3D, self.texname)
        ogl.glBegin(ogl.GL_TRIANGLES)
        # texture coordinates are always specified before the vertex they apply to.
        for x in range(4):
            ogl.glTexCoord3d(self.center[0], self.center[1], self.center[2])
            ogl.glVertex3d(self.center[0], self.center[1], self.center[2])
            
            ogl.glTexCoord3d(self.base[x][0], self.base[x][1], self.base[x][2])
            ogl.glVertex3d(self.base[x][0], self.base[x][1], self.base[x][2])
            
            ogl.glTexCoord3d(self.base[(x+1)%4][0], self.base[(x+1)%4][1], self.base[(x+1)%4][2])
            ogl.glVertex3d(self.base[(x+1)%4][0], self.base[(x+1)%4][1], self.base[(x+1)%4][2])
        ogl.glEnd()
    def init(self):
        self.restoreStateFromFile()
        self.help()
        imgs = [QImage(4,4,QImage.Format_ARGB32) for i in range(4)]
        imgs[0].fill(qRgb(128,0,0))
        imgs[1].fill(qRgb(0,128,0))
        imgs[2].fill(qRgb(0,0,128))
        imgs[3].fill(qRgb(128,128,128))
        self.texname = self.bindTexture3D(imgs)
        self.setSceneRadius(1)
        self.startAnimation()
    def helpString(self):
        return helpstr
    def closeEvent(self,event):
        helpwidget = self.helpWidget()
        if helpwidget.isVisible() :
            helpwidget.hide()
        if self.texname > 0:
            ogl.glDeleteTextures(self.texname)
        QGLViewer.closeEvent(self,event)

def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.setWindowTitle("texture3D")
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()
