# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fiat(CMakePackage):
    """FIAT (Fortran IFS and Arpege Toolkit) is a collection of selected
    Fortran utility libraries, extracted from the IFS/Arpege model."""

    homepage = "https://github.com/ecmwf-ifs/fiat"
    git = "https://github.com/ecmwf-ifs/fiat.git"
    url = "https://github.com/ecmwf-ifs/fiat/archive/1.0.0.tar.gz"

    maintainers("climbfuji")

    license("Apache-2.0")

    version("main", branch="main", no_cache=True)
    version("1.4.1", sha256="7d49316150e59afabd853df0066b457a268731633898ab51f6f244569679c84a")
    version("1.4.0", sha256="5dc5a8bcac5463690529d0d96d2c805cf9c0214d125cd483ee69d36995ff15d3")
    version("1.2.0", sha256="758147410a4a3c493290b87443b4091660b915fcf29f7c4d565c5168ac67745f")
    version("1.1.0", sha256="58354e60d29a1b710bfcea9b87a72c0d89c39182cb2c9523ead76a142c695f82")
    version("1.0.0", sha256="45afe86117142831fdd61771cf59f31131f2b97f52a2bd04ac5eae9b2ab746b8")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant(
        "build_type",
        default="RelWithDebInfo",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo"),
    )

    variant("mpi", default=True, description="Use MPI")
    variant("openmp", default=True, description="Use OpenMP")
    variant("fckit", default=True, description="Use fckit")

    depends_on("ecbuild", type=("build"))
    depends_on("mpi", when="+mpi")
    depends_on("eckit", when="+fckit")
    depends_on("fckit", when="+fckit")

    patch("intel_warnings_v110.patch", when="@:1.1.0")
    patch("intel_warnings_v120.patch", when="@1.2.0:")

    def cmake_args(self):
        args = [
            self.define_from_variant("ENABLE_OMP", "openmp"),
            self.define_from_variant("ENABLE_MPI", "mpi"),
            self.define_from_variant("ENABLE_FCKIT", "fckit"),
        ]

        return args
