from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQGLViewer import *
import OpenGL.GL as ogl

helpstr = """<h2>K e y F r a m e s</h2>
A <i>KeyFrameInterpolator</i> holds an interpolated path defined by key frames. 
It can then smoothly make its associed frame follow that path. Key frames can interactively be manipulated, even 
during interpolation.<br><br>
Note that the camera holds 12 such keyFrameInterpolators, binded to F1-F12. Press <b>Alt+Fx</b> to define new key 
frames, and then press <b>Fx</b> to make the camera follow the path. Press <b>C</b> to visualize these paths.<br><br>
<b>+/-</b> changes the interpolation speed. Negative values are allowed.<br><br>
<b>Return</b> starts-stops the interpolation.<br><br>
Use the left and right arrows to change the manipulated KeyFrame. 
Press <b>Control</b> to move it or simply hover over it."""

class Viewer(QGLViewer):
    def __init__(self):
        QGLViewer.__init__(self)
        self.setStateFileName('.keyFrames.xml')        
        self.restoreStateFromFile()
        self.nbKeyFrames = 4
        self.myFrame = Frame()
        self.kfi = KeyFrameInterpolator()
        self.kfi.setFrame(self.myFrame)
        self.kfi.setLoopInterpolation()
        self.keyFrame = [ManipulatedFrame() for i in range(self.nbKeyFrames)]
        for i,kf in enumerate(self.keyFrame):
            kf.setPosition(-1.0 + 2.0*i/(self.nbKeyFrames-1), 0.0, 0.0)
            self.kfi.addKeyFrame(kf)
        self.currentKF = 0
        self.setManipulatedFrame(self.keyFrame[self.currentKF])

        # Enable direct frame manipulation when the mouse hovers.
        self.setMouseTracking(True)

        self.setKeyDescription(Qt.Key_Plus, "Increases interpolation speed")
        self.setKeyDescription(Qt.Key_Minus, "Decreases interpolation speed")
        self.setKeyDescription(Qt.Key_Left, "Selects previous key frame")
        self.setKeyDescription(Qt.Key_Right, "Selects next key frame")
        self.setKeyDescription(Qt.Key_Return, "Starts/stops interpolation")
        self.help()
        QObject.connect(self.kfi, SIGNAL("interpolated()"), self.updateGL)
        self.kfi.startInterpolation()
    def draw(self):
        # Draw interpolated frame
        ogl.glPushMatrix()
        ogl.glMultMatrixd(self.kfi.frame().matrix())
        self.drawAxis(0.3)
        ogl.glPopMatrix()

        self.kfi.drawPath(5, 10)

        for i in range(self.nbKeyFrames):
            ogl.glPushMatrix()
            ogl.glMultMatrixd(self.kfi.keyFrame(i).matrix())
            if i == self.currentKF or self.keyFrame[i].grabsMouse():
                self.drawAxis(0.4)
            else:
                self.drawAxis(0.2)

            ogl.glPopMatrix()
    def helpString(self):
        return helpstr
    def keyPressEvent(self,e):
        if e.key() == Qt.Key_Left :
            self.currentKF = (self.currentKF+self.nbKeyFrames-1) % self.nbKeyFrames
            self.setManipulatedFrame(self.keyFrame[self.currentKF])
            self.updateGL()
        elif e.key() == Qt.Key_Right :
            self.currentKF = (self.currentKF+1) % self.nbKeyFrames
            self.setManipulatedFrame(self.keyFrame[self.currentKF])
            self.updateGL()
        elif e.key() == Qt.Key_Return :
            self.kfi.toggleInterpolation()
        elif e.key() == Qt.Key_Plus :
            self.kfi.setInterpolationSpeed(self.kfi.interpolationSpeed()+0.25)
        elif e.key() == Qt.Key_Minus :
            self.kfi.setInterpolationSpeed(self.kfi.interpolationSpeed()-0.25)
        else:
            QGLViewer.keyPressEvent(self,e)
    def closeEvent(self,event):
        helpwidget = self.helpWidget()
        if helpwidget.isVisible() :
            helpwidget.hide()
        QGLViewer.closeEvent(self,event)

def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.setWindowTitle("keyFrames")
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()
