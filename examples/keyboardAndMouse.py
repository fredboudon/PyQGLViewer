from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQGLViewer import *
from qgllogo import *
import OpenGL.GL as ogl

helpstr = """<h2>K e y b o a r d A n d M o u s e</h2>
This example illustrates the mouse and key bindings customization.<br><br>
Use <code>setShortcut()</code> to change standard action key bindings (display of axis, grid or fps, exit shortcut...).<br><br>
Use <code>setMouseBinding()</code> and <code>setWheelBinding()</code> to change standard action mouse bindings 
(camera rotation, translation, object selection...).<br><br>
If you want to define <b>new</b> key or mouse actions, overload <code>keyPressEvent()</code> and/or 
<code>mouse(Press|Move|Release)Event()</code> to define and bind your own new actions. 
Use <code>setKeyDescription()</code> and <code>setMouseBindingDescription()</code> to add a description of your bindings in the help window.<br><br>
In this example, we defined the <b>F</b> and <b>W</b> keys and the right mouse button opens a popup menu. 
See the keyboard and mouse tabs in this help window for the complete bindings description.<br><br>
By the way, exit shortcut has been binded to <b>Ctrl+Q</b>."""

class Viewer(QGLViewer):
    def __init__(self):
        QGLViewer.__init__(self)
        self.setStateFileName('.keyboardAndMouse.xml')        
        self.__wireframe = False
        self.__flatShading = False
    def draw(self):
        draw_qgl_logo()
    def init(self):
        self.restoreStateFromFile()
        #       Keyboard shortcut customization
        #      Changes standard action key bindings
        # Define 'Control+Q' as the new exit shortcut (default was 'Escape')
        self.setShortcut(QGLViewer.EXIT_VIEWER, Qt.CTRL+Qt.Key_Q)
        # Set 'Control+F' as the FPS toggle state key.
        self.setShortcut(QGLViewer.DISPLAY_FPS, Qt.CTRL+Qt.Key_F)
        # Disable draw grid toggle shortcut (default was 'G')
        self.setShortcut(QGLViewer.DRAW_GRID, 0)
        # Add custom key description (see keyPressEvent).
        self.setKeyDescription(Qt.Key_W, "Toggles wire frame display")
        self.setKeyDescription(Qt.Key_F, "Toggles flat shading display")
        #         Mouse bindings customization
        #     Changes standard action mouse bindings
        # Left and right buttons together make a camera zoom : emulates a mouse third button if needed.
        self.setMouseBinding(Qt.LeftButton | Qt.RightButton, QGLViewer.CAMERA, QGLViewer.ZOOM)
        # Disable previous TRANSLATE mouse binding (and remove it from help mouse tab).
        self.setMouseBinding(Qt.RightButton, QGLViewer.NO_CLICK_ACTION)
        self.setMouseBinding(int(Qt.ControlModifier) | Qt.ShiftModifier | Qt.RightButton, QGLViewer.SELECT)
        self.setWheelBinding(Qt.AltModifier, QGLViewer.CAMERA, QGLViewer.MOVE_FORWARD)
        self.setMouseBinding(int(Qt.AltModifier) | Qt.LeftButton, QGLViewer.CAMERA, QGLViewer.TRANSLATE)
        # Add custom mouse bindings description (see mousePressEvent())
        self.setMouseBindingDescription(Qt.RightButton, "Opens a camera path context menu")
        # Display the help window. The help window tabs are automatically updated when you define new
        # standard key or mouse bindings (as is done above). Custom bindings descriptions are added using
        # setKeyDescription() and setMouseBindingDescription().
        self.help()
    def helpString(self):
        return helpstr
    def closeEvent(self,event):
        helpwidget = self.helpWidget()
        if helpwidget and helpwidget.isVisible() :
            helpwidget.hide()
        QGLViewer.closeEvent(self,event)
    def keyPressEvent(self,e):
        modifiers = e.modifiers()
        # A simple switch on e->key() is not sufficient if we want to take state key into account.
        # With a switch, it would have been impossible to separate 'F' from 'CTRL+F'.
        # That's why we use imbricated if...else and a "handled" boolean.
        handled = False
        if ((e.key()==Qt.Key_W) and (modifiers==Qt.NoModifier)):
            self.__wireframe = not self.__wireframe
            if self.__wireframe:
                ogl.glPolygonMode(ogl.GL_FRONT_AND_BACK, ogl.GL_LINE)
            else:
                ogl.glPolygonMode(ogl.GL_FRONT_AND_BACK, ogl.GL_FILL)
            handled = True
            self.updateGL()
        elif (e.key()==Qt.Key_F) and (modifiers==Qt.NoModifier):
            self.__flatShading = not self.__flatShading
            if self.__flatShading:
                ogl.glShadeModel(ogl.GL_FLAT)
            else:
                ogl.glShadeModel(ogl.GL_SMOOTH)
            handled = True
            self.updateGL()
        # ... and so on with other elif blocks.
        
        if not handled:
            QGLViewer.keyPressEvent(self,e)
    def mousePressEvent(self,e):
        if (e.button() == Qt.RightButton) and (e.modifiers() == Qt.NoModifier):
            menu= QMenu( self )
            menu.addAction("Camera positions")
            menu.addSeparator()
            menuMap = {}

            atLeastOne = False
            # We only test the 20 first indexes. This is a limitation.
            for i in range(20):
                if self.camera().keyFrameInterpolator(i):
                    atLeastOne = True
                    if camera().keyFrameInterpolator(i).numberOfKeyFrames() == 1:
                        text = "Position "+str(i)
                    else:
                        text = "Path "+str(i)
                    menuMap[menu.addAction(text)] = i

            if not atLeastOne:
                menu.addAction("No position defined")
                menu.addAction("Use to Alt+Fx to define one")

            action = menu.exec_(e.globalPos())

            if atLeastOne and action:
                self.camera().playPath(menuMap[action])
        else:
            QGLViewer.mousePressEvent(self,e)

def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.setWindowTitle("keyboardAndMouse")
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()
