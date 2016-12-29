Branch of FFmpeg that supports building with clang-cl
=====================================================

Dependencies
============

Cygwin environment including python, yasm, yasm-devel, make

I'm using clang-cl from LLVM developer snapshots here: http://llvm.org/builds/ (have been using the 64bit builds)

As per the clang-cl documentation you need to use vscarsall.bat to set up your environment. I use a script like this to run the cygwin terminal:

```bash
@echo off

echo "Loading Visual Studio environment..."
call "C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\vcvarsall.bat" x64

echo "Starting mintty..."
start C:\cygwin64\bin\mintty.exe -i /Cygwin-Terminal.ico -
```

An annoying problem I hit was that clang-cl.exe also handles running link.exe but doesn't forward .o files to the linker if they come after a /link option, and on the other hand doesn't forward .lib files to the linker if they come before. I wrote this wrapper linker script, named link.py at the root of the source directory:

```
#!/usr/bin/env python
import sys
from subprocess import call

libs = []
final_args = [ 'clang-cl.exe' ]

for arg in sys.argv[1:]:
    if arg.endswith(('.lib')):
        libs.append(arg)
    else:
        final_args.append(arg)

if len(libs) > 0:
    final_args.append("-link")
    for lib in libs:
        final_args.append(lib)

ret = call(final_args)
sys.exit(ret)
```

To build ffplay with SDL I downloaded SDL devel binaries from here: https://www.libsdl.org/download-1.2.php (note 1x not 2x)
I hacked an sdl-config script at the root of the ffmpeg source directory:

```
#!/bin/sh

if test "$1" = "--libs"; then
    echo "-L../SDL/lib/x64 -lSDL"
elif test "$1" = "--cflags"; then
    echo "-I../SDL/include"
fi
```
*Note may need to run dos2unix to keep cygwin/bash happy*

Building
========

The ffmpeg source directory needs to be added to your PATH so that the link.py and sdl-config scripts will be found.

`./configure --prefix=/cygdrive/c/Users/Robert/local/ffmpeg-cl --toolchain=msvc --cc=clang-cl.exe --ld=link.py --ar=llvm-lib --enable-sdl --enable-shared`

Notes about ./configure script changes
======================================

clang-cl doesn't handle all the #pragmas of msvc for intrinsics and so the script makes sure to add `-D__BMI__ -FIintrin.h` to the build cflags.

The way the script would recognise the MSVC cl.exe compiler didn't Just Work™ to recognise clang-cl.exe so the script needed another section to recognise and init common variables similar to how it would for msvc (but different enough to warrent a separate section).
