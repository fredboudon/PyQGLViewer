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

    virtual ~Constraint();

    virtual void constrainTranslation(Vec& translation, const Frame * frame) ;
    virtual void constrainRotation(Quaternion& rotation, const Frame * frame);
  };



class AxisPlaneConstraint : Constraint
  {
%TypeHeaderCode
#include <QGLViewer/constraint.h>
using qglviewer::AxisPlaneConstraint;
%End

  public:
    AxisPlaneConstraint();
    virtual ~AxisPlaneConstraint() ;
    enum Type { FREE, AXIS, PLANE, FORBIDDEN };
    virtual void constrainTranslation(Vec& translation, const Frame* frame) ;

    void setTranslationConstraint(Type type, const Vec& direction);
    void setTranslationConstraintType(Type type) ;
    void setTranslationConstraintDirection(const Vec& direction);

    Type translationConstraintType() const;
    Vec translationConstraintDirection() const ;

    virtual void constrainRotation(Quaternion& rotation, const Frame* frame);

    void setRotationConstraint(Type type, const Vec& direction);
    void setRotationConstraintType(Type type);
    void setRotationConstraintDirection(const Vec& direction);

    Type rotationConstraintType() const;
    Vec rotationConstraintDirection() const;

};


class LocalConstraint : AxisPlaneConstraint
{
%TypeHeaderCode
#include <QGLViewer/constraint.h>
using qglviewer::LocalConstraint;
%End
  public:
    virtual ~LocalConstraint();

    virtual void constrainTranslation(Vec&     translation, const Frame* frame);
    virtual void constrainRotation   (Quaternion& rotation, const Frame* frame);
};



class WorldConstraint : AxisPlaneConstraint
{
%TypeHeaderCode
#include <QGLViewer/constraint.h>
using qglviewer::WorldConstraint;
%End
  public:
    virtual ~WorldConstraint();

    virtual void constrainTranslation(Vec&     translation, const Frame* frame);
    virtual void constrainRotation   (Quaternion& rotation, const Frame* frame);
};



class CameraConstraint : AxisPlaneConstraint
{
%TypeHeaderCode
#include <QGLViewer/constraint.h>
using qglviewer::CameraConstraint;
#include <QGLViewer/camera.h>
using qglviewer::Camera;
%End
public:
    CameraConstraint(const Camera* camera);
    virtual ~CameraConstraint();

    virtual void constrainTranslation(Vec&     translation, const Frame* frame);
    virtual void constrainRotation   (Quaternion& rotation, const Frame* frame);

    const Camera* camera() const ;

};

