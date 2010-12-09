AM_CPPFLAGS = -DDATADIR=\"$(datadir)\" \
	      -DPKGDATADIR=\"$(pkgdatadir)\" \
	      -DG_LOG_DOMAIN=\"libfreesmartphone-glib\"

AM_CFLAGS = -Wall -Wextra -Werror @DEPS_CFLAGS@ -I..
AM_LDFLAGS = @DEPS_LIBS@

xmldir = @FSO_SPECS_DIR@
cfgdir = $(top_srcdir)/cfg

noinst_LTLIBRARIES = libopimd.la

BUILT_SOURCES = \
	$(DBUS_OPIMD_SOURCES) \
	dbus/fields.xml \
	dbus/fields.h \
	dbus/callquery.xml \
	dbus/callquery.h \
	dbus/call.xml \
	dbus/call.h \
	dbus/calls.xml \
	dbus/calls.h \
	dbus/contactquery.xml \
	dbus/contactquery.h \
	dbus/contact.xml \
	dbus/contact.h \
	dbus/contacts.xml \
	dbus/contacts.h \
	dbus/messagequery.xml \
	dbus/messagequery.h \
	dbus/messagefolder.xml \
	dbus/messagefolder.h \
	dbus/message.xml \
	dbus/message.h \
	dbus/messages.xml \
	dbus/messages.h

DBUS_OPIMD_SOURCES = \
	dbus.h \
	fields.c \
	fields.h \
	callquery.c \
	callquery.h \
	call.c \
	call.h \
	calls.c \
	calls.h \
	contactquery.c \
	contactquery.h \
	contact.c \
	contact.h \
	contacts.c \
	contacts.h \
	messagequery.c \
	messagequery.h \
	messagefolder.c \
	messagefolder.h \
	message.c \
	message.h \
	messages.c \
	messages.h

$(BUILT_SOURCES): Makefile
	$(top_srcdir)/tools/dbus-rapid-bindings.py . minimal freesmartphone-glib opimd org.freesmartphone.opimd "$(cfgdir)" \
	"$(xmldir)/org.freesmartphone.PIM.Fields.xml" \
	"$(xmldir)/org.freesmartphone.PIM.CallQuery.xml" \
	"$(xmldir)/org.freesmartphone.PIM.Call.xml" \
	"$(xmldir)/org.freesmartphone.PIM.Calls.xml" \
	"$(xmldir)/org.freesmartphone.PIM.ContactQuery.xml" \
	"$(xmldir)/org.freesmartphone.PIM.Contact.xml" \
	"$(xmldir)/org.freesmartphone.PIM.Contacts.xml" \
	"$(xmldir)/org.freesmartphone.PIM.MessageFolder.xml" \
	"$(xmldir)/org.freesmartphone.PIM.MessageQuery.xml" \
	"$(xmldir)/org.freesmartphone.PIM.Messages.xml" \
	"$(xmldir)/org.freesmartphone.PIM.Message.xml"

libopimd_la_SOURCES = \
	$(DBUS_OPIMD_SOURCES)

libfreesmartphone_glib_HEADERS = \
	dbus.h \
	fields.h \
	call.h \
	calls.h \
	callquery.h \
	contact.h \
	contacts.h \
	contactquery.h \
	messagefolder.h \
	messagequery.h \
	messages.h \
	message.h

libfreesmartphone_glibdir = $(includedir)/freesmartphone-glib/opimd

CLEANFILES = \
	$(BUILT_SOURCES)

MAINTAINERCLEANFILES = \
	Makefile.in

clean-local:
	$(RM) -R dbus
