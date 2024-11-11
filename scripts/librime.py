from common import Builder, patch

project = 'librime'

patch(project)

Builder(project, [
    '-DENABLE_THREADING=OFF',
    '-DBUILD_TEST=OFF'
]).exec()
