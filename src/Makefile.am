SUBDIRS = ogsmd ousaged opimd odeviced gypsy

dbus_archives = \
	ogsmd/libogsmd.la \
	ousaged/libousaged.la \
	opimd/libopimd.la \
	odeviced/libodeviced.la \
	gypsy/libgypsy.la

AM_CPPFLAGS = -DDATADIR=\"$(datadir)\" \
	      -DPKGDATADIR=\"$(pkgdatadir)\" \
	      -DG_LOG_DOMAIN=\"libfreesmartphone-glib\"

AM_CFLAGS = -Wall -Wextra -Werror @DEPS_CFLAGS@
AM_LDFLAGS = @DEPS_LIBS@

xmldir = @FSO_SPECS_DIR@
cfgdir = $(top_srcdir)/cfg

lib_LTLIBRARIES = libfreesmartphone-glib.la

libfreesmartphone_glib_la_LDFLAGS = $(all_libraries) -version-info 1:0:0 -no-undefined
libfreesmartphone_glib_la_LIBADD = $(dbus_archives)

dbus-marshal.h: dbus-marshal.list
	( @GLIB_GENMARSHAL@ $< --prefix=freesmartphone_glib_marshal --header > dbus-marshal.tmp \
	&& mv dbus-marshal.tmp dbus-marshal.h ) \
	|| ( rm -f dbus-marshal.tmp && exit 1 )

dbus-marshal.c: dbus-marshal.list dbus-marshal.h
	( @GLIB_GENMARSHAL@ $< --prefix=freesmartphone_glib_marshal --body > dbus-marshal.tmp \
	&& mv dbus-marshal.tmp dbus-marshal.c ) \
	|| ( rm -f dbus-marshal.tmp && exit 1 )

libfreesmartphone_glib_la_SOURCES = \
	freesmartphone-glib.h \
	dbus-types.c \
	dbus-types.h \
	$(BUILT_SOURCES)

BUILT_SOURCES = \
	dbus-marshal.c \
	dbus-marshal.h \
	$(DBUS_GENERATED_SOURCES)

DBUS_GENERATED_SOURCES = \
	$(DBUS_COMMON_SOURCES) \
	$(DBUS_ERRORS_SOURCES)

DBUS_COMMON_SOURCES = \
	common.c \
	common.h

$(DBUS_COMMON_SOURCES): Makefile
	$(top_srcdir)/tools/dbus-rapid-bindings.py . minimal freesmartphone-glib common org.freesmartphone

DBUS_ERRORS_SOURCES = \
	errors.c \
	errors.h

$(DBUS_ERRORS_SOURCES): Makefile
	$(top_srcdir)/tools/dbus-rapid-bindings.py . minimal freesmartphone-glib errors org.freesmartphone "$(cfgdir)" \
	$(wildcard $(xmldir)/*.xml)


libfreesmartphone_glib_HEADERS = \
	freesmartphone-glib.h \
	errors.h

libfreesmartphone_glibdir = $(includedir)/freesmartphone-glib

EXTRA_DIST = \
	dbus-marshal.list

CLEANFILES = \
	$(BUILT_SOURCES)

MAINTAINERCLEANFILES = \
	Makefile.in
