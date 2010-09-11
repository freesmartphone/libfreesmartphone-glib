AM_CPPFLAGS = -DDATADIR=\"$(datadir)\" \
	      -DPKGDATADIR=\"$(pkgdatadir)\" \
	      -DG_LOG_DOMAIN=\"libfreesmartphone-glib\"

AM_CFLAGS = -Wall -Wextra -Werror @DBUS_CFLAGS@ -I..
AM_LDFLAGS = @DBUS_LIBS@

xmldir = $(top_srcdir)/xml

noinst_LIBRARIES = libogsmd.a

DBUS_OGSMD_SOURCES = \
	call.c \
	call.h \
	dbus.h \
	device.c \
	device.h \
	network.c \
	network.h \
	sim.c \
	sim.h \
	sms.c \
	sms.h

$(DBUS_OGSMD_SOURCES): Makefile
	$(top_srcdir)/tools/dbus-rapid-bindings.py . minimal freesmartphone-glib ogsmd org.freesmartphone.ogsmd \
	$(xmldir)/org.freesmartphone.GSM.Device.xml \
	$(xmldir)/org.freesmartphone.GSM.Call.xml \
	$(xmldir)/org.freesmartphone.GSM.Network.xml \
	$(xmldir)/org.freesmartphone.GSM.SIM.xml \
	$(xmldir)/org.freesmartphone.GSM.SMS.xml

libogsmd_a_SOURCES = \
	$(DBUS_OGSMD_SOURCES)

libfreesmartphone_glib_HEADERS = \
	call.h \
	dbus.h \
	device.h \
	network.h \
	sim.h \
	sms.h

libfreesmartphone_glibdir = $(includedir)/freesmartphone-glib/ogsmd

CLEANFILES = \
	$(BUILT_SOURCES) \
	$(RM) -fR dbus

MAINTAINERCLEANFILES = \
	Makefile.in
