from common import Builder

Builder('json-c', [
    '-DDISABLE_EXTRA_LIBS=ON'
]).exec()
