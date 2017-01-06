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

%Include QGLViewerModuleConfig.sip

%Import QtCore/QtCoremod.sip
%Import QtGui/QtGuimod.sip
%Import QtOpenGL/QtOpenGLmod.sip
%Import QtXml/QtXmlmod.sip

%Timeline {QGLViewer_2_2_3 QGLViewer_2_2_4 QGLViewer_2_2_5 QGLViewer_2_2_6 
           QGLViewer_2_3_0 QGLViewer_2_3_1 QGLViewer_2_3_2 QGLViewer_2_3_3 QGLViewer_2_3_4 QGLViewer_2_3_5 
		   QGLViewer_2_3_6 QGLViewer_2_3_7 QGLViewer_2_3_8 QGLViewer_2_3_9
		   QGLViewer_2_3_10 QGLViewer_2_3_11 QGLViewer_2_3_12 QGLViewer_2_3_13
		   QGLViewer_2_3_14 QGLViewer_2_3_15 QGLViewer_2_3_16 QGLViewer_2_3_17
           QGLViewer_2_4_0 QGLViewer_2_4_1 QGLViewer_2_5_0 QGLViewer_2_5_1 QGLViewer_2_5_2 QGLViewer_2_5_3 QGLViewer_2_5_4
           QGLViewer_2_6_0 QGLViewer_2_6_1 QGLViewer_2_6_2 QGLViewer_2_6_3 QGLViewer_2_6_4}
%Feature FRIEND_EQUAL_SUPPORT

%Copying
Copyright (c) 2006-2016
	F. Boudon, V. Plants Team

This file is part of PyQGLViewer.
%End

// typedef double GLdouble;

%Include vec.sip
%Include quaternion.sip
%Include frame.sip
%Include constraint.sip
%Include keyFrameInterpolator.sip
%Include mouseGrabber.sip
%Include manipulatedFrame.sip
%Include manipulatedCameraFrame.sip
%Include camera.sip
%Include qglviewer.sip
%Include domUtils.sip
%Include qglviewerversion.sip
