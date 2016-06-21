import sys
import pandas as pd
import json
import petl as etl
import pymysql
import dbconfig

id_to_predict = 11111

read_db_conn = pymysql.connect(host=dbconfig.db_host,
                              port=dbconfig.db_port,
                              charset="utf8",
                              user=dbconfig.db_user,
                              password=dbconfig.db_pass,
                              db=dbconfig.db_name)

df = pd.read_csv('trained_data.csv', index_col=False)

query = "SELECT id,names FROM {} WHERE id = {} ".format(dbconfig.db_table_items,
                                                        id_to_predict)

items_to_predict = etl.fromdb(read_db_conn, query)
print items_to_predict.values('name')

similiar_items = df.loc[lambda df:df.id == id_to_predict, 'similiar_items']
similiar_items = json.loads(similiar_items.values[0])

results_ids = []
for similarity, item_id in similiar_items:
    print similarity, item_id
    if similarity > 0.04:
        # put some threshold
        results_ids.append(str(item_id))


query = "SELECT image, name, vendor_id FROM {} WHERE id IN ({})".format(dbconfig.db_table_items,
                                                                        ",".join(results_ids))

prediction = etl.fromdb(read_db_conn, query)
print prediction
