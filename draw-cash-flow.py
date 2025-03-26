%%bash
python - << 'EOF'
import pandas as pd
import matplotlib.pyplot as plt

csv_file = 'free-cash-flow.csv'
df = pd.read_csv(csv_file)

order = ['TTM', '2023-12-31', '2022-12-31', '2021-12-31']
df['Date'] = pd.Categorical(df['Date'], categories=order, ordered=True)
df = df.sort_values('Date')

plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['China Life'], marker='o', label='China Life Insurance Company')
plt.plot(df['Date'], df['Ping An'], marker='s', label='Ping An Insurance Company')

plt.title('Free Cash Flow Comparison (in Thousands)')
plt.xlabel('Period')
plt.ylabel('Free Cash Flow (Thousands)')
plt.grid(True)
plt.legend()

for index, row in df.iterrows():
    plt.annotate(f"{row['China Life']:,}", (row['Date'], row['China Life']),
                 textcoords="offset points", xytext=(0,5), ha='center', fontsize=8)
    plt.annotate(f"{row['Ping An']:,}", (row['Date'], row['Ping An']),
                 textcoords="offset points", xytext=(0,-15), ha='center', fontsize=8)

plt.tight_layout()
plt.savefig("cash-flow.png")
plt.close()
EOF
