set OSVERSION=WCE700
set PLATFORM=VC-CE
REM set TARGETCPU=ARMV4I
REM set LIB="C:\Program Files (x86)\Windows CE Tools\SDKs\Stellar_EC7\Lib\ARMv4I";"C:\Program Files (x86)\Microsoft Visual Studio 9.0\VC\ce7\lib\armv4i"
REM set INCLUDE="C:\Program Files (x86)\Windows CE Tools\SDKs\Stellar_EC7\Include\Armv4i";"C:\Program Files (x86)\Microsoft Visual Studio 9.0\VC\ce7\include";
REM set Path="C:\Program Files (x86)\Microsoft Visual Studio 9.0\Common7\IDE";"C:\Program Files (x86)\Microsoft Visual Studio 9.0\VC\ce\bin\x86_arm";%Path%
REM set LIBPATH="C:\Program Files (x86)\Windows CE Tools\SDKs\Stellar_EC7\Lib\ARMv4I";"C:\Program Files (x86)\Microsoft Visual Studio 9.0\VC\ce7\lib\armv4i"


@echo off

rem ------------------------------------------------------------
set TARGETCPU=ARMV4I
set VSINSTALLDIR=c:\Program Files (x86)\Microsoft Visual Studio 9.0
set SDKROOT=c:\Program Files (x86)\Windows CE Tools
set BOOST_WINCEADAPTER_INCL=%SYSTEM1300_ROOT%\3rdParty\boost\boost-WinCEAdapter\include
set BINARY_LIB_PATH=%SYSTEM1300_ROOT%\Binary\VS2008\Output\Stellar_EC7 (ARMV4I)\%1
rem ------------------------------------------------------------

echo Setting target CPU to %TARGETCPU%
echo Setting boost-WinCEAdapter include to %BOOST_WINCEADAPTER_INCL%
echo Setting binary lib path to %BINARY_LIB_PATH%
echo.

rem call "c:\Program Files (x86)\Microsoft Visual Studio 9.0\VC\vcvarsall.bat" x86_arm

rem Note: make sure to prepend the includes to the existing path (otherwise a wrong executable - e.g. link.exe from cygwin - could be used)
set PATH=%VSINSTALLDIR%\VC\ce\bin\x86_arm;%VSINSTALLDIR%\VC\bin;%VSINSTALLDIR%\Common7\IDE;%PATH%
set PLATFORMROOT=%SDKROOT%\SDKs\Stellar_EC7
rem Note order: WinCE\include;SDK\include\targetCpu;SDK\include;WinCE\atlmfc\include (see also http://geekswithblogs.net/WernerWillemsens/archive/2013/09/13/building-windows-ce-6-or-7-smart-device-application-with.aspx)
REM set INCLUDE=%BOOST_WINCEADAPTER_INCL%;%VSINSTALLDIR%\VC\ce7\include;%VSINSTALLDIR%\VC\ce\include;%PLATFORMROOT%\include\%TARGETCPU%;%PLATFORMROOT%\include\;%VSINSTALLDIR%\VC\ce\atlmfc\include;%VSInstallDir%\SmartDevices\SDK\SQL Server\Mobile\v3.0
set INCLUDE=%BOOST_WINCEADAPTER_INCL%;%PLATFORMROOT%\include\%TARGETCPU%;%PLATFORMROOT%\include\;%VSINSTALLDIR%\VC\ce7\include;%VSINSTALLDIR%\VC\ce\include;%VSINSTALLDIR%\VC\ce\atlmfc\include;%VSInstallDir%\SmartDevices\SDK\SQL Server\Mobile\v3.0
set LIB=%BINARY_LIB_PATH%;%PLATFORMROOT%\lib\%TARGETCPU%;%VSINSTALLDIR%\VC\ce\ATLMFC\LIB\%TARGETCPU%;%VSINSTALLDIR%\VC\ce\lib\%TARGETCPU%;%VSINSTALLDIR%\VC\lib
set LIBPATH=%LIB%;%LIBPATH%

echo PATH at %PATH%
echo.

echo INCLUDE is %INCLUDE%
echo.

echo LIB is %LIB%
echo.
