from pythonforandroid.toolchain import Recipe, shprint, current_directory
from os.path import exists, join
import sh


class C_iGraphRecipe(Recipe):
    # This could also inherit from PythonRecipe etc. if you want to
    # use their pre-written build processes

    version = '0.7.1'
    url = 'http://igraph.org/nightly/get/c/igraph-0.7.1.tar.gz'
    dir_name = 'c_igraph'
    depends = []
    patches = ['sysdep1.h.patch', 'uninit.c.patch']

    def should_build(self, arch):
        # Add a check for whether the recipe is already built if you
        # want, and return False if it is.
        return not exists(join(self.get_build_dir(arch.arch), '.built'))

    def prebuild_arch(self, arch):
        super(C_iGraphRecipe, self).prebuild_arch(arch)
        sh.cp('-f', join(self.get_recipe_dir(), 'arith.h'), join(self.get_build_dir(arch.arch), 'src', 'f2c', 'arith.h'))

    def get_recipe_env(self, arch):
        env = super(C_iGraphRecipe, self).get_recipe_env(arch)
        env['CPPFLAGS'] = env.get('CPPFLAGS', '') + ' -I{ndk}/sources/cxx-stl/gnu-libstdc++/4.4.3/include -I{ndk}/sources/cxx-stl/gnu-libstdc++/4.4.3/libs/armeabi/include -L{ndk}/platforms/android-$ANDROIDAPI/arch-arm/usr/lib'.format(ndk=self.ctx.ndk_dir)
        return env

    def build_arch(self, arch):
        super(C_iGraphRecipe, self).build_arch(arch)
        jobs = self.get_recipe_env(arch).get('MAKE_JOBS', 1)
        with current_directory(self.get_build_dir(arch.arch)):
            shprint(sh.bash, './configure', '--prefix={}/python-install'.format(self.get_build_container_dir(arch.arch)), '--host=arm-linux-eabi')
            shprint(sh.make, '-j{}'.format(jobs))
            shprint(sh.make, '-j{}'.format(jobs), 'install')

    def postbuild_arch(self, arch):
        super(C_iGraphRecipe, self).postbuild_arch(arch)
        sh.touch(join(self.get_build_dir(arch.arch), '.built'))


recipe = C_iGraphRecipe()
