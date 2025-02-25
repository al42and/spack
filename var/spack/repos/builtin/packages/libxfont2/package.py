# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxfont2(AutotoolsPackage, XorgPackage):
    """libXfont provides the core of the legacy X11 font system, handling the
    index files (fonts.dir, fonts.alias, fonts.scale), the various font file
    formats, and rasterizing them.   It is used by the X servers, the
    X Font Server (xfs), and some font utilities (bdftopcf for instance),
    but should not be used by normal X11 clients.  X11 clients access fonts
    via either the new API's in libXft, or the legacy API's in libX11."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXfont"
    xorg_mirror_path = "lib/libXfont2-2.0.1.tar.gz"

    license("MIT")

    maintainers("wdconinc")

    version("2.0.7", sha256="90b331c2fd2d0420767c4652e007d054c97a3f03a88c55e3b986bd3acfd7e338")
    version("2.0.6", sha256="a944df7b6837c8fa2067f6a5fc25d89b0acc4011cd0bc085106a03557fb502fc")
    version("2.0.1", sha256="381b6b385a69343df48a082523c856aed9042fbbc8ee0a6342fb502e4321230a")

    depends_on("c", type="build")

    depends_on("libfontenc")
    depends_on("freetype")

    depends_on("xtrans")
    depends_on("xproto", type=("build", "link"))
    depends_on("fontsproto@2.1.3:", type=("build", "link"))
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
