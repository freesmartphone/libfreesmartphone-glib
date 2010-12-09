AM_CPPFLAGS = -DDATADIR=\"$(datadir)\" \
	      -DPKGDATADIR=\"$(pkgdatadir)\" \
	      -DG_LOG_DOMAIN=\"libfreesmartphone-glib\"

AM_CFLAGS = -Wall -Wextra -Werror @DEPS_CFLAGS@ -I..
AM_LDFLAGS = @DEPS_LIBS@

xmldir = @FSO_SPECS_DIR@
cfgdir = $(top_srcdir)/cfg

noinst_LTLIBRARIES = libogsmd.la

BUILT_SOURCES = \
	$(DBUS_OGSMD_SOURCES) \
	dbus/call.xml \
	dbus/call.h \
	dbus/device.xml \
	dbus/device.h \
	dbus/network.xml \
	dbus/network.h \
	dbus/sim.xml \
	dbus/sim.h \
	dbus/sms.xml \
	dbus/sms.h

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

$(BUILT_SOURCES): Makefile
	$(top_srcdir)/tools/dbus-rapid-bindings.py . minimal freesmartphone-glib ogsmd org.freesmartphone.ogsmd "$(cfgdir)" \
	"$(xmldir)/org.freesmartphone.GSM.Device.xml" \
	"$(xmldir)/org.freesmartphone.GSM.Call.xml" \
	"$(xmldir)/org.freesmartphone.GSM.Network.xml" \
	"$(xmldir)/org.freesmartphone.GSM.SIM.xml" \
	"$(xmldir)/org.freesmartphone.GSM.SMS.xml"

libogsmd_la_SOURCES = \
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
	$(BUILT_SOURCES)

MAINTAINERCLEANFILES = \
	Makefile.in

clean-local:
	$(RM) -R dbus
