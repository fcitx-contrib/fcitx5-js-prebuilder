from common import Builder, patch

project = 'libthai'

patch(project, 'libthai.cmake', 'CMakeLists.txt')
patch(project, 'libthai.pc.in', '.')

Builder(project).exec()
