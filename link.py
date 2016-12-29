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

