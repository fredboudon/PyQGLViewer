/****************************************************************************

 Copyright (C) 2007 Frederic Boudon (frederic.boudon@cirad.fr)
 This file is part of the PyQGLViewer Python extension module.
 It is based on libQGLViewer project developped by Gilles Debunne
 http://artis.imag.fr/Members/Gilles.Debunne/QGLViewer

 PyQGLViewer is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 PyQGLViewer is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with PyQGLViewer; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

*****************************************************************************/

class MouseGrabber
{

%TypeHeaderCode
#include <QGLViewer/mouseGrabber.h>
using qglviewer::MouseGrabber;
#include <QGLViewer/camera.h>
using qglviewer::Camera;
%End

  public:
    MouseGrabber();
    virtual ~MouseGrabber();

  public:
    virtual void checkIfGrabsMouse(int x, int y, const Camera* camera /In/) = 0;
    bool grabsMouse() const ;

  protected:
    void setGrabsMouse(bool grabs) ;

  public:
    static const QList<MouseGrabber*>& MouseGrabberPool() ;

    bool isInMouseGrabberPool() const ;
    void addInMouseGrabberPool();
    void removeFromMouseGrabberPool();
    void clearMouseGrabberPool(bool autoDelete=false);

  protected:
    virtual void mousePressEvent       (QMouseEvent* event /In/, Camera* camera /In/) ;
    virtual void mouseDoubleClickEvent (QMouseEvent* event /In/, Camera* camera /In/) ;
    virtual void mouseReleaseEvent     (QMouseEvent* event /In/, Camera* camera /In/) ;
    virtual void mouseMoveEvent        (QMouseEvent* event /In/, Camera* camera /In/) ;
    virtual void wheelEvent            (QWheelEvent* event /In/, Camera* camera /In/) ;

  private:
    MouseGrabber(const MouseGrabber&);
};

