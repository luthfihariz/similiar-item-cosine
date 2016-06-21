import petl as etl
import re
from collections import OrderedDict
import pymysql
import dbconfig

read_db_conn = pymysql.connect(host=dbconfig.db_host,
                              port=dbconfig.db_port,
                              charset="utf8",
                              user=dbconfig.db_user,
                              password=dbconfig.db_pass,
                              db=dbconfig.db_name)


products = etl.fromdb(read_db_conn, "SELECT id,name,description FROM {} limit 5000".format(dbconfig.db_table_items))

# remove non-alphanumeric character
def cleanString(val):
    nonewline = val.replace('\n'," ")
    return re.sub(r'\W+', ' ', nonewline).lower()

mappings = OrderedDict()
mappings['id'] = 'id'
mappings['item_description'] = lambda val : cleanString(val['name'] + " " +val['description'])

products = etl.fieldmap(products, mappings)
etl.tocsv(products, 'query_result.csv')
