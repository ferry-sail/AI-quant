import tushare as ts
import pandas as pd
import json
import os

TOKEN = "ee4a8006049705f03970463dd2aeeef0ec12dd9ae51c219ceb2786a7"
ts.set_token(TOKEN)
pro = ts.pro_api()

# 获取金安国纪 002636.SZ 近一年日线数据
df = pro.daily(ts_code='002636.SZ', start_date='20250704', end_date='20260704')

if df.empty:
    print("ERROR: 未获取到数据")
    exit(1)

# 按交易日期升序排列
df = df.sort_values('trade_date').reset_index(drop=True)

output_dir = r"D:\量化操作\data"
os.makedirs(output_dir, exist_ok=True)

# 保存 CSV
csv_path = os.path.join(output_dir, "002636_金安国纪_daily.csv")
df.to_csv(csv_path, index=False, encoding='utf-8-sig')
print(f"CSV 已保存: {csv_path}")

# 保存 JSON（给 HTML 用）
# 取近200个交易日
df_200 = df.tail(200)
data_json = []
for _, row in df_200.iterrows():
    data_json.append([
        row['trade_date'],
        float(row['open']),
        float(row['close']),
        float(row['low']),
        float(row['high']),
        float(row['vol']),
        float(row['amount']),
        float(row['pct_chg'])
    ])

json_path = os.path.join(output_dir, "002636_金安国纪_daily.json")
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data_json, f, ensure_ascii=False)
print(f"JSON 已保存: {json_path}")

# 打印摘要
print(f"\n数据摘要:")
print(f"  股票: 金安国纪 (002636.SZ)")
print(f"  数据条数: {len(df)}")
print(f"  日期范围: {df['trade_date'].min()} ~ {df['trade_date'].max()}")
print(f"  最新收盘价: {df.iloc[-1]['close']}")
print(f"  最高价: {df['high'].max()}, 最低价: {df['low'].min()}")
