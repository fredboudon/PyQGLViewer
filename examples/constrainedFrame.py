from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQGLViewer import *
from qgllogo import *

helpstr = """<h2>C o n s t r a i n e d F r a m e</h2>
A manipulated frame can be constrained in its displacement.<br><br>
Try the different translation (press <b>G</b> and <b>T</b>) and rotation 
(<b>D</b> and <b>R</b>) constraints while moving the frame with the mouse.<br><br>
The constraints can be defined with respect to various coordinates
systems : press <b>Space</b> to switch.<br><br>
Press the <b>Control</b> key while moving the mouse to move the camera.<br>
Press the <b>Shift</b> key to temporally disable the constraint.<br><br>
You can easily define your own constraints to create a specific frame behavior."""

TranslationConstraintTypeDict = { 
    AxisPlaneConstraint.FREE  : AxisPlaneConstraint.PLANE,
    AxisPlaneConstraint.PLANE : AxisPlaneConstraint.AXIS,
    AxisPlaneConstraint.AXIS  : AxisPlaneConstraint.FORBIDDEN,
    AxisPlaneConstraint.FORBIDDEN : AxisPlaneConstraint.FREE }
    
def nextTranslationConstraintType(consttype):
    return TranslationConstraintTypeDict.get(consttype,AxisPlaneConstraint.FREE)


RotationConstraintTypeDict = { 
    AxisPlaneConstraint.FREE  : AxisPlaneConstraint.AXIS,
    AxisPlaneConstraint.AXIS  : AxisPlaneConstraint.FORBIDDEN,
    AxisPlaneConstraint.PLANE : AxisPlaneConstraint.FREE,
    AxisPlaneConstraint.FORBIDDEN : AxisPlaneConstraint.FREE }
    
def nextRotationConstraintType(consttype):
    return RotationConstraintTypeDict.get(consttype,AxisPlaneConstraint.FREE)


class Viewer(QGLViewer):
    def __init__(self):
        QGLViewer.__init__(self)
        self.setStateFileName('.constrainedFrame.xml')        
    def draw(self):
        ogl.glMultMatrixd(self.__frame.matrix())
        self.drawAxis(0.4)
        scale = 0.3
        ogl.glScalef(scale, scale, scale)
        draw_qgl_logo()
        self.displayText()
    def init(self):
        self.__transDir = 0
        self.__rotDir = 0
        self.__activeConstraint = 0
        self.__constraints = [ WorldConstraint(), LocalConstraint(), CameraConstraint(self.camera())]
        self.__frame = ManipulatedFrame()
        self.setManipulatedFrame(self.__frame)
        self.__frame.setConstraint(self.__constraints[self.__activeConstraint])
        self.setAxisIsDrawn()
        
        self.setHandlerKeyboardModifiers(QGLViewer.CAMERA, Qt.AltModifier)
        self.setHandlerKeyboardModifiers(QGLViewer.FRAME, Qt.NoModifier)
        self.setHandlerKeyboardModifiers(QGLViewer.CAMERA, Qt.ControlModifier)
        
        self.setMouseBinding(int(Qt.ShiftModifier) | Qt.LeftButton,  QGLViewer.FRAME, QGLViewer.ROTATE,    False)
        self.setMouseBinding(int(Qt.ShiftModifier) | Qt.RightButton, QGLViewer.FRAME, QGLViewer.TRANSLATE, False)
        self.setMouseBinding(int(Qt.ShiftModifier) | Qt.MidButton,   QGLViewer.FRAME, QGLViewer.ZOOM,      False)
        self.setWheelBinding(Qt.ShiftModifier,                  QGLViewer.FRAME, QGLViewer.ZOOM,      False)
        
        self.setKeyDescription(Qt.Key_G, "Change translation constraint direction")
        self.setKeyDescription(Qt.Key_D, "Change rotation constraint direction")
        self.setKeyDescription(Qt.Key_Space, "Change constraint reference")
        self.setKeyDescription(Qt.Key_T, "Change translation constraint type")
        self.setKeyDescription(Qt.Key_R, "Change rotation constraint type")
        
        self.restoreStateFromFile()
        self.help()
    def helpString(self):
        return helpstr
    def keyPressEvent(self,e):
        if e.key() == Qt.Key_G : 
            self.__transDir = (self.__transDir+1)%3
        elif e.key() == Qt.Key_D : 
            self.__rotDir   = (self.__rotDir+1)%3
        elif e.key() == Qt.Key_Space: 
            self.__changeConstraint()
        elif e.key() == Qt.Key_T :
            self.__constraints[self.__activeConstraint].setTranslationConstraintType(nextTranslationConstraintType(self.__constraints[self.__activeConstraint].translationConstraintType()))
        elif e.key() == Qt.Key_R :
            self.__constraints[self.__activeConstraint].setRotationConstraintType(nextRotationConstraintType(self.__constraints[self.__activeConstraint].rotationConstraintType()))
        else:
            QGLViewer.keyPressEvent(self,e)
        
        dir = Vec(0.0, 0.0, 0.0)
        dir[self.__transDir] = 1.0
        self.__constraints[self.__activeConstraint].setTranslationConstraintDirection(dir)
        
        dir = Vec(0.0, 0.0, 0.0)
        dir[self.__rotDir] = 1.0
        self.__constraints[self.__activeConstraint].setRotationConstraintDirection(dir)
        self.updateGL()
        
    def displayText(self):
        self.qglColor(self.foregroundColor())
        ogl.glDisable(ogl.GL_LIGHTING)
        self.drawText(10,self.height()-30, "TRANSLATION :")
        self.displayDir(self.__transDir, 190, self.height()-30, 'G')
        self.displayType(self.__constraints[self.__activeConstraint].translationConstraintType(), 10, self.height()-60, 'T')

        self.drawText(self.width()-220,self.height()-30, "ROTATION :")
        self.displayDir(self.__rotDir, self.width()-100, self.height()-30, 'D')
        self.displayType(self.__constraints[self.__activeConstraint].rotationConstraintType(), self.width()-220, self.height()-60, 'R')
        if self.__activeConstraint == 0:
            self.drawText(20,20, "Constraint direction defined w/r to WORLD (SPACE)")
        elif self.__activeConstraint == 1:
            self.drawText(20,20, "Constraint direction defined w/r to LOCAL (SPACE)")
        else:
            self.drawText(20,20, "Constraint direction defined w/r to CAMERA (SPACE)")
        ogl.glEnable(ogl.GL_LIGHTING)
    def displayType(self,constraint_type, x, y, c):
        if constraint_type == AxisPlaneConstraint.FREE:  
            text = QString("FREE (%1)").arg(c)
        elif constraint_type == AxisPlaneConstraint.PLANE: 
            text = QString("PLANE (%1)").arg(c)
        elif constraint_type == AxisPlaneConstraint.AXIS:
            text = QString("AXIS (%1)").arg(c)
        elif constraint_type == AxisPlaneConstraint.FORBIDDEN: 
            text = QString("FORBIDDEN (%1)").arg(c)
        self.drawText(x, y, text)
    def displayDir(self,dir, x, y, c):
        if dir == 0: 
            text = QString("X (%1)").arg(c)
        elif dir == 1: 
            text = QString("Y (%1)").arg(c)
        elif dir == 2: 
            text = QString("Z (%1)").arg(c)
        self.drawText(x, y, text)
    def __changeConstraint(self):
        previous = self.__activeConstraint
        self.__activeConstraint = (self.__activeConstraint+1)%3
        self.__constraints[self.__activeConstraint].setTranslationConstraintType(self.__constraints[previous].translationConstraintType())
        self.__constraints[self.__activeConstraint].setTranslationConstraintDirection(self.__constraints[previous].translationConstraintDirection())
        self.__constraints[self.__activeConstraint].setRotationConstraintType(self.__constraints[previous].rotationConstraintType())
        self.__constraints[self.__activeConstraint].setRotationConstraintDirection(self.__constraints[previous].rotationConstraintDirection())
        self.__frame.setConstraint(self.__constraints[self.__activeConstraint])
        
def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.setWindowTitle("constrainedFrame")
    viewer.show()
    qapp.exec_()

main()
