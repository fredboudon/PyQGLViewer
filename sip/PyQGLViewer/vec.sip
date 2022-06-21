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
  qreal x;
  qreal y;
  qreal z;
  Vec();
  Vec(qreal x, qreal y, qreal z);
  void setValue(qreal x, qreal y, qreal z);

  qreal __getitem__(int i) const ;
%MethodCode
  if ((a0 = (int)sipConvertFromSequenceIndex(a0, 3)) < 0)
        sipIsErr = 1;
   else
       sipRes = (*sipCpp)[a0] ;
%End

  void __setitem__(int i, qreal );
%MethodCode
   if ((a0 = (int)sipConvertFromSequenceIndex(a0, 3)) < 0)
        sipIsErr = 1;
   else
       (*sipCpp)[a0] = a1;
%End
 
  Vec& operator+=(const Vec &a);
  Vec& operator-=(const Vec &a);
  Vec& operator*=(qreal k);
  Vec& operator/=(qreal k);
  Vec orthogonalVec() const;
  qreal sqNorm() const;
  qreal squaredNorm();
  qreal norm() const;
  qreal normalize();
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
 
  const char * __str__() const;
%MethodCode
        QString val = QString("Vec(%1,%2,%3)").arg((*sipCpp)[0]).arg((*sipCpp)[1]).arg((*sipCpp)[2]);
        sipRes = qPrintable(val);
%End
  
  const char * __repr__() const;
%MethodCode
        QString val = QString("<Vec(%1,%2,%3) at 0x%4>").arg((*sipCpp)[0]).arg((*sipCpp)[1]).arg((*sipCpp)[2]).arg((qlonglong)sipCpp,8,16,QChar('0'));
        sipRes = qPrintable(val);
%End

%If (!FRIEND_EQUAL_SUPPORT)
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

%If (FRIEND_EQUAL_SUPPORT)
bool operator==(Vec s1, Vec s2);
bool operator!=(Vec s1, Vec s2);
%End

Vec operator+(Vec a, Vec b);
Vec operator-(Vec a, Vec b);
Vec operator-(Vec &a);
Vec operator*(Vec a, qreal k);
Vec operator*(qreal k, Vec a);
Vec operator/(Vec a, qreal k);
qreal operator*(Vec a, Vec b);
Vec operator^(Vec a, Vec b);
Vec cross(Vec a, Vec b);
// std::ostream& operator<<(std::ostream& o, const Vec&);

