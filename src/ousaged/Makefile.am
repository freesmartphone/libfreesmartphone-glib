AM_CPPFLAGS = -DDATADIR=\"$(datadir)\" \
	      -DPKGDATADIR=\"$(pkgdatadir)\" \
	      -DG_LOG_DOMAIN=\"libfreesmartphone-glib\"

AM_CFLAGS = -Wall -Wextra -Werror @DBUS_CFLAGS@ -I..
AM_LDFLAGS = @DBUS_LIBS@

xmldir = $(top_srcdir)/xml

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
	$(top_srcdir)/tools/dbus-rapid-bindings.py . minimal freesmartphone-glib ousaged org.freesmartphone.ousaged \
	$(xmldir)/org.freesmartphone.Usage.xml

libousaged_la_SOURCES = \
	$(DBUS_OUSAGED_SOURCES)

libfreesmartphone_glib_HEADERS = \
	usage.h \
	dbus.h

libfreesmartphone_glibdir = $(includedir)/freesmartphone-glib/ousaged

CLEANFILES = \
	$(BUILT_SOURCES) \
	dbus

MAINTAINERCLEANFILES = \
	Makefile.in
