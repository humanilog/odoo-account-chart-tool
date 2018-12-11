from collections import namedtuple
from typing import List
from xml.etree.ElementTree import Element, SubElement

Account = namedtuple('Chart', 'id code name reconcile deprecated user_type_id tag_id1 tag_id2 tag_id3')

chart_template_id = "l10n_chart_de_skr49"
account_705_code = "0705"


def create_chart_xml(accounts: List[Account]) -> Element:
    root = Element('odoo') # FIXME , {'noupdate': '1'})

    # Special handling for account 0705 at the beginning
    account_705 = find_account(accounts, account_705_code)
    create_account_record(account_705, root)
    create_account_chart(account_705, root)
    record = SubElement(root, 'record', {'id': account_705.id, 'model': 'account.account.template'})
    SubElement(record, 'field', {'name': 'chart_template_id', 'ref': chart_template_id})

    # All the other accounts from CSV
    for chart in (x for x in accounts if x.code != account_705_code):
        create_account_record(chart, root)

    # More attributes for the account.chart.template
    add_more_chart_attributes(accounts, root)

    return root


def add_more_chart_attributes(accounts, data):
    chart2 = SubElement(data, 'record', {'id': chart_template_id, 'model': 'account.chart.template'})
    SubElement(chart2, 'field', {'name': 'cash_account_code_prefix'}).text = '0920'
    SubElement(chart2, 'field', {'name': 'bank_account_code_prefix'}).text = '0945'
    SubElement(chart2, 'field', {'name': 'property_account_receivable_id', 'ref': find_account(accounts, '0652').id})
    SubElement(chart2, 'field', {'name': 'property_account_payable_id', 'ref': find_account(accounts, '1346').id})
    SubElement(chart2, 'field', {'name': 'property_account_expense_categ_id', 'ref': find_account(accounts, '8154').id})
    SubElement(chart2, 'field', {'name': 'property_account_income_categ_id', 'ref': find_account(accounts, '8030').id})
    SubElement(chart2, 'field',
               {'name': 'income_currency_exchange_account_id', 'ref': find_account(accounts, '4154').id})
    SubElement(chart2, 'field',
               {'name': 'expense_currency_exchange_account_id', 'ref': find_account(accounts, '4715').id})


def find_account(accounts, code):
    return next(account for account in accounts if account.code == code)


def create_account_chart(account_705, data):
    chart = SubElement(data, 'record', {'id': chart_template_id, 'model': 'account.chart.template'})
    SubElement(chart, 'field', {'name': 'name'}).text = "Deutscher Kontenplan SKR49"
    SubElement(chart, 'field', {'name': 'currency_id', 'ref': 'base.EUR'})
    SubElement(chart, 'field', {'name': 'transfer_account_id', 'ref': account_705.id})


def create_account_record(account, data):
    record = SubElement(data, 'record', {'id': account.id, 'model': 'account.account.template'})
    SubElement(record, 'field', {'name': 'name'}).text = account.name
    SubElement(record, 'field', {'name': 'code'}).text = account.code
    SubElement(record, 'field', {'name': 'reconcile', 'eval': account.reconcile.title()})
    if account.deprecated.title() == "True":
        SubElement(record, 'field', {'name': 'deprecated', 'eval': account.deprecated.title()})
    SubElement(record, 'field', {'name': 'user_type_id', 'ref': "account.{}".format(account.user_type_id)})
    if account.code != account_705_code:
        SubElement(record, 'field', {'name': 'chart_template_id', 'ref': chart_template_id})
    if account.tag_id1 or account.tag_id2 or account.tag_id3:
        SubElement(record, 'field', {'name': 'tag_ids', 'eval': create_tag_reference([account.tag_id1, account.tag_id2, account.tag_id3])})


def create_tag_reference(tagRefs):
    refs = ", ".join(["ref('{}')".format(tagRef) for tagRef in tagRefs if tagRef])
    return "[(6,0,[{}])]".format(refs)
