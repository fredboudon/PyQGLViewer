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


class QGLViewer : QOpenGLWidget {

%TypeHeaderCode
#include <QGLViewer/qglviewer.h>

#include <QtOpenGL/qgl.h>

#ifdef Q_OS_MAC
	#include <OpenGL/glu.h>
#else
	#include <GL/glu.h>
#endif

#ifdef Q_WS_X11
	#define GL_GLEXT_PROTOTYPES
	#include <GL/glext.h>
#endif

#ifndef GL_BGRA
	#define GL_BGRA 0x80E1
#endif

#ifndef GL_TEXTURE_3D
	#define GL_TEXTURE_3D 0x806F
	#define GL_TEXTURE_3D_NO_DEFAULT_DEFINITION
	
	#ifdef Q_WS_X11
		#warning "No default glTexture3D definition found"
	#else
		#pragma message("No default glTexture3D definition found")
	#endif
#endif

%End

public:
%If (QGLViewer_2_7_0 - )
    explicit QGLViewer(QWidget* parent /TransferThis/ =0,
                       Qt::WindowFlags flags=Qt::WindowFlags());

    explicit QGLViewer(QWidget* parent /TransferThis/, 
                       const QGLWidget* shareWidget, Qt::WindowFlags flags=0);
%End

%If ( - QGLViewer_2_6_4)
    explicit QGLViewer(QWidget* parent /TransferThis/ = 0, 
                       const QGLWidget* shareWidget=0, Qt::WindowFlags flags=0);
%End


    explicit QGLViewer(QGLContext *context, 
                       QWidget* parent /TransferThis/=0, const QGLWidget* shareWidget=0, Qt::WindowFlags flags=0);

    explicit QGLViewer(const QGLFormat& format, 
                       QWidget* parent /TransferThis/=0, const QGLWidget* shareWidget=0, Qt::WindowFlags flags=0);

    virtual ~QGLViewer();
    
    bool axisIsDrawn() const;
    bool gridIsDrawn() const;
    bool FPSIsDisplayed() const;
    bool textIsEnabled() const;
    bool cameraIsEdited() const;

public slots:
    void setAxisIsDrawn(bool draw=true);
    void setGridIsDrawn(bool draw=true);
    void setFPSIsDisplayed(bool display=true);
    void setTextIsEnabled(bool enable=true);
    void setCameraIsEdited(bool edit=true);

    void toggleAxisIsDrawn();
    void toggleGridIsDrawn();
    void toggleFPSIsDisplayed();
    void toggleTextIsEnabled();
    void toggleCameraIsEdited();
    
public:
    QColor backgroundColor() const;
    QColor foregroundColor() const;
    
public slots:
    
    void setBackgroundColor(const QColor& color /In/);
    void setForegroundColor(const QColor& color /In/);

public:
    qreal sceneRadius() const;
    Vec sceneCenter() const;
    
public slots:
    virtual void setSceneRadius(qreal radius);
    virtual void setSceneCenter(const Vec& center /In/);

    void setSceneBoundingBox(const Vec& min /In/, const Vec& max /In/);
    void showEntireScene();

public:
    Camera* camera() const;
    ManipulatedFrame* manipulatedFrame() const;
    
public slots:
    void setCamera(Camera* camera /Transfer/);
    void setManipulatedFrame(ManipulatedFrame* frame /Transfer/);
    
public:
    MouseGrabber* mouseGrabber() const;
    void setMouseGrabberIsEnabled(const MouseGrabber * mouseGrabber /In/, bool enabled=true);
    bool mouseGrabberIsEnabled(const MouseGrabber* mouseGrabber /In/);
    
public slots:
    void setMouseGrabber(MouseGrabber* mouseGrabber /Transfer/);

public:
    qreal aspectRatio() const;
    qreal currentFPS();
    bool isFullScreen() const;
    bool displaysInStereo() const;
    virtual QSize sizeHint() const;

    
public slots:
    void setFullScreen(bool fullScreen=true);
    void setStereoDisplay(bool stereo=true);
    void toggleFullScreen();
    void toggleStereoDisplay();
    void toggleCameraMode();
    
public:
    static void drawArrow(qreal length=1.0, qreal radius=-1.0, int nbSubdivisions=12);
    static void drawArrow(const Vec& from, const Vec& to, qreal radius=-1.0, int nbSubdivisions=12);
    static void drawAxis(qreal length=1.0);
    static void drawGrid(qreal size=1.0, int nbSubdivisions=10);

    virtual void startScreenCoordinatesSystem(bool upward=false) const;
    virtual void stopScreenCoordinatesSystem() const;

    void drawText(int x, int y, const QString& text, const QFont& fnt=QFont());
    void displayMessage(const QString& message, int delay=2000);

protected:
    virtual void drawLight(GLenum light, qreal scale = 1.0) const;

public:
    int width() const;
    int height() const;

%If (QGLViewer_2_7_0 - )
    void update();
%End

%If ( - QGLViewer_2_6_4)
    virtual void updateGL();
    static QImage convertToGLFormat(const QImage & image /In/);
    void qglColor(const QColor& color /In/) const;
    void qglClearColor(const QColor& color /In/) const;
    bool isSharing() const;
%End

    bool isValid() const;
    void makeCurrent();
    bool hasMouseTracking () const;

public slots:
    void resize(int width, int height);
    void setMouseTracking(bool enable);

%If ( - QGLViewer_2_6_4)
protected:
    bool autoBufferSwap() const;

protected slots:
    void setAutoBufferSwap(bool on);
%End

public:
    const QString& snapshotFileName() const;
    const QString& snapshotFormat() const;
    int snapshotCounter() const;
    int snapshotQuality();

public slots:
    void saveSnapshot(bool automatic=true, bool overwrite=false); 
    void saveSnapshot(const QString& fileName /In/, bool overwrite=false);
    void setSnapshotFileName(const QString& name /In/);
    void setSnapshotFormat(const QString& format /In/);
    void setSnapshotCounter(int counter);
    void setSnapshotQuality(int quality);
    bool openSnapshotFormatDialog();
    void snapshotToClipboard();

public:
    QFont scaledFont(const QFont& font) const;

    GLuint bufferTextureId() const;
    qreal bufferTextureMaxU() const;
    qreal bufferTextureMaxV() const;

%If (QGLViewer_2_7_0 - )
  void renderText(int x, int y, const QString &str /In/,
                  const QFont &font /In/ = QFont());

  void renderText(double x, double y, double z, 
                  const  QString &str /In/,
                  const QFont &font /In/ = QFont());

%End

public slots:
    void copyBufferToTexture(GLint internalFormat, GLenum format = GL_NONE);
      
public:
    bool animationIsStarted() const;
    int animationPeriod() const;

public slots:
    void setAnimationPeriod(int period);
    virtual void startAnimation();
    virtual void stopAnimation();
  
    virtual void animate();
    void toggleAnimation();

signals:

    void viewerInitialized();
    void drawNeeded();
    void drawFinished(bool automatic);
    void animateNeeded();
    void helpRequired();
    void axisIsDrawnChanged(bool drawn);
    void gridIsDrawnChanged(bool drawn);
    void FPSIsDisplayedChanged(bool displayed);
    void textIsEnabledChanged(bool enabled);
    void cameraIsEditedChanged(bool edited);
    void stereoChanged(bool on);
    void pointSelected(QMouseEvent* e /In/);
    void mouseGrabberChanged(MouseGrabber* mouseGrabber /In/);

public:
    virtual QString helpString() const ;
    virtual QString mouseString() const;
    virtual QString keyboardString() const;

    virtual QString mouseBindingsString () const;
    virtual QString shortcutBindingsString () const;

public slots:
    virtual void help();
    virtual void aboutQGLViewer();

protected:
    QTabWidget* helpWidget();

    virtual void resizeGL(int width, int height);
    virtual void initializeGL();

    virtual void init();
%VirtualCatcherCode
        glGetError();
        PyObject * result = sipCallMethod(&sipIsErr, sipMethod, "");

        if (result != NULL)
        {
            Py_DECREF(result);
        }
%End
%VirtualCallCode
        glGetError();
%End

    virtual void paintGL();
    virtual void preDraw();
    virtual void preDrawStereo(bool leftBuffer=true);

    virtual void draw();
    virtual void fastDraw();
    virtual void postDraw();

    virtual void mousePressEvent(QMouseEvent * event /In/);
    virtual void mouseMoveEvent(QMouseEvent * event /In/);
    virtual void mouseReleaseEvent(QMouseEvent * event /In/);
    virtual void mouseDoubleClickEvent(QMouseEvent * event /In/);
    virtual void wheelEvent(QWheelEvent * event /In/);
    virtual void keyPressEvent(QKeyEvent * event /In/);
    virtual void timerEvent(QTimerEvent * event /In/);
    virtual void closeEvent(QCloseEvent * event /In/);

public:
    int selectedName() const;
    int selectBufferSize() const;
    int selectRegionWidth() const;
    int selectRegionHeight() const;
    void* selectBuffer();
%MethodCode
    sipRes = sipCpp->selectBuffer();
%End

  SIP_PYOBJECT getMultipleSelection() ;
%MethodCode
  // Flush GL buffers
  glFlush();

  // Get the number of objects that were seen through the pick matrix frustum. Reset GL_RENDER mode.
  GLint nbHits = glRenderMode(GL_RENDER);

  if (nbHits > 0)
    {
      sipRes = PyList_New(nbHits);
      // Interpret results : each object created 4 values in the selectBuffer().
      // (selectBuffer())[4*i+3] is the id pushed on the stack.
      GLuint * buffer = sipCpp->selectBuffer();
      GLuint names;
      float zmax, zmin;
      GLuint id;
      for (int i=0; i<nbHits; ++i)
      {
        names = *buffer; ++buffer;
        zmin = (float)*buffer; ++buffer;
        zmax = (float)*buffer; ++buffer;
        PyObject * item = PyTuple_New(3);
        PyList_SetItem(sipRes,i,item);
        PyTuple_SetItem(item,0,PyFloat_FromDouble(zmin));
        PyTuple_SetItem(item,1,PyFloat_FromDouble(zmax));
        if (names <= 1){
            id = *buffer; ++buffer;
            PyTuple_SetItem(item,2,PyLong_FromUnsignedLong(id));
        }
        else {
            PyObject * py_ids = PyList_New(names);
            for(unsigned int j = 0 ; j < names ; j++){
                id = *buffer; ++buffer;
                PyList_SetItem(py_ids,j,PyLong_FromUnsignedLong(id));
            }
            PyTuple_SetItem(item,2,py_ids);
        }
      }
    }
    else { 
        sipRes = Py_None;
        Py_INCREF(sipRes);
    }
%End


public slots:
    virtual void select(const QMouseEvent* event /In/);
    virtual void select(const QPoint& point /In/);

    void setSelectBufferSize(int size);
    void setSelectRegionWidth(int width);
    void setSelectRegionHeight(int height);
    void setSelectedName(int id);

 protected:
 
    virtual void beginSelection(const QPoint& point /In/);
    virtual void drawWithNames();
    virtual void endSelection(const QPoint& point /In/);
    virtual void postSelection(const QPoint& point /In/) ;

public:
    enum KeyboardAction { DRAW_AXIS, DRAW_GRID, DISPLAY_FPS, ENABLE_TEXT, EXIT_VIEWER,
                          SAVE_SCREENSHOT, CAMERA_MODE, FULL_SCREEN, STEREO, ANIMATION, HELP, EDIT_CAMERA,
                          MOVE_CAMERA_LEFT, MOVE_CAMERA_RIGHT, MOVE_CAMERA_UP, MOVE_CAMERA_DOWN,
                          INCREASE_FLYSPEED, DECREASE_FLYSPEED, SNAPSHOT_TO_CLIPBOARD
    }; 

    unsigned int shortcut(KeyboardAction action) const;

    unsigned int keyboardAccelerator(KeyboardAction action) const;
    Qt::Key keyFrameKey(unsigned int index) const;
    Qt::KeyboardModifiers playKeyFramePathStateKey() const;
    Qt::KeyboardModifiers addKeyFrameStateKey() const;
    Qt::KeyboardModifiers playPathStateKey() const;

    Qt::Key pathKey(unsigned int index) const;
    Qt::KeyboardModifiers addKeyFrameKeyboardModifiers() const;
    Qt::KeyboardModifiers playPathKeyboardModifiers() const;

public slots:
    void setShortcut(KeyboardAction action, unsigned int key);
    void setKeyboardAccelerator(KeyboardAction action, unsigned int key);
    void setKeyDescription(unsigned int key, QString description);
    void clearShortcuts();


    virtual void setKeyFrameKey(unsigned int index, int key);
    virtual void setPlayKeyFramePathStateKey(unsigned int buttonState);
    virtual void setPlayPathStateKey(unsigned int buttonState);
    virtual void setAddKeyFrameStateKey(unsigned int buttonState);
    virtual void setPathKey(int key, unsigned int index = 0);
    virtual void setPlayPathKeyboardModifiers(Qt::KeyboardModifiers modifiers);
    virtual void setAddKeyFrameKeyboardModifiers(Qt::KeyboardModifiers modifiers);

public:

    enum MouseHandler { CAMERA, FRAME };

    enum ClickAction { NO_CLICK_ACTION, ZOOM_ON_PIXEL, ZOOM_TO_FIT, SELECT, RAP_FROM_PIXEL, RAP_IS_CENTER,
                       CENTER_FRAME, CENTER_SCENE, SHOW_ENTIRE_SCENE, ALIGN_FRAME, ALIGN_CAMERA };


    enum MouseAction { NO_MOUSE_ACTION,
                       ROTATE, ZOOM, TRANSLATE,
                       MOVE_FORWARD, LOOK_AROUND, MOVE_BACKWARD,
                       SCREEN_ROTATE, ROLL, DRIVE,
                       SCREEN_TRANSLATE, ZOOM_ON_REGION };

 
    MouseAction mouseAction(unsigned int state) const;
    int mouseHandler(unsigned int state) const;
    int mouseButtonState(MouseHandler handler, MouseAction action, bool withConstraint=true) const;
    ClickAction clickAction(unsigned int state, bool doubleClick, Qt::MouseButtons buttonsBefore) const;
    void getClickButtonState(ClickAction action, unsigned int& state, bool& doubleClick, Qt::MouseButtons& buttonsBefore) const;
    unsigned int wheelButtonState(MouseHandler handler, MouseAction action, bool withConstraint=true) const;


    MouseAction mouseAction(Qt::Key key, Qt::KeyboardModifiers modifiers, Qt::MouseButton button) const;
    int mouseHandler(Qt::Key key, Qt::KeyboardModifiers modifiers, Qt::MouseButton button) const;

    void getMouseActionBinding(MouseHandler handler, MouseAction action, bool withConstraint,
                               Qt::Key& key, Qt::KeyboardModifiers& modifiers, Qt::MouseButton& button) const;

    ClickAction clickAction(Qt::Key key, Qt::KeyboardModifiers modifiers, Qt::MouseButton button,
                            bool doubleClick=false, Qt::MouseButtons buttonsBefore=Qt::NoButton) const;

    void getClickActionBinding(ClickAction action, Qt::Key& key, Qt::KeyboardModifiers& modifiers,
                               Qt::MouseButton& button, bool& doubleClick, Qt::MouseButtons& buttonsBefore) const;

    MouseAction wheelAction(Qt::Key key, Qt::KeyboardModifiers modifiers) const;
    int wheelHandler(Qt::Key key, Qt::KeyboardModifiers modifiers) const;

    void getWheelActionBinding(MouseHandler handler, MouseAction action, bool withConstraint,
                               Qt::Key& key, Qt::KeyboardModifiers& modifiers) const;
public slots:
    void setMouseBinding(unsigned int state, MouseHandler handler, MouseAction action, bool withConstraint=true);
    void setMouseBinding(unsigned int state, ClickAction action, bool doubleClick=false, Qt::MouseButtons buttonsBefore=Qt::NoButton);
    void setMouseBindingDescription(unsigned int state, QString description, bool doubleClick=false, Qt::MouseButtons buttonsBefore=Qt::NoButton);
    
    void setMouseBinding(Qt::KeyboardModifiers modifiers, Qt::MouseButton buttons, MouseHandler handler, MouseAction action, bool withConstraint=true);
    void setMouseBinding(Qt::KeyboardModifiers modifiers, Qt::MouseButton button, ClickAction action, bool doubleClick=false, Qt::MouseButtons buttonsBefore=Qt::NoButton);
    void setWheelBinding(Qt::KeyboardModifiers modifiers, MouseHandler handler, MouseAction action, bool withConstraint=true);
    void setMouseBindingDescription(Qt::KeyboardModifiers modifiers, Qt::MouseButton button, QString description, bool doubleClick=false, Qt::MouseButtons buttonsBefore=Qt::NoButton);

    void setMouseBinding(Qt::Key key, Qt::KeyboardModifiers modifiers, Qt::MouseButton buttons, MouseHandler handler, MouseAction action, bool withConstraint=true);
    void setMouseBinding(Qt::Key key, Qt::KeyboardModifiers modifiers, Qt::MouseButton button, ClickAction action, bool doubleClick=false, Qt::MouseButtons buttonsBefore=Qt::NoButton);
    void setWheelBinding(Qt::Key key, Qt::KeyboardModifiers modifiers, MouseHandler handler, MouseAction action, bool withConstraint=true);
    void setMouseBindingDescription(Qt::Key key, Qt::KeyboardModifiers modifiers, Qt::MouseButton button, QString description, bool doubleClick=false, Qt::MouseButtons buttonsBefore=Qt::NoButton);

    void clearMouseBindings();

    MouseAction wheelAction(Qt::KeyboardModifiers modifiers) const;
    int wheelHandler(Qt::KeyboardModifiers modifiers) const;

    void setHandlerKeyboardModifiers(MouseHandler handler, Qt::KeyboardModifiers modifiers);
    void setHandlerStateKey(MouseHandler handler, unsigned int buttonState);
    void setMouseStateKey(MouseHandler handler, unsigned int buttonState);

public:

    QString stateFileName() const;
    virtual QDomElement domElement(const QString& name /In/, QDomDocument& document /In/) const;

public slots:

    virtual void initFromDOMElement(const QDomElement& element /In/);
    virtual void saveStateToFile(); // cannot be const because of QMessageBox
    virtual bool restoreStateFromFile();

    void setStateFileName(const QString& name /In/) ;

    void saveToFile(const QString& fileName /In/ =QString());
    bool restoreFromFile(const QString& fileName /In/ =QString());


public:
    static const QList<QGLViewer*>& QGLViewerPool() ;
    static int QGLViewerIndex(const QGLViewer* viewer);

public:
    virtual void setVisualHintsMask(int mask, int delay = 2000);
    virtual void drawVisualHints();

public slots:
    virtual void resetVisualHints();


public:

%TypeCode
    static bool isPowerOfTwo(int val){
        long i=0;
        while ((1<<i)<val) i++;
        if (val==(1<<i)) return true;
        return false;     
     }
%End


private:
  QGLViewer(const QGLViewer& v);


};
