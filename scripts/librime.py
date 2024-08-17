from common import Builder

Builder('librime', [
    '-DENABLE_THREADING=OFF',
    '-DBUILD_TEST:BOOL=OFF'
]).exec()
