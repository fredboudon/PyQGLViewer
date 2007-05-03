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
    void setRotationSensitivity(float sensitivity) ;
    void setTranslationSensitivity(float sensitivity) ;
    void setSpinningSensitivity(float sensitivity) ;
    void setWheelSensitivity(float sensitivity) ;
  public:
    float rotationSensitivity() const ;
    float translationSensitivity() const ;
    float spinningSensitivity() const ;
    float wheelSensitivity() const ;

  public:
    bool isSpinning() const ;
    Quaternion spinningQuaternion() const ;

  public slots:
    void setSpinningQuaternion(const Quaternion& spinningQuaternion);
    virtual void startSpinning(int updateInterval);
    virtual void stopSpinning() ;
  protected slots:
    virtual void spin();
  private slots:
    void spinUpdate();
  protected:
    virtual void mousePressEvent      (QMouseEvent* event, Camera* camera); 
    virtual void mouseMoveEvent       (QMouseEvent* event, Camera* camera);
    virtual void mouseReleaseEvent    (QMouseEvent* event, Camera* camera);
    virtual void mouseDoubleClickEvent(QMouseEvent* event, Camera* camera);
    virtual void wheelEvent           (QWheelEvent* event, Camera* camera);

  public:
    bool isManipulated() const;

  public:
    virtual void checkIfGrabsMouse(int x, int y, const Camera* camera);

  public:
    virtual QDomElement domElement(const QString& name, QDomDocument& document) const;
  public slots:
    virtual void initFromDOMElement(const QDomElement& element);

  protected:
    Quaternion deformedBallQuaternion(int x, int y, float cx, float cy, const Camera* camera);
    virtual void startAction(int ma, bool withConstraint=true); 
    void computeMouseSpeed(const QMouseEvent* e);
    int mouseOriginalDirection(const QMouseEvent* e);

  };

