import glob #serch()で必要特定のファイルやフォルダを取得する.
import sys #search()で使用．プログラムを強制終了させる．
import yaml #fetch_csv()で使用．yamlファイルを読み込む． 
import csv #fetch_csv()で使用ファイルを読み込む

def search():
    file = glob.glob('./config.yml')
    if len(file) < 1:
        print(f"見つからないよ．config.ymlを作成してください．")
        sys.exit()
    else:
        print("見つかりました！")
        
        
def fetch_csv(x):
    with open('config.yml', 'r') as yml:
        config = yaml.safe_load(yml)
    print(config['bucket'])
    # query = f'from(bucket: "{config[bucket]}") |> range(start: v.timeRangeStart, stop: v.timeRangeStop) |> filter(fn: (r) => r["namespace"] == {namespace}) |> filter(fn: (r) => r["_field"] == "cpu_usage_nanocores") |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false) |> yield(name: "mean")'
    # InfluxDBサーバーのIPアドレスとポート
    
    # url = "http://192.168.100.78:8086"
    # # 対象organization
    # org = config[org]
    # # 対象bucket
    # bucket = config[bucket]
    # # 発行したToken
    # token = config[token]
    # client = InfluxDBClient(url=url, token=token, org=org)
    # query_api = client.query_api()

    # ## using Table structure
    # csv_result = query_api.query_csv(query)
    # csv_file = open(f"{x}.csv", "w",newline='')
    # writer = csv.writer(csv_file)
    # for row in csv_result:
    #     writer.writerow(row)
    # csv_file.close()

query_csvfile("data")

    
