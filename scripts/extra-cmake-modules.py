from common import Builder

Builder('extra-cmake-modules', [
    '-DBUILD_TESTING=OFF'
], dep=True).exec()
