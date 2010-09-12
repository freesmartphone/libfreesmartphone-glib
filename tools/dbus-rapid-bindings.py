#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
dbus-rapid-bindings
GLib C code generator for D-Bus introspection files
Copyright (C) 2010-2011 Daniele Ricci <daniele.athome@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

from xml.etree.ElementTree import ElementTree
import os, sys

"""
Esempio di firma:
<interface name="org.freesmartphone.PIM.Calls">
    <method name="Query">
        <annotation name="org.freedesktop.DBus.GLib.Async" value="true"/>
        <arg direction="in" type="a{sv}" name="query"/>
        <arg direction="out" type="s" name="query_path"/>
    </method>
</interface>
"""

# special namespace (enumeration, struct, etc.)
fso_namespace = 'http://www.freesmartphone.org/schemas/DBusSpecExtension'

def is_fso(name):
    if name.startswith('{' + fso_namespace + '}'):
        return name[len(fso_namespace) + 2]
    else:
        return False


dbus_type_mapping = {
    # stringa
    's' : 'char*',
    'o' : 'char*',
    # boolean
    'b' : 'gboolean',
    # intero
    'i' : 'gint',
    # intero unsigned
    'u' : 'guint',
    # byte unsigned
    'y' : 'guint8',
    # variant (GValue)
    'v' : 'GValue',
    # vettore: mappa o array
    'a' : {
        '{' : ('GHashTable*', '}'),
        '(' : ('GPtrArray*', ')')
    }
}

dbus_type_marshal = {
    # stringa
    's' : 'string',
    # boolean
    'b' : 'boolean',
    # intero
    'i' : 'int',
    # intero unsigned
    'u' : 'uint',
    # byte unsigned
    'y' : 'byte',
    # variant
    'v' : 'variant',
    # map
    'a' : {
        '{' : 'hashtable',
        '(' : 'array'
    }
}

def cname_from_dbus_name(name):
    '''Converte un nome di metodo D-Bus in nome di metodo C.
    Procedura di conversione:
    1. trasforma le maiuscole in minuscole
    2. le maiuscole dovranno essere integrate con un underscore (_)
    3. risultato: GetFields -> get_fields
    '''
    ret = ''

    for i in range(len(name)):
        ch = name[i]
        if ch.isupper():
            if i > 0 and name[i + 1].islower(): ret += '_'

        ret += ch.lower()

    return ret

def cifname_from_dbus_ifname(name):
    '''Converte un nome di interfaccia D-Bus in un prefisso per un metodo C.
    org.freesmartphone.PIM.Calls -> org_freesmartphone_PIM_Calls
    converte i punti in underscore :)
    '''
    return name.replace('.', '_')

def cdefname_from_dbus_name(name):
    '''Converte un nome D-Bus in nome di define C.
    Risultato: GetFields -> GET_FIELDS
    '''
    return cname_from_dbus_name(name).upper()

def parse_arguments(c):
    in_args = []
    out_args = []
    default_direction_in = True if c.tag == 'signal' else False

    for arg in c.getchildren():
        if arg.tag == 'arg':
            direction = arg.get('direction')
            star = ''
            name = arg.get('name')
            arg_type = arg.get('type')
            special_type = arg.get('{%s}type' % (fso_namespace))
            skip = 0

            for i in range(len(arg_type)):
                if skip > 0:
                    skip -= 1
                    continue

                ch = arg_type[i]
                type_map = dbus_type_mapping[ch]
                complex_struct = False
                if type(type_map) is dict:
                    # tipo complesso, controlla carattere successivo
                    ch = arg_type[i + 1]
                    complex_struct = True
                    try:
                        type2 = type_map[ch][1]
                        skip = arg_type.find(type2, i + 1) - i
                        type_map = type_map[ch][0]
                        #complex_struct = arg_type[i + 2 : skip]
                    except:
                        # e' un'array semplice :)
                        star = '*'
                        skip = 1
                        type_map = dbus_type_mapping[ch]
                        #complex_struct = arg_type[i + 1]
                        # porco zio...
                        if type(type_map) is dict:
                            star = ''
                            ch = arg_type[i + 2]
                            type2 = type_map[ch][1]
                            skip = arg_type.find(type2, i + 1) - i
                            type_map = type_map['('][0]

                if direction == 'in' or (direction is None and default_direction_in) and arg_type[i] == 's':
                    const_add = 'const '
                else:
                    const_add = ''

                arg_def = {
                    'name' : name,
                    'type' : '%s%s%s' % (const_add, type_map, star),
                    'complex' : complex_struct,
                    'converter' : special_type
                }

                if direction == 'in' or (direction is None and default_direction_in):
                    in_args.append(arg_def)
                else:
                    out_args.append(arg_def)

    return (in_args, out_args)

"""
def complex_type_resolve(sig):
    conv = []
    for i in range(len(sig)):
        c = sig[i]
        if c in dbus_type_marshal:
            val = dbus_type_marshal[c]
            print val, sig

            if type(val) is dict:
                try:
                    val = val[sig[i+1]]
                except:
                    val = sig[i]

            print "Value:", val
            conv.append(val)

    #print conv
    return conv
"""

class DBusCodeGen:

    def __init__(self, argv):
        self.basedir = argv[1]
        self.filename_format = argv[2]
        self.filename_prefix = argv[3]
        self.function_prefix = argv[4]
        self.bus_name = argv[5]
        self.xmlfiles = argv[6:]
        self.xmltree = ElementTree()
        self.uscore_fprefix = self.filename_prefix.replace('-', '_')

    def preformat_arguments(self, args, use_special = False):
        # formatta argomenti di input
        fmt_args = []
        fmt_args_expl = []
        fmt_args_impl = []
        for arg in args:
            parg = dict(arg)
            if use_special and arg['converter'] is not None:
                conv = self.converters[parg['converter']]
                type_map = conv['out_type'][1]

                parg['type'] = type_map
                if conv['function_call']:
                    func_str = conv['function_call']
                else:
                    func_str = conv['function']

                try:
                    parg['name'] = func_str % (parg['name'])
                except:
                    parg['name'] = func_str

            fmt_args.append('%s %s' % (parg['type'], parg['name']))
            fmt_args_expl.append(parg['name'])
            fmt_args_impl.append(parg['type'])

        return fmt_args, fmt_args_expl, fmt_args_impl

    def format_arguments(self, args, use_special = False):
        fmt_args, fmt_args_expl, fmt_args_impl = self.preformat_arguments(args, use_special)

        fmt_args = ', '.join(fmt_args)
        fmt_args_expl = ', '.join(fmt_args_expl)
        fmt_args_impl = ', '.join(fmt_args_impl)

        return fmt_args, fmt_args_expl, fmt_args_impl

    def get_filename(self, part1, part2, extension):
        if self.filename_format == 'short':
            return '%s-%s%s' % (part1, part2, extension)
        elif self.filename_format == 'minimal':
            return '%s%s' % (part2, extension)
        else:
            return '%s-%s-%s%s' % (self.filename_prefix, part1, part2, extension)

    def write_common_source(self):
        srcfname = self.get_filename('', 'common', '.c')
        print "Writing common source file %s" % (srcfname, )

        def_prefix = self.filename_prefix.replace('-', '_').upper()

        marshallers_include = ""
        marshallers_register_code = ""
        mlist = open('dbus-marshal.list', 'r')
        comment = None

        for l in mlist:
            l = l.strip()
            if l[0] == '#':
                comment = l[1:].split(',')
                continue
            if l[-1] == '\n':
                l = l[:-1]

            if not len(marshallers_include):
                marshallers_include = "#include \"dbus-marshal.h\""
            print "Generating code for marshaller", l
            ret_type, p_types = l.split(':', 2)
            param_types = p_types.split(',')

            param_g_types = []
            ibox = 0
            for p in param_types:
                if p == 'BOXED' and comment:
                    param_g_types.append(comment[ibox] + "()")
                    ibox += 1
                else:
                    param_g_types.append('G_TYPE_%s' % (p))

            marshallers_register_code += """
    dbus_g_object_register_marshaller
        (%s_marshal_%s__%s, G_TYPE_NONE,
         %s, G_TYPE_INVALID);
""" % (self.uscore_fprefix, ret_type, '_'.join(param_types),
        ', '.join(param_g_types))

            comment = None

        srcfile = open(os.path.join(self.basedir, srcfname), 'w')
        print >>srcfile, """
#include <dbus/dbus-glib.h>
#include <dbus/dbus-glib-bindings.h>
#include "%s"
#include "%s"
#include "dbus-types.h"
%s

DBusGConnection *global_bus = NULL;

DBusGProxy* dbus_connect_to_interface(const char *bus_name, const char *path,
              const char *interface)
{
    DBusGProxy *itf = NULL;
    if (global_bus != NULL) {
        itf = dbus_g_proxy_new_for_name(global_bus, bus_name, path, interface);
        if (itf == NULL) {
            g_warning("Couln't connect to interface %%s", interface);
        }
    }
    return itf;
}

void g_critical_error(const char *prefix, GError* error)
{
    g_critical("%%s: %%s, %%d (%%s), code %%d", prefix, error->message,
        error->domain, g_quark_to_string(error->domain), error->code);
}

GError* dbus_handle_errors(GError* dbus_error)
{
    GError *error = NULL;
    if (dbus_error->domain == DBUS_GERROR) {
        if (dbus_error->code == DBUS_GERROR_REMOTE_EXCEPTION) {
            error = dbus_handle_remote_error(dbus_error);
        }
        else {
            error = dbus_handle_internal_errors(dbus_error);
        }
    }
    else {
        g_critical_error("Unknown dbus error", dbus_error);
    }

    return error;
}

GError* dbus_handle_internal_errors(GError * error)
{
    int dbusError = 0;

    if (error->code == DBUS_GERROR_SERVICE_UNKNOWN) {
        dbusError = %s_DBUS_ERROR_SERVICE_NOT_AVAILABLE;
    }
    else if (error->code == DBUS_GERROR_NO_REPLY) {
        dbusError = %s_DBUS_ERROR_NO_REPLY;
    }
    else {
        g_critical_error("Unknown internal dbus error", error);
    }

    return g_error_new(%s_DBUS_ERROR, dbusError, "%%s",
               error->message);
}

void dbus_free_data(GType type, gpointer data)
{
    GValue foo = {0,{{0}}};
    g_value_init(&foo, type);
    g_value_take_boxed(&foo, data);
    g_value_unset(&foo);
}

void %s_init(void)
{
    GError *error = NULL;
    g_type_init();

    g_debug("Trying to get the system bus");
    global_bus = dbus_g_bus_get(DBUS_BUS_SYSTEM, &error);

    if (!global_bus) {
        g_critical_error("Couldn't connect to system bus", error);
        g_error("Unable to connect to system bus. Exiting.");
    }

    // register marshallers
    %s
}

""" % (self.get_filename('', 'common', '.h'),
        self.get_filename('', 'errors', '.h'), marshallers_include,
        def_prefix, def_prefix, def_prefix, def_prefix.lower(),
        marshallers_register_code)

        srcfile.close()

    def write_common_header(self):
        def_name = '%s_COMMON_H' % (
            self.filename_prefix.replace('-', '_').upper(), )

        # file header comune bus
        hdrfname = self.get_filename('', 'common', '.h')
        print "Writing header file %s" % (hdrfname, )

        hdrfile = open(os.path.join(self.basedir, hdrfname), 'w')
        print >>hdrfile, """
#ifndef %s
#define %s

#include <glib.h>
#include <dbus/dbus-glib.h>

G_BEGIN_DECLS

typedef struct {
    gpointer callback;
    gpointer userdata;
} callback_data_t;

extern DBusGConnection *global_bus;

DBusGProxy* dbus_connect_to_interface(const char *bus_name, const char *path,
              const char *interface);

void g_critical_error(const char *prefix, GError* error);

GError* dbus_handle_errors(GError* dbus_error);
GError* dbus_handle_internal_errors(GError* error);
void dbus_free_data(GType type, gpointer data);

void %s_init(void);

G_END_DECLS

#endif""" % (def_name, def_name, self.filename_prefix.replace('-', '_'))
        hdrfile.close()

    def write_generic_dbus_file(self):
        def_name = '%s_%s_DBUS_H' % (
            self.filename_prefix.replace('-', '_').upper(),
            self.function_prefix.upper()
            )

        # file header comune bus
        hdrfname = self.get_filename(self.function_prefix, 'dbus', '.h')
        print "Writing header file %s" % (hdrfname, )

        hdrfile = open(os.path.join(self.basedir, hdrfname), 'w')
        print >>hdrfile, """
#ifndef %s
#define %s

#include <glib.h>
#include <dbus/dbus-glib.h>

G_BEGIN_DECLS

#define %s_BUS                   "%s"

G_END_DECLS

#endif""" % (def_name, def_name, self.function_prefix.upper(), self.bus_name)
        hdrfile.close()

    def write_errors_file(self, xmlfiles):
        '''Scrive i sorgenti per gestire e descrivere gli errori dei metodi D-Bus.
        L'header (es. frameworkd-glib-errors.h) conterrà i nomi degli errori e le relative costanti numeriche.
        Il sorgente (es. frameworkd-glib-errors.c) conterrà la funzione di conversione da nomi di errori a costanti numeriche (dbus_handle_errors)
        '''
        srcfname = self.get_filename('', self.function_prefix, '.c')
        hdrfname = self.get_filename('', self.function_prefix, '.h')

        srcfile = open(os.path.join(self.basedir, srcfname), 'w')
        hdrfile = open(os.path.join(self.basedir, hdrfname), 'w')

        def_name_prefix = self.filename_prefix.replace('-', '_').upper()
        def_name = '%s_%s_H' % (
            def_name_prefix,
            self.function_prefix.upper()
            )

        print >>hdrfile, """
#ifndef %s
#define %s

GError* dbus_handle_remote_error(GError* dbus_error);

#define %s_DBUS_ERROR    g_quark_from_static_string("dbus")
#define %s_IS_DBUS_ERROR(error, code) g_error_matches(error, %s_DBUS_ERROR, code)

enum {
    %s_DBUS_ERROR_SERVICE_NOT_AVAILABLE = 0,
    %s_DBUS_ERROR_NO_REPLY,
};
""" % (def_name, def_name, def_name_prefix, def_name_prefix, def_name_prefix,
        def_name_prefix, def_name_prefix)

        print >>srcfile, """
#include <string.h>
#include <dbus/dbus-glib.h>
#include <dbus/dbus-glib-bindings.h>
#include "%s"

GError* dbus_handle_remote_error(GError* dbus_error)
{
    const char* error_name = dbus_g_error_get_name(dbus_error);
    int error = 0;
    GQuark quark = 0;

""" % (self.get_filename('', 'errors', '.h'))

        for xmlfile in self.xmlfiles:
            self.root = self.xmltree.parse(xmlfile)
            self.xmlfile = xmlfile

            self.insert_error_code(srcfile, hdrfile,
                self.root.getiterator('errordomain'))

        print >>hdrfile, "#endif"

        print >>srcfile, """
    return g_error_new(quark, error, "TODO %%s", error_name);
}
""" % ()

        srcfile.close()
        hdrfile.close()

    def insert_error_code(self, srcfile, hdrfile, fiter):
        i_else = 0

        for f in fiter:
            name = f.get('name')
            def_prefix = f.get('prefix')
            if def_prefix:
                def_prefix += "_"
            else:
                def_prefix = ""

            print "Processing error domain %s" % (name)
            enum = "\nenum {\n"
            i_enum = 0

            quark_name = "%s_%sERROR" % (self.filename_prefix.replace('-', '_').upper(), def_prefix)
            print >>hdrfile, """
#define %s  g_quark_from_static_string("%s")
#define %s_IS_%sERROR(error, code) g_error_matches(error, %s, code)""" % (
                quark_name, name, self.filename_prefix.replace('-', '_').upper(),
                def_prefix, quark_name)

            if len(def_prefix) > 0:
                enum_prefix = ""
            else:
                enum_prefix = self.filename_prefix.replace('-', '_').upper() + '_'

            for c in f.getchildren():
                if c.tag == 'error':
                    errname = c.get('name')

                    this_errname = "%s%sDBUS_ERROR_%s" % (
                        enum_prefix, def_prefix,
                        cdefname_from_dbus_name(errname)
                    )
                    print >>hdrfile, """#define %s        \"%s.%s\"""" % (
                        this_errname, name, errname)

                    this_enum = "   %s%sERROR_%s" % (enum_prefix,
                        def_prefix, cdefname_from_dbus_name(errname))
                    enum += this_enum

                    if i_enum == 0:
                        enum += " = 0"

                    i_enum += 1
                    enum += ",\n"

                    if i_else > 0:
                        print >>srcfile, "\n    else"

                    i_else += 1

                    print >>srcfile, """    if (!strcmp(error_name, %s)) {
        error = %s;
        quark = %s;
    }""" % (this_errname, this_enum, quark_name)

            enum += "};\n"
            print >>hdrfile, enum

    def generate_dbus_stub(self, f):
        # filtra i nostri tag
        dbus_fname = os.path.join(self.basedir, 'dbus', '%s.h' % (self.methods_prefix, ))
        dbus_xmlfile = os.path.join(self.basedir, 'dbus', '%s.xml' % (self.methods_prefix, ))
        print "Writing D-Bus stub header dbus/%s.h" % (self.methods_prefix, )

        xmltree = ElementTree()
        root = xmltree.parse(self.xmlfile)
        for iface in root.getiterator('interface'):
            if iface.get('name') != f.get('name'):
                root.remove(iface)
            else:
                for child in iface.getchildren():
                    if child.tag == 'proxy':
                        iface.remove(child)

        xmltree.write(dbus_xmlfile, 'utf-8')

        # genera binding stub dbus
        os.system("dbus-binding-tool --mode=glib-client --output=%s %s" % (
            dbus_fname, dbus_xmlfile))

    def prepare_converters(self):
        '''Prepara i convertitori per poter generare il codice in seguito.'''
        nodes = self.root.getiterator('node')

        for f in nodes[0].getchildren():
            if f.tag == '{' + fso_namespace + '}enumeration':
                # definisci enumeration e funzione di conversione
                self.converters[f.get('name')] = self.converter_enumeration(f)

            elif f.tag == '{' + fso_namespace + '}struct':
                # definisci struct e funzione di conversione
                #print "Adding converter for", f.get('name')
                self.converters[f.get('name')] = self.converter_struct(f)

    def converter_struct(self, f):
        struct_name = f.get('name').rsplit('.', 1)[-1]
        struct_defname = cdefname_from_dbus_name(struct_name)
        struct_list = []
        struct_list_def = []
        alloc_code = []
        member_index = 0
        for c in f.getchildren():
            name = is_fso(c.tag)
            if not name: continue

            sig_type = c.get('type')
            try:
                member_type = dbus_type_mapping[sig_type]
            except:
                # prova tipo composto
                member_type = dbus_type_mapping[sig_type[0]]
                if type(member_type) is dict:
                    member_type = member_type[sig_type[1]][0]

            member_def = {
                'name' : c.get('name'),
                'type' : (sig_type, member_type)
            }
            struct_list.append(member_def)
            struct_list_def.append('%s %s' % (
                member_def['type'][1], member_def['name']))

            try:
                g_value_func_suffix = dbus_type_marshal[member_def['type'][0]]
            except KeyError:
                g_value_func_suffix = 'boxed'

            alloc_code.append("""
    value = g_value_array_get_nth(array, %d);
    mb->%s = (%s)g_value_get_%s(value);""" % (member_index,
                member_def['name'], member_def['type'][1], g_value_func_suffix)
            )
            member_index += 1

        struct_hdr = """
typedef struct {
    %s;
} %s;
""" % (';\n    '.join(struct_list_def) if len(struct_list) > 1 else '',
        struct_name)

        handler_args = 'GPtrArray*'

        struct_hdr += """
%s %s_handle_%s_array(%s value);
""" % (handler_args, self.function_prefix, struct_defname.lower(), handler_args)

        struct_src = """
static void %s_struct_%s_convert(gpointer data, gpointer userdata)
{
    GValueArray* array = (GValueArray*) data;
    GPtrArray* conv = (GPtrArray*) userdata;
    GValue* value = NULL;
    %s* mb = g_new0(%s, 1);
    %s

    g_ptr_array_add(conv, mb);
}
""" % (self.function_prefix, struct_defname.lower(),
        struct_name, struct_name,
        '\n'.join(alloc_code))

        struct_src += """

%s %s_handle_%s_array(%s value)
{
    if (!value) return NULL;
    GPtrArray* conv = g_ptr_array_new_with_free_func(g_free);

    g_ptr_array_foreach(value, %s_struct_%s_convert, conv);
    return conv;
}
""" % (handler_args, self.function_prefix, struct_defname.lower(), handler_args,
        self.function_prefix, struct_defname.lower())

        return {
            'name' : struct_name,
            'list' : struct_list,
            'function' : '%s_handle_%s_array(%%s)' % (self.function_prefix, struct_defname.lower()),
            'function_call' : '__struct_%s',
            'in_type' : ('a', 'GPtrArray*'),
            'out_type' : ('a', 'GPtrArray*'),
            'header' : struct_hdr,
            'source' : struct_src,
            'interface' : f.get('interface')
        }

    def converter_enumeration(self, f):
        enum_name = f.get('name').rsplit('.', 1)[-1]
        enum_defname = cdefname_from_dbus_name(enum_name)
        enum_list = []
        enum_values = {}
        conv_type = f.get('type')
        for c in f.getchildren():
            name = is_fso(c.tag)
            if not name: continue

            name = '    %s_%s' % ( enum_defname, c.get('name').replace('-', '_').upper())
            enum_list.append(name)
            enum_values[name] = c.get('value')

        enum_hdr = """
typedef enum {
%s = 0,
%s
} %s;
""" % (enum_list[0], ',\n'.join(enum_list[1:]) if len(enum_list) > 1 else '',
        enum_name)

        handler_args = dbus_type_mapping[conv_type]

        enum_hdr += """
int %s_handle_%s(const %s value);
""" % (self.function_prefix, enum_defname.lower(), handler_args)

        if conv_type == 's':
            condition = '!strcmp(value, "%s")'
        else:
            raise RuntimeError('Unknown converter argument type \'%s\'' % (conv_type))

        enum_src = """
int %s_handle_%s(const %s value)
{""" % (self.function_prefix, enum_defname.lower(), handler_args)

        i_else = False
        for name, value in enum_values.items():
            if i_else:
                enum_src += "\nelse "
            else:
                i_else = True

            enum_src += """
    if (%s)
        return %s;""" % (condition % (value), name)

        enum_src += """
    return 0;
}
"""

        return {
            'name' : enum_name,
            'list' : enum_list,
            'function' : '%s_handle_%s(%%s)' % (self.function_prefix, enum_defname.lower()),
            'function_call' : None,
            'in_type' : (conv_type, handler_args),
            'out_type' : ('i', 'gint'),
            'header' : enum_hdr,
            'source' : enum_src,
            'interface' : f.get('interface')
        }


    def write_interface_file(self, f):
        fname = f.get('name')
        print "Processing interface %s" % (fname, )

        # scrivi file header preliminare
        self.methods_prefix = fname.rsplit('.', 1)[-1].lower()

        # stub dbus :)
        self.generate_dbus_stub(f)

        hdrfname = self.get_filename(self.function_prefix, self.methods_prefix, '.h')
        print "Writing header file %s" % (hdrfname, )

        hdrfile = open(os.path.join(self.basedir, hdrfname), 'w')
        def_name = '%s_%s_%s_H' % (
            self.uscore_fprefix.upper(),
            self.function_prefix.upper(),
            self.methods_prefix.upper()
            )
        self.proxy_name = '%s%sBus' % (
            self.function_prefix.lower(),
            self.methods_prefix.capitalize()
        )

        print >>hdrfile, """
#ifndef %s
#define %s

#include <glib.h>
#include <dbus/dbus-glib.h>
#include <string.h>

G_BEGIN_DECLS
""" % (def_name, def_name)

        srcfname = self.get_filename(self.function_prefix, self.methods_prefix, '.c')
        print "Writing source file %s" % (srcfname, )
        srcfile = open(os.path.join(self.basedir, srcfname), 'w')

        # intestazione sorgenti
        self.write_source_header(srcfile)

        c = f.find('proxy')
        if c is None:
            raise RuntimeError('Proxy definition tag not found.')

        # costruttore del proxy dbus
        self.proxy_type = self.write_proxy_constructor(f, c, hdrfile, srcfile)

        if self.proxy_type == 'static':
            print >>hdrfile, """
extern DBusGProxy *%s;""" % (self.proxy_name)

        for c in f.getchildren():
            if c.tag == 'method':
                self.write_method(f, c, hdrfile, srcfile)

            elif c.tag == 'signal':
                self.write_signal(f, c, hdrfile, srcfile)

        # convertitori :)
        for name, conv in self.converters.items():
            if conv['interface'] == fname:
                print >>hdrfile, conv['header']
                print >>srcfile, conv['source']

        print >>hdrfile, """
G_END_DECLS

#endif"""

        # chiudi tutto
        hdrfile.close()
        srcfile.close()

    def write_source_header(self, srcfile):
        print >>srcfile, """
#include <dbus/dbus-glib.h>
#include <dbus/dbus-glib-bindings.h>
#include "%s"
#include "%s"
#include "%s"
#include "dbus-types.h"
#include "dbus/%s.h"
""" % (self.get_filename(self.function_prefix, self.methods_prefix, '.h'),
        self.get_filename(self.function_prefix, 'dbus', '.h'),
        self.get_filename('', 'common', '.h'),
        self.methods_prefix)

    def write_proxy_constructor(self, f, c, hdrfile, srcfile):
        proxy_type = c.get('type')
        if proxy_type == 'static':
            params = "void"
            proxy_decl = "DBusGProxy* %s;\n" % (self.proxy_name)
            path_def = "%s_%s_BUS_PATH" % (self.function_prefix.upper(),
                self.methods_prefix.upper())
            # path dbus
            print >>hdrfile, "#define %s_%s_BUS_PATH         \"%s\"" % (
                self.function_prefix.upper(), self.methods_prefix.upper(),
                c.get('path'))

        elif proxy_type == 'path':
            params = "const char* path"
            path_def = "path"
            proxy_decl = ""
        else:
            raise RuntimeError('Unknown proxy type %s' % (proxy_type))

        print >>hdrfile, """
DBusGProxy* %s_%s_dbus_connect(%s);""" % (self.function_prefix,
            self.methods_prefix, params)

        # scrivi sorgente :)
        print >>srcfile, """%s

DBusGProxy* %s_%s_dbus_connect(%s)
{
""" % (proxy_decl, self.function_prefix, self.methods_prefix, params)

        if proxy_type == 'path':
            print >>srcfile, """
    DBusGProxy *%s =""" % (self.proxy_name)

        elif proxy_type == 'static':
            print >>srcfile, """
    if (%s == NULL) %s = """ % (self.proxy_name, self.proxy_name)

        print >>srcfile, """dbus_connect_to_interface(%s_BUS, %s, "%s");

    return %s;
}
""" % (self.function_prefix.upper(), path_def, f.get('name'), self.proxy_name)

        # servira' per la costruzione dei metodi
        return proxy_type

    def write_method(self, f, c, hdrfile, srcfile):
        # f: tag interfaccia
        # c: tag metodo
        in_args, out_args = parse_arguments(c)

        #print in_args
        #print out_args
        self.write_method_callback(f, c, hdrfile, srcfile, out_args)
        self.write_method_body(f, c, hdrfile, srcfile, in_args, out_args)

    def write_method_callback(self, f, c, hdrfile, srcfile, out_args):
        fmt_name = cname_from_dbus_name(c.get('name'))

        # formatta argomenti di output per il callback
        fmt_out_args, fmt_out_args_expl, fmt_out_args_impl = self.format_arguments(out_args)
        fmt_out_args_sp, fmt_out_args_sp_expl, fmt_out_args_sp_impl = self.format_arguments(out_args, True)

        if len(out_args) > 0:
            fmt_out_args += ', '
            fmt_out_args_expl += ', '
            fmt_out_args_impl += ', '
            fmt_out_args_sp += ', '
            fmt_out_args_sp_expl += ', '
            fmt_out_args_sp_impl += ', '

        complex_args_free = ""
        complex_args_extra = ""
        complex_args_decl = ""
        for arg in out_args:
            if arg['complex'] and (arg['type'].startswith('GPtrArray') or arg['type'].startswith('GHashTable')):
                complex_args_free += "dbus_free_data(dbus_type_%s_%s_%s_%s(), %s);" % (
                    self.function_prefix, self.methods_prefix, fmt_name,
                    arg['name'], arg['name']);

                if arg['converter'] is not None:
                    complex_args_extra += "if (__struct_%s) g_ptr_array_free(__struct_%s, TRUE);\n" % (arg['name'], arg['name'])
                    conv = self.converters[arg['converter']]
                    type_map = conv['out_type'][1]
                    try:
                        arg_def = conv['function'] % (arg['name'])
                    except:
                        arg_def = conv['function']

                    complex_args_decl += "GPtrArray* __struct_%s = %s;\n" % (
                        arg['name'], arg_def)

        print >>srcfile, """
static void %s_%s_%s_callback(DBusGProxy *proxy, %sGError *dbus_error, gpointer userdata)
{
    (void)proxy;
    callback_data_t *__data = (callback_data_t *)userdata;
    GError *error = NULL;

    if (__data->callback != NULL) {
        if (dbus_error != NULL)
            error = dbus_handle_errors(dbus_error);

        %s
        void (*callback)(GError*, %sgpointer) = __data->callback;
        callback(error, %s__data->userdata);
        if (error != NULL)
            g_error_free(error);
        %s
    }
    if (dbus_error != NULL)
        g_error_free(dbus_error);

    g_free(__data);
    %s
}
""" % (self.function_prefix, self.methods_prefix, fmt_name,
        fmt_out_args, complex_args_decl,
        fmt_out_args_sp_impl, fmt_out_args_sp_expl,
        complex_args_extra, complex_args_free)

    def write_method_body(self, f, c, hdrfile, srcfile, in_args, out_args):
        async_method_prefix = cifname_from_dbus_ifname(f.get('name'))
        fmt_name = cname_from_dbus_name(c.get('name'))

        # formatta argomenti di input
        fmt_in_args, fmt_in_args_expl, fmt_in_args_impl = self.format_arguments(in_args)

        if len(in_args) > 0:
            fmt_in_args += ', '
            fmt_in_args_expl += ', '

        # formatta argomenti di output per il callback
        fmt_out_args, fmt_out_args_expl, fmt_out_args_impl = self.format_arguments(out_args)
        fmt_out_args_sp, fmt_out_args_sp_expl, fmt_out_args_sp_impl = self.format_arguments(out_args, True)

        if len(out_args) > 0:
            fmt_out_args += ', '
            fmt_out_args_impl += ', '
            fmt_out_args_sp += ', '
            fmt_out_args_sp_impl += ', '

        if self.proxy_type == 'static':
            construct_decl = ''
            construct_args = ''
            construct_args_expl = ''
        elif self.proxy_type == 'path':
            construct_decl = 'DBusGProxy* %s = ' % (self.proxy_name)
            construct_args = 'const char* path, '
            construct_args_expl = 'path'

        print >>srcfile, """
void %s_%s_%s(%s%svoid (*callback)(GError*, %sgpointer), gpointer userdata)
{
    %s%s_%s_dbus_connect(%s);

    callback_data_t *__data = g_malloc(sizeof(callback_data_t));
    __data->callback = callback;
    __data->userdata = userdata;
    %s_%s_async(%s, %s%s_%s_%s_callback, __data);
}
""" % (self.function_prefix, self.methods_prefix, fmt_name, construct_args,
        fmt_in_args, fmt_out_args_sp_impl, construct_decl, self.function_prefix,
        self.methods_prefix, construct_args_expl,
        async_method_prefix, fmt_name, self.proxy_name, fmt_in_args_expl,
        self.function_prefix, self.methods_prefix, fmt_name)

        print >>hdrfile, """
void %s_%s_%s(%s%svoid (*callback)(GError*, %sgpointer), gpointer userdata);""" % (
        self.function_prefix, self.methods_prefix, fmt_name, construct_args,
        fmt_in_args, fmt_out_args_sp_impl)

    def write_signal_callback(self, f, c, hdrfile, srcfile, in_args):
        fmt_args, fmt_args_expl, fmt_args_impl = self.format_arguments(in_args)
        fmt_args_sp, fmt_args_sp_expl, fmt_args_sp_impl = self.format_arguments(in_args, True)

        if len(in_args) > 0:
            fmt_args += ', '
            fmt_args_expl = ', ' + fmt_args_expl
            fmt_args_impl = ', ' + fmt_args_impl
            fmt_args_sp += ', '
            fmt_args_sp_expl = ', ' + fmt_args_sp_expl
            fmt_args_sp_impl = ', ' + fmt_args_sp_impl

        print >>srcfile, """
static void %s_%s_%s_handler(DBusGProxy *proxy,
        %sgpointer userdata)
{
    (void)proxy;
    gpointer* __data = userdata;
    void (*callback)(gpointer userdata%s) = __data[0];

    if (callback != NULL)
        (callback)(__data[1]%s);
}
""" % (self.function_prefix, self.methods_prefix,
        cname_from_dbus_name(c.get('name')), fmt_args,
        fmt_args_sp_impl, fmt_args_sp_expl)

    def write_signal_connect(self, f, c, hdrfile, srcfile, in_args):
        ifname = '%s.%s' % (f.get('name'), c.get('name'))
        fmt_args, fmt_args_expl, fmt_args_impl = self.format_arguments(in_args)
        fmt_args_sp, fmt_args_sp_expl, fmt_args_sp_impl = self.format_arguments(in_args, True)

        if len(in_args) > 0:
            fmt_args += ', '
            fmt_args_expl = ', ' + fmt_args_expl
            fmt_args_impl = ', ' + fmt_args_impl
            fmt_args_sp += ', '
            fmt_args_sp_expl = ', ' + fmt_args_sp_expl
            fmt_args_sp_impl = ', ' + fmt_args_sp_impl

        if self.proxy_type == 'static':
            construct_decl = ''
            construct_args = ''
            construct_args_expl = ''
            proxy_connection = ''
        elif self.proxy_type == 'path':
            construct_decl = 'DBusGProxy* %s = ' % (self.proxy_name)
            construct_args = 'const char* path, '
            construct_args_expl = 'path'
            proxy_connection = '%s%s_%s_dbus_connect(%s);' % (
                construct_decl, self.function_prefix, self.methods_prefix,
                construct_args_expl)

        print >>hdrfile, """
gpointer %s_%s_%s_connect(%svoid (*callback)(gpointer userdata%s), gpointer userdata);""" % (
        self.function_prefix, self.methods_prefix,
        cname_from_dbus_name(c.get('name')), construct_args, fmt_args_sp_impl)

        print >>srcfile, """
gpointer %s_%s_%s_connect(%svoid (*callback)(gpointer userdata%s), gpointer userdata)
{
    static gboolean signal_added = FALSE;

    %s%s_%s_dbus_connect(%s);

    if (!signal_added) {
        dbus_g_proxy_add_signal(%s,
            "%s", G_TYPE_STRING, G_TYPE_STRING,
            G_TYPE_INT, G_TYPE_INVALID);
        signal_added = TRUE;
    }

    gpointer* __data = g_new0(gpointer, 2);
    __data[0] = callback;
    __data[1] = userdata;

    dbus_g_proxy_connect_signal(%s,
            "%s", G_CALLBACK (%s_%s_%s_handler),
            __data, NULL);

    g_debug("registered callback %%p to %s", __data);
    return __data;
}""" % (self.function_prefix, self.methods_prefix,
        cname_from_dbus_name(c.get('name')), construct_args, fmt_args_sp_impl,
        construct_decl, 
        self.function_prefix, self.methods_prefix, construct_args_expl,
        self.proxy_name, c.get('name'),
        # TODO parametri
        self.proxy_name, c.get('name'),
        self.function_prefix, self.methods_prefix,
        cname_from_dbus_name(c.get('name')), ifname)

        print >>hdrfile, """
void %s_%s_%s_disconnect(%sgpointer callback_data);""" % (
        self.function_prefix, self.methods_prefix,
        cname_from_dbus_name(c.get('name')), construct_args)

        print >>srcfile, """
void %s_%s_%s_disconnect(%sgpointer callback_data)
{
    %s
    dbus_g_proxy_disconnect_signal(%s,
            "Event", G_CALLBACK(%s_%s_%s_handler),
            callback_data);

    g_free(callback_data);
    g_debug("unregistered callback %%p from %s", callback_data);
}
""" % (self.function_prefix, self.methods_prefix,
        cname_from_dbus_name(c.get('name')), construct_args,
        proxy_connection, self.proxy_name,
        self.function_prefix, self.methods_prefix,
        cname_from_dbus_name(c.get('name')), ifname)

    def write_signal(self, f, c, hdrfile, srcfile):
        # f: tag interfaccia
        # c: tag metodo
        in_args, out_args = parse_arguments(c)

        self.write_signal_callback(f, c, hdrfile, srcfile, in_args)
        self.write_signal_connect(f, c, hdrfile, srcfile, in_args)

    def run(self):
        try: os.mkdir(self.basedir)
        except: print "Source directory already exists, ignoring"

        if self.function_prefix == 'errors':
            self.write_errors_file(self.xmlfiles)

        elif self.function_prefix == 'common':
            self.write_common_source()
            self.write_common_header()

        else:
            try: os.mkdir(os.path.join(self.basedir, 'dbus'))
            except: print "D-Bus stub directory already exists, ignoring"

            self.write_generic_dbus_file()
            self.converters = {}

            for xmlfile in self.xmlfiles:
                self.root = self.xmltree.parse(xmlfile)
                self.xmlfile = xmlfile

                self.prepare_converters()
                map(self.write_interface_file, self.root.getiterator('interface'))

        return 0


if __name__ == '__main__':
    sys.exit(DBusCodeGen(sys.argv).run())
