from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQGLViewer import *
from qgllogo import *
import OpenGL.GL as ogl

helpstr = """<<h2>S t a n d a r d C a m e r a</h2>
An overloaded <code>Camera</code> class is used, that reproduces the 'standard' OpenGL settings.<br><br>
With this camera, the near and (resp. far) plane distance is set to a very small (resp. very large) value.
With the orthographic camera type, the frustum dimensions are fixed. Use <code>Shift</code> and the mouse wheel to change them.<br><br>
On the other hand, the QGLViewer camera fits the near and far distances to the scene radius. 
Fine tuning is available using <code>zClippingCoefficient()</code> and <code>zNearCoefficient()</code>.
However, visual results do not seem to be impacted by this zBuffer fitted range.<br><br>
The QGLViewer camera also adapts the orthographic frustum dimensions to the distance to the <code>revolveAroundPoint()</code> to mimic a perspective camera.
Since this behavior may not be needed, this example shows how to override it.<br><br>
The second viewer displays the first one's camera to show its configuration.<br><br>
Use <b>M</b> to switch between 'standard' and QGLViewer camera behavior.<br>
Use <b>T</b> to switch between perspective and orthographic camera type.<br><br>
Use <b>Shift+wheel</b> to change standard camera orthographic size."""

class StandardCamera (Camera):
    def __init__(self):
        Camera.__init__(self)
        self.standard  = True
        self.orthoSize = 1.0
    def toggleMode(self) :
        self.standard = not self.standard
    def isStandard(self) :
        return self.standard
    def zNear(self) :
        if self.standard:
            return 0.001 
        else :
            return Camera.zNear(self)
    def zFar(self) :
        if self.standard:
            return 1000.0
        else :
            return Camera.zFar(self)
    def changeOrthoFrustumSize(self,delta):
        if delta > 0:
            self.orthoSize *= 1.1
        else:
            self.orthoSize /= 1.1
    def getOrthoWidthHeight(self):
        if self.standard :
            return self.aspectRatio() * self.orthoSize, self.orthoSize
        else :
            return Camera.getOrthoWidthHeight(self)

class CameraViewer (QGLViewer):
    def __init__(self,camera,parent = None):
        QGLViewer.__init__(self,parent)
        self.c = camera
    def draw(self):
        draw_qgl_logo()
        # Draws the other viewer's camera
        ogl.glDisable(ogl.GL_LIGHTING)
        ogl.glLineWidth(4.0)
        ogl.glColor4f(1.0, 1.0, 1.0, 0.5)
        self.c.draw()
        ogl.glEnable(ogl.GL_LIGHTING)
    def init(self):
        if not self.restoreStateFromFile():
            # Make near and far planes much further from scene in order not to clip c's display.
            self.camera().setZClippingCoefficient(50.0)
            self.camera().setViewDirection(Vec(0.0, -1.0, 0.0))
            self.showEntireScene()
        # Enable semi-transparent culling planes
        ogl.glEnable(ogl.GL_BLEND)
        ogl.glBlendFunc(ogl.GL_SRC_ALPHA, ogl.GL_ONE_MINUS_SRC_ALPHA)


class Viewer(QGLViewer):
    def __init__(self,camera,parent = None):
        QGLViewer.__init__(self,parent)
        self.setStateFileName('.standardCamera.xml')        
        self.setCamera(camera)
    def draw(self):
        draw_qgl_logo()
    def init(self):
        if not self.restoreStateFromFile():
            self.showEntireScene()

        self.setKeyDescription(Qt.Key_T, "Toggles camera type (perspective or orthographic)")
        self.setKeyDescription(Qt.Key_M, "Toggles camera mode (standard or QGLViewer)")
        self.setMouseBindingDescription(Qt.SHIFT + Qt.MidButton, "Change frustum size (for standard camera in orthographic mode)")
        
        self.help()
    def helpString(self):
        return helpstr
    def closeEvent(self,event):
        helpwidget = self.helpWidget()
        if helpwidget.isVisible() :
            helpwidget.hide()
        QGLViewer.closeEvent(self,event)
    def keyPressEvent(self,e):
        if e.key() == Qt.Key_M :
            # 'M' changes mode : standard or QGLViewer camera
            self.camera().toggleMode()
            self.__showMessage()
        elif e.key() == Qt.Key_T:
            # 'T' changes the projection type : perspective or orthogonal
            if self.camera().type() == Camera.ORTHOGRAPHIC:
                self.camera().setType(Camera.PERSPECTIVE)
            else:
                self.camera().setType(Camera.ORTHOGRAPHIC)
            self.__showMessage()
        else:
            QGLViewer.keyPressEvent(self,e)
    def wheelEvent (self,e):
        if self.camera().type() == Camera.ORTHOGRAPHIC and self.camera().isStandard() and (e.modifiers() & Qt.ShiftModifier) :
            self.camera().changeOrthoFrustumSize(e.delta())
            self.emit(SIGNAL("cameraChanged()"))
            self.updateGL()
        else:
            QGLViewer.wheelEvent(self,e)
    def __showMessage(self):
        if self.camera().isStandard():
            std = "Standard camera"
        else:
            std = "QGLViewer camera"
        if self.camera().type() == Camera.PERSPECTIVE:
            camera_type = "Perspective"
        else :
            camera_type = "Orthographic"
        self.displayMessage(std + " - " + camera_type)
        self.emit(SIGNAL("cameraChanged()"))

def main(singleWidget = True):
    qapp = QApplication([])
  
    # Instantiate the two viewers.
    sc = StandardCamera()
    if singleWidget :
        hSplit  = QSplitter(Qt.Vertical)
    else:
        hSplit  = None
    viewer = Viewer(sc,hSplit)
    cviewer = CameraViewer(sc,hSplit)
    
    # Make sure every v camera movement updates the camera viewer
    QObject.connect(viewer.camera().frame(), SIGNAL("manipulated()"), cviewer.updateGL)
    QObject.connect(viewer.camera().frame(), SIGNAL("spun()"), cviewer.updateGL)
    # Also update on camera change (type or mode)
    QObject.connect(viewer, SIGNAL("cameraChanged()"), cviewer.updateGL)
  
    if singleWidget :
        hSplit.setWindowTitle("standardCamera")
        hSplit.show()
    else:
        viewer.setWindowTitle("standardCamera")
        cviewer.setWindowTitle("Camera Viewer")
        viewer.show()
        cviewer.show()
    
    qapp.exec_()

if __name__ == '__main__':
    main()

