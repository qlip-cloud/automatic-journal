frappe.ui.form.on("Company", "refresh", function(frm) {
    frm.add_custom_button(__("Validate Journal Entry by Batch"), () => {
        frappe.confirm(__("This process will create background job for submit Journal Entries indicated. Are you certain?"), function() {

            var d = new frappe.ui.Dialog({
                'fields': [
                    {'fieldname': 'ht', 'fieldtype': 'HTML'},
                    {'fieldname': 'company', 'fieldtype': 'Data', 'default': frm.doc.name, 'reqd': 1, 'label': __('Company'), 'read_only': 1},
                    {'fieldname': 'name_from', 'fieldtype': 'Data', 'default': '', 'reqd': 1, 'label': __('Name From')},
                    {'fieldname': 'name_to', 'fieldtype': 'Data', 'default': '', 'reqd': 1, 'label': __('Name To')}
                ],
                primary_action: function(){
                    d.hide();
                    frappe.call({
                        method: "automatic_journal.automatic_journal.uses_cases.validate_journal_entry.processing_validate_journal_entry",
                        args: {
                            args: d.get_values()
                        },
                        freeze: true,
                        callback: () => {
                            frappe.msgprint({
                                title: __("Sync Started"),
                                message: __("The process has started in the background."),
                                alert: 1
                            });
                        }
                    });
                }
            });
            d.fields_dict.ht.$wrapper.html(__('This action will create background job for submit Journal Entries'));
            d.show();
            
        });
    });
    });
