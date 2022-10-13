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

class Camera
{

%TypeHeaderCode
#include <QGLViewer/camera.h>
using qglviewer::Camera;
%End
public:
    Camera();
    virtual ~Camera();

    Camera(const Camera& camera);

    enum Type { PERSPECTIVE, ORTHOGRAPHIC };

    Vec position() const;
    Vec upVector() const;
    Vec viewDirection() const;
    Vec rightVector() const;
    
    Quaternion orientation() const;
    void setFromModelViewMatrix(SIP_PYOBJECT modelViewMatrix);
%MethodCode
	int isSequence = PySequence_Check(a0);
	if (!isSequence || PySequence_Size(a0) != 16)
        sipIsErr = 1;
    else
    {
		GLdouble src[16];
		for (int i = 0; i < 16; ++i)
			src[i] = PyFloat_AsDouble(PySequence_GetItem(a0,i));
		sipCpp->setFromModelViewMatrix(src);
	}	
%End

    void setFromProjectionMatrix(SIP_PYOBJECT matrix);
%MethodCode	
	int isSequence = PySequence_Check(a0);
	if (!isSequence || PySequence_Size(a0) != 12)
        sipIsErr = 1;
    else
    {
		GLdouble src[12];
		for (int i = 0; i < 12; ++i)
			src[i] = PyFloat_AsDouble(PySequence_GetItem(a0,i));
		sipCpp->setFromModelViewMatrix(src);
	}	
%End

  public slots:
    void setPosition(const Vec& pos /In/) ;
    void setOrientation(const Quaternion& q /In/);
    void setOrientation(qreal theta, qreal phi);
    void setUpVector(const Vec& up /In/, bool noMove=true);
    void setViewDirection(const Vec& direction /In/);

    void lookAt(const Vec& target /In/);
    void showEntireScene();
    void fitSphere(const Vec& center /In/, qreal radius);
    void fitBoundingBox(const Vec& min /In/, const Vec& max /In/);
    void fitScreenRegion(const QRect& rectangle /In/);
    void centerScene();
    void interpolateToZoomOnPixel(const QPoint& pixel /In/);
    void interpolateToFitScene();
    void interpolateTo(const Frame& fr /In/, qreal duration);

public:
    Type type() const;
    qreal fieldOfView() const;
    qreal horizontalFieldOfView() const;
    qreal aspectRatio() const;
    int screenWidth() const;
    int screenHeight() const;
    SIP_PYOBJECT getViewport() const;
%MethodCode	
	GLint viewport[4];
	sipCpp->getViewport(viewport);
	sipRes = PyList_New(4);
	for(int i = 0; i < 4; ++i)
		PyList_SetItem(sipRes,i,PyLong_FromLong(viewport[i]));
%End

    qreal pixelGLRatio(Vec position) const;
    qreal zNearCoefficient() const;
    
    qreal zClippingCoefficient() const;
    virtual qreal zNear() const;
    virtual qreal zFar()  const;
    virtual void getOrthoWidthHeight(GLdouble& halfWidth /Out/, GLdouble& halfHeight /Out/) const;
    
    SIP_PYOBJECT getFrustumPlanesCoefficients() const;
%MethodCode	
	GLdouble coef[6][4];
	sipCpp->getFrustumPlanesCoefficients(coef);
	sipRes = PyList_New(6);
	for(int i = 0; i < 6; ++i){
		PyObject * row = PyList_New(4);
		for(int j = 0; j < 4; ++j){
			PyList_SetItem(row,j,PyFloat_FromDouble(coef[i][j]));
		}
		PyList_SetItem(sipRes,i,row);
	}
%End

  public slots:
    void setType(Type type);

    void setFieldOfView(qreal fov) ;
    void setHorizontalFieldOfView(qreal hfov);

    void setFOVToFitScene();
    void setAspectRatio(qreal aspect);

    void setScreenWidthAndHeight(int width, int height);
    void setZNearCoefficient(qreal coef);
    void setZClippingCoefficient(qreal coef);

public:
    qreal sceneRadius() const ;

    Vec sceneCenter() const ;
    qreal distanceToSceneCenter() const;
    
  public slots:
    void setSceneRadius(qreal radius);
    void setSceneCenter(const Vec& center /In/);
    bool setSceneCenterFromPixel(const QPoint& pixel /In/);
    void setSceneBoundingBox(const Vec& min /In/, const Vec& max /In/);

 public slots:
 %If (QGLViewer_2_6_0 - )
    void setPivotPoint(const Vec& point /In/);
    bool setPivotPointFromPixel(const QPoint& pixel /In/);

public:
     Vec pivotPoint() const;
 
 public slots:
 %End

    void setRevolveAroundPoint(const Vec& point /In/);
    bool setRevolveAroundPointFromPixel(const QPoint& pixel /In/);

 public:
    Vec revolveAroundPoint() const;
 
 public:
    ManipulatedCameraFrame* frame() const;
 public slots:
    void setFrame(ManipulatedCameraFrame* mcf /Transfer/);

 public:
    KeyFrameInterpolator* keyFrameInterpolator(unsigned int i) const;

 public slots:
    void setKeyFrameInterpolator(unsigned int i, KeyFrameInterpolator* kfi /Transfer/);
    virtual void addKeyFrameToPath(unsigned int i);
    virtual void playPath(unsigned int i);
    virtual void deletePath(unsigned int i);
    virtual void resetPath(unsigned int i);
    virtual void drawAllPaths();

  public:
    virtual void loadProjectionMatrix(bool reset=true) const;
    virtual void loadModelViewMatrix(bool reset=true) const;
    void computeProjectionMatrix() const;
    void computeModelViewMatrix() const;

    virtual void loadProjectionMatrixStereo(bool leftBuffer=true) const;
    virtual void loadModelViewMatrixStereo(bool leftBuffer=true) const;

    SIP_PYOBJECT getProjectionMatrix() const;
%MethodCode	
	GLdouble m[16];
	sipCpp->getProjectionMatrix(m);
	sipRes = PyList_New(16);
	for(int i = 0; i < 16; ++i)
		PyList_SetItem(sipRes,i,PyFloat_FromDouble(m[i]));
%End

    SIP_PYOBJECT getModelViewMatrix() const;
%MethodCode	
	GLdouble m[16];
	sipCpp->getModelViewMatrix(m);
	sipRes = PyList_New(16);
	for(int i = 0; i < 16; ++i)
		PyList_SetItem(sipRes,i,PyFloat_FromDouble(m[i]));
%End

    SIP_PYOBJECT getModelViewProjectionMatrix() const;
%MethodCode	
	GLdouble m[16];
	sipCpp->getModelViewProjectionMatrix(m);
	sipRes = PyList_New(16);
	for(int i = 0; i < 16; ++i)
		PyList_SetItem(sipRes,i,PyFloat_FromDouble(m[i]));
%End

    static void drawCamera(qreal scale=1.0, qreal aspectRatio=1.33, qreal fieldOfView=qreal(M_PI)/4.0);
    virtual void draw(bool drawFarPlane=true, qreal scale=1.0) const;

  public:
    Vec cameraCoordinatesOf(Vec src) const ;
    Vec worldCoordinatesOf(Vec src) const ;
    
    // void getCameraCoordinatesOf(const float src[3], float res[3]) const;
	SIP_PYOBJECT getCameraCoordinatesOf(SIP_PYOBJECT) const;
%MethodCode
	int isSequence = PySequence_Check(a0);
	if (!isSequence || PySequence_Size(a0) != 3)
        sipIsErr = 1;
    else
    {
		qreal src[3];
		for (int i = 0; i < 3; ++i)
			src[i] = PyFloat_AsDouble(PySequence_GetItem(a0,i));
		qreal res[3];
		sipCpp->getCameraCoordinatesOf(src,res);
		sipRes = PyTuple_New(3);
		for(int i = 0; i < 3; ++i)
			PyTuple_SetItem(sipRes,i,PyFloat_FromDouble(res[i]));
	}	
%End
    
    // void getWorldCoordinatesOf(const float src[3], float res[3]) const;
	SIP_PYOBJECT getWorldCoordinatesOf(SIP_PYOBJECT) const;
%MethodCode
	int isSequence = PySequence_Check(a0);
	if (!isSequence || PySequence_Size(a0) != 3)
        sipIsErr = 1;
    else
    {
		qreal src[3];
		for (int i = 0; i < 3; ++i)
			src[i] = PyFloat_AsDouble(PySequence_GetItem(a0,i));
		qreal res[3];
		sipCpp->getWorldCoordinatesOf(src,res);
		sipRes = PyTuple_New(3);
		for(int i = 0; i < 3; ++i)
			PyTuple_SetItem(sipRes,i,PyFloat_FromDouble(res[i]));
	}	
%End

  public:
    Vec projectedCoordinatesOf(const Vec& src /In/ , const Frame* frame /In/ =NULL ) const;
    Vec unprojectedCoordinatesOf(const Vec& src /In/, const Frame* frame /In/ =NULL) const;
    // void getProjectedCoordinatesOf(const float src[3], float res[3], const Frame* frame /In/ =NULL) const;
	SIP_PYOBJECT getProjectedCoordinatesOf(SIP_PYOBJECT, const Frame* frame /In/ =NULL) const;
%MethodCode
	int isSequence = PySequence_Check(a0);
	if (!isSequence || PySequence_Size(a0) != 3)
        sipIsErr = 1;
    else
    {
		qreal src[3];
		for (int i = 0; i < 3; ++i)
			src[i] = PyFloat_AsDouble(PySequence_GetItem(a0,i));
		qreal res[3];
		sipCpp->getProjectedCoordinatesOf(src,res,a1);
		sipRes = PyTuple_New(3);
		for(int i = 0; i < 3; ++i)
			PyTuple_SetItem(sipRes,i,PyFloat_FromDouble(res[i]));
	}	
%End
    
    // void getUnprojectedCoordinatesOf(const float src[3], float res[3], const Frame* frame=NULL) const;
	SIP_PYOBJECT getUnprojectedCoordinatesOf(SIP_PYOBJECT, const Frame* frame /In/ =NULL) const;
%MethodCode
	int isSequence = PySequence_Check(a0);
	if (!isSequence || PySequence_Size(a0) != 3)
        sipIsErr = 1;
    else
    {
		qreal src[3];
		for (int i = 0; i < 3; ++i)
			src[i] = PyFloat_AsDouble(PySequence_GetItem(a0,i));
		qreal res[3];
		sipCpp->getUnprojectedCoordinatesOf(src,res,a1);
		sipRes = PyTuple_New(3);
		for(int i = 0; i < 3; ++i)
			PyTuple_SetItem(sipRes,i,PyFloat_FromDouble(res[i]));
	}	
%End
    void convertClickToLine(const QPoint& pixel /In/, Vec& orig /Out/, Vec& dir /Out/) const;
    Vec pointUnderPixel(const QPoint& pixel /In/, bool& found /Out/) const;


  public:
    qreal flySpeed() const;
  public slots:
    void setFlySpeed(qreal speed) ;

  public:
    qreal IODistance() const;
    qreal physicalDistanceToScreen() const;
    qreal physicalScreenWidth() const ;
    qreal focusDistance() const ;
    
  public slots:
    void setIODistance(qreal distance) ;
    void setPhysicalDistanceToScreen(qreal distance) ;
    void setPhysicalScreenWidth(qreal width);
    void setFocusDistance(qreal distance);

  public:
    virtual QDomElement domElement(const QString& name /In/, QDomDocument& document /In/) const;
  public slots:
    virtual void initFromDOMElement(const QDomElement& element /In/);
};