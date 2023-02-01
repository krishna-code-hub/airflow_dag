from databricks import sql
import os

with sql.connect(server_hostname = "adb-55xxxxxxxxx.7.azuredatabricks.net",
                 http_path       = "/sql/1.0/warehouses/aa44e84xxxxxxxx",
                 access_token    = "xxxxxxxxx") as connection:

  with connection.cursor() as cursor:
    cursor.execute("with history as ( describe history rbdatahub.core_schema.transactions_part ) , latest as ( select * from history where version = ( select max(version) from history )) select * from latest")
    result = cursor.fetchall()

    for row in result:
      print(row)
