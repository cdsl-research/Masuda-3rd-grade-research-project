import glob #search()で必要特定のファイルやフォルダを取得する.
import sys #search()で使用．プログラムを強制終了させる
import yaml #fetch()で使用．yamlファイルを読み込む． 
import csv #fetch()で使用ファイルを読み込む
from csv import reader
from influxdb_client import InfluxDBClient
import pandas
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import math

# conf.ymlがprepareディレクトリに存在するかの確認 なければ実行中のapp.pyを強制終了
def search():
    file = glob.glob('./prepare/conf.yml')
    if len(file) < 1:
        print("ないよ")
        sys.exit()
    else:
        print("あるよ")

# InfluxDBへクエリを行い，リソースメトリクスが保存されているCSVファイルを取得する
def fetch(x):
    with open('./prepare/conf.yml', 'r') as yml:
        config = yaml.safe_load(yml)
    
    # InfluxDBサーバーのIPアドレスとポート
    url = "http://192.168.100.78:8086"
    # 対象organization
    org = config["org"]
    # 対象bucket
    bucket = config["bucket"]
    # 発行したToken
    token = config["token"]
    client = InfluxDBClient(url=url, token=token, org=org)
    
    query = f"""from(bucket: "{bucket}") \
  |> range(start: 2022-10-01T06:00:00Z, stop: 2022-11-01T06:00:00Z) \
  |> filter(fn: (r) => r["namespace"] == "{config["namespace"]}") \
  |> filter(fn: (r) => r["_field"] == "cpu_usage_nanocores") \
  |> aggregateWindow(every: 3600s, fn: mean, createEmpty: false) \
  |> yield(name: "mean")"""
  
    query_api = client.query_api()
    csv_result = query_api.query_csv(query)
    csv_file = open(f"{x}.csv", "w",newline='')
    writer = csv.writer(csv_file)
    for row in csv_result:
        writer.writerow(row)

    csv_file.close()

# fetch("data2")
    
def data(csv):
    pods_cpu_dic = {}
    pods_date_dic = {}
    with open(csv) as f:
        r = reader(f)
        for i,row in enumerate(r):
            #最初の4行をスキップする
            if i < 4:
                continue
            #Pod名をリストにappend
            try:
                pod = row[len(row)-1]
                if pod not in pods_cpu_dic:
                    pods_cpu_dic[pod] = []
                if pod not in pods_date_dic:
                    pods_date_dic[pod] = []
            except:
                pass
    
            #CPU使用量をリストにappend
            try:
                amount = int(float(row[6]))/ 1000000000
                pods_cpu_dic[pod].append(int(float(row[6]))/ 1000000000)
            except:
                pass
        

            #日付をリストにappend
            try:
                date = row[5]                
                d = date.replace("T", "-", )
                dd = d.replace(":", "-")
                ddd = dd.replace("Z", "")
                dddd = str(int(ddd.replace("-", "")) // 10000)
                pods_date_dic[pod].append(dddd)

            except:
                pass
    # print(pods_cpu_dic["productcatalogservice-697c6cd9c7-rk9c5"])
    # print(pods_date_dic["productcatalogservice-697c6cd9c7-rk9c5"])
    # print(len(pods_cpu_dic["productcatalogservice-697c6cd9c7-rk9c5"]), len(pods_date_dic["productcatalogservice-697c6cd9c7-rk9c5"]))
    for i, a in enumerate(pods_cpu_dic):
        xs = pods_date_dic[a]
        ys = pods_cpu_dic[a]
        fig, ax = plt.subplots()      
        ax.plot(xs, ys)
        if len(ys) > 100:
            plt.xticks(xs[::24], rotation = 45)
        elif len(ys) > 6:
            s = len(ys) % 6
            plt.xticks(xs[::s], rotation = 45)
        else:
            plt.xticks(xs, rotation = 45)
        plt.rcParams["font.size"] = 12

        ax.set_title(f'Pod:{a}')
        ax.set_xlabel("Date")
        ax.set_ylabel("CPU USAGE(vCPU)")
        plt.tight_layout()
        plt.show()
        plt.savefig(f"./static/images/graph{i}.png")
    
