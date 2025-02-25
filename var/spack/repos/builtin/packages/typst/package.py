# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Typst(CargoPackage):
    """Typst is a new markup-based typesetting system for the sciences."""

    homepage = "https://typst.app"
    git = "https://github.com/typst/typst"
    executables = ["^typst$"]

    maintainers("upsj")

    license("Apache-2.0", checked_by="upsj")

    version("0.13.0", commit="8dce676dcd691f75696719e0480cd619829846a9", tag="v0.13.0")
    version("0.12.0", commit="737895d769188f6fc154523e67a9102bc24c872e", tag="v0.12.0")

    depends_on("rust@1.80:", type="build")
    depends_on("openssl")
    depends_on("pkgconfig", type="build")

    build_directory = "crates/typst-cli"

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"typst ([0-9.]+)", output)
        return match.group(1) if match else None
