from PyQt4.QtGui import *
from PyQGLViewer import *
import OpenGL.GL as ogl
import math

helpstr = """<h2>T e x t u r e 3 D</h2>
An example to show how to build a 3D texture and apply it on a dynamic pyramid."""

class Viewer(QGLViewer):
    def __init__(self,parent = None):
        QGLViewer.__init__(self,parent)
        self.setStateFileName('.texture3D.xml')        
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
            ogl.glTexCoord3dv(self.center)
            ogl.glVertex3dv(self.center)
            
            ogl.glTexCoord3dv(self.base[x])
            ogl.glVertex3dv(self.base[x])
            
            ogl.glTexCoord3dv(self.base[(x+1)%4])
            ogl.glVertex3dv(self.base[(x+1)%4])
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
        if not helpwidget is None and helpwidget.isVisible() :
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
