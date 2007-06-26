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

class QGLViewer : QGLWidget
{

%TypeHeaderCode
#include <QGLViewer/qglviewer.h>
#include <GL/gl.h>
#ifdef Q_WS_X11
#include <GL/glext.h>
#endif

#ifndef GL_BGRA
#define GL_BGRA 0x80E1
#endif

#ifndef GL_TEXTURE_3D
#define GL_TEXTURE_3D 0x806F
#endif

%End

public:
    explicit QGLViewer(QWidget* parent /TransferThis/ =0, const QGLWidget* shareWidget=0, Qt::WFlags flags=0);
    explicit QGLViewer(QGLContext *context, QWidget* parent /TransferThis/=0, const QGLWidget* shareWidget=0, Qt::WFlags flags=0);
    explicit QGLViewer(const QGLFormat& format, QWidget* parent /TransferThis/=0, const QGLWidget* shareWidget=0, Qt::WFlags flags=0);
    virtual ~QGLViewer();
    
    bool axisIsDrawn() const;
    bool gridIsDrawn() const;
    bool FPSIsDisplayed() const;
    bool textIsEnabled() const;
    bool cameraIsEdited() const;
    
    QColor backgroundColor() const;
    QColor foregroundColor() const;
    
    float sceneRadius() const;
    Vec sceneCenter() const;
    
    Camera* camera() const;
    ManipulatedFrame* manipulatedFrame() const;
    
    MouseGrabber* mouseGrabber() const;
    void setMouseGrabberIsEnabled(const MouseGrabber * mouseGrabber /In/, bool enabled=true);
    bool mouseGrabberIsEnabled(const MouseGrabber* mouseGrabber /In/);
    
    float aspectRatio() const;
    float currentFPS();
    bool isFullScreen() const;
    bool displaysInStereo() const;
    virtual QSize sizeHint() const;
    
    static void drawArrow(float length=1.0, float radius=-1.0, int nbSubdivisions=12);
    static void drawArrow(const Vec& from, const Vec& to, float radius=-1.0, int nbSubdivisions=12);
    static void drawAxis(float length=1.0);
    static void drawGrid(float size=1.0, int nbSubdivisions=10);

    virtual void startScreenCoordinatesSystem(bool upward=false) const;
    virtual void stopScreenCoordinatesSystem() const;

    void drawText(int x, int y, const QString& text, const QFont& fnt=QFont());
    void displayMessage(const QString& message, int delay=2000);

  int width() const;
  int height() const;
  virtual void updateGL();
  static QImage convertToGLFormat(const QImage & image /In/);
  void qglColor(const QColor& color /In/) const;
  void qglClearColor(const QColor& color /In/) const;
  bool isValid() const;
  bool isSharing() const;
  virtual void makeCurrent();
  bool hasMouseTracking () const;
  
  const QString& snapshotFileName() const;
  const QString& snapshotFormat() const;
  int snapshotCounter() const;
  int snapshotQuality();
  
  GLuint bufferTextureId() const;
  float bufferTextureMaxU() const;
  float bufferTextureMaxV() const;
  
  bool animationIsStarted() const;
  int animationPeriod() const;

  virtual QString helpString() const ;
  virtual QString mouseString() const;
  virtual QString keyboardString() const;

  virtual QString mouseBindingsString () const;
  virtual QString shortcutBindingsString () const;
  
  int selectedName() const;
  int selectBufferSize() const;
  int selectRegionWidth() const;
  int selectRegionHeight() const;
  void* selectBuffer();
%MethodCode
    sipRes = sipCpp->selectBuffer();
%End

  SIP_PYOBJECT getMultipleSelection() const;
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

  GLuint bindTexture3D(const QVector<QImage> & image, GLenum target = GL_TEXTURE_3D, GLint format = GL_RGBA );
%MethodCode

#define isPowerOfTwo(a) ((log((float)a)/log(2.f)) - int(log((float)a)/log(2.f)) <  0.0001)
    
    sipRes = 0;
    
#ifdef Q_OS_WIN32

#ifndef APIENTRY
#define APIENTRY
#endif

    typedef void (APIENTRY *_glTexImage3D) (GLenum, GLint, GLint, GLsizei, GLsizei, GLsizei, GLint, GLenum, GLenum, const GLvoid *);
    static _glTexImage3D glTexImage3D = NULL;
    if (glTexImage3D == NULL){
        glTexImage3D = (_glTexImage3D)wglGetProcAddress("glTexImage3D");
    }
    if (glTexImage3D == NULL){
        printf("Cannot load 'glTexImage3D' function.\n");
        sipIsErr = -1;
    }
    else {
#endif   
    int depth = a0->size();
    if(depth == 0 || !isPowerOfTwo(depth) ){
        sipIsErr = -1;
    }
    else{
        int w = a0->at(0).width();
        int h = a0->at(0).height();
        if( w == 0 || h == 0 || ! isPowerOfTwo(w) || ! isPowerOfTwo(h) ){
            sipIsErr = -1;
        }
        else{
             for(QVector<QImage>::const_iterator itImage = a0->begin()+1; itImage != a0->end() && sipRes != -1; ++itImage){
                if (itImage->width() != w || itImage->height() != h)
                   sipIsErr = -1;                
             }
             if (sipIsErr != -1){

                size_t byteperpixel = 4;
                size_t msize= w*h*depth*byteperpixel;
                GLubyte * texels = (GLubyte *)malloc(msize);
                if (texels == NULL) sipIsErr = -1;
                else {
                    GLubyte * itTexel = texels;

                    for(QVector<QImage>::const_iterator itImage = a0->begin(); itImage != a0->end(); ++itImage){
                        QImage img = sipCpp->convertToGLFormat(*itImage);
                        size_t imsize = img.numBytes();
                        memcpy(itTexel,img.bits(),imsize);
                        itTexel += imsize;
                    }

                    if(itTexel != texels+msize) printf("Invalid texture size.\n"); 
                
                    glEnable(GL_TEXTURE_3D);
                    glGenTextures(1, &sipRes);
                    glBindTexture(GL_TEXTURE_3D, sipRes);
                    if (sipRes != 0)
                    {
                        glTexParameterf(a1, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
                        glTexParameterf(a1, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
                        glTexImage3D(a1, 0, a2, w, h, depth, 0, GL_RGBA, GL_UNSIGNED_BYTE, texels);
                    }
                    else sipIsErr = -1;
                    delete [] texels;
                }
             }
#ifdef Q_OS_WIN32
        }
#endif
    } }
%End

  Qt::Key keyFrameKey(int index) const;
  Qt::KeyboardModifiers playKeyFramePathStateKey() const;
  Qt::KeyboardModifiers addKeyFrameStateKey() const;
  Qt::KeyboardModifiers playPathStateKey() const;

  Qt::Key pathKey(int index) const;
  Qt::KeyboardModifiers addKeyFrameKeyboardModifiers() const;
  Qt::KeyboardModifiers playPathKeyboardModifiers() const;

  enum MouseAction { 
	NO_MOUSE_ACTION,
	ROTATE, 
	ZOOM, 
	TRANSLATE,
	MOVE_FORWARD,
	LOOK_AROUND,
	MOVE_BACKWARD,
	SCREEN_ROTATE,
	ROLL,
	DRIVE,
	SCREEN_TRANSLATE,
	ZOOM_ON_REGION 
	};
	

 
  QString stateFileName() const;
  virtual QDomElement domElement(const QString& name /In/, QDomDocument& document /In/) const;

  static const QList<QGLViewer*>& QGLViewerPool() ;
  static int QGLViewerIndex(const QGLViewer* viewer);

  virtual void setVisualHintsMask(int mask, int delay = 2000);
  virtual void drawVisualHints();

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
	
	void setBackgroundColor(const QColor& color /In/);
	void setForegroundColor(const QColor& color /In/);

	virtual void setSceneRadius(float radius);
    virtual void setSceneCenter(const Vec& center /In/);
    void setSceneBoundingBox(const Vec& min /In/, const Vec& max /In/);
	void showEntireScene();
	
    void setCamera(Camera* camera /Transfer/);
    void setManipulatedFrame(ManipulatedFrame* frame /Transfer/);
	
   void setMouseGrabber(MouseGrabber* mouseGrabber /Transfer/);
	
	void setFullScreen(bool fullScreen=true);
	void setStereoDisplay(bool stereo=true);
	void toggleFullScreen();
	void toggleStereoDisplay();

  virtual void resize(int width, int height);
  virtual void setMouseTracking(bool enable);
	
  void saveSnapshot(bool automatic=true, bool overwrite=false);	
  void saveSnapshot(const QString& fileName /In/, bool overwrite=false);
  void setSnapshotFileName(const QString& name /In/);
  void setSnapshotFormat(const QString& format /In/);
  void setSnapshotCounter(int counter);
  void setSnapshotQuality(int quality);
  bool openSnapshotFormatDialog();
  
  void copyBufferToTexture(GLint internalFormat, GLenum format=GL_NONE);

  void setAnimationPeriod(int period);
  virtual void startAnimation();
  virtual void stopAnimation();
  
  virtual void animate();
  void toggleAnimation();

  virtual void help();
  virtual void aboutQGLViewer();
  
  virtual void select(const QMouseEvent* event /In/);
  virtual void select(const QPoint& point /In/);

  void setSelectBufferSize(int size);
  void setSelectRegionWidth(int width);
  void setSelectRegionHeight(int height);
  void setSelectedName(int id);
  
  virtual void setKeyFrameKey(int index, int key);
  virtual void setPlayKeyFramePathStateKey(int buttonState);
  virtual void setPlayPathStateKey(int buttonState);
  virtual void setAddKeyFrameStateKey(int buttonState);
  virtual void setPathKey(int key, int index = 0);
  virtual void setPlayPathKeyboardModifiers(Qt::KeyboardModifiers modifiers);
  virtual void setAddKeyFrameKeyboardModifiers(Qt::KeyboardModifiers modifiers);

  virtual void initFromDOMElement(const QDomElement& element /In/);
  virtual void saveStateToFile(); 
  virtual bool restoreStateFromFile();
  void setStateFileName(const QString& name /In/) ;

  void saveToFile(const QString& fileName /In/ =QString::null);
  bool restoreFromFile(const QString& fileName /In/ =QString::null);

  virtual void resetVisualHints();


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
  void pointSelected(const QMouseEvent* e /In/);
  void mouseGrabberChanged(MouseGrabber* mouseGrabber /In/);
 

 protected:
  virtual void drawLight(GLenum light, float scale = 1.0) const;
    
  bool autoBufferSwap() const;
 
  QTabWidget* helpWidget();

  virtual void resizeGL(int width, int height);
  virtual void initializeGL();

  virtual void init();

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
  virtual void beginSelection(const QPoint& point /In/);
  virtual void drawWithNames();
  virtual void endSelection(const QPoint& point /In/);
  virtual void postSelection(const QPoint& point /In/) ;
  
    enum KeyboardAction { 
	DRAW_AXIS, 
	DRAW_GRID, 
	DISPLAY_FPS, 
	ENABLE_TEXT, 
	EXIT_VIEWER,
	SAVE_SCREENSHOT, 
	CAMERA_MODE, 
	FULL_SCREEN, 
	STEREO, 
	ANIMATION, 
	HELP, 
	EDIT_CAMERA,
	MOVE_CAMERA_LEFT,
	MOVE_CAMERA_RIGHT,
	MOVE_CAMERA_UP,
	MOVE_CAMERA_DOWN,
	INCREASE_FLYSPEED,
	DECREASE_FLYSPEED 
	}; 

  int shortcut(KeyboardAction action) const;
  int keyboardAccelerator(KeyboardAction action) const;
 
  enum MouseHandler { 
	CAMERA,
	FRAME 
	};

  enum ClickAction { 
	NO_CLICK_ACTION, 
	ZOOM_ON_PIXEL, 
	ZOOM_TO_FIT, 
	SELECT, 
	RAP_FROM_PIXEL, 
	RAP_IS_CENTER,
	CENTER_FRAME, 
	CENTER_SCENE, 
	SHOW_ENTIRE_SCENE, 
	ALIGN_FRAME, 
	ALIGN_CAMERA 
	};
	
  MouseAction mouseAction(int state) const;
  int mouseHandler(int state) const;
  int mouseButtonState(MouseHandler handler, MouseAction action, bool withConstraint=true) const;
  ClickAction clickAction(int state, bool doubleClick, Qt::MouseButtons buttonsBefore) const;
  void getClickButtonState(ClickAction action, int& state, bool& doubleClick, Qt::MouseButtons& buttonsBefore) const;

  MouseAction wheelAction(Qt::KeyboardModifiers modifiers) const;
  int wheelHandler(Qt::KeyboardModifiers modifiers) const;
  int wheelButtonState(MouseHandler handler, MouseAction action, bool withConstraint=true) const;

protected slots:
  void setAutoBufferSwap(bool on);
  
  void setShortcut(KeyboardAction action, int key);
  void setKeyboardAccelerator(KeyboardAction action, int key);
  void setKeyDescription(int key, QString description);

  void setMouseBinding(int state, MouseHandler handler, MouseAction action, bool withConstraint=true);
  void setMouseBinding(int state, ClickAction action, bool doubleClick=false, Qt::MouseButtons buttonsBefore=Qt::NoButton);
  void setMouseBindingDescription(int state, QString description, bool doubleClick=false, Qt::MouseButtons buttonsBefore=Qt::NoButton);
  void setWheelBinding(Qt::KeyboardModifiers modifiers, MouseHandler handler, MouseAction action, bool withConstraint=true);
  void setHandlerKeyboardModifiers(MouseHandler handler, Qt::KeyboardModifiers modifiers);
  void setHandlerStateKey(MouseHandler handler, int buttonState);
  void setMouseStateKey(MouseHandler handler, int buttonState);

private:
  QGLViewer(const QGLViewer& v);


};
