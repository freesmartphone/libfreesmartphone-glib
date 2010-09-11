#include "dbus-types.h"
#include "dbus-marshal.h"

GType dbus_type_string_variant_hashtable(void)
{
    static GType foo = 0;
    if (G_UNLIKELY(foo == 0))
        foo = dbus_g_type_get_map("GHashTable",
                G_TYPE_STRING, G_TYPE_VALUE);
    return foo;
}

GType dbus_type_string_int_hashtable(void)
{
    static GType foo = 0;
    if (G_UNLIKELY(foo == 0))
        foo = dbus_g_type_get_map("GHashTable",
                G_TYPE_STRING, G_TYPE_INT);
    return foo;
}

/* org.freesmartphone.GSM.Call */

GType dbus_type_ogsmd_call_list_calls_call_details(void)
{
    static GType foo = 0;
    if (G_UNLIKELY(foo == 0))
        foo = dbus_g_type_get_collection("GPtrArray",
            dbus_g_type_get_struct("GValueArray",
                G_TYPE_INT,
                G_TYPE_STRING,
                dbus_type_string_variant_hashtable(),
                G_TYPE_INVALID));
    return foo;
}

/* org.freesmartphone.GSM.Network */

GType dbus_type_ogsmd_network_list_providers_providers(void)
{
    static GType foo = 0;
    if (G_UNLIKELY(foo == 0))
        foo = dbus_g_type_get_collection("GPtrArray",
            dbus_g_type_get_struct("GValueArray",
                G_TYPE_STRING,
                G_TYPE_STRING,
                G_TYPE_STRING,
                G_TYPE_STRING,
                G_TYPE_STRING,
                G_TYPE_INVALID));
    return foo;
}

/* org.freesmartphone.GSM.SIM */

GType dbus_type_ogsmd_sim_retrieve_phonebook_entries(void)
{
    static GType foo = 0;
    if (G_UNLIKELY(foo == 0))
        foo = dbus_g_type_get_collection("GPtrArray",
            dbus_g_type_get_struct("GValueArray",
                G_TYPE_INT,
                G_TYPE_STRING,
                G_TYPE_STRING,
                G_TYPE_INVALID));
    return foo;
}

GType dbus_type_ogsmd_sim_get_home_zone_parameters_homezones(void)
{
    static GType foo = 0;
    if (G_UNLIKELY(foo == 0))
        foo = dbus_g_type_get_collection("GPtrArray",
            dbus_g_type_get_struct("GValueArray",
                G_TYPE_STRING,
                G_TYPE_INT,
                G_TYPE_INT,
                G_TYPE_INT,
                G_TYPE_INVALID));
    return foo;
}

/* org.freesmartphone.GSM.SMS */

GType dbus_type_ogsmd_sms_retrieve_text_messages_messages(void)
{
    static GType foo = 0;
    if (G_UNLIKELY(foo == 0))
        foo = dbus_g_type_get_collection("GPtrArray",
            dbus_g_type_get_struct("GValueArray",
                G_TYPE_INT,
                G_TYPE_STRING,
                G_TYPE_STRING,
                G_TYPE_STRING,
                G_TYPE_STRING,
                dbus_type_string_variant_hashtable(),
                G_TYPE_INVALID));
    return foo;
}

/* org.freesmartphone.PIM.CallQuery */

GType dbus_type_opimd_callquery_get_multiple_results_resultset(void)
{
    static GType foo = 0;
    if (G_UNLIKELY(foo == 0))
        foo = dbus_g_type_get_collection("GPtrArray",
                dbus_type_string_variant_hashtable());
    return foo;
}
