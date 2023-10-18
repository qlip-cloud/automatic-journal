import frappe
from frappe import _
from frappe.utils.background_jobs import get_jobs
from six import string_types
import json


@frappe.whitelist()
def processing_validate_journal_entry(args):

    try:

        if isinstance(args, string_types):
            args = json.loads(args)

        process_validate_journal_entry(args)

        return "okay"


    except Exception as error:

        frappe.log_error(message=frappe.get_traceback(), title="processing_validate_journal_entry")

        pass

    return "error"


def process_validate_journal_entry(args):

    # company, name_from, name_to

    # Validar duplicacion de ejecución de proceso
    enqueued_method = 'automatic_journal.automatic_journal.uses_cases.validate_journal_entry.ejecutar_proceso' 
    jobs = get_jobs()

    if not jobs or enqueued_method not in jobs[frappe.local.site]:

        frappe.enqueue(enqueued_method, args=args, queue='long', is_async=True, timeout=14400)


def ejecutar_proceso(args):

    args = frappe._dict(args)

    # buscar asientos
    sql_str = '''
        select distinct name
        from `tabJournal Entry`
        where company = '{0}' and name >= '{1}' and name <= '{2}' and docstatus = 0
    '''.format(args.company, args.name_from, args.name_to)
    journal_entries = frappe.db.sql_list(sql_str)

    # recorrer asientos y validarlos
    for journal_entry in journal_entries:
        try:
            doc = frappe.get_doc("Journal Entry", journal_entry)
            doc.submit()
            frappe.db.commit()

        except Exception as error:
            frappe.db.rollback()
            frappe.log_error(message=frappe.get_traceback(), title="validate_journal_entry {0}".format(journal_entry))
            pass

    return
