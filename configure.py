#!/usr/bin/python
#
# Generate the build trees and Makefiles for PyQGLViewer.
# This file is inspired from PyQwt configure.py

import compileall
import glob
import optparse
import os
import pprint
import re
import shutil
import sys
import traceback

# distutils.sysconfig

class Die(Exception):
    def __init__(self, info):
        Exception.__init__(self, info)


try:
    required = 'At least SIP-4.5 and its development tools are required.'
    import sipconfig
except ImportError:
    raise Die, required
if 0x040500 > sipconfig._pkg_config['sip_version']:
    raise Die, required
del required


def get_pyqt_configuration(options):
    """Return the PyQt configuration for Qt4.
    """
    required = 'At least PyQt-4.1 and its development tools are required.'
    try:
        import PyQt4.pyqtconfig as pyqtconfig
    except ImportError:
        raise Die, required
    if 0x040100 > pyqtconfig._pkg_config['pyqt_version']:
        raise Die, required
    try:
        configuration = pyqtconfig.Configuration()
    except AttributeError:
        raise Die, (
            'Check if SIP and PyQt or PyQt4 have been installed properly.'
            )
    return configuration

# get_pyqt_configuration()


def compile_qt_program(name, configuration,
                       extra_defines=[],
                       extra_include_dirs=[],
                       extra_lib_dirs=[],
                       extra_libs=[],
                       verbose = False):
    """Compile a simple Qt application.

    name is the name of the single source file
    configuration is the pyqtconfig.Configuration()
    extra_defines is a list of extra preprocessor definitions
    extra_include_dirs is a list of extra directories to search for headers
    extra_lib_dirs is a list of extra directories to search for libraries
    extra_libs is a list of extra libraries
    """    
    makefile = sipconfig.ProgramMakefile(
        configuration, console=True, qt=['QtCore','QtGui','QtOpenGL','QtXml'], opengl=True, warnings=True)
    
    makefile.extra_defines.extend(extra_defines)
    makefile.extra_include_dirs.extend(extra_include_dirs)
    makefile.extra_lib_dirs.extend(extra_lib_dirs)
    makefile.extra_libs.extend(extra_libs)

    exe, build = makefile.build_command(name)

    # zap a spurious executable
    try:
        os.remove(exe)
    except OSError:
        pass
    
    if verbose:
        print(build)
    os.system(build)

    if not os.access(exe, os.X_OK):
        return None

    if sys.platform != 'win32':
        exe = './' + exe

    return exe

# compile_qt_program()

    
def copy_files(sources, directory):
    """Copy a list of files to a directory
    """ 
    for source in sources:
        shutil.copy2(source, os.path.join(directory, os.path.basename(source)))

# copy_files()


def fix_build_file(name, extra_sources, extra_headers, extra_moc_headers):
    """Extend the targets of a SIP build file with extra files 
    """    
    keys = ('target', 'sources', 'headers', 'moc_headers')
    sbf = {}
    for key in keys:
        sbf[key] = []

    # Parse,
    nr = 0
    for line in open(name, 'r'):
        nr += 1
        if line[0] != '#':
            eq = line.find('=')
            if eq == -1:
                raise Die, ('"%s\" line %d: Line must be in the form '
                            '"key = value value...."' % (name, nr)
                            )
        key = line[:eq].strip()
        value = line[eq+1:].strip()
        if key in keys:
            sbf[key].append(value)

    # extend,
    sbf['sources'].extend(extra_sources)
    sbf['headers'].extend(extra_headers)
    sbf['moc_headers'].extend(extra_moc_headers)

    # and write.
    output = open(name, 'w')
    for key in keys:
        if sbf[key]:
            print >> output, '%s = %s' % (key, ' '.join(sbf[key]))

# fix_build_file()


def fix_typedefs(sources):
    """Work around a code generation bug in SIP-4.5.x
    """
    for source in sources:
        old = open(source).read()
        new = old.replace('"QtCore"', '"PyQt4.QtCore"')
        if new != old:
            open(source, 'w').write(new)

# fix_typedefs()


def lazy_copy_file(source, target):
    """Lazy copy a file to another file:
    - check for a SIP time stamp to skip,
    - check if source and target do really differ,
    - copy the source file to the target if they do,
    - return True on copy and False on no copy.
    """
    if not os.path.exists(target):
        shutil.copy2(source, target)
        return True

    sourcelines = open(source).readlines()
    targetlines = open(target).readlines()

    # global length check
    if len(sourcelines) != len(targetlines):
        shutil.copy2(source, target)
        return True
    
    # skip a SIP time stamp 
    if (len(sourcelines) > 3
        and sourcelines[3].startswith(' * Generated by SIP')
        ):
        line = 4
    else:
        line = 0
        
    # line by line check
    while line < len(sourcelines):
        if sourcelines[line] != targetlines[line]:
            shutil.copy2(source, target)
            return True
        line = line + 1
        
    return False



def check_os(configuration, options):
    """Check operating system specifics.
    """
    print "Found '%s' operating system:" % os.name
    print "Found Python " + sys.version

    if os.name == 'nt':
        options.extra_defines.append('WIN32')

    return options


def check_sip(configuration, options):
    """Check if PyQGLViewer can be built with SIP.
    """
    version = configuration.sip_version
    version_str = configuration.sip_version_str
    
    print "Found SIP-%s." % version_str

    if 0x040500 > version:
        raise Die, 'PyQGLViewer requires at least SIP-4.5.x.'

    if 0x040700 < version or version >= 0x040705 :
        options.excluded_features.append("-x FRIEND_EQUAL_SUPPORT")
    return options



def check_qglviewer(configuration, options):
    pj = os.path.join
    qglviewer_sources = options.qglviewer_sources
    if qglviewer_sources is None or not os.path.exists(qglviewer_sources):
        options.qglviewer_sources = None
        defaultdir = [pj('/','usr','include'),pj('/','usr','local','include'),pj('/','opt','local','include')]
        for ddir in defaultdir:
            if os.path.exists(pj(ddir, "QGLViewer")):
                qglviewer_sources = ddir
                break
        else: qglviewer_sources = defaultdir[0]
    qglviewer_config = os.path.join(qglviewer_sources, "QGLViewer", "config.h")

    QGLVIEWER_VERSION_STR = None
    if os.access(qglviewer_config, os.F_OK):
        # Get the qglviewer version string.
        QGLVIEWER_VERSION, QGLVIEWER_VERSION_STR = sipconfig.read_version(qglviewer_config, "QGLViewer", "QGLVIEWER_VERSION")
    else:
        raise Die, 'Cannot find libQGLViewer headers. Use option -Q for that.'
    
    if QGLVIEWER_VERSION_STR is None:
        QGLVIEWER_VERSION_STR = str((QGLVIEWER_VERSION & 0xff0000) >> 16)+'.'+str((QGLVIEWER_VERSION & 0x00ff00) >> 8)+'.'+str((QGLVIEWER_VERSION  & 0x0000ff))
        
    options.timelines.append('-t QGLViewer_'+QGLVIEWER_VERSION_STR.replace('.','_'))
    if options.qglviewer_sources:
        print ("Found libQGLViewer-%s in '%s'." % (QGLVIEWER_VERSION_STR, options.qglviewer_sources))
    else:
        print ('Found libQGLViewer-%s.' % QGLVIEWER_VERSION_STR)
 
    return options


def setup_qglviewer_build(configuration, options, package):
    """Setup the qglviewer module build
    """
   
    print 'Setup the qglviewer package build.'

    build_dir = 'build'
    tmp_dir = os.path.join('tmp')
    build_file = os.path.join(tmp_dir, 'QGLViewer.sbf' )
    extra_sources = []
    extra_headers = []
    extra_moc_headers = []
    extra_py_files = glob.glob(os.path.join('src', 'python', '*.py'))
               

    # zap the temporary directory
    try:
        shutil.rmtree(tmp_dir)
    except:
        pass
    # make a clean temporary directory
    try:
        os.mkdir(tmp_dir)
    except:
        raise Die, 'Failed to create the temporary build directory.'

    # copy the extra files
    copy_files(extra_sources, tmp_dir)
    copy_files(extra_headers, tmp_dir)
    copy_files(extra_moc_headers, tmp_dir)
    copy_files(extra_py_files, tmp_dir)

    pyqt_sip_flags = configuration.pyqt_sip_flags
        
    # invoke SIP
    cmd = ' '.join(
        [configuration.sip_bin,
         # SIP assumes POSIX style path separators
         '-I', configuration.pyqt_sip_dir.replace('\\', '/'),
         '-b', build_file,
         '-c', tmp_dir,
         #'-m', 'PyQGLViewer.xml', # Forgenerating xml doc tree
         options.jobs,
         options.trace,
         pyqt_sip_flags,
         ]
        + options.sip_include_dirs
        + options.excluded_features
        + options.timelines
        # SIP assumes POSIX style path separators
        + [options.qglviewer_sipfile.replace('\\', '/')]
        )
    
    if options.verbose_config:
        print 'sip invokation:'
        pprint.pprint(cmd)
    if os.path.exists(build_file):
        os.remove(build_file)
    os.system(cmd)
    if not os.path.exists(build_file):
        raise Die, 'SIP failed to generate the C++ code.'

    # fix the SIP build file
    fix_build_file(build_file,
                   [os.path.basename(f) for f in extra_sources],
                   [os.path.basename(f) for f in extra_headers],
                   [os.path.basename(f) for f in extra_moc_headers])
    

    # copy lazily to the build directory to speed up recompilation
    if not os.path.exists(build_dir):
        try:
            os.mkdir(build_dir)
        except:
            raise Die, 'Failed to create the build directory.'

    lazy_copies = 0
    for pattern in ('*.c', '*.cpp', '*.h', '*.py', '*.sbf'):
        for source in glob.glob(os.path.join(tmp_dir, pattern)):
            target = os.path.join(build_dir, os.path.basename(source))
            if lazy_copy_file(source, target):
                if options.verbose_config:
                    print 'Copy %s -> %s.' % (source, target)
                lazy_copies += 1
    print '%s file(s) lazily copied.' % lazy_copies

    # byte-compile the Python files
    compileall.compile_dir(build_dir, 1, options.module_install_path)

    # files to be installed
    installs = []
    installs.append([[os.path.basename(f) for f in glob.glob(
        os.path.join(build_dir, '*.py*'))], options.module_install_path])

    sip_install_dir = os.path.abspath( os.path.join( configuration.pyqt_sip_dir, os.path.pardir, 'QGLViewer'))
    if options.verbose_config:
        print 'Module installation dir will be :',options.module_install_path 
        print 'Sip files installation dir will be :',sip_install_dir
    # creation of 
    #if not os.path.exists(sip_install_dir):
    #    try:
    #        os.mkdir(sip_install_dir)
    #    except:
    #        raise Die, 'Failed to create the sip files repository.'
    pattern = os.path.join('src', 'sip', '*.sip')
    sip_files = glob.glob(pattern)
    sip_files = [ os.path.abspath(i) for i in sip_files ]
    installs.append( [sip_files, sip_install_dir])
        
    
    # module makefile
    makefile = sipconfig.SIPModuleMakefile(
            configuration = configuration,
            build_file = os.path.basename(build_file),
            dir = build_dir,
            install_dir = options.module_install_path,
            installs = installs,
            qt = ['QtOpenGL', 'QtXml', 'QtCore', 'QtGui'],
            warnings = 1,
            debug = options.debug,
            )

    makefile.extra_cflags.extend(options.extra_cflags)
    makefile.extra_cxxflags.extend(options.extra_cxxflags)
    makefile.extra_defines.extend(options.extra_defines)
    makefile.extra_include_dirs.extend(options.extra_include_dirs)
    makefile.extra_lflags.extend(options.extra_lflags)
    makefile.extra_libs.extend(options.extra_libs)
    makefile.extra_lib_dirs.extend(options.extra_lib_dirs)
    makefile.generate()


# setup_QGLViewer5_build()


def setup_parent_build(configuration, options):
    """Generate the parent Makefile
    """
    print "Setup the PyQGLViewer build."
     
    sipconfig.ParentMakefile(configuration = configuration,
                             subdirs = options.subdirs).generate()

# setup_parent_build()


def parse_args():
    """Return the parsed options and args from the command line
    """
    usage = (
        'python configure.py [options]'
        '\n\nEach option takes at most one argument, but some options'
        '\naccumulate arguments when repeated. For example, invoke:'
        '\n\n\tpython configure.py -I %s -I %s'
        '\n\nto search the current *and* parent directories for headers.'
        ) % (os.curdir, os.pardir)

    parser = optparse.OptionParser(usage=usage)

    if sys.platform == 'win32':
        defaultinstallpathes = [ 'C:']
    else:
        defaultinstallpathes = [ '/usr/local/include', '/opt/local/include', '/usr/include']

    for installpath in defaultinstallpathes:
        if os.path.exists(installpath) and os.path.exists(os.path.join(installpath, 'QGLViewer')):
            defaultinstallpath = installpath
            break
    else:
        defaultinstallpath = defaultinstallpathes[-1]

    common_options = optparse.OptionGroup(parser, 'Common options')
    common_options.add_option(
        '-Q', '--qglviewer-sources', default=defaultinstallpath, action='store',
        type='string', metavar='/sources/of/qglviewer',
        help=('link with the QGLViewer source files in'
              ' /sources/of/qglviewer into PyQGLViewer'))
    common_options.add_option(
        '-I', '--extra-include-dirs', default=[], action='append',
        type='string', metavar='/usr/lib/qglviewer/include',
        help=('add an extra directory to search for headers'
              ' (the compiler must be able to find the QGLViewer headers'
              ' without the -Q option)'))
    common_options.add_option(
        '-L', '--extra-lib-dirs', default=[], action='append',
        type='string', metavar='/usr/lib/qglviewer/lib',
        help=('add an extra directory to search for libraries'
              ' (the linker must be able to find the QGLViewer library'
              ' without the -Q option)'))
    common_options.add_option(
        '-j', '--jobs', default=0, action='store',
        type='int', metavar='N',
        help=('concatenate the SIP generated code into N files'
              ' [default 1 per class] (to speed up make by running '
              ' simultaneous jobs on multiprocessor systems)'))
    common_options.add_option(
        '-v','--verbose-config', default=False, action='store_true',
        help=('enable verbose configuration'
              ' [default disabled]'))
    common_options.add_option(
        '-3','--force-import-glteximage3d', default=False, action='store_true',
        help=('force the import of glteximage3d extention'
              ' [default disabled]'))
    parser.add_option_group(common_options)

    make_options = optparse.OptionGroup(parser, 'Make options')
    make_options.add_option(
        '--debug', default=False, action='store_true',
        help='enable debugging symbols [default disabled]')
    make_options.add_option(
        '--extra-cflags', default=[], action='append',
        type='string', metavar='EXTRA_CFLAG',
        help='add an extra C compiler flag')
    make_options.add_option(
        '--extra-cxxflags', default=[], action='append',
        type='string', metavar='EXTRA_CXXFLAG',
        help='add an extra C++ compiler flag')
    make_options.add_option(
        '-D', '--extra-defines', default=[], action='append',
        type='string', metavar='HAS_EXTRA_SENSORY_PERCEPTION',
        help='add an extra preprocessor definition')
    make_options.add_option(
        '-l', '--extra-libs', default=[], action='append',
        type='string', metavar='extra_sensory_perception',
        help='add an extra library')
    make_options.add_option(
        '--extra-lflags', default=[], action='append',
        type='string', metavar='EXTRA_LFLAG',
        help='add an extra linker flag')
    if sys.platform == 'darwin':
        make_options.add_option(
            '-f','--framework', default=[], action='append',
            type='string', metavar='EXTRA_LFLAG',
            help=('enable use of framework. You may specify path to framework'
                  ' [default disabled]'))
    parser.add_option_group(make_options)

    sip_options = optparse.OptionGroup(parser, 'SIP options')
    sip_options.add_option(
        '-x', '--excluded-features', default=[], action='append',
        type='string', metavar='EXTRA_SENSORY_PERCEPTION',
        help=('add a feature for SIP to exclude'
              ' (normally one of the features in sip/features.sip)'))
    sip_options.add_option(
        '-t', '--timelines', default=[], action='append',
        type='string', metavar='EXTRA_SENSORY_PERCEPTION',
        help=('add a timeline option for SIP'
              ' (normally one of the timeline options in sip/timelines.sip)'))
    sip_options.add_option(
        '--sip-include-dirs', default=[],
        action='append', type='string', metavar='SIP_INCLUDE_DIR',
        help='add an extra directory for SIP to search')
    sip_options.add_option(
        '--trace', default=False, action='store_true',
        help=('enable trace of the execution of the bindings'
              ' [default disabled]'))
    parser.add_option_group(sip_options)
    
    install_options = optparse.OptionGroup(parser, 'Install options')
    install_options.add_option(
        '--module-install-path', default='', action='store',
        help= 'specify the install directory for the Python modules'
        )
    parser.add_option_group(install_options)

    options, args =  parser.parse_args()
    
    # tweak some of the options to facilitate later processing
    if options.jobs < 1:
        options.jobs = ''
    else:
        options.jobs = '-j %s' % options.jobs
        
    options.excluded_features = [
        ('-x %s' % f) for f in options.excluded_features
        ]

    # SIP assumes POSIX style path separators
    options.sip_include_dirs = [
        ('-I %s' % f).replace('\\', '/') for f in options.sip_include_dirs
    ]
    
    options.timelines = [
        ('-t %s' % t) for t in options.timelines
        ]

    if options.trace:
        options.trace = '-r'
    else:
        options.trace = ''
     
    if options.force_import_glteximage3d:
        options.extra_defines.extend(['GL_TEXTURE_3D_NO_DEFAULT_DEFINITION'])        
    
    options.subdirs = ['build']
    
    options.qglviewer_sipfile = os.path.join('src','sip','QGLViewerModule.sip')
    
    if sys.platform == 'win32':       
       options.extra_libs.append('QGLViewer2')
       
    elif sys.platform == 'darwin':
        if options.framework:
            if len(options.framework) > 0:
                options.extra_lflags.append('-F'+' -F'.join(options.framework))
                options.extra_include_dirs.extend(list(x+'/QGLViewer.framework/Headers' for x in options.framework))
        if not os.path.exists(options.qglviewer_sources):
            if len(options.framework) > 0:
                options.qglviewer_sources = options.framework[0]+'/QGLViewer.framework/Headers'
                options.extra_lflags.append("-framework QGLViewer")
        else:        
            options.extra_libs.append('QGLViewer')
    else:
       options.extra_libs.append('QGLViewer')

    if options.qglviewer_sources:
        options.qglviewer_sources = os.path.abspath(options.qglviewer_sources)        
        options.extra_include_dirs.append(options.qglviewer_sources)

        qgl_lib_dir = os.path.abspath(os.path.join(options.qglviewer_sources,os.pardir,'lib'))
        if os.path.exists(qgl_lib_dir):
            options.extra_lib_dirs.append(qgl_lib_dir)
        else:
            qgl_lib_dir = os.path.join(options.qglviewer_sources,'QGLViewer')
            if os.path.exists(qgl_lib_dir):
                options.extra_lib_dirs.append(qgl_lib_dir)
        
            if sys.platform == 'win32':       
                qgl_release_lib_dir= os.path.join(qgl_lib_dir,'release')
                options.extra_lib_dirs.append(qgl_release_lib_dir)

        
    return options, args


def main():
    """Generate the build tree and the Makefiles
    """
    options, args = parse_args()

    if options.verbose_config:
        print 'Command line options:'
        pprint.pprint(options.__dict__)
        print

    configuration = get_pyqt_configuration(options)
    
    options = check_sip(configuration, options)
    options = check_os(configuration, options)
    options = check_qglviewer(configuration, options)
    if not options.module_install_path:
        options.module_install_path = os.path.abspath( os.path.join( configuration.pyqt_mod_dir, os.path.pardir))

    if options.verbose_config:
        print
        print 'Extended command line options:'
        pprint.pprint(options.__dict__)
        print
    print
    setup_qglviewer_build(configuration, options, 'PyQGLViewer')
    print
    setup_parent_build(configuration, options)
    print
    print 'Great, run make or nmake to build and install PyQGLViewer.'


if __name__ == '__main__':
    try:
        main()
    except Die, info:
        print info
        sys.exit(1)
    except:
        for entry in traceback.extract_tb(sys.exc_info()[-1]):
            if 'optparse.py' in entry[0]:
                sys.exit(0)
        else:
            print (
                'An internal error occured.  Please report all the output\n'
                'from the program, including the following traceback, to\n'
                'pyqglviewer-users@lists.sourceforge.net'
                )
            traceback.print_exc()
            sys.exit(1)
        
# Local Variables: ***
# mode: python ***
# End: ***
