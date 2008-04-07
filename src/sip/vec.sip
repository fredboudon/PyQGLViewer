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



class Vec
{

%TypeHeaderCode
#include <QGLViewer/vec.h>
using qglviewer::Vec;
%End
public:
  float x;
  float y;
  float z;
  Vec();
  Vec(float x, float y, float z);
  void setValue(float x, float y, float z);

  float __getitem__(int i) const ;
%MethodCode
  if ((a0 = (int)sipConvertFromSequenceIndex(a0, 3)) < 0)
        sipIsErr = 1;
   else
       sipRes = (*sipCpp)[a0] ;
%End

  void __setitem__(int i, float );
%MethodCode
   if ((a0 = (int)sipConvertFromSequenceIndex(a0, 3)) < 0)
        sipIsErr = 1;
   else
       (*sipCpp)[a0] = a1;
%End
 
  Vec& operator+=(const Vec &a);
  Vec& operator-=(const Vec &a);
  Vec& operator*=(float k);
  Vec& operator/=(float k);
  Vec orthogonalVec() const;
  float sqNorm() const;
  float squaredNorm();
  float norm() const;
  float normalize();
  Vec unit() const;
  void projectOnAxis(const Vec& direction);
  void projectOnPlane(const Vec& normal);

  explicit Vec(const QDomElement& element /In/);
  QDomElement domElement(const QString& name /In/, QDomDocument& document /In/) const;
  void initFromDOMElement(const QDomElement& element /In/);

   int __len__() const;
%MethodCode
	sipRes = 3;
%End
 
  char * __str__() const;
%MethodCode
        QString val = QString("Vec(%1,%2,%3)").arg((*sipCpp)[0]).arg((*sipCpp)[1]).arg((*sipCpp)[2]);
        sipRes = val.toAscii().data();
%End
  
  char * __repr__() const;
%MethodCode
        QString val = QString("<Vec(%1,%2,%3) at 0x%4>").arg((*sipCpp)[0]).arg((*sipCpp)[1]).arg((*sipCpp)[2]).arg((qlonglong)sipCpp,8,16,QChar('0'));
        sipRes = val.toAscii().data();
%End

%If (!SIP_FRIEND_EQUAL_SUPPORT)
  bool __eq__(const Vec&) const;
%MethodCode
    sipRes = (*sipCpp == *a0);
%End

  bool __ne__(const Vec&) const;
%MethodCode
    sipRes = (*sipCpp != *a0);
%End

%End

%PickleCode
    sipRes = Py_BuildValue((char *)"fff", sipCpp->x, sipCpp->y, sipCpp->z);
%End
};

%If (SIP_FRIEND_EQUAL_SUPPORT)
bool operator==(Vec s1, Vec s2);
bool operator!=(Vec s1, Vec s2);
%End

Vec operator+(Vec a, Vec b);
Vec operator-(Vec a, Vec b);
Vec operator-(Vec &a);
Vec operator*(Vec a, float k);
Vec operator*(float k, Vec a);
Vec operator/(Vec a, float k);
float operator*(Vec a, Vec b);
Vec operator^(Vec a, Vec b);
Vec cross(Vec a, Vec b);
// std::ostream& operator<<(std::ostream& o, const Vec&);

