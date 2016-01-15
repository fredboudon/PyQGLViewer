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


class DomUtils
{
%TypeHeaderCode
#include <qglobal.h>
#include <QGLViewer/domUtils.h>
%End
public:
%If ( - QGLViewer_2_6_0)
  static float floatFromDom(const QDomElement& e /In/, const QString& attribute /In/, float defValue);
  static double doubleFromDom(const QDomElement& e /In/, const QString& attribute /In/, double defValue);

%End

%If (QGLViewer_2_6_0 - )
  static qreal qrealFromDom(const QDomElement& e /In/, const QString& attribute /In/, qreal defValue);
%End

  static int intFromDom(const QDomElement& e /In/, const QString& attribute /In/, int defValue);

%If (QGLViewer_2_6_0 - )
  static unsigned int uintFromDom(const QDomElement& e /In/, const QString& attribute /In/, unsigned int defValue);
%End

  static bool boolFromDom(const QDomElement& e /In/, const QString& attribute /In/, bool defValue);
  static void setBoolAttribute(QDomElement& element /In/, const QString& attribute /In/, bool value);

  static QDomElement QColorDomElement(const QColor& color /In/, const QString& name /In/, QDomDocument& doc /In/);
  static QColor QColorFromDom(const QDomElement& e /In/);
};

