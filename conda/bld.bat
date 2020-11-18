if "%PY3K%"=="1" (
    :: Python 3 -> MSVC 2015
    %PYTHON% configureQt5.py --verbose --pyqt=PyQt5
) else (
    :: Python 2 -> MSVC 2008
    %PYTHON% configureQt5.py --verbose --pyqt=PyQt5 --spec=win32-msvc2008
)

if errorlevel 1 exit 1

nmake release

if errorlevel 1 exit 1

%PYTHON% setup.py install --prefix=${PREFIX}

:: COPY src\python\PyQGLViewer.py %SP_DIR%
:: COPY build\PyQGLViewerQt5\PyQGLViewerQt5.pyd %SP_DIR%
