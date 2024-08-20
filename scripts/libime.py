import os
from common import Builder, ensure, patch

root = os.getcwd()

ensure('sed', [
    '-i',
    f'"s|\\"/usr/include|\\"{root}/build/sysroot/usr/include|g"',
    '$(find build/sysroot/usr -name "*.cmake")'
])

ensure('sed', [
    '-i',
    f'"s|prefix=/usr|prefix={root}/build/sysroot/usr|g"',
    'build/sysroot/usr/lib/pkgconfig/libzstd.pc'
])

project = 'libime'

patch(project)

Builder(project, [
    '-DENABLE_TEST=OFF',
    '-DENABLE_DATA=OFF'
]).exec()
