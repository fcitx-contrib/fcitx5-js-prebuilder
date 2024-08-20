from common import Builder

Builder('json-c', [
    '-DBUILD_TESTING=OFF',
    '-DBUILD_APPS=OFF',
    '-DDISABLE_EXTRA_LIBS=ON'
]).exec()
