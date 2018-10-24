from src.chartdata import Account, create_chart_xml
from src.tagdata import Tag, create_tag_xml
from src.csvhelper import *
from src.xmlhelper import *

# Convert test chart csv file
test_accounts = readdata('resources/test/20160527_HLO_SKR49_Vorlage-chart.csv', Account)
write('out/test/account_chart.xml', prettify(create_chart_xml(test_accounts)))

# Convert test tags csv file
test_tags = readdata('resources/test/20160527_HLO_SKR49_Vorlage-tag.csv', Tag)
write('out/test/account_account_tags_data.xml', prettify(create_tag_xml(test_tags)))

# Convert chart csv file
test_accounts = readdata('resources/SKR49_accounts.csv', Account)
write('out/account_chart.xml', prettify(create_chart_xml(test_accounts)))

# Convert tags csv file
test_tags = readdata('resources/SKR49_tags.csv', Tag)
write('out/account_account_tags_data.xml', prettify(create_tag_xml(test_tags)))
