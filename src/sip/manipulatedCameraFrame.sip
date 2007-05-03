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

class ManipulatedCameraFrame : ManipulatedFrame 
{

%TypeHeaderCode
#include <QGLViewer/manipulatedCameraFrame.h>
using qglviewer::ManipulatedCameraFrame;
#include <QGLViewer/camera.h>
using qglviewer::Camera;
%End

  public:
    ManipulatedCameraFrame();
    virtual ~ManipulatedCameraFrame() ;

    ManipulatedCameraFrame(const ManipulatedCameraFrame& mcf);
    // ManipulatedCameraFrame& operator=(const ManipulatedCameraFrame& mcf);

  public:
    Vec revolveAroundPoint() const;
    void setRevolveAroundPoint(const Vec& revolveAroundPoint) ; 

  public slots:
    void setFlySpeed(float speed) ;
    void setFlyUpVector(const Vec& up) ;

  public:
    float flySpeed() const ;
    Vec flyUpVector() const ;

  protected:
    virtual void mouseReleaseEvent(QMouseEvent* event, Camera* camera);
    virtual void mouseMoveEvent   (QMouseEvent* event, Camera* camera);
    virtual void wheelEvent       (QWheelEvent* event, Camera* camera);

  protected slots:
    virtual void spin();

  public:
    virtual QDomElement domElement(const QString& name, QDomDocument& document) const;
  public slots:
    virtual void initFromDOMElement(const QDomElement& element);

  protected:
    virtual void startAction(int ma, bool withConstraint=true); 

  private slots:
    virtual void flyUpdate();

  private:
    void updateFlyUpVector();
    Quaternion turnQuaternion(int x, const Camera* camera);
    Quaternion pitchYawQuaternion(int x, int y, const Camera* camera);

};

