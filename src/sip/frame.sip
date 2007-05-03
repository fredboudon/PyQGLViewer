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

class Frame : QObject
{

%TypeHeaderCode
#include <QGLViewer/frame.h>
using qglviewer::Frame;
#include <QGLViewer/vec.h>
using qglviewer::Vec;
#include <QGLViewer/quaternion.h>
using qglviewer::Quaternion;
%End

public:
    Frame();

    virtual ~Frame() ;

    Frame(const Frame& frame);
    // Frame& operator=(const Frame& frame);

  signals:
    void modified();
    void interpolated();

  public:
    Frame(Vec position, Quaternion orientation);

    void setPosition(Vec position);
    void setPosition(float x, float y, float z);
    void setPositionWithConstraint(Vec& position /In, Out/);

    void setOrientation(Quaternion orientation);
    void setOrientation(double q0, double q1, double q2, double q3);
    void setOrientationWithConstraint(Quaternion& orientation /In, Out/);

    void setPositionAndOrientation(Vec position, Quaternion orientation);
    void setPositionAndOrientationWithConstraint(Vec& position /In, Out/, Quaternion& orientation /In, Out/);

    Vec position() const ;
    Quaternion orientation() const;

    void getPosition(float& x /Out/, float& y /Out/, float& z /Out/) const;
    void getOrientation(double& q0 /Out/, double& q1 /Out/, double& q2 /Out/, double& q3 /Out/) const;

    public:

    void setTranslation(Vec translation) ;
    void setTranslation(float x, float y, float z);
    void setTranslationWithConstraint(Vec& translation /In, Out/);

    void setRotation(Quaternion rotation) ;
    void setRotation(double q0, double q1, double q2, double q3);
    void setRotationWithConstraint(Quaternion& rotation /In, Out/);

    void setTranslationAndRotation(Vec translation, Quaternion rotation);
    void setTranslationAndRotationWithConstraint(Vec& translation /In, Out/, Quaternion& rotation /In, Out/);

    Vec translation() const ;
    Quaternion rotation() const ;
    
	void getTranslation( float & x /Out/, float & y /Out/, float & z /Out/) const;	
    void getRotation(double& q0 /Out/, double& q1 /Out/, double& q2 /Out/, double& q3 /Out/) const;

    public:

    const Frame* referenceFrame() const ;
    void setReferenceFrame(const Frame* refFrame);
    bool settingAsReferenceFrameWillCreateALoop(const Frame* frame);

    void translate(Vec& t /In, Out/); 
    void rotate(Quaternion& q /In, Out/);
    
    void rotateAroundPoint(Quaternion& rotation /In, Out/, Vec point);

    void alignWithFrame(const Frame* frame , bool move = false, float threshold=0.85);
    void projectOnLine(Vec origin, Vec direction);


    Vec coordinatesOf(Vec src) const;
    Vec inverseCoordinatesOf(Vec src) const;
    Vec localCoordinatesOf(Vec src) const;
    Vec localInverseCoordinatesOf(Vec src) const;
    Vec coordinatesOfIn(Vec src, const Frame* in /In/) const;
    Vec coordinatesOfFrom(Vec src, const Frame* from /In/) const;

	SIP_PYOBJECT getCoordinatesOf(SIP_PYOBJECT);
%MethodCode
	int isSequence = PySequence_Check(a0);
	if (!isSequence || PySequence_Size(a0) != 3)
        sipIsErr = 1;
    else
    {
		float src[3];
		for (int i = 0; i < 3; ++i)
			src[i] = PyFloat_AsDouble(PySequence_GetItem(a0,i));
		float res[3];
		sipCpp->getCoordinatesOf(src,res);
		sipRes = PyTuple_New(3);
		for(int i = 0; i < 3; ++i)
			PyTuple_SetItem(sipRes,i,PyFloat_FromDouble(res[i]));
	}	
%End

     SIP_PYOBJECT getInverseCoordinatesOf(SIP_PYOBJECT) const;
%MethodCode
	int isSequence = PySequence_Check(a0);
	if (!isSequence || PySequence_Size(a0) != 3)
        sipIsErr = 1;
    else
    {
		float src[3];
		for (int i = 0; i < 3; ++i)
			src[i] = PyFloat_AsDouble(PySequence_GetItem(a0,i));
		float res[3];
		sipCpp->getInverseCoordinatesOf(src,res);
		sipRes = PyTuple_New(3);
		for(int i = 0; i < 3; ++i)
			PyTuple_SetItem(sipRes,i,PyFloat_FromDouble(res[i]));
	}	
%End

     SIP_PYOBJECT getLocalCoordinatesOf(SIP_PYOBJECT) const;
%MethodCode
	int isSequence = PySequence_Check(a0);
	if (!isSequence || PySequence_Size(a0) != 3)
        sipIsErr = 1;
    else
    {
		float src[3];
		for (int i = 0; i < 3; ++i)
			src[i] = PyFloat_AsDouble(PySequence_GetItem(a0,i));
		float res[3];
		sipCpp->getLocalCoordinatesOf(src,res);
		sipRes = PyTuple_New(3);
		for(int i = 0; i < 3; ++i)
			PyTuple_SetItem(sipRes,i,PyFloat_FromDouble(res[i]));
	}	
%End

     SIP_PYOBJECT getLocalInverseCoordinatesOf(SIP_PYOBJECT) const;
%MethodCode
	int isSequence = PySequence_Check(a0);
	if (!isSequence || PySequence_Size(a0) != 3)
        sipIsErr = 1;
    else
    {
		float src[3];
		for (int i = 0; i < 3; ++i)
			src[i] = PyFloat_AsDouble(PySequence_GetItem(a0,i));
		float res[3];
		sipCpp->getLocalInverseCoordinatesOf(src,res);
		sipRes = PyTuple_New(3);
		for(int i = 0; i < 3; ++i)
			PyTuple_SetItem(sipRes,i,PyFloat_FromDouble(res[i]));
	}	
%End

     SIP_PYOBJECT getCoordinatesOfIn(SIP_PYOBJECT, const Frame* in) const;
%MethodCode
	int isSequence = PySequence_Check(a0);
	if (!isSequence || PySequence_Size(a0) != 3)
        sipIsErr = 1;
    else
    {
		float src[3];
		for (int i = 0; i < 3; ++i)
			src[i] = PyFloat_AsDouble(PySequence_GetItem(a0,i));
		float res[3];
		sipCpp->getCoordinatesOfIn(src,res,a1);
		sipRes = PyTuple_New(3);
		for(int i = 0; i < 3; ++i)
			PyTuple_SetItem(sipRes,i,PyFloat_FromDouble(res[i]));
	}	
%End

     SIP_PYOBJECT getCoordinatesOfFrom(SIP_PYOBJECT, const Frame* from) const;
%MethodCode
	int isSequence = PySequence_Check(a0);
	if (!isSequence || PySequence_Size(a0) != 3)
        sipIsErr = 1;
    else
    {
		float src[3];
		for (int i = 0; i < 3; ++i)
			src[i] = PyFloat_AsDouble(PySequence_GetItem(a0,i));
		float res[3];
		sipCpp->getCoordinatesOfFrom(src,res,a1);
		sipRes = PyTuple_New(3);
		for(int i = 0; i < 3; ++i)
			PyTuple_SetItem(sipRes,i,PyFloat_FromDouble(res[i]));
	}	
%End

    Vec transformOf(Vec src) const;
    Vec inverseTransformOf(Vec src) const;
    Vec localTransformOf(Vec src) const;
    Vec localInverseTransformOf(Vec src) const;
    Vec transformOfIn(Vec src, const Frame* in /In/) const;
    Vec transformOfFrom(Vec src, const Frame* from /In/) const;

	SIP_PYOBJECT getTransformOf(SIP_PYOBJECT);
%MethodCode
	int isSequence = PySequence_Check(a0);
	if (!isSequence || PySequence_Size(a0) != 3)
        sipIsErr = 1;
    else
    {
		float src[3];
		for (int i = 0; i < 3; ++i)
			src[i] = PyFloat_AsDouble(PySequence_GetItem(a0,i));
		float res[3];
		sipCpp->getTransformOf(src,res);
		sipRes = PyTuple_New(3);
		for(int i = 0; i < 3; ++i)
			PyTuple_SetItem(sipRes,i,PyFloat_FromDouble(res[i]));
	}	
%End

	SIP_PYOBJECT getInverseTransformOf(SIP_PYOBJECT);
%MethodCode
	int isSequence = PySequence_Check(a0);
	if (!isSequence || PySequence_Size(a0) != 3)
        sipIsErr = 1;
    else
    {
		float src[3];
		for (int i = 0; i < 3; ++i)
			src[i] = PyFloat_AsDouble(PySequence_GetItem(a0,i));
		float res[3];
		sipCpp->getInverseTransformOf(src,res);
		sipRes = PyTuple_New(3);
		for(int i = 0; i < 3; ++i)
			PyTuple_SetItem(sipRes,i,PyFloat_FromDouble(res[i]));
	}	
%End

	SIP_PYOBJECT getLocalTransformOf(SIP_PYOBJECT);
%MethodCode
	int isSequence = PySequence_Check(a0);
	if (!isSequence || PySequence_Size(a0) != 3)
        sipIsErr = 1;
    else
    {
		float src[3];
		for (int i = 0; i < 3; ++i)
			src[i] = PyFloat_AsDouble(PySequence_GetItem(a0,i));
		float res[3];
		sipCpp->getLocalTransformOf(src,res);
		sipRes = PyTuple_New(3);
		for(int i = 0; i < 3; ++i)
			PyTuple_SetItem(sipRes,i,PyFloat_FromDouble(res[i]));
	}	
%End

	SIP_PYOBJECT getLocalInverseTransformOf(SIP_PYOBJECT);
%MethodCode
	int isSequence = PySequence_Check(a0);
	if (!isSequence || PySequence_Size(a0) != 3)
        sipIsErr = 1;
    else
    {
		float src[3];
		for (int i = 0; i < 3; ++i)
			src[i] = PyFloat_AsDouble(PySequence_GetItem(a0,i));
		float res[3];
		sipCpp->getLocalInverseTransformOf(src,res);
		sipRes = PyTuple_New(3);
		for(int i = 0; i < 3; ++i)
			PyTuple_SetItem(sipRes,i,PyFloat_FromDouble(res[i]));
	}	
%End

	SIP_PYOBJECT getTransformOfIn(SIP_PYOBJECT, const Frame* in);
%MethodCode
	int isSequence = PySequence_Check(a0);
	if (!isSequence || PySequence_Size(a0) != 3)
        sipIsErr = 1;
    else
    {
		float src[3];
		for (int i = 0; i < 3; ++i)
			src[i] = PyFloat_AsDouble(PySequence_GetItem(a0,i));
		float res[3];
		sipCpp->getTransformOfIn(src,res,a1);
		sipRes = PyTuple_New(3);
		for(int i = 0; i < 3; ++i)
			PyTuple_SetItem(sipRes,i,PyFloat_FromDouble(res[i]));
	}	
%End

	SIP_PYOBJECT getTransformOfFrom(SIP_PYOBJECT, const Frame* from) const;
%MethodCode
	int isSequence = PySequence_Check(a0);
	if (!isSequence || PySequence_Size(a0) != 3)
        sipIsErr = 1;
    else
    {
		float src[3];
		for (int i = 0; i < 3; ++i)
			src[i] = PyFloat_AsDouble(PySequence_GetItem(a0,i));
		float res[3];
		sipCpp->getTransformOfFrom(src,res,a1);
		sipRes = PyTuple_New(3);
		for(int i = 0; i < 3; ++i)
			PyTuple_SetItem(sipRes,i,PyFloat_FromDouble(res[i]));
	}	
%End

    Constraint* constraint() const ;
    void setConstraint(Constraint* constraint /Transfer/) ;
%MethodCode
        Constraint* currentConstraint = sipCpp->constraint();
        sipCpp->setConstraint(a0);
        // Release the ownership of previous constraint to python.
        PyObject * pyCurrentConstraint = sipConvertFromInstance(currentConstraint,sipClass_Constraint,Py_None);
%End

  public:
    SIP_PYOBJECT matrix() const;
%MethodCode
	const GLdouble * mat = sipCpp->matrix();
    if (mat == NULL)
        sipIsErr = 1;
    else
    {
		
		PyObject * res = PyTuple_New(16);
		for(int i = 0; i < 16; ++i)
			PyTuple_SetItem(res,i,PyFloat_FromDouble(mat[i]));
		sipRes = res;
    }	
%End

    SIP_PYOBJECT worldMatrix() const;
%MethodCode
	const GLdouble * mat = sipCpp->worldMatrix();
    if (mat == NULL)
        sipIsErr = 1;
    else
    {
		
		PyObject * res = PyTuple_New(16);
		for(int i = 0; i < 16; ++i)
			PyTuple_SetItem(res,i,PyFloat_FromDouble(mat[i]));
		sipRes = res;
    }	
%End

	void setFromMatrix(SIP_PYOBJECT);
%MethodCode
	int isSequence = PySequence_Check(a0);
	if (!isSequence || PySequence_Size(a0) != 16)
        sipIsErr = 1;
    else
    {
		GLdouble values[16];
		for (int i = 0; i < 16; ++i)
			values[i] = PyFloat_AsDouble(PySequence_GetItem(a0,i));
		sipCpp->setFromMatrix(values);
	}	
%End
	
    Frame inverse() const;
    Frame worldInverse() const;

  public:
    virtual QDomElement domElement(const QString& name, QDomDocument& document) const;
  public slots:
    virtual void initFromDOMElement(const QDomElement& element);
};

