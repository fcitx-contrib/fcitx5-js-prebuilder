import os

INSTALL_PREFIX = '/usr'


def ensure(program: str, args: list[str]):
    command = " ".join([program, *args])
    print(command)
    if os.system(command) != 0:
        raise Exception("Command failed")


def patch(project: str, src: str | None = None, dst: str | None = None):
    if src and dst:
        ensure('cp', [
            f'patches/{src}',
            f'{project}/{dst}'
        ])
    else:
        ensure('git', [
            'apply',
            f'--directory={project}',
            f'patches/{project}.patch'
        ])


def cache(url: str):
    file = url[url.rindex('/') + 1:]
    path = f'cache/{file}'
    if os.path.isfile(path):
        print(f'Using cached {file}')
        return
    ensure('wget', [
        '-P',
        'cache',
        url
    ])

class Builder:
    def __init__(self, name: str, options: list[str] | None=None, src='.', build='build', dep=False):
        self.name = name
        self.root = os.getcwd()
        self.destdir = f'{self.root}/build/{self.name}'
        self.options = options or []
        self.src = src
        self.build_ = build
        self.dep = dep

    def configure(self):
        os.environ['PKG_CONFIG_PATH'] = f'{self.root}/build/sysroot/usr/lib/pkgconfig'
        os.chdir(f'{self.root}/{self.name}')
        ensure('emcmake', ['cmake',
            '-B', self.build_, '-G', 'Ninja',
            '-S', self.src,
            '-DBUILD_SHARED_LIBS=OFF',
            f'-DCMAKE_INSTALL_PREFIX={INSTALL_PREFIX}',
            f'-DCMAKE_FIND_ROOT_PATH={self.root}/build/sysroot/usr',
            '-DCMAKE_BUILD_TYPE=Release',
            '-DCMAKE_C_FLAGS=-fPIC',
            '-DCMAKE_CXX_FLAGS=-fPIC',
            *self.options
        ])

    def build(self):
        ensure('cmake', ['--build', self.build_])

    def install(self):
        os.environ['DESTDIR'] = self.destdir
        ensure('cmake', ['--install', self.build_])

    def package(self):
        os.chdir(f'{self.destdir}{INSTALL_PREFIX}')
        ensure('tar', ['cjvf', f'{self.destdir}.tar.bz2', '*'])

    def extract(self):
        directory = 'build/sysroot/usr'
        os.chdir(self.root)
        ensure('mkdir', ['-p', directory])
        ensure('tar', ['xjvf', f'{self.destdir}.tar.bz2', '-C', directory])

    def exec(self):
        self.configure()
        self.build()
        self.install()
        self.package()
        if self.dep:
            self.extract()


class MesonBuilder(Builder):
    def configure(self):
        os.chdir(f'{self.root}/{self.name}')
        ensure('meson', [
            'setup',
            'build',
            '--cross-file=../scripts/meson-cross.ini',
            '--buildtype=release',
            '--prefix=/usr',
            '--default-library=static',
            *self.options
        ])

    def build(self):
        ensure('ninja', ['-C', 'build', 'clean'])
        ensure('ninja', ['-C', 'build'])

    def install(self):
        os.environ['DESTDIR'] = self.destdir
        ensure('ninja', ['-C', 'build', 'install'])


class MakeBuilder(Builder):
    def configure(self):
        os.chdir(f'{self.root}/{self.name}')
        ensure('./configure', [
            '-C',
            '--prefix=/usr',
            *self.options
        ])

    def build(self):
        ensure('make', ['-j8'])

    def install(self):
        os.environ['DESTDIR'] = self.destdir
        ensure('make', ['install'])
 