from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.build import check_min_cppstd, can_run


class kdlRecipe(ConanFile):
    name = "orocos-kdl"
    version = "1.5.2"
    package_type = "library"

    license = "LGPL-2.1-or-later"
    author = "orocos ()"
    url = "https://github.com/orocos/orocos_kinematics_dynamics/tree/master"
    description = "Orocos Kinematics and Dynamics C++ library"
    topics = ("motion", "kinamatics", "dynamics")

    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {"shared": True, "fPIC": True}

    exports_sources = (
        "CMakeLists.txt",
        "*.in",
        "cmake/*",
        "src/*",
        "tests/*",
    )

    def _bypass_test(self):
        if (
            self.settings.get_safe("compiler") == "msvc"
            and self.settings.get_safe("build_type") == "Debug"
        ):
            """
            cppunit fail building under above condition
            """
            return True
        return False

    def requirements(self):
        self.requires("eigen/[~3]")
        self.tool_requires("cmake/[>=3.12 <5]")
        if not self._bypass_test():
            self.test_requires("cppunit/[>=1.14.0 <2]")

    def validate(self):
        check_min_cppstd(self, "14")

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)

        if not self.conf.get("tools.build:skip_test", default=False) and not self._bypass_test():
            tc.variables["ENABLE_TESTS"] = True
        else:
            tc.variables["ENABLE_TESTS"] = False

        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["orocos-kdl"]  # orocos-kdl-models
