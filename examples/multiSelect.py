from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQGLViewer import *
from qgllogo import *
import OpenGL.GL as ogl
import OpenGL.GLU as glu

helpstr = """<h2>m u l t i S e l e c t </h2>
This example illustrates an application of the <code>select()</code> function that
enables the selection of several objects.<br><br>
Object selection is preformed using the left mouse button. Press <b>Shift</b> to add objects 
to the selection, and <b>Alt</b> to remove objects from the selection.<br><br>
Individual objects (click on them) as well as rectangular regions (click and drag mouse) can be selected. 
To do this, the selection region size is modified and the <code>endSelection()</code> function 
has been overloaded so that <i>all</i> the objects of the region are taken into account 
(the default implementation only selects the closest object).<br><br>
The selected objects can then be manipulated by pressing the <b>Control</b> key. 
Other set operations (parameter edition, deletion...) can also easily be applied to the selected objects."""

class Object:
    def __init__(self):
        self.frame = Frame()
    def draw(self):
        quad = glu.gluNewQuadric()
        ogl.glPushMatrix()
        ogl.glMultMatrixd(self.frame.matrix())
        glu.gluSphere(quad, 0.03, 10, 6)
        glu.gluCylinder(quad, 0.03, 0.0, 0.09, 10, 1)
        ogl.glPopMatrix()

class ManipulatedFrameSetConstraint (Constraint):
    def __init__(self):
        Constraint.__init__(self)
        self.objects = []
    def clearSet(self):
        self.objects = []
    def addObjectToSet(self,object):
        self.objects.append(object)
    def constrainTranslation(self,translation, frame):
        for i in self.objects:
            i.frame.translate(translation)
    def constrainRotation(self,rotation, frame):
        # A little bit of math. Easy to understand, hard to guess (tm).
        # rotation is expressed in the frame local coordinates system. Convert it back to world coordinates.
        worldAxis = frame.inverseTransformOf(rotation.axis())
        pos = frame.position()
        angle = rotation.angle()
        for it in self.objects:
            # Rotation has to be expressed in the object local coordinates system.
            qObject = Quaternion(it.frame.transformOf(worldAxis), angle)
            it.frame.rotate(qObject)
            # Comment these lines only rotate the objects
            qWorld = Quaternion(worldAxis, angle)
            # Rotation around frame world position (pos)
            it.frame.setPosition(pos + qWorld.rotate(it.frame.position() - pos))


class Viewer(QGLViewer):
    # The Different selection modes
    NONE = 0
    ADD = 1
    REMOVE = 2
    
    def __init__(self):
        QGLViewer.__init__(self)
        self.setStateFileName('.multiSelect.xml')        
        # Current rectangular selection
        self.__rectangle = QRect()
        self.__selectionMode = Viewer.NONE
        self.__objects = []
        self.__selection = []
        nb = 10
        for i in range(-nb,nb+1):
            for j in range(-nb,nb+1):
                o = Object()
                o.frame.setPosition(Vec(i/float(nb),j/float(nb),0))
                self.__objects.append(o)
    def draw(self):
        # Draws selected objects only.
        ogl.glColor3f(0.9, 0.3, 0.3)
        for it in self.__selection:
            self.__objects[it].draw()
        # Draws all the objects. Selected ones are not repainted because of GL depth test.
        ogl.glColor3f(0.8, 0.8, 0.8)
        for obj in self.__objects:
            obj.draw()
        # Draws manipulatedFrame (the set's rotation center)
        if self.manipulatedFrame().isManipulated():
            ogl.glPushMatrix()
            ogl.glMultMatrixd(self.manipulatedFrame().matrix())
            self.drawAxis(0.5)
            ogl.glPopMatrix()
        # Draws rectangular selection area. Could be done in postDraw() instead.
        if self.__selectionMode != Viewer.NONE:
            self.__drawSelectionRectangle()
    def init(self):
        # A ManipulatedFrameSetConstraint will apply displacements to the selection
        self.setManipulatedFrame(ManipulatedFrame())
        self.manipulatedFrame().setConstraint(ManipulatedFrameSetConstraint())
        # Used to display semi-transparent relection rectangle
        ogl.glBlendFunc(ogl.GL_ONE, ogl.GL_ONE)
        
        self.restoreStateFromFile()
        self.help()
    def helpString(self):
        return helpstr
    def closeEvent(self,event):
        helpwidget = self.helpWidget()
        if helpwidget.isVisible() :
            helpwidget.hide()
        QGLViewer.closeEvent(self,event)
    # Selection functions
    def drawWithNames(self):
        for i,obj in enumerate(self.__objects):
            ogl.glPushName(i)
            obj.draw()
            ogl.glPopName()
    def endSelection(self,p):
        selection = self.getMultipleSelection()
        for zmin,zmax,id in selection:
            if self.__selectionMode == Viewer.ADD:
                self.addIdToSelection(id)
            elif self.__selectionMode == Viewer.REMOVE : 
                self.removeIdFromSelection(id)
        self.__selectionMode = Viewer.NONE
    def mousePressEvent(self,e):
        """ Mouse events functions """
        # Start selection. Mode is ADD with Shift key and TOGGLE with Alt key.
        self.__rectangle = QRect(e.pos(), e.pos())
        if e.button() == Qt.LeftButton and e.modifiers() == Qt.ShiftModifier:
            self.__selectionMode = Viewer.ADD
        elif e.button() == Qt.LeftButton and e.modifiers() == Qt.AltModifier:
            self.__selectionMode = Viewer.REMOVE
        else:
            if e.modifiers() == Qt.ControlModifier:
                self.__startManipulation()
            QGLViewer.mousePressEvent(self,e)
    def mouseMoveEvent(self,e):
        if self.__selectionMode != Viewer.NONE:
            # Updates rectangle_ coordinates and redraws rectangle
            self.__rectangle.setBottomRight(e.pos())
            self.updateGL()
        else:
            QGLViewer.mouseMoveEvent(self,e)
    def mouseReleaseEvent(self,e):
        if self.__selectionMode != Viewer.NONE:
            # Actual selection on the rectangular area.
            # Possibly swap left/right and top/bottom to make rectangle_ valid.
            self.__rectangle = self.__rectangle.normalized()
            # Define selection window dimensions
            self.setSelectRegionWidth(self.__rectangle.width())
            self.setSelectRegionHeight(self.__rectangle.height())
            # Compute rectangle center and perform selection
            self.select(self.__rectangle.center())
            # Update display to show new selected objects
            self.updateGL()
        else:
            QGLViewer.mouseReleaseEvent(self,e)
    def __startManipulation(self):
        averagePosition = Vec ()
        mfsc = self.manipulatedFrame().constraint()
        mfsc.clearSet()
        for it in self.__selection:
            mfsc.addObjectToSet(self.__objects[it])
            averagePosition += self.__objects[it].frame.position()
        if len(self.__selection) > 0:
            self.manipulatedFrame().setPosition(averagePosition / len(self.__selection))
    def __drawSelectionRectangle(self):
        self.startScreenCoordinatesSystem()
        ogl.glDisable(ogl.GL_LIGHTING)
        ogl.glEnable(ogl.GL_BLEND)

        ogl.glColor4f(0.0, 0.0, 0.3, 0.3)
        ogl.glBegin(ogl.GL_QUADS)
        ogl.glVertex2i(self.__rectangle.left(),  self.__rectangle.top())
        ogl.glVertex2i(self.__rectangle.right(), self.__rectangle.top())
        ogl.glVertex2i(self.__rectangle.right(), self.__rectangle.bottom())
        ogl.glVertex2i(self.__rectangle.left(),  self.__rectangle.bottom())
        ogl.glEnd()

        ogl.glLineWidth(2.0)
        ogl.glColor4f(0.4, 0.4, 0.5, 0.5)
        ogl.glBegin(ogl.GL_LINE_LOOP)
        ogl.glVertex2i(self.__rectangle.left(),  self.__rectangle.top())
        ogl.glVertex2i(self.__rectangle.right(), self.__rectangle.top())
        ogl.glVertex2i(self.__rectangle.right(), self.__rectangle.bottom())
        ogl.glVertex2i(self.__rectangle.left(),  self.__rectangle.bottom())
        ogl.glEnd()

        ogl.glDisable(ogl.GL_BLEND)
        ogl.glEnable(ogl.GL_LIGHTING)
        self.stopScreenCoordinatesSystem()
    def addIdToSelection(self,id):
        if not id in self.__selection:
            self.__selection.append(id)
    def removeIdFromSelection(self,id):
        self.__selection.remove(id)

  

def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.setWindowTitle("multiSelect")
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()
