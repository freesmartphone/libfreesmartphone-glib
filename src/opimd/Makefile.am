AM_CPPFLAGS = -DDATADIR=\"$(datadir)\" \
	      -DPKGDATADIR=\"$(pkgdatadir)\" \
	      -DG_LOG_DOMAIN=\"libfreesmartphone-glib\"

AM_CFLAGS = -Wall -Wextra -Werror @DBUS_CFLAGS@ -I..
AM_LDFLAGS = @DBUS_LIBS@

xmldir = $(top_srcdir)/xml

noinst_LTLIBRARIES = libopimd.la

BUILT_SOURCES = \
	$(DBUS_OPIMD_SOURCES) \
	dbus/callquery.xml \
	dbus/callquery.h \
	dbus/call.xml \
	dbus/call.h \
	dbus/calls.xml \
	dbus/calls.h

DBUS_OPIMD_SOURCES = \
	callquery.c \
	callquery.h \
	call.c \
	call.h \
	calls.c \
	calls.h \
	dbus.h

$(BUILT_SOURCES): Makefile
	$(top_srcdir)/tools/dbus-rapid-bindings.py . minimal freesmartphone-glib opimd org.freesmartphone.opimd \
	$(xmldir)/org.freesmartphone.PIM.CallQuery.xml \
	$(xmldir)/org.freesmartphone.PIM.Call.xml \
	$(xmldir)/org.freesmartphone.PIM.Calls.xml

libopimd_la_SOURCES = \
	$(DBUS_OPIMD_SOURCES)

libfreesmartphone_glib_HEADERS = \
	call.h \
	calls.h \
	callquery.h \
	dbus.h

libfreesmartphone_glibdir = $(includedir)/freesmartphone-glib/opimd

CLEANFILES = \
	$(BUILT_SOURCES)

MAINTAINERCLEANFILES = \
	Makefile.in

clean-local:
	$(RM) -R dbus
