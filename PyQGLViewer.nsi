# PyQGLViewer NSIS installer script.
#
# Copyright (c) 2006
# 	Riverbank Computing Limited <info@riverbankcomputing.co.uk>
# 
# This file is part of PyQGLViewer.
# 
# This copy of PyQGLViewer is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2, or (at your option) any later
# version.
# 
# PyQGLViewer is supplied in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# 
# You should have received a copy of the GNU General Public License along with
# PyQGLViewer; see the file LICENSE.  If not, write to the Free Software Foundation,
# Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.


# These will change with different releases.
!define PYQGLVIEWER_VERSION        "0.11.0"
!define PYQGLVIEWER_LICENSE        "GPL"
!define PYQGLVIEWER_LICENSE_LC     "gpl"
!define PYQGLVIEWER_PYTHON_MINOR   "7"
!define PYQGLVIEWER_QT_VERS        "4.8.1"
!define PYQGLVIEWER_QGLVIEWER_VERS "2.3.17"
!define PYQGLVIEWER_COMPILER       "MinGW"

# These are all derived from the above.
!define PYQGLVIEWER_NAME           "PyQGLViewer ${PYQGLVIEWER_LICENSE} v${PYQGLVIEWER_VERSION}"
!define PYQGLVIEWER_INSTALLDIR     "C:\Python2${PYQGLVIEWER_PYTHON_MINOR}\"
!define PYQGLVIEWER_PYTHON_VERS    "2.${PYQGLVIEWER_PYTHON_MINOR}"
!define PYQGLVIEWER_PYTHON_HKLM    "Software\Python\PythonCore\${PYQGLVIEWER_PYTHON_VERS}\InstallPath"
!define PYQGLVIEWER_QT_HKLM        "Software\OpenAlea\Versions\${PYQGLVIEWER_QT_VERS}"
!define PYQGLVIEWER_QGLVIEWER_SRCDIR     "..\..\libQGLViewer-${PYQGLVIEWER_QGLVIEWER_VERS}"


# Tweak some of the standard pages.
!define MUI_WELCOMEPAGE_TEXT \
"This wizard will guide you through the installation of ${PYQGLVIEWER_NAME}.\r\n\
\r\n\
This copy of PyQGLViewer has been built with the ${PYQGLVIEWER_COMPILER} compiler against \
Python v${PYQGLVIEWER_PYTHON_VERS}.x, Qt v${PYQGLVIEWER_QT_VERS} and libQGLViewer v${PYQGLVIEWER_QGLVIEWER_VERS}.\r\n\
\r\n\
Any code you write must be released under a license that is compatible with \
the GPL.\r\n\
\r\n\
Click Next to continue."

!define MUI_FINISHPAGE_LINK "Get the latest news of PyQGLViewer here"
!define MUI_FINISHPAGE_LINK_LOCATION "http://pyqglviewer.gforge.inria.fr/"


# Include the tools we use.
!include MUI.nsh
!include LogicLib.nsh


# Define the product name and installer executable.
Name "PyQGLViewer"
Caption "${PYQGLVIEWER_NAME} Setup"
OutFile "PyQGLViewer-${PYQGLVIEWER_VERSION}-${PYQGLVIEWER_QGLVIEWER_VERS}-Py2.${PYQGLVIEWER_PYTHON_MINOR}-Qt${PYQGLVIEWER_QT_VERS}.exe"


# Set the install directory, from the registry if possible.
InstallDir "${PYQGLVIEWER_INSTALLDIR}"
InstallDirRegKey HKLM "${PYQGLVIEWER_PYTHON_HKLM}" ""


# The different installation types.  "Full" is everything.  "Minimal" is the
# runtime environment.
InstType "Full"
InstType "Minimal"


# Maximum compression.
SetCompressor /SOLID lzma


# We want the user to confirm they want to cancel.
!define MUI_ABORTWARNING

Var QTPLUGINS_FOLDER
Var PYQGLVIEWER_INSTDIR

Function .onInit
    # Check where Qt has been installed.
    ReadEnvStr $QTPLUGINS_FOLDER QTDIR
    StrCmp $QTPLUGINS_FOLDER "" 0 +2
        StrCpy $QTPLUGINS_FOLDER "C:\Qt\${PYQGLVIEWER_QT_VERS}"
    
    StrCpy $PYQGLVIEWER_INSTDIR "$PROGRAMFILES\PyQGLViewer"
    
    # Check the right version of Python has been installed.
    ReadRegStr $0 HKLM "${PYQGLVIEWER_PYTHON_HKLM}" ""

    ${If} $0 == ""
        MessageBox MB_YESNO|MB_ICONQUESTION \
"This copy of PyQGLViewer has been built against Python v${PYQGLVIEWER_PYTHON_VERS}.x which \
doesn't seem to be installed.$\r$\n\
$\r$\n\
Do you with to continue with the installation?" IDYES GotPython
            Abort
GotPython:
    ${Endif}
FunctionEnd


# Define the different pages.
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "doc/LICENSE.txt"
!insertmacro MUI_PAGE_COMPONENTS
!define MUI_DIRECTORYPAGE_TEXT_DESTINATION "Python repository"
!insertmacro MUI_PAGE_DIRECTORY

!define MUI_DIRECTORYPAGE_TEXT_DESTINATION "Qt repository"
!define MUI_DIRECTORYPAGE_VARIABLE $QTPLUGINS_FOLDER
!insertmacro MUI_PAGE_DIRECTORY

!define MUI_DIRECTORYPAGE_TEXT_DESTINATION "PyQGLViewer repository"
!define MUI_DIRECTORYPAGE_VARIABLE $PYQGLVIEWER_INSTDIR
!insertmacro MUI_PAGE_DIRECTORY

!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
  
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

  
# Other settings.
!insertmacro MUI_LANGUAGE "English"


# Installer sections.

Section "Extension modules" SecModules
    SectionIn 1 2 RO

    # Make sure this is clean and tidy.
    RMDir /r $PYQGLVIEWER_INSTDIR
    CreateDirectory $PYQGLVIEWER_INSTDIR

    SetOverwrite on

    # We have to take the SIP files from where they should have been installed.
    SetOutPath $INSTDIR\Lib\site-packages
    File .\build\PyQGLViewer.pyd
    File ${PYQGLVIEWER_QGLVIEWER_SRCDIR}\QGLViewer\release\QGLViewer2.dll
    SetOutPath $QTPLUGINS_FOLDER\plugins\designer
    File ${PYQGLVIEWER_QGLVIEWER_SRCDIR}\designerPlugin\release\qglviewerplugin.dll
    
SectionEnd

Section "Developer tools" SecTools
    SectionIn 1

    SetOverwrite on

    SetOutPath $INSTDIR\sip\QGLViewer
    File .\src\sip\vec.sip
    File .\src\sip\quaternion.sip
    File .\src\sip\frame.sip
    File .\src\sip\constraint.sip
    File .\src\sip\keyFrameInterpolator.sip
    File .\src\sip\mouseGrabber.sip
    File .\src\sip\manipulatedFrame.sip
    File .\src\sip\manipulatedCameraFrame.sip
    File .\src\sip\camera.sip
    File .\src\sip\qglviewer.sip
    File .\src\sip\domUtils.sip
    SetOutPath $INSTDIR\include\QGLViewer
    File ${PYQGLVIEWER_QGLVIEWER_SRCDIR}\QGLViewer\*.h

SectionEnd

Section "Documentation" SecDocumentation
    SectionIn 1

    SetOverwrite on

    SetOutPath $PYQGLVIEWER_INSTDIR\doc
    File .\doc\*
SectionEnd

Section "Examples and tutorial" SecExamples
    SectionIn 1

    SetOverwrite on

    IfFileExists "$PYQGLVIEWER_INSTDIR\examples" 0 +2
        CreateDirectory $PYQGLVIEWER_INSTDIR\examples

    SetOutPath $PYQGLVIEWER_INSTDIR\examples
    File .\examples\*.py
    File .\examples\*.ui
SectionEnd

Section "Start Menu shortcuts" SecShortcuts
    SectionIn 1

    # Make sure this is clean and tidy.
    RMDir /r "$SMPROGRAMS\${PYQGLVIEWER_NAME}"
    CreateDirectory "$SMPROGRAMS\${PYQGLVIEWER_NAME}"

    IfFileExists "$PYQGLVIEWER_INSTDIR\doc" 0 +2
        CreateShortCut "$SMPROGRAMS\${PYQGLVIEWER_NAME}\Web Site.lnk" "http://pyqglviewer.gforge.inria.fr/"

    IfFileExists "$PYQGLVIEWER_INSTDIR\examples" 0 +2
        CreateShortCut "$SMPROGRAMS\${PYQGLVIEWER_NAME}\Examples Source.lnk" "$PYQGLVIEWER_INSTDIR\examples"

    CreateShortCut "$SMPROGRAMS\${PYQGLVIEWER_NAME}\Uninstall PyQGLViewer.lnk" "$PYQGLVIEWER_INSTDIR\Uninstall.exe"
SectionEnd

Section -post
    # Tell Windows about the package.
    WriteRegExpandStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PyQGLViewer" "UninstallString" '"$PYQGLVIEWER_INSTDIR\Uninstall.exe"'
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PyQGLViewer" "DisplayName" "${PYQGLVIEWER_NAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PyQGLViewer" "DisplayVersion" "${PYQGLVIEWER_VERSION}"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PyQGLViewer" "NoModify" "1"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PyQGLViewer" "NoRepair" "1"

    # Save the installation directory for the uninstaller.
    WriteRegStr HKLM "Software\PyQGLViewer\" "Python" $INSTDIR
    WriteRegStr HKLM "Software\PyQGLViewer\" "QtPlugins" $QTPLUGINS_FOLDER
    WriteRegStr HKLM "Software\PyQGLViewer\" "PyQGLViewer" $PYQGLVIEWER_INSTDIR

    # Create the uninstaller.
    WriteUninstaller "$PYQGLVIEWER_INSTDIR\Uninstall.exe"
SectionEnd


# Section description text.
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
!insertmacro MUI_DESCRIPTION_TEXT ${SecModules} \
"The PyQGLViewer binaries."
!insertmacro MUI_DESCRIPTION_TEXT ${SecTools} \
"The PyQGLViewer developper tools (.sip and .h files)."
!insertmacro MUI_DESCRIPTION_TEXT ${SecDocumentation} \
"The PyQGLViewer documentation."
!insertmacro MUI_DESCRIPTION_TEXT ${SecExamples} \
"Ports to Python of the standard QGLViewer examples and tutorial."
!insertmacro MUI_DESCRIPTION_TEXT ${SecShortcuts} \
"This adds shortcuts to your Start Menu."
!insertmacro MUI_FUNCTION_DESCRIPTION_END


Section "Uninstall"
    # Get the install directory.
    ReadRegStr $INSTDIR HKLM "Software\PyQGLViewer" "Python"
    ReadRegStr $QTPLUGINS_FOLDER HKLM "Software\PyQGLViewer" "QtPlugins"
    ReadRegStr $PYQGLVIEWER_INSTDIR HKLM "Software\PyQGLViewer" "PyQGLViewer"

    # The modules section.
    Delete  $INSTDIR\Lib\site-packages\PyQGLViewer.pyd
    Delete  $INSTDIR\Lib\site-packages\QGLViewer2.dll
    # The designer plugins
    Delete $QTPLUGINS_FOLDER\plugins\designer\qglviewerplugin.dll
    
    # The Developer section    
    RMDir /r  $INSTDIR\sip\QGLViewer
    RMDir /r  $INSTDIR\include\QGLViewer

    # The shortcuts section.
    RMDir /r "$SMPROGRAMS\${PYQGLVIEWER_NAME}"

    # The examples section and the installer itself.
    RMDir /r "$PYQGLVIEWER_INSTDIR"

    # Clean the registry.
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PyQGLViewer"
    DeleteRegKey HKLM "Software\PyQGLViewer"
SectionEnd
