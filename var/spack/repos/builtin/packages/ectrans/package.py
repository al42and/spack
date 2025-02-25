# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ectrans(CMakePackage):
    """Ectrans is the global spherical Harmonics transforms library,
    extracted from the IFS. It is using a hybrid of MPI and OpenMP
    parallelisation strategies. The package contains both single- and double precision
    Fortran libraries (trans_sp, trans_dp), as well as a
    C interface to the double-precision version (transi_dp)."""

    homepage = "https://github.com/ecmwf-ifs/ectrans"
    git = "https://github.com/ecmwf-ifs/ectrans.git"
    url = "https://github.com/ecmwf-ifs/ectrans/archive/1.1.0.tar.gz"

    maintainers("climbfuji")

    license("Apache-2.0")

    version("develop", branch="develop", no_cache=True)
    version("main", branch="main", no_cache=True)
    version("1.5.0", sha256="8b2b24d1988b92dc3793b29142946614fca9e9c70163ee207d2a123494430fde")
    version("1.4.0", sha256="1364827511a2eb11716aaee85062c3ab0e6b5d5dca7a7b9c364e1c43482b8691")
    version("1.2.0", sha256="2ee6dccc8bbfcc23faada1d957d141f24e41bb077c1821a7bc2b812148dd336c")
    version("1.1.0", sha256="3c9848bb65033fbe6d791084ee347b3adf71d5dfe6d3c11385000017b6469a3e")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant(
        "build_type",
        default="RelWithDebInfo",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo"),
    )

    variant("mpi", default=True, description="Use MPI")
    variant("openmp", default=True, description="Use OpenMP")

    variant("double_precision", default=True, description="Support for double precision")
    variant("single_precision", default=True, description="Support for single precision")

    variant("mkl", default=False, description="Use MKL")
    variant("fftw", default=True, description="Use FFTW")

    variant("transi", default=True, description="Compile TransI C-interface to trans")

    depends_on("ecbuild", type="build")
    depends_on("mpi", when="+mpi")
    depends_on("blas")
    depends_on("lapack")
    depends_on("fftw-api", when="+fftw")
    depends_on("mkl", when="+mkl")

    depends_on("fiat~mpi", when="~mpi")
    depends_on("fiat+mpi", when="+mpi")

    # https://github.com/ecmwf-ifs/ectrans/issues/194
    patch(
        "https://github.com/ecmwf-ifs/ectrans/commit/98f0d505d5b0866cab68a15e86e1a495bafd93d2.patch?full_index=1",
        sha256="17999486a320a5c6a1a442adcdf2c341b49d005f45d09ad0e525594d50bdc39c",
        when="@1.3.1:1.5.1",
    )

    def cmake_args(self):
        args = [
            self.define_from_variant("ENABLE_MPI", "mpi"),
            self.define_from_variant("ENABLE_OMP", "openmp"),
            self.define_from_variant("ENABLE_DOUBLE_PRECISION", "double_precision"),
            self.define_from_variant("ENABLE_SINGLE_PRECISION", "single_precision"),
            self.define_from_variant("ENABLE_FFTW", "fftw"),
            self.define_from_variant("ENABLE_MKL", "mkl"),
            self.define_from_variant("ENABLE_TRANSI", "transi"),
            # Turn off use of contiguous keyword in Fortran because a number
            # of compilers have issues with it, and the hardcoded list of "bad"
            # compilers in ectrans is incomplete and isn't kept up to date
            # https://github.com/JCSDA/spack-stack/issues/1522
            "-DECTRANS_HAVE_CONTIGUOUS_ISSUE=ON",
        ]
        return args
