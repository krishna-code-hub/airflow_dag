from databricks import sql
import os

with sql.connect(server_hostname = "adb-5580940915006447.7.azuredatabricks.net",
                 http_path       = "/sql/1.0/warehouses/aa44e84e43e93688",
                 access_token    = "dapi2e9b2ca6d3acdc9119e17f75d59d31d8") as connection:

  with connection.cursor() as cursor:
    cursor.execute("with history as ( describe history rbdatahub.core_schema.transactions_part ) , latest as ( select * from history where version = ( select max(version) from history )) select * from latest")
    result = cursor.fetchall()

    for row in result:
      print(row)