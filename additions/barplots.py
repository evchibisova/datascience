# построение гистограммы
import pandas as pd
import seaborn as sns
from matplotlib import pyplot
sns.set(font_scale=1.5)
sns.set_style('white')

df = pd.read_excel('../data.xlsx', sheet_name='emotions')
df = df[df['date'] != '27-04']

# средние значения эмоций
print(df.groupby(by='emo')['emo value'].mean())
p = sns.barplot(data=df, x="emo", y="emo value", palette='RdYlGn', ci=None)
pyplot.xlabel('emotion')
pyplot.ylabel('emotion average value, %')
pyplot.show()
