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

class KeyFrameInterpolator : QObject
{

%TypeHeaderCode
#include <QGLViewer/keyFrameInterpolator.h>
using qglviewer::KeyFrameInterpolator;
%End

  public:
    KeyFrameInterpolator(Frame* fr=NULL);
    virtual ~KeyFrameInterpolator();

  signals:
    void interpolated();
    void endReached();

  public slots:
    void addKeyFrame(const Frame* frame /Transfer/);
    void addKeyFrame(const Frame* frame /Transfer/, qreal time);

    void deletePath();

  public:
    Frame* frame() const;

  public slots:
    void setFrame(Frame* frame /Transfer/);

  public:
    Frame keyFrame(int index) const;
    qreal keyFrameTime(int index) const;
    int numberOfKeyFrames() const;
    qreal duration() const;
    qreal firstTime() const;
    qreal lastTime() const;

  public:
    qreal interpolationTime() const;
    qreal interpolationSpeed() const;
    int interpolationPeriod() const ;
    bool loopInterpolation() const ;
    bool closedPath() const ;
  public slots:
    void setInterpolationTime(qreal time);
    void setInterpolationSpeed(qreal speed) ;
    void setInterpolationPeriod(int period) ;
    void setLoopInterpolation(bool loop=true) ;
    void setClosedPath(bool closed=true) ;

  public:
    bool interpolationIsStarted() const ;
  public slots:
    void startInterpolation(int period = -1);
    void stopInterpolation();
    void resetInterpolation();
    void toggleInterpolation() ;
    virtual void interpolateAtTime(qreal time);

  public:
    virtual void drawPath(int mask=1, int nbFrames=6, qreal scale=1.0);

  public:
    virtual QDomElement domElement(const QString& name /In/, QDomDocument& document /In/) const;
    virtual void initFromDOMElement(const QDomElement& element /In/);

  private slots:
    virtual void update();
    virtual void invalidateValues();



};

