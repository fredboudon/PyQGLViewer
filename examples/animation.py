from PyQt4.QtGui import *
from PyQGLViewer import *
import OpenGL.GL as ogl
import math
import random as rd

class Particle:
    def __init__(self):
        self.init()
    def init(self):
        self.pos = Vec(0.0,0.0,0.0)
        angle = 2.0 * math.pi * rd.uniform(0,1) 
        norm  = 0.04 * rd.uniform(0,1)
        self.speed = Vec(norm*math.cos(angle), norm*math.sin(angle), rd.uniform(0,1) )
        self.age = 0
        self.ageMax = 50 + rd.uniform(0,100)
    def draw(self):
        ogl.glColor3f(self.age/self.ageMax, self.age/self.ageMax, 1.0)
        ogl.glVertex3f(self.pos.x,self.pos.y,self.pos.z)
    def animate(self):
        self.speed.z -= 0.05
        self.pos     += self.speed * 0.1
        if self.pos.z < 0.0:
            self.speed.z = -0.8*self.speed.z
            self.pos.z = 0.0
        self.age +=1
        if self.age >= self.ageMax:
            self.init()

helpstr = """<h2>A n i m a t i o n</h2>
Use the <i>animate()</i> function to implement the animation part of your
application. Once the animation is started, <i>animate()</i> and <i>draw()</i>
are called in an infinite loop, at a frequency that can be fixed.<br><br>
Press <b>Return</b> to start/stop the animation."""
 
class Viewer(QGLViewer):
    def __init__(self):
        QGLViewer.__init__(self)
        self.setStateFileName('.animation.xml')        
        self.particles = []
    def init(self):
        self.restoreStateFromFile()
        ogl.glDisable(ogl.GL_LIGHTING)
        self.particles = [Particle() for i in range(2000)]
        ogl.glPointSize(3.0)
        self.setGridIsDrawn()
        self.help()
        self.startAnimation()
    def draw(self):
        ogl.glBegin(ogl.GL_POINTS)
        for p in self.particles:
            p.draw()
        ogl.glEnd()
    def animate(self):
        for p in self.particles:
            p.animate()        
    def helpString(self):
        return helpstr

def main(argv = []):
    app = QApplication(argv)
    viewer = Viewer()
    viewer.setWindowTitle("animation")
    viewer.show()
    app.exec_()

if __name__ == '__main__':
    main()
