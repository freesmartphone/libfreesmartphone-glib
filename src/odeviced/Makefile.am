AM_CPPFLAGS = -DDATADIR=\"$(datadir)\" \
	      -DPKGDATADIR=\"$(pkgdatadir)\" \
	      -DG_LOG_DOMAIN=\"libfreesmartphone-glib\"

AM_CFLAGS = -Wall -Wextra -Werror @DBUS_CFLAGS@ -I..
AM_LDFLAGS = @DBUS_LIBS@

xmldir = $(top_srcdir)/xml

noinst_LTLIBRARIES = libodeviced.la

BUILT_SOURCES = \
	$(DBUS_ODEVICED_SOURCES) \
	dbus/display.xml \
	dbus/display.h \
	dbus/idlenotifier.xml \
	dbus/idlenotifier.h \
	dbus/input.xml \
	dbus/input.h \
	dbus/vibrator.xml \
	dbus/vibrator.h \
	dbus/led.xml \
	dbus/led.h \
	dbus/orientation.xml \
	dbus/orientation.h \
	dbus/powersupply.xml \
	dbus/powersupply.h \
	dbus/audio.xml \
	dbus/audio.h

DBUS_ODEVICED_SOURCES = \
	display.c \
	display.h \
	idlenotifier.c \
	idlenotifier.h \
	input.c \
	input.h \
	vibrator.c \
	vibrator.h \
	led.c \
	led.h \
	orientation.c \
	orientation.h \
	powersupply.c \
	powersupply.h \
	audio.c \
	audio.h \
	dbus.h

$(BUILT_SOURCES): Makefile
	$(top_srcdir)/tools/dbus-rapid-bindings.py . minimal freesmartphone-glib odeviced org.freesmartphone.odeviced \
	$(xmldir)/org.freesmartphone.Device.Display.xml \
	$(xmldir)/org.freesmartphone.Device.IdleNotifier.xml \
	$(xmldir)/org.freesmartphone.Device.Input.xml \
	$(xmldir)/org.freesmartphone.Device.Vibrator.xml \
	$(xmldir)/org.freesmartphone.Device.LED.xml \
	$(xmldir)/org.freesmartphone.Device.Orientation.xml \
	$(xmldir)/org.freesmartphone.Device.PowerSupply.xml \
	$(xmldir)/org.freesmartphone.Device.Audio.xml

libodeviced_la_SOURCES = \
	$(DBUS_ODEVICED_SOURCES)

libfreesmartphone_glib_HEADERS = \
	display.h \
	idlenotifier.h \
	input.h \
	vibrator.h \
	led.h \
	orientation.h \
	powersupply.h \
	audio.h \
	dbus.h

libfreesmartphone_glibdir = $(includedir)/freesmartphone-glib/odeviced

CLEANFILES = \
	$(BUILT_SOURCES)

MAINTAINERCLEANFILES = \
	Makefile.in

clean-local:
	$(RM) -R dbus
