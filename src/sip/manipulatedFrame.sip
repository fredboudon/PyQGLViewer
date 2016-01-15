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

class ManipulatedFrame : Frame, MouseGrabber
{

%TypeHeaderCode
#include <QGLViewer/manipulatedFrame.h>
using qglviewer::ManipulatedFrame;
#include <QGLViewer/camera.h>
using qglviewer::Camera;
%End

  public:
    ManipulatedFrame();
    virtual ~ManipulatedFrame() ;

    ManipulatedFrame(const ManipulatedFrame& mf);
    // ManipulatedFrame& operator=(const ManipulatedFrame& mf);

    signals:
    void manipulated();
    void spun();

  public slots:
    void setRotationSensitivity(qreal sensitivity) ;
    void setTranslationSensitivity(qreal sensitivity) ;
    void setSpinningSensitivity(qreal sensitivity) ;
    void setWheelSensitivity(qreal sensitivity) ;
    
%If (QGLViewer_2_6_0 - )
    void setZoomSensitivity(qreal sensitivity);
%End

  public:
    qreal rotationSensitivity() const ;
    qreal translationSensitivity() const ;
    qreal spinningSensitivity() const ;
    qreal wheelSensitivity() const ;
%If (QGLViewer_2_6_0 - )
    qreal zoomSensitivity() const;
%End

  public:
    bool isSpinning() const ;
    Quaternion spinningQuaternion() const ;

  public slots:
    void setSpinningQuaternion(const Quaternion& spinningQuaternion /In/);
    virtual void startSpinning(int updateInterval);
    virtual void stopSpinning() ;
  protected slots:
    virtual void spin();
  private slots:
    void spinUpdate();
  protected:
    virtual void mousePressEvent      (QMouseEvent* event /In/, Camera* camera /In/); 
    virtual void mouseMoveEvent       (QMouseEvent* event /In/, Camera* camera /In/);
    virtual void mouseReleaseEvent    (QMouseEvent* event /In/, Camera* camera /In/);
    virtual void mouseDoubleClickEvent(QMouseEvent* event /In/, Camera* camera /In/);
    virtual void wheelEvent           (QWheelEvent* event /In/, Camera* camera /In/);

  public:
    bool isManipulated() const;
%If (QGLViewer_2_6_0 - )
    QGLViewer::MouseAction currentMouseAction() const ;
%End

  public:
    virtual void checkIfGrabsMouse(int x, int y, const Camera* camera /In/);

  public:
    virtual QDomElement domElement(const QString& name /In/, QDomDocument& document /In/) const;
  public slots:
    virtual void initFromDOMElement(const QDomElement& element /In/);

  protected:
    Quaternion deformedBallQuaternion(int x, int y, qreal cx, qreal cy, const Camera* camera /In/);
    virtual void startAction(int ma, bool withConstraint=true); 
    void computeMouseSpeed(const QMouseEvent* e /In/);
    int mouseOriginalDirection(const QMouseEvent* e /In/);
%If (QGLViewer_2_6_0 - )
    qreal deltaWithPrevPos(QMouseEvent*  event /In/, Camera* camera /In/) const;
    /*! Returns a normalized wheel delta, proportionnal to wheelSensitivity(). */
    qreal wheelDelta(const QWheelEvent* event /In/) const;
%End
  };

