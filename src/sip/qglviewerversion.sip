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


%ModuleHeaderCode
#include <QGLViewer/config.h>
%End

%ModuleCode

#define PYQGLVIEWER_VERSION 0x010001

static const char * PyQGLViewerVersionString(){
  return qPrintable(QString::number((PYQGLVIEWER_VERSION & 0xff0000) >> 16) + "." +
                     QString::number((PYQGLVIEWER_VERSION & 0x00ff00) >> 8) + "." +
                     QString::number(PYQGLVIEWER_VERSION  & 0x0000ff));
}

static const int __version__ = PYQGLVIEWER_VERSION;

static const char * QGLViewerVersionString(){
  return qPrintable(QString::number((QGLVIEWER_VERSION & 0xff0000) >> 16) + "." +
                    QString::number((QGLVIEWER_VERSION & 0x00ff00) >> 8) + "." +
                    QString::number(QGLVIEWER_VERSION  & 0x0000ff));
}

static const int QGLViewerVersion = QGLVIEWER_VERSION;
%End

const char * QGLViewerVersionString();
const int QGLViewerVersion;

const char * PyQGLViewerVersionString();
const int __version__;
