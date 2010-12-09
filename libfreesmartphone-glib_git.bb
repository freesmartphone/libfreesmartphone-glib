DESCRIPTION = "freesmartphone.org API GLib wrapper (auto-generated)"
LICENSE = "LGPL"
SECTION = "devel"
DEPENDS = "dbus-glib fso-specs"
SRCREV = "FIXME"
PV = "0.2+gitr${SRCPV}"
PE = "1"
PR = "r0"

SRC_URI = "${FREESMARTPHONE_GIT}/libfreesmartphone-glib.git;protocol=git;branch=master"
S = "${WORKDIR}/git"

inherit autotools pkgconfig
