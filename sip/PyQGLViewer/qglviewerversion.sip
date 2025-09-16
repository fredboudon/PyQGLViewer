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

#ifndef PYQGLVIEWER_VERSION
#define PYQGLVIEWER_VERSION 0.0.0
#endif

#define QUOTE(x) #x
#define STR(x) QUOTE(x)

#define PYQGLVIEWER_VERSION_STR STR(PYQGLVIEWER_VERSION)
#include <string>
#include <vector>

unsigned int version_to_hex(const std::string& version) {
    std::vector<int> parts;
    std::string number;

    for (char c : version) {
        if (std::isdigit(static_cast<unsigned char>(c))) {
            number.push_back(c);              // accumuler les chiffres
        } else {
            if (!number.empty()) {
                parts.push_back(std::stoi(number));
                number.clear();
            }
        }
    }
    if (!number.empty()) {
        parts.push_back(std::stoi(number));
    }

    // ajustement à 3 éléments (majeur, mineur, revision)
    while (parts.size() < 3) {
        parts.push_back(0);
    }
    if (parts.size() > 3) {
        parts.resize(3);
    }

    // format : 0xMMmmrrdd
    unsigned int hex_version = 0;
    hex_version |= (parts[0] & 0xFF) << 16; // majeur
    hex_version |= (parts[1] & 0xFF) << 8;  // mineur
    hex_version |= (parts[2] & 0xFF);       // révision

    return hex_version;
}

/*
static const char * PyQGLViewerVersionString(){
  return qPrintable(QString::number((PYQGLVIEWER_VERSION & 0xff0000) >> 16) + "." +
                     QString::number((PYQGLVIEWER_VERSION & 0x00ff00) >> 8) + "." +
                     QString::number(PYQGLVIEWER_VERSION  & 0x0000ff));
}
*/
static const char * PyQGLViewerVersionString(){
  return STR(PYQGLVIEWER_VERSION);
}

static const int __version__ = version_to_hex(STR(PYQGLVIEWER_VERSION));

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
