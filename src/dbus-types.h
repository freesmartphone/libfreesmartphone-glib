#ifndef __DBUS_TYPES_H
#define __DBUS_TYPES_H

#include <glib.h>
#include <glib-object.h>
#include <dbus/dbus-glib.h>

GType dbus_type_string_variant_hashtable(void);
GType dbus_type_string_int_hashtable(void);

/* org.freesmartphone.GSM.Device */
#define dbus_type_ogsmd_device_get_features_features dbus_type_string_variant_hashtable

/* org.freesmartphone.GSM.Call */
GType dbus_type_ogsmd_call_list_calls_call_details(void);

/* org.freesmartphone.GSM.Network */
#define dbus_type_ogsmd_network_get_status_status dbus_type_string_variant_hashtable
GType dbus_type_ogsmd_network_list_providers_providers(void);
#define dbus_type_ogsmd_network_get_call_forwarding_status dbus_type_string_variant_hashtable

/* org.freesmartphone.GSM.SIM */
#define dbus_type_ogsmd_sim_retrieve_message_properties dbus_type_string_variant_hashtable
GType dbus_type_ogsmd_sim_retrieve_phonebook_entries(void);
#define dbus_type_ogsmd_sim_get_unlock_counters_counters dbus_type_string_variant_hashtable
#define dbus_type_ogsmd_sim_get_sim_info_info dbus_type_string_variant_hashtable
GType dbus_type_ogsmd_sim_get_home_zone_parameters_homezones(void);

/* org.freesmartphone.GSM.SMS */
GType dbus_type_ogsmd_sms_retrieve_text_messages_messages(void);

/* org.freesmartphone.Device.IdleNotifier */
#define dbus_type_odeviced_idlenotifier_get_timeouts_status dbus_type_string_int_hashtable

/* org.freesmartphone.PIM.Call */
#define dbus_type_opimd_call_get_content_call_data dbus_type_string_variant_hashtable
#define dbus_type_opimd_call_get_multiple_fields_field_data dbus_type_string_variant_hashtable

/* org.freesmartphone.PIM.CallQuery */
#define dbus_type_opimd_callquery_get_result_item dbus_type_string_variant_hashtable
GType dbus_type_opimd_callquery_get_multiple_results_resultset(void);

/* org.freesmartphone.PIM.ContactQuery */
#define dbus_type_opimd_contactquery_get_result_item dbus_type_string_variant_hashtable
#define dbus_type_opimd_contactquery_get_multiple_results_resultset dbus_type_opimd_callquery_get_multiple_results_resultset

/* org.freesmartphone.PIM.Contact */
#define dbus_type_opimd_contact_get_content_contact_data dbus_type_string_variant_hashtable
#define dbus_type_opimd_contact_get_multiple_fields_field_data dbus_type_string_variant_hashtable

/* org.freesmartphone.PIM.Fields */
GType dbus_type_opimd_fields_list_fields_fields(void);

#endif
