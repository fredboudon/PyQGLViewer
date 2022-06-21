from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQGLViewer import *
from qgllogo import *
import OpenGL.GL as ogl

class Scene:
    def __init__(self):
        pass
    def draw(self):
        draw_qgl_logo()

class Viewer(QGLViewer):
    def __init__(self,scene, view_type, parent):
        QGLViewer.__init__(self,parent)
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
    top   = Viewer(scene,1,vSplit1)
    front = Viewer(scene,2,vSplit2)
    persp = Viewer(scene,3,vSplit2)
    
    hSplit.setWindowTitle("multiView")    
    hSplit.show()
    qapp.exec_()

if __name__ == '__main__':
    main()
