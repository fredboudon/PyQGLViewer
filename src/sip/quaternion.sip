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

class Quaternion
{

%TypeHeaderCode
#include <QGLViewer/quaternion.h>
using qglviewer::Quaternion;
%End
public:
  Quaternion();
  Quaternion(const Vec& axis, double angle);
  Quaternion(const Vec& from, const Vec& to);
  Quaternion(double q0, double q1, double q2, double q3);
  Quaternion(const Quaternion& Q);

  // Quaternion& operator=(const Quaternion& Q);

  void setAxisAngle(const Vec& axis, double angle);

  void setValue(double q0, double q1, double q2, double q3);

  // void setFromRotationMatrix(const double m[3][3]);
  void setFromRotationMatrix(SIP_PYOBJECT);
%MethodCode
	int isSequence = PySequence_Check(a0);
	if (!isSequence )
        sipIsErr = 1;     
    else
    {
        int len = PySequence_Size(a0);
        if (len != 3 && len != 9)
            sipIsErr = 1;
        else {
		    double src[3][3];
		    if (len == 9){
		        for (int i = 0; i < 3; ++i)
		            for (int j = 0; j < 3; ++j)
			            src[i][j] = PyFloat_AsDouble(PySequence_GetItem(a0,3*i+j));
			 }
			 else {
		        for (int i = 0; i < 3; ++i){
		            PyObject * row = PySequence_GetItem(a0,i);
		            if (! PySequence_Check(row) && PySequence_Size(row) == 3){
		                for (int j = 0; j < 3; ++j){
			                src[i][j] = PyFloat_AsDouble(PySequence_GetItem(row,j));
			            }
			        }
			     }
			 }
		    if (!sipIsErr) sipCpp->setFromRotationMatrix(src);
		}
	}	
%End
  
  void setFromRotatedBasis(const Vec& X, const Vec& Y, const Vec& Z);


  Vec axis() const;
  float angle() const;
  void getAxisAngle(Vec& axis /Out/, float& angle /Out/) const;
  
  // double operator[](int i) const ;
  // double& operator[](int i);
  
  double __getitem__(int i) const ;
%MethodCode
  if ((a0 = (int)sipConvertFromSequenceIndex(a0, 4)) < 0)
        sipIsErr = 1;
   else
       sipRes = (*sipCpp)[a0] ;
%End

  void __setitem__(int i, double );
%MethodCode
   if ((a0 = (int)sipConvertFromSequenceIndex(a0, 4)) < 0)
        sipIsErr = 1;
   else
       (*sipCpp)[a0] = a1;
%End

  // Quaternion& operator*=(const Quaternion& q);

  Vec rotate(const Vec& v) const;
  Vec inverseRotate(const Vec& v) const;
  Quaternion inverse() const;
  void invert() ;
  void negate() ;
  double normalize();
  Quaternion normalized() const;

  // const GLdouble* matrix() const; 
  // void getMatrix(GLdouble m[4][4]) const;
  // void getMatrix(GLdouble m[16]) const;
  // void getRotationMatrix(float m[3][3]) const;
  SIP_PYOBJECT getMatrix() const; 
%MethodCode
    const GLdouble* values = sipCpp->matrix();
    sipRes = PyList_New(16);
	for(int i = 0; i < 16; ++i)
			PyList_SetItem(sipRes,i,PyFloat_FromDouble(values[i]));
%End

  SIP_PYOBJECT getMatrix4() const; 
%MethodCode
    const GLdouble* values = sipCpp->matrix();
    sipRes = PyList_New(4);
	for(int i = 0; i < 4; ++i){
	    PyObject * row = PyList_New(4);
	    PyList_SetItem(sipRes,i,row);
	    for(int j = 0; j < 4; ++j)
			PyList_SetItem(row,j,PyFloat_FromDouble(values[4*i+j]));
	}
%End

  SIP_PYOBJECT getRotationMatrix() const; 
%MethodCode
    float values[3][3];
    sipCpp->getRotationMatrix(values);
    sipRes = PyList_New(16);
	for(int i = 0; i < 16; ++i)
			PyList_SetItem(sipRes,i,PyFloat_FromDouble(values[i/3][i%3]));
%End

  SIP_PYOBJECT getRotationMatrix3() const; 
%MethodCode
    float values[3][3];
    sipCpp->getRotationMatrix(values);
    sipRes = PyList_New(3);
	for(int i = 0; i < 3; ++i){
	    PyObject * row = PyList_New(3);
	    PyList_SetItem(sipRes,i,row);
	    for(int j = 0; j < 3; ++j)
			PyList_SetItem(row,j,PyFloat_FromDouble(values[i][j]));
	}
%End

  // const GLdouble* inverseMatrix() const;
  // void getInverseMatrix(GLdouble m[4][4]) const;
  // void getInverseMatrix(GLdouble m[16]) const;
  // void getInverseRotationMatrix(float m[3][3]) const;
  SIP_PYOBJECT getInverseMatrix() const; 
%MethodCode
    const GLdouble* values = sipCpp->inverseMatrix();
    sipRes = PyList_New(16);
	for(int i = 0; i < 16; ++i)
			PyList_SetItem(sipRes,i,PyFloat_FromDouble(values[i]));
%End

  SIP_PYOBJECT getInverseMatrix4() const; 
%MethodCode
    const GLdouble* values = sipCpp->inverseMatrix();
    sipRes = PyList_New(4);
	for(int i = 0; i < 4; ++i){
	    PyObject * row = PyList_New(4);
	    PyList_SetItem(sipRes,i,row);
	    for(int j = 0; j < 4; ++j)
			PyList_SetItem(row,j,PyFloat_FromDouble(values[4*i+j]));
	}
%End

  SIP_PYOBJECT getInverseRotationMatrix() const; 
%MethodCode
    float values[3][3];
    sipCpp->getRotationMatrix(values);
    sipRes = PyList_New(16);
	for(int i = 0; i < 16; ++i)
			PyList_SetItem(sipRes,i,PyFloat_FromDouble(values[i/3][i%3]));
%End

  SIP_PYOBJECT getInverseRotationMatrix3() const; 
%MethodCode
    float values[3][3];
    sipCpp->getRotationMatrix(values);
    sipRes = PyList_New(3);
	for(int i = 0; i < 3; ++i){
	    PyObject * row = PyList_New(3);
	    PyList_SetItem(sipRes,i,row);
	    for(int j = 0; j < 3; ++j)
			PyList_SetItem(row,j,PyFloat_FromDouble(values[i][j]));
	}
%End


  static Quaternion slerp(const Quaternion& a, const Quaternion& b, float t, bool allowFlip=true);
  static Quaternion squad(const Quaternion& a, const Quaternion& tgA, const Quaternion& tgB, const Quaternion& b, float t);
  static double dot(const Quaternion& a, const Quaternion& b);

  Quaternion log();
  Quaternion exp();
  
  static Quaternion lnDif(const Quaternion& a, const Quaternion& b);
  static Quaternion squadTangent(const Quaternion& before, const Quaternion& center, const Quaternion& after);

  static Quaternion randomQuaternion();

  explicit Quaternion(const QDomElement& element);
  QDomElement domElement(const QString& name, QDomDocument& document) const;
  void initFromDOMElement(const QDomElement& element);

   int __len__() const;
%MethodCode
	sipRes = 4;
%End
 
  char * __str__() const;
%MethodCode
        QString val = QString("Quaternion(%1,%2,%3,%4)").arg((*sipCpp)[0]).arg((*sipCpp)[1]).arg((*sipCpp)[2]).arg((*sipCpp)[3]);
        sipRes = val.toAscii().data();
%End
  
  char * __repr__() const;
%MethodCode
        QString val = QString("<Quaternion(%1,%2,%3,%4) at 0x%5>").arg((*sipCpp)[0]).arg((*sipCpp)[1]).arg((*sipCpp)[2]).arg((*sipCpp)[3]).arg((qlonglong)sipCpp,8,16,QChar('0'));
        sipRes = val.toAscii().data();
%End

};

Quaternion operator*(Quaternion a, Quaternion b);
Vec operator*(Quaternion q, Vec v);
