# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Survey(CMakePackage):
    """Survey is a high level performance tool product from Trenza, Inc.
    The survey collector/analytics framework is a new generation,
    high level, lightweight multiplatform Linux tool set that
    targets metric collection for high level performance analysis
    of applications running on both single node and on large scale
    platforms, including the Cray platforms.

    The collector is designed to work on sequential, MPI, OpenMP,
    and hybrid codes and directly leverages several interfaces
    available for tools inside current MPI implementations including:
    MPICH, MVAPICH, MPT, and OpenMPI. It also supports multiple
    architectures and has been tested on machines based on Intel,
    AMD, ARM, and IBM P8/9 processors and integrated AMD and NVIDIA GPUs.

    Survey is a licensed product with the source not openly available.
    To access the survey source and build with spack please contact:
    Trenza Inc. via: dmont@trenzasynergy.com or
                     jeg@trenzasynergy.com
    """

    homepage = "https://www.trenzasynergy.com"
    git = "ssh://git@gitlab.com/trenza/survey.git"

    maintainers("jgalarowicz")

    version("1.1.1", branch="1.1.1")
    version("1.1.0", tag="1.1.0")
    version("1.0.9", tag="1.0.9")
    version("1.0.8.1", branch="1.0.8.1")
    version("1.0.8", tag="1.0.8")
    version("1.0.7", tag="1.0.7")
    version("1.0.6", tag="1.0.6")
    version("1.0.5", tag="1.0.5")
    version("1.0.4", tag="1.0.4")
    version("1.0.3", tag="1.0.3")
    version("1.0.2", tag="1.0.2")
    version("1.0.1.1", tag="1.0.1.1")
    version("1.0.1", tag="1.0.1")
    version("1.0.0", branch="1.0.0")

    variant("mpi", default=False, description="Enable mpi, build MPI data collector")
    variant("debug", default=False, description="Build a debug survey version")

    variant(
        "tls_model",
        default="explicit",
        description="The TLS model to build with",
        values=("implicit", "explicit"),
    )

    # must have cmake at 3.12 or greater to find python3
    depends_on("cmake@3.12:", type="build")

    # for collectors
    depends_on("libmonitor@2021.11.08+commrank", type=("build", "link", "run"), when="@:1.0.9")
    depends_on("libmonitor@2023.03.15+commrank", type=("build", "link", "run"), when="@1.1.0:")

    depends_on("papi@5:", type=("build", "link", "run"))
    depends_on("gotcha@master", type=("build", "link"), when="@:1.0.7")
    depends_on("gotcha@1.0.4", type=("build", "link"), when="@1.0.8:")
    depends_on("llvm-openmp@9.0.0", type=("build", "link"), when="@:1.0.3")
    depends_on("llvm-openmp@12.0.1+multicompat", type=("build", "link"), when="@1.0.4:")

    # MPI Installation
    depends_on("mpi", type="build", when="+mpi")

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pip", type="build")
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-sqlalchemy", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-seaborn", type=("build", "run"), when="@1.0.3:")
    depends_on("py-jinja2", type=("build", "run"), when="@1.0.3:")
    depends_on("py-matplotlib", type=("build", "run"), when="@1.0.3:")
    depends_on("py-more-itertools", type=("build", "run"), when="@1.0.4:")
    depends_on("py-versioneer", type=("build", "run"), when="@1.0.5:")
    depends_on("py-filelock", type=("build", "run"), when="@1.0.7:")
    depends_on("py-zipp", type=("build", "run"), when="@1.0.7:")
    depends_on("py-humanize", type=("build", "run"), when="@1.0.8:")
    depends_on("py-importlib-resources", type=("build", "run"), when="@1.0.8:")
    depends_on("py-gitpython", type=("build", "run"), when="@1.0.9:")
    depends_on("py-smmap", type=("build", "run"), when="@1.0.9:")
    depends_on("py-gitdb", type=("build", "run"), when="@1.0.9:")
    depends_on("py-pyparsing", type=("build", "run"), when="@1.0.9:")
    depends_on("py-markupsafe", type=("build", "run"), when="@1.0.9:")
    depends_on("py-packaging", type=("build", "run"), when="@1.0.9:")
    depends_on("py-pillow", type=("build", "run"), when="@1.0.9:")
    depends_on("py-cycler", type=("build", "run"), when="@1.0.9:")
    depends_on("py-kiwisolver", type=("build", "run"), when="@1.0.9:")

    extends("python")

    parallel = False

    def get_mpi_cmake_options(self, spec):
        # Returns MPI cmake_options that will enable the appropriate
        # MPI implementation is specified as a cmake argument.
        mpi_args = ["-D%s_DIR=%s" % (spec["mpi"].name.upper(), spec["mpi"].prefix)]
        return mpi_args

    def cmake_args(self):
        spec = self.spec

        if "tls_model=implicit" in spec:
            spack_tls_model = "implicit"
        else:
            spack_tls_model = "explicit"

        # Add in paths for finding package config files that tell us
        # where to find these packages
        cmake_args = [
            "-DCMAKE_VERBOSE_MAKEFILE=ON",
            "-DTLS_MODEL=%s" % spack_tls_model,
            "-DLIBMONITOR_DIR=%s" % spec["libmonitor"].prefix,
            "-DPAPI_DIR=%s" % spec["papi"].prefix,
            "-DLIBIOMP_DIR=%s" % spec["llvm-openmp"].prefix,
            "-DPYTHON_DIR=%s" % spec["python"].prefix,
            "-DGOTCHA_DIR=%s" % spec["gotcha"].prefix,
        ]

        # Add any MPI implementations coming from variant settings
        if "+mpi" in spec:
            mpi_options = self.get_mpi_cmake_options(spec)
            cmake_args.extend(mpi_options)

        if "+debug" in spec:
            cmake_args.append("-DCMAKE_C_FLAGS=-g -O2")
            cmake_args.append("-DCMAKE_CXX_FLAGS=-g -O2")
            cmake_args.append("-DCMAKE_BUILD_TYPE=Custom")

        return cmake_args

    @property
    def python_lib_dir(self):
        python_vers_phrase = "python{0}".format(self.spec["python"].version.up_to(2))
        return join_path("lib", python_vers_phrase)

    @property
    def site_packages_dir(self):
        return join_path(self.python_lib_dir, "site-packages")

    def setup_run_environment(self, env):
        """Set up the compile and runtime environments for a package."""

        # Set SURVEY_MPI_IMPLEMENTATON to the appropriate mpi implementation
        # This is needed by survey to deploy the correct mpi runtimes.
        if "+mpi" in self.spec:
            env.set("SURVEY_MPI_IMPLEMENTATION", self.spec["mpi"].name.lower())

        # For compatibility reasons we need
        env.prepend_path("PATH", self.spec["python"].prefix.bin)
        # Add paths for sub-tools that are used by survey
        env.prepend_path("PATH", self.spec["papi"].prefix.bin)
        env.prepend_path("PATH", self.spec["libmonitor"].prefix.bin)

        env.prepend_path(
            "PYTHONPATH", join_path(self.spec["python"].prefix, self.site_packages_dir)
        )
        env.prepend_path(
            "PYTHONPATH", join_path(self.spec["py-pandas"].prefix, self.site_packages_dir)
        )
        env.prepend_path(
            "PYTHONPATH", join_path(self.spec["py-python-dateutil"].prefix, self.site_packages_dir)
        )
        env.prepend_path(
            "PYTHONPATH", join_path(self.spec["py-setuptools"].prefix, self.site_packages_dir)
        )
        env.prepend_path(
            "PYTHONPATH", join_path(self.spec["py-numpy"].prefix, self.site_packages_dir)
        )
        env.prepend_path(
            "PYTHONPATH", join_path(self.spec["py-pytz"].prefix, self.site_packages_dir)
        )
        env.prepend_path(
            "PYTHONPATH", join_path(self.spec["py-six"].prefix, self.site_packages_dir)
        )
        env.prepend_path(
            "PYTHONPATH", join_path(self.spec["py-psutil"].prefix, self.site_packages_dir)
        )
        env.prepend_path(
            "PYTHONPATH", join_path(self.spec["py-sqlalchemy"].prefix, self.site_packages_dir)
        )
        env.prepend_path(
            "PYTHONPATH", join_path(self.spec["py-pyyaml"].prefix, self.site_packages_dir)
        )
        env.prepend_path(
            "PYTHONPATH", join_path(self.spec["py-matplotlib"].prefix, self.site_packages_dir)
        )
        env.prepend_path(
            "PYTHONPATH", join_path(self.spec["py-filelock"].prefix, self.site_packages_dir)
        )
        env.prepend_path(
            "PYTHONPATH", join_path(self.spec["py-humanize"].prefix, self.site_packages_dir)
        )
        env.prepend_path(
            "PYTHONPATH",
            join_path(self.spec["py-importlib-resources"].prefix, self.site_packages_dir),
        )
        env.prepend_path(
            "PYTHONPATH", join_path(self.spec["py-pip"].prefix, self.site_packages_dir)
        )
        env.prepend_path(
            "PYTHONPATH", join_path(self.spec["py-seaborn"].prefix, self.site_packages_dir)
        )
        env.prepend_path(
            "PYTHONPATH", join_path(self.spec["py-jinja2"].prefix, self.site_packages_dir)
        )
        env.prepend_path(
            "PYTHONPATH", join_path(self.spec["py-more-itertools"].prefix, self.site_packages_dir)
        )
        env.prepend_path(
            "PYTHONPATH", join_path(self.spec["py-versioneer"].prefix, self.site_packages_dir)
        )
        env.prepend_path(
            "PYTHONPATH", join_path(self.spec["py-zipp"].prefix, self.site_packages_dir)
        )
        env.prepend_path(
            "PYTHONPATH", join_path(self.spec["py-gitpython"].prefix, self.site_packages_dir)
        )
        env.prepend_path(
            "PYTHONPATH", join_path(self.spec["py-smmap"].prefix, self.site_packages_dir)
        )
        env.prepend_path(
            "PYTHONPATH", join_path(self.spec["py-gitdb"].prefix, self.site_packages_dir)
        )
        env.prepend_path(
            "PYTHONPATH", join_path(self.spec["py-pyparsing"].prefix, self.site_packages_dir)
        )
        env.prepend_path(
            "PYTHONPATH", join_path(self.spec["py-markupsafe"].prefix, self.site_packages_dir)
        )
        env.prepend_path(
            "PYTHONPATH", join_path(self.spec["py-packaging"].prefix, self.site_packages_dir)
        )
        env.prepend_path(
            "PYTHONPATH", join_path(self.spec["py-pillow"].prefix, self.site_packages_dir)
        )
        env.prepend_path(
            "PYTHONPATH", join_path(self.spec["py-cycler"].prefix, self.site_packages_dir)
        )
        env.prepend_path(
            "PYTHONPATH", join_path(self.spec["py-kiwisolver"].prefix, self.site_packages_dir)
        )
