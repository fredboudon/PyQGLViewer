from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQGLViewer import *
from qgllogo import *
import OpenGL.GL as ogl
from math import pi,cos,sin

helpstr = """<h2>S e l e c t</h2>
Left click while pressing the <b>Shift</b> key to select an object of the scene.<br><br>
A line is drawn between the selected point and the camera selection position. 
using <i>convertClickToLine()</i>, a useful function for analytical intersections.<br><br>
To add object selection in your viewer, all you need to do is to define the <i>drawWithNames</i> function. 
It gives a name to each selectable object and selection is then performed using the OpenGL <i>GL_SELECT</i> render mode.<br><br>
Feel free to cut and paste this implementation in your own applications."""

class Viewer(QGLViewer):
    def __init__(self):
        QGLViewer.__init__(self)
        self.setStateFileName('.select.xml')        
        self.nb = 10
        self.orig= Vec()
        self.dir= Vec()
        self.selectedPoint = Vec()
        QObject.connect(self,SIGNAL("pointSelected(QMouseEvent*)"),self.mypostSelection)
    def draw(self):
        # Draw ten spirals
        for i in range(self.nb):
            ogl.glPushMatrix()
            ogl.glTranslatef(cos(2.0*i*pi/self.nb), sin(2.0*i*pi/self.nb), 0.0)
            draw_qgl_logo(200.,i == self.selectedName())
            ogl.glPopMatrix()
        # Draw the intersection line
        ogl.glBegin(ogl.GL_LINES)
        ogl.glVertex3fv(list(self.orig))
        ogl.glVertex3fv(list(self.orig + 100.0*self.dir))
        ogl.glEnd()

        # Draw (approximated) intersection point on selected object
        if self.selectedName() >= 0:
            ogl.glColor3f(0.9, 0.2, 0.1)
            ogl.glBegin(ogl.GL_POINTS)
            ogl.glVertex3fv(list(self.selectedPoint))
            ogl.glEnd()
    def drawWithNames(self):
        # Draw spirals, pushing a name (id) for each of them
        for i in range(self.nb):
            ogl.glPushMatrix()
            ogl.glTranslatef(cos(2.0*i*pi/self.nb), sin(2.0*i*pi/self.nb), 0.)

            ogl.glPushName(i)
            draw_qgl_logo()
            ogl.glPopName()

            ogl.glPopMatrix()
    def mypostSelection(self,event):
        point = event.pos()
        # Compute orig and dir, used to draw a representation of the intersecting line
        self.orig, self.dir = self.camera().convertClickToLine(point)

        # Find the selectedPoint coordinates, using camera()->pointUnderPixel().
        self.selectedPoint, found = self.camera().pointUnderPixel(point)
        self.selectedPoint -= 0.01*self.dir # Small offset to make point clearly visible.
        # Note that "found" is different from (selectedObjectId()>=0) because of the size of the select region.

        if self.selectedName() == -1:
            QMessageBox.information(self, "No selection",
                 "No object selected under pixel " + str(point.x()) + "," + str(point.y()))
        else:
            QMessageBox.information(self, "Selection",
                 "Spiral number " + str(self.selectedName()) + " selected under pixel " +
                 str(point.x()) + "," + str(point.y()))
    def init(self):
        self.restoreStateFromFile()
        ogl.glLineWidth(3.0)
        ogl.glPointSize(10.0)
        self.help()
    def helpString(self):
        return helpstr
    def closeEvent(self,event):
        helpwidget = self.helpWidget()
        if helpwidget.isVisible() :
            helpwidget.hide()
        QGLViewer.closeEvent(self,event)

def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.setWindowTitle("select")
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()
