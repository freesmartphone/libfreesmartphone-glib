AM_CPPFLAGS = -DDATADIR=\"$(datadir)\" \
	      -DPKGDATADIR=\"$(pkgdatadir)\" \
	      -DG_LOG_DOMAIN=\"libfreesmartphone-glib\"

AM_CFLAGS = -Wall -Wextra -Werror @DEPS_CFLAGS@ -I..
AM_LDFLAGS = @DEPS_LIBS@

xmldir = @FSO_SPECS_DIR@
cfgdir = $(top_srcdir)/cfg

noinst_LTLIBRARIES = libousaged.la

BUILT_SOURCES = \
	$(DBUS_OUSAGED_SOURCES) \
	dbus/usage.xml \
	dbus/usage.h

DBUS_OUSAGED_SOURCES = \
	usage.c \
	usage.h \
	dbus.h

$(BUILT_SOURCES): Makefile
	$(top_srcdir)/tools/dbus-rapid-bindings.py . minimal freesmartphone-glib ousaged org.freesmartphone.ousaged "$(cfgdir)" \
	"$(xmldir)/org.freesmartphone.Usage.xml"

libousaged_la_SOURCES = \
	$(DBUS_OUSAGED_SOURCES)

libfreesmartphone_glib_HEADERS = \
	usage.h \
	dbus.h

libfreesmartphone_glibdir = $(includedir)/freesmartphone-glib/ousaged

CLEANFILES = \
	$(BUILT_SOURCES)

MAINTAINERCLEANFILES = \
	Makefile.in

clean-local:
	$(RM) -R dbus
