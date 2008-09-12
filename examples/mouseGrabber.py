from PyQt4.QtGui import *
from PyQGLViewer import *
from qgllogo import *
import OpenGL.GL as ogl
from math import cos,sin,sqrt

helpstr = """<h2>M o u s e G r a b b e r </h2>
This example illustrates the use of <i>MouseGrabber</i>, which is an abstract
class for objects that react (usually when the mouse hovers over them).<br><br>
Define new camera paths (or positions) using <b>Alt</b>+[<b>F1</b>-<b>F12</b>].
New <i>MouseGrabbers</i> are then created and displayed in the upper left corner.
Note how they react when the mouse hovers, and click them to play the associated path.<br><br>
<i>ManipulatedFrame</i>, such as the ones which define the spirals' positions, are
also <i>MouseGrabbers</i>. When the mouse is close to the spiral center, the <i>ManipulatedFrame</i>
will grab to mouse click (as if the <b>Control</b> key was pressed). This is very convenient
to intuitively move scene objects (such as lights) without any key or GUI interaction.<br><br>
Note that <code>setMouseTracking()</code> must be enabled to use <i>MouseGrabbers</i>."""

class CameraPathPlayer (MouseGrabber):
    def __init__(self,nb) :
        MouseGrabber.__init__(self)
        self.pathNb = nb
    def checkIfGrabsMouse(self,x, y, camera):
        # Rectangular activation array - May have to be tune depending on your default font size
        self.setGrabsMouse((x < 80) and (y<yPos()) and ((yPos()-y) < 16))
    def yPos(self):
        return 25*self.pathNb
    def mousePressEvent(self, event, camera) :
        camera.playPath(self.pathNb)

class Spiral:
    def __init__(self):
        self.mf = ManipulatedFrame()
    def draw(self) :
        ogl.glPushMatrix()
        ogl.glMultMatrixd(self.mf.matrix())
        # Draw a spiral
        nbSteps = 100.0
        ogl.glBegin(ogl.GL_QUAD_STRIP)
        for i in range(int(nbSteps)):
            ratio = i/nbSteps
            angle = 21.0*ratio
            c = cos(angle)
            s = sin(angle)
            r1 = 0.2 - 0.15*ratio
            r2 = 0.16 - 0.15*ratio
            alt = 0.2 * (ratio - 0.5)
            nor = .5
            up = sqrt(1.0-nor*nor)
            if self.mf.grabsMouse():
                ogl.glColor3f(1-ratio, 0.8 , ratio/2.0)
            else:
                ogl.glColor3f(1-ratio, 0.2 , ratio)
            ogl.glNormal3f(nor*c, up, nor*s)
            ogl.glVertex3f(r1*c, alt, r1*s)
            ogl.glVertex3f(r2*c, alt+0.01, r2*s)
        ogl.glEnd()
        ogl.glPopMatrix()
    def setPosition(self,pos):
        self.mf.setPosition(pos)


class Viewer(QGLViewer):
    def __init__(self):
        QGLViewer.__init__(self)
        self.setStateFileName('.mouseGrabber.xml')        
    def draw(self):
        for spiral in self.spiral:
            spiral.draw()
        self.updatePlayers()
        ogl.glDisable(ogl.GL_LIGHTING)
        self.displayPlayers()
        ogl.glEnable(ogl.GL_LIGHTING)
    def init(self):
        # Absolutely needed for MouseGrabber
        self.setMouseTracking(True)
        # In order to make the manipulatedFrame displacements clearer
        self.setAxisIsDrawn()

        # Initialize the CameraPathPlayer MouseGrabber array
        self.nbPlayers = 12
        self.player = [None for i in range(self.nbPlayers)]

        # Create a scene with several spirals.
        nbSpirals = 7
        self.spiral = []
        for i in range(-nbSpirals/2, nbSpirals/2+1):
            s = Spiral()
            s.setPosition(Vec(1.8*i/nbSpirals, 0.0, 0.0))
            self.spiral.append(s)
        self.restoreStateFromFile()
        self.help()
    def helpString(self):
        return helpstr
    def closeEvent(self,event):
        helpwidget = self.helpWidget()
        if helpwidget.isVisible() :
            helpwidget.hide()
        QGLViewer.closeEvent(self,event)
    def displayPlayers(self):
        for i in range(self.nbPlayers):
            cpp = self.player[i]
            if not cpp is None:
                if cpp.grabsMouse():
                    ogl.glColor3f(1,1,1)
                    if self.camera().keyFrameInterpolator(i).numberOfKeyFrames() > 1:
                        s = "Play path F" + str(i)
                    else:
                        s = "Restore pos F" + str(i)
                else:
                    ogl.glColor3f(0.6, 0.6, 0.6)
                    if self.camera().keyFrameInterpolator(i).numberOfKeyFrames() > 1:
                        s = "Path F" + str(i)
                    else:
                        s = "Pos F" + str(i)
                self.drawText(10, cpp.yPos()-3, s)
    def updatePlayers(self):
        for  i in range(self.nbPlayers):
            # Check if CameraPathPlayer is still valid
            if (not self.player[i] is None) and (not self.camera().keyFrameInterpolator(i) is None):
                self.player[i] = None
            # Or add it if needed
            if (not self.camera().keyFrameInterpolator(i) is None) and (self.player[i] is None):
                self.player[i] = CameraPathPlayer(i)


def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.setWindowTitle("mouseGrabber")
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()
