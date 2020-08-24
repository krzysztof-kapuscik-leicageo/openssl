#!/usr/bin/python3.4

# Build OpenSSL 1.0.2 as static library (with dynamic runtime) for Win32 and WinEC7 (Stellar)
# Dependencies:
# - perl
# - VS2008 (C:\Program Files (x86)\Microsoft Visual Studio 9.0)

import getopt, os, re, sys

def PatchMakefileWin32(filename):
    file = open(filename, "r+")
    content = file.read()
    file.seek(0)
    content = re.sub(r'(^CFLAG=.*)/MT ', r'\g<1>/MD ', content, flags=re.MULTILINE)
    file.write(content)
    file.truncate()
    file.close()

def PatchMakefileWinCE(filename, configuration, buildTests):
    file = open(filename, "r+")
    content = file.read()
    file.seek(0)
    content = re.sub(r'(^CFLAG=.*)/MT ', r'\g<1>/MD ', content, flags=re.MULTILINE)
    content = re.sub(r'(^CFLAG=.*)', r'\g<1>-DBUFSIZ=512 /FI "boost-winceadapter_stdlib.h" /FI "boost-winceadapter_errno.h" /FI "boost-winceadapter_time.h" /FI "boost-winceadapter_winbase.h" /FI "boost-winceadapter_string.h"', content, flags=re.MULTILINE)

    if buildTests:
        if configuration == "debug":
            content = re.sub(r'(^EX_LIBS=.*)', r'\g<1> corelibc.lib coredll.lib boost-WinCEAdapterd.lib"', content, flags=re.MULTILINE)
        else:
            content = re.sub(r'(^EX_LIBS=.*)', r'\g<1> corelibc.lib coredll.lib boost-WinCEAdapter.lib"', content, flags=re.MULTILINE)

        content = re.sub(r'(^LFLAGS=.*)', r'\g<1> /ENTRY:mainACRTStartup', content, flags=re.MULTILINE)
        # Remark: AreFileApisANSI always returns true (see boost-winceadapter_winbase.h), hack to make compiler & linker happy. Only used in "apps/s_server.c", we don't need this app anyways.
        content = re.sub(r'(^CFLAG=.*)', r'\g<1> -D_access=access -D_kbhit=AreFileApisANSI', content, flags=re.MULTILINE)

    file.write(content)
    file.truncate()
    file.close()

def HelpOutput():
    return "usage: build.py [-c {debug,release}] [-p {Win32,WinEC7}] [-t]\n\
\t-c ... Configuration (debug or release)\n\
\t-p ... Platform (Win32 or WinEC7)\n\
\t-t ... Build tests"

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hc:p:t")
    except getopt.GetoptError:
        print(HelpOutput())
        sys.exit(2)

    configuration = 'release'
    platform = 'Win32'
    buildTests = False

    for opt, arg in opts:
        if opt == '-h':
            print(HelpOutput())
            sys.exit()
        elif opt == '-c':
            configuration = arg
        elif opt == '-p':
            platform = arg
        elif opt == '-t':
            buildTests = True

    # constants
    pathToScriptFile = sys.path[0]
    pathToDoMs = os.path.join(pathToScriptFile, 'ms', 'do_ms')
    pathToVcvarsall = os.path.abspath("C:/Program Files (x86)/Microsoft Visual Studio 9.0/VC/vcvarsall.bat");
    buildTargets = "init exe" if buildTests else "init lib"

    owd = os.getcwd()
    os.chdir(pathToScriptFile)

    try:
        if platform == 'Win32':
            target = ''
            if configuration == "release":
                target = "VC-WIN32"
            elif configuration == "debug":
                target = "debug-VC-WIN32"
            else:
                print("Invalid configuration")
                print(HelpOutput())
                sys.exit(2)

            pathToMakFile = os.path.join(pathToScriptFile, 'ms', 'nt.mak') # static: nt.mak / dynamic: ntdll.mak

            print("> Configure OpenSSL")
            if os.system("perl.exe Configure no-comp no-idea no-asm no-ssl3 no-zlib no-hw no-md2 no-md4 no-unit-test {}".format(target)) != 0:
                print("Error configuring OpenSSL")
                sys.exit(1)

            print('> Generate build files ("{}")'.format(pathToDoMs))
            if os.system(pathToDoMs) != 0:
                print("Error generating build files")
                sys.exit(1)

            print('> Patch "{}"'.format(pathToMakFile))
            PatchMakefileWin32(pathToMakFile)

            print("> Build OpenSSL")
            if os.system('call "{}" x86 && nmake -f "{}" {}'.format(pathToVcvarsall, pathToMakFile, buildTargets)) != 0:
                print("Error building OpenSSL")
                sys.exit(1)

        elif platform == 'WinEC7':
            target = "VC-CE"

            if configuration == "release":
                pass
            elif configuration == "debug":
                pass
            else:
                print("Invalid configuration")
                print(HelpOutput())
                sys.exit(2)

            pathToMakFile = os.path.join(pathToScriptFile, 'ms', 'ce.mak') # static: ce.mak / dynamic: cedll.mak
            pathToSetEnvVariables = os.path.join(pathToScriptFile, 'WinEC7_SetEnvVariables.bat')

            print("> Configure OpenSSL")
            if os.system('perl.exe Configure -wd4005 -wd4022 -wd4047 -wd4748 -wd4996 no-comp no-idea no-asm no-ssl3 no-zlib no-hw no-md2 no-md4 no-unit-test {}'.format(target)) != 0:
                print("Error configuring OpenSSL")
                sys.exit(1)

            print('> Generate build files ("{}")'.format(pathToDoMs))
            if os.system('{} {} && {}'.format(pathToSetEnvVariables, configuration, pathToDoMs)) != 0:
                print("Error generating build files")
                sys.exit(1)

            print('> Patch "{}"'.format(pathToMakFile))
            PatchMakefileWinCE(pathToMakFile, configuration, buildTests)

            print("> Build OpenSSL")
            if os.system('call "{}" x86 && {} {} && nmake -f "{}" {}'.format(pathToVcvarsall, pathToSetEnvVariables, configuration, pathToMakFile, buildTargets)) != 0:
                print("Error building OpenSSL")
                sys.exit(1)

            print('> To run the tests copy the folders "out32_ARMV4I", "apps" and "test" to "/SD Card/OpenSSL".')

        else:
            print("Invalid platform")
            print(HelpOutput())
            sys.exit(2)

    except Exception as e:
        print("Error: {}".format(repr(e)))
    finally:
        os.chdir(owd)

if __name__ == "__main__":
    main(sys.argv[1:])