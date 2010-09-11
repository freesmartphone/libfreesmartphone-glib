AC_INIT([libfreesmartphone-glib], [0.2], [daniele.athome@gmail.com], [libfreesmartphone-glib])
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

dnl glib-genmarshal
AC_PATH_PROG(GLIB_GENMARSHAL, glib-genmarshal)

# base deps
PKG_CHECK_MODULES(DBUS, dbus-glib-1)

AC_SUBST(DBUS_CFLAGS)
AC_SUBST(DBUS_LIBS)

# output files
AC_OUTPUT([
Makefile
src/Makefile
src/ogsmd/Makefile
src/ousaged/Makefile
libfreesmartphone-glib.pc
])
