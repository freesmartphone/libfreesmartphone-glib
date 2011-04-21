AC_INIT([libfreesmartphone-glib], [2011.04.15.1], [daniele.athome@gmail.com], [libfreesmartphone-glib])
AC_CONFIG_SRCDIR(Makefile.am)
AC_CONFIG_HEADERS(config.h)
AC_CONFIG_MACRO_DIR([m4])

AM_INIT_AUTOMAKE

AC_DISABLE_STATIC
AC_PROG_LIBTOOL
AC_SUBST(ACLOCAL_AMFLAGS, "$ACLOCAL_FLAGS -I m4")
AC_PROG_CC

AC_STDC_HEADERS
AC_LIBTOOL_DLOPEN

# glib-genmarshal
AC_PATH_PROG(GLIB_GENMARSHAL, glib-genmarshal)

GLIB_REQUIRED=2.12.0
DBUS_REQUIRED=0.70
SPECS_REQUIRED=$PACKAGE_VERSION

# glib/dbus
PKG_CHECK_MODULES(DEPS,
    glib-2.0 >= $GLIB_REQUIRED
    gobject-2.0 >= $GLIB_REQUIRED
    dbus-glib-1 >= $DBUS_REQUIRED
    dbus-1 >= $DBUS_REQUIRED)

# fso specs
PKG_CHECK_MODULES(SPECS,
    fso-specs >= $SPECS_REQUIRED)

# specs directory
FSO_SPECS_DIR="`$PKG_CONFIG --variable=specsdir fso-specs`"
AC_SUBST(FSO_SPECS_DIR)

AC_SUBST(DBUS_CFLAGS)
AC_SUBST(DBUS_LIBS)

# output files
AC_OUTPUT([
Makefile
src/Makefile
src/ogsmd/Makefile
src/ousaged/Makefile
src/opimd/Makefile
src/odeviced/Makefile
src/gypsy/Makefile
libfreesmartphone-glib.pc
])
