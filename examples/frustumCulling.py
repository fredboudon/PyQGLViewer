from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQGLViewer import *
from qgllogo import *
import OpenGL.GL as ogl

helpstr = """<h2>F r u s t u m C u l l i n g</h2>
A hierarchical octree structure is clipped against the camera's frustum clipping planes, obtained
using <code>getFrustumPlanesCoefficients</code>. A second viewer uses <code>drawCamera()</code> to 
display an external view of the first viewer's camera.<br><br>
This frustum culling implementation is quite naive. Many optimisation techniques are available in 
the litterature."""


def corner(c,p1,p2):
    pos = Vec()
    if c&4 :
        pos.x = p1.x
    else:
        pos.x = p2.x
    if c&2 :
        pos.y = p1.y
    else:
        pos.y = p2.y
    if c&1 :
        pos.z = p1.z
    else:
        pos.z = p2.z
    return pos

class CullingCamera (Camera):
    def __init__(self):
        Camera.__init__(self)
        self.planeCoefficients = [[0 for j in range(4)] for i in range(6)]
    def computeFrustumPlanesEquations(self) :
        self.planeCoefficients = self.getFrustumPlanesCoefficients()
    def distanceToFrustumPlane(self,index, pos) :
        return pos * Vec(*(self.planeCoefficients[index][:3])) - self.planeCoefficients[index][3]
    def sphereIsVisible(self,center, radius) :
        for i in range(0,6):
            if self.distanceToFrustumPlane(i, center) > radius:
                return False
        return True
    def aaBoxIsVisible(self,p1, p2):
        allInForAllPlanes = True
        for i in range(0,6):
            allOut = True
            for c in range(0,8):
                pos = corner(c,p1,p2)
                if self.distanceToFrustumPlane(i, pos) > 0.0:
                    allInForAllPlanes = False
                else:
                    allOut = False
        # The eight points are on the outside side of this plane
        if allOut:
            return False,False
        else:
            return True,allInForAllPlanes

class Box:
    def __init__(self, P1, P2) : 
        self.p1 = P1
        self.p2 = P2
        self.level = 0
        self.child = []
    def draw(self) :
        ogl.glColor3f(0.3*self.level, 0.2, 1.0-0.3*self.level)
        ogl.glLineWidth(self.level+1)

        ogl.glBegin(ogl.GL_LINE_STRIP)
        ogl.glVertex3fv((self.p1.x, self.p1.y, self.p1.z))
        ogl.glVertex3fv((self.p1.x, self.p2.y, self.p1.z))
        ogl.glVertex3fv((self.p2.x, self.p2.y, self.p1.z))
        ogl.glVertex3fv((self.p2.x, self.p1.y, self.p1.z))
        ogl.glVertex3fv((self.p1.x, self.p1.y, self.p1.z))
        ogl.glVertex3fv((self.p1.x, self.p1.y, self.p2.z))
        ogl.glVertex3fv((self.p1.x, self.p2.y, self.p2.z))
        ogl.glVertex3fv((self.p2.x, self.p2.y, self.p2.z))
        ogl.glVertex3fv((self.p2.x, self.p1.y, self.p2.z))
        ogl.glVertex3fv((self.p1.x, self.p1.y, self.p2.z))
        ogl.glEnd()

        ogl.glBegin(ogl.GL_LINES)
        ogl.glVertex3fv((self.p1.x, self.p2.y, self.p1.z))
        ogl.glVertex3fv((self.p1.x, self.p2.y, self.p2.z))
        ogl.glVertex3fv((self.p2.x, self.p2.y, self.p1.z))
        ogl.glVertex3fv((self.p2.x, self.p2.y, self.p2.z))
        ogl.glVertex3fv((self.p2.x, self.p1.y, self.p1.z))
        ogl.glVertex3fv((self.p2.x, self.p1.y, self.p2.z))
        ogl.glEnd()
    def drawIfAllChildrenAreVisible(self,camera) :
        visible,entirely = camera.aaBoxIsVisible(self.p1, self.p2)
        if visible:
            if entirely:
                self.draw()
            else:
                if len(self.child) > 0 :
                    for child in self.child:
                        child.drawIfAllChildrenAreVisible(camera)
                else:
                    self.draw()
    def buildBoxHierarchy(self,l):
        self.level = l
        middle = (self.p1+self.p2) / 2.0
        self.child = []
        for i in range(0,8):
            # point in one of the 8 box corners
            point = corner(i,self.p1,self.p2)
            if self.level > 0:
                self.child.append(Box(point, middle))
                self.child[-1].buildBoxHierarchy(l-1)

 
class Viewer(QGLViewer):
    def __init__(self,parent = None):
        QGLViewer.__init__(self,parent)
        self.setStateFileName('.frustumCulling.xml')        
    def setCullingCamera(self,cc):
        self.cullingCamera = cc
    def draw(self):
        Box.Root.drawIfAllChildrenAreVisible(self.cullingCamera)
        if self.cullingCamera == self.camera():
            # Main viewer computes its plane equation
            self.cullingCamera.computeFrustumPlanesEquations()
        else :
            # Observer viewer draws cullingCamera
            ogl.glLineWidth(4.0)
            ogl.glColor4f(1.0, 1.0, 1.0, 0.5)
            self.cullingCamera.draw()
    def init(self):
        # self.restoreStateFromFile()
        if self.cullingCamera != self.camera():
            # Observer viewer configuration
            ogl.glEnable(ogl.GL_BLEND)
            ogl.glBlendFunc(ogl.GL_SRC_ALPHA, ogl.GL_ONE_MINUS_SRC_ALPHA)
        ogl.glDisable(ogl.GL_LIGHTING)
    def helpString(self):
        return helpstr
    def closeEvent(self,event):
        helpwidget = self.helpWidget()
        if helpwidget.isVisible() :
            helpwidget.hide()
        QGLViewer.closeEvent(self,event)

def main():
    qapp = QApplication([])
    
    # Create octree AABBox hierarchy
    p = Vec(1.0, 0.7, 1.3)
    Box.Root = Box(-p, p)
    Box.Root.buildBoxHierarchy(3)
  
    # Instantiate the two viewers.
    hSplit  = QSplitter(Qt.Vertical)
    viewer = Viewer(hSplit)
    observer = Viewer(hSplit)
    
    # Give v a cullingCamera
    cc = CullingCamera()
    viewer.setCamera(cc)
    viewer.showEntireScene()

    # Both viewers share the culling camera
    viewer.setCullingCamera(cc)
    observer.setCullingCamera(cc)

    # Place observer 
    observer.setSceneRadius(10.0)
    observer.camera().setViewDirection(Vec(0.0, -1.0, 0.0))
    observer.showEntireScene()

    # Make sure every culling Camera movement updates the outer viewer
    QObject.connect(viewer.camera().frame(), SIGNAL("manipulated()"), observer.updateGL)
    QObject.connect(viewer.camera().frame(), SIGNAL("spun()"), observer.updateGL)
    
    viewer.help()
    hSplit.setWindowTitle("frustumCulling")
    hSplit.show()
    qapp.exec_()


if __name__ == '__main__':
    main()
