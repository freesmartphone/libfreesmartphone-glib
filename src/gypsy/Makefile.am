AM_CPPFLAGS = -DDATADIR=\"$(datadir)\" \
	      -DPKGDATADIR=\"$(pkgdatadir)\" \
	      -DG_LOG_DOMAIN=\"libfreesmartphone-glib\"

AM_CFLAGS = -Wall -Wextra -Werror -I- @DEPS_CFLAGS@ -I..
AM_LDFLAGS = @DEPS_LIBS@

xmldir = @FSO_SPECS_DIR@
cfgdir = $(top_srcdir)/cfg

noinst_LTLIBRARIES = libgypsy.la

BUILT_SOURCES = \
	$(DBUS_GYPSY_SOURCES) \
	dbus/accuracy.xml \
	dbus/accuracy.h \
	dbus/course.xml \
	dbus/course.h \
	dbus/device.xml \
	dbus/device.h \
	dbus/position.xml \
	dbus/position.h \
	dbus/time.xml \
	dbus/time.h

DBUS_GYPSY_SOURCES = \
	accuracy.c \
	accuracy.h \
	course.c \
	course.h \
	device.c \
	device.h \
	position.c \
	position.h \
	time.c \
	time.h \
	dbus.h

$(BUILT_SOURCES): Makefile
	$(top_srcdir)/tools/dbus-rapid-bindings.py . minimal freesmartphone-glib gypsy org.freedesktop.Gypsy "$(cfgdir)" \
	"$(xmldir)/org.freedesktop.Gypsy.Accuracy.xml" \
	"$(xmldir)/org.freedesktop.Gypsy.Course.xml" \
	"$(xmldir)/org.freedesktop.Gypsy.Device.xml" \
	"$(xmldir)/org.freedesktop.Gypsy.Position.xml" \
	"$(xmldir)/org.freedesktop.Gypsy.Time.xml"


libgypsy_la_SOURCES = \
	$(DBUS_GYPSY_SOURCES)

libfreesmartphone_glib_HEADERS = \
	accuracy.h \
	course.h \
	device.h \
	position.h \
	time.h \
	dbus.h

libfreesmartphone_glibdir = $(includedir)/freesmartphone-glib/gypsy

CLEANFILES = \
	$(BUILT_SOURCES)

MAINTAINERCLEANFILES = \
	Makefile.in

clean-local:
	$(RM) -R dbus
