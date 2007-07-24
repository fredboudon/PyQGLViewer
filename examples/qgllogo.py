import OpenGL.GL as ogl
import math

def draw_qgl_logo(nbSteps = 200.0, specialColor = False):
    ogl.glBegin(ogl.GL_QUAD_STRIP)
    for i in range(0,int(nbSteps)):
        ratio = i/float(nbSteps)
        angle = 21.0*ratio
        c = math.cos(angle)
        s = math.sin(angle)
        r1 = 1.0 - 0.8*ratio
        r2 = 0.8 - 0.8*ratio
        alt = ratio - 0.5
        nor = 0.5
        up = math.sqrt(1.0-nor*nor)
        if specialColor:
            ogl.glColor3f(1.0-ratio, .8 , ratio/2.0)
        else:
            ogl.glColor3f(1.0-ratio, 0.2 , ratio)
        ogl.glNormal3f(nor*c, up, nor*s)
        ogl.glVertex3f(r1*c, alt, r1*s)
        ogl.glVertex3f(r2*c, alt+0.05, r2*s)
    ogl.glEnd()

