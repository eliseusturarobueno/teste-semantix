
#Importação dos arquivos
rdd_july = sc.textFile("/FileStore/tables/access_log_Jul95")
rdd_aug = sc.textFile("/FileStore/tables/access_log_Aug95")

#União dos arquivos criando um novo RDD
rdd_full = rdd_july.union(rdd_aug)

#Mapeia o RDD unido e quebra ele através do split, atribuindo valor 0
rdd_hosts = rdd_full.map(lambda row: row.split(" - - ")[0])

#Conta os Hosts Distintos
rdd_hosts.distinct().count()

#Filtra o RDD para encontrar os erros 404 e atribui os valores para o novo RDD
rdd_404 = rdd_full.filter(lambda row: " 404 " in row)

#Conta a quantidade de erros 404
rdd_404.count()

#Mapeia o RDD que contém os erros 404 quebrando ele onde contém as urls (Chave) e atribuindo valor 1
rdd_url = rdd_404.map(lambda row: row.split("\"")[1]).map(lambda x: (x, 1)).reduceByKey(lambda v1,v2: v1+v2)

#Imprime as 5 Urls ordenadas pelas que mais ocorreram o erro 404
rdd_url.sortBy(lambda x: x[1], ascending = False).take(5)

#Mapeia o RDD_404 e atribui ao RDD_DATA uma quebra atribuindo como chave a data e como valor 1
rdd_data = rdd_404.map(lambda row: row.split("[")[1][0:11]).map(lambda x: (x, 1)).reduceByKey(lambda v1,v2: v1+v2)

#Importa a biblioteca do Parse - Conta a quantidade de dias para atribuilos ao Take, imprime em ordem crescente de data todas as datas que contém o erro 404 e as respectivas quantidades deste erro por dia
from dateutil.parser import parse
rdd_dias = rdd_data.count()
rdd_data.sortBy(lambda x: parse(x[0])).take(rdd_dias)