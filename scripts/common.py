import os

INSTALL_PREFIX = '/usr'


def ensure(program: str, args: list[str]):
    command = " ".join([program, *args])
    print(command)
    if os.system(command) != 0:
        raise Exception("Command failed")


class Builder:
    def __init__(self, name: str, options: list[str] | None=None):
        self.name = name
        self.root = os.getcwd()
        self.destdir = f'{self.root}/build/{self.name}'
        self.options = options or []

    def configure(self):
        os.chdir(f'{self.root}/{self.name}')
        ensure('emcmake', ['cmake',
            '-B', 'build', '-G', 'Ninja',
            '-DBUILD_SHARED_LIBS=OFF',
            f'-DCMAKE_INSTALL_PREFIX={INSTALL_PREFIX}',
            '-DCMAKE_BUILD_TYPE=Release',
            '-DCMAKE_C_FLAGS=-fPIC',
            '-DCMAKE_CXX_FLAGS=-fPIC',
            *self.options
        ])

    def build(self):
        ensure('cmake', ['--build', 'build'])

    def install(self):
        os.environ['DESTDIR'] = self.destdir
        ensure('cmake', ['--install', 'build'])

    def package(self):
        os.chdir(f'{self.destdir}{INSTALL_PREFIX}')
        ensure('tar', ['cjvf', f'{self.destdir}.tar.bz2', '*'])

    def exec(self):
        self.configure()
        self.build()
        self.install()
        self.package()
