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
#include <QGLViewer/vec.h>
using qglviewer::Vec;
#include <QGLViewer/quaternion.h>
using qglviewer::Quaternion;
#include <QGLViewer/frame.h>
using qglviewer::Frame;
%End

class Constraint
{

%TypeHeaderCode
#include <QGLViewer/constraint.h>
using qglviewer::Constraint;
%End
public:
    virtual ~Constraint();

    virtual void constrainTranslation(Vec& translation /In, Out/,  Frame * frame /In/) ;
    virtual void constrainRotation(Quaternion& rotation /In, Out/, Frame * frame /In/);
  };



class AxisPlaneConstraint : Constraint
  {
%TypeHeaderCode
#include <QGLViewer/constraint.h>
using qglviewer::Constraint;
using qglviewer::AxisPlaneConstraint;
%End

  public:
    AxisPlaneConstraint();
    virtual ~AxisPlaneConstraint() ;
    enum Type { FREE, AXIS, PLANE, FORBIDDEN };
    virtual void constrainTranslation(Vec& translation /In, Out/, Frame* frame /In/) ;

    void setTranslationConstraint(Type type, const Vec& direction /In/);
    void setTranslationConstraintType(Type type) ;
    void setTranslationConstraintDirection(const Vec& direction /In/);

    Type translationConstraintType() const;
    Vec translationConstraintDirection() const ;

    virtual void constrainRotation(Quaternion& rotation /In, Out/, Frame* frame /In/);

    void setRotationConstraint(Type type, const Vec& direction /In/);
    void setRotationConstraintType(Type type);
    void setRotationConstraintDirection(const Vec& direction /In/);

    Type rotationConstraintType() const;
    Vec rotationConstraintDirection() const;

};


class LocalConstraint : AxisPlaneConstraint
{
%TypeHeaderCode
#include <QGLViewer/constraint.h>
using qglviewer::AxisPlaneConstraint;
using qglviewer::LocalConstraint;
%End
  public:
    virtual ~LocalConstraint();

    virtual void constrainTranslation(Vec&     translation /In, Out/, Frame* frame /In/);
    virtual void constrainRotation   (Quaternion& rotation /In, Out/, Frame* frame /In/);
};



class WorldConstraint : AxisPlaneConstraint
{
%TypeHeaderCode
#include <QGLViewer/constraint.h>
using qglviewer::AxisPlaneConstraint;
using qglviewer::WorldConstraint;
%End
  public:
    virtual ~WorldConstraint();

    virtual void constrainTranslation(Vec&     translation /In, Out/, Frame* frame /In/);
    virtual void constrainRotation   (Quaternion& rotation /In, Out/, Frame* frame /In/);
};



class CameraConstraint : AxisPlaneConstraint
{
%TypeHeaderCode
#include <QGLViewer/constraint.h>
using qglviewer::AxisPlaneConstraint;
using qglviewer::CameraConstraint;
#include <QGLViewer/camera.h>
using qglviewer::Camera;
%End
public:
    CameraConstraint(const Camera* camera /Transfer/);
    virtual ~CameraConstraint();

    virtual void constrainTranslation(Vec&     translation /In, Out/, Frame* frame /In/);
    virtual void constrainRotation   (Quaternion& rotation /In, Out/, Frame* frame /In/);

    const Camera* camera() const ;

};

