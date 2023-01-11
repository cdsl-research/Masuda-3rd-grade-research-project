import glob #serch()で必要特定のファイルやフォルダを取得する.
import sys #search()で使用．プログラムを強制終了させる
import yaml #fetch_csv()で使用．yamlファイルを読み込む． 
import csv #fetch_csv()で使用ファイルを読み込む
from csv import reader
from influxdb_client import InfluxDBClient
import pandas
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime




def search():
    file = glob.glob('./conf.yml')
    if len(file) < 1:
        print("ないよ")
        sys.exit()
    else:
        print("あるよ")
        
# search()

def fetch_csv(x):
    with open('config.yml', 'r') as yml:
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

# fetch_csv("data2")

def data(csv):
    name_rows = []
    date_rows = []
    amount_rows = []
    with open(csv) as f:
        r = reader(f)
        for i,row in enumerate(r):
            
            #最初の4行をスキップする
            if i < 4:
                continue
            
            #Pod名をリストにappend
            try:
                pod = row[len(row)-1]
                if pod not in name_rows:
                    name_rows.append(pod)
            except:
                pass
            
            #日付をリストにappend
            try:
                date = row[5]
                amout = row[6]
                if date not in date_rows:
                    # d = date.replace("T", "-", )
                    # dd = d.replace(":", "-")
                    # ddd = dd.replace("Z", " ")
                    print(type(datetime.datetime.fromisoformat(date)))
                    # date_rows.append(date)
                    # amount_rows[pod] = amount

            except:
                pass
            
            #CPU使用量をリストにappend
            try:
                if row[len(row) -1] == name_rows[0]:
                    amount_rows.append(int(float(row[6]))/ 1000000000)

            except:
                pass
                
        del name_rows[0:4]
        del date_rows[0:4]
        del amount_rows[0:4]
    
    x = date_rows
    y = amount_rows
    
    fig, ax = plt.subplots()
    
    ax.plot(x, y)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%y/%m"))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    plt.gcf().autofmt_xdate()


    

    print(123)
    ax.set_title(name_rows[0])
    ax.set_xlabel("Date")
    ax.set_ylabel("CPU USAGE(vCPU)")
    plt.show()
    plt.savefig("cos2.png")
    
data("data2.csv")

