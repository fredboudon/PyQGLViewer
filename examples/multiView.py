from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQGLViewer import *
from qgllogo import *
import OpenGL.GL as ogl

class Scene:
    def __init__(self):
        pass
    def draw(self):
        draw_qgl_logo()

class Viewer(QGLViewer):
    def __init__(self,scene, view_type, parent, shareWidget = None):
        QGLViewer.__init__(self,parent,shareWidget)
        self.setStateFileName('.multiView.xml')        
        self.__scene = scene
        self.setAxisIsDrawn()
        self.setGridIsDrawn()

        if view_type < 3:
            # Move camera according to viewer type (on X, Y or Z axis)
            position = { 0 : Vec(1.0,0.0,0.0) , 1 : Vec(0.0,1.0,0.0), 2 : Vec(0.0,0.0,1.0) }
            self.camera().setPosition(position[view_type])
            self.camera().lookAt(self.sceneCenter())

            self.camera().setType(Camera.ORTHOGRAPHIC)
            self.camera().showEntireScene()

            # Forbid rotation
            self.constraint = WorldConstraint()
            self.constraint.setRotationConstraintType(AxisPlaneConstraint.FORBIDDEN)
            self.camera().frame().setConstraint(self.constraint)

    def draw(self):
        self.__scene.draw()

def main():
    qapp = QApplication([])
    hSplit  = QSplitter(Qt.Vertical)
    vSplit1 = QSplitter(hSplit)
    vSplit2 = QSplitter(hSplit)
    
    # Create the scene
    scene = Scene()

    # Instantiate the viewers.
    side  = Viewer(scene,0,vSplit1)
    top   = Viewer(scene,1,vSplit1, side)
    front = Viewer(scene,2,vSplit2, side)
    persp = Viewer(scene,3,vSplit2, side)
    
    hSplit.setWindowTitle("multiView")    
    hSplit.show()
    qapp.exec_()

if __name__ == '__main__':
    main()
