from common import Builder

Builder('libexpat', [
    '-DEXPAT_BUILD_TOOLS=OFF',
    '-DEXPAT_BUILD_EXAMPLES=OFF',
    '-DEXPAT_BUILD_TESTS=OFF'
], src='expat').exec()
