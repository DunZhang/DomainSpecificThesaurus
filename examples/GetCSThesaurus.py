from DST.datasets.CleanData import CleanDataSO,CleanDataWiki
from DST.domain_thesaurus.DomainThesaurus import DomainThesaurus

# clean Stack Overflow data
clean_so = CleanDataSO(so_xml_path="xx/xxx/xxx.xml",clean_data_path="xxx/xxx.xml")
clean_so.transform()