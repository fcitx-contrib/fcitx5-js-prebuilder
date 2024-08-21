import os
from common import Builder, cache, ensure, patch

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

prebuilt = 'libime-arm64.tar.bz2'
url = f'https://github.com/fcitx-contrib/fcitx5-macos-prebuilder/releases/download/latest/{prebuilt}'

cache(url)
directory = 'build/libime/usr'
ensure('mkdir', ['-p', directory])
ensure('tar', [
    'xjvf',
    f'cache/{prebuilt}',
    '-C',
    directory,
    'lib/libime',
    'share'
])

project = 'libime'

patch(project)

Builder(project, [
    '-DENABLE_TEST=OFF',
    '-DENABLE_DATA=OFF'
]).exec()
