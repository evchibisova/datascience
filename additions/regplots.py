import pandas as pd
import seaborn as sns
import os
from matplotlib import pyplot
sns.set(font_scale=1.5)
sns.set_style('white')


def emo_regplot(feature, folder, postfix):
    for i in df['emo'].unique():
        cur_df = df[df['emo'] == i]
        ax = sns.regplot(data=cur_df, x=cur_df[feature], y=cur_df['emo value'], label=i)
        ax.legend(loc=i)
        if not os.path.exists('diagrams/' + folder): os.makedirs('diagrams/' + folder)
        pyplot.subplots_adjust(bottom=0.15)
        pyplot.savefig('diagrams/' + folder + '/' + i + postfix + '.png')
        pyplot.clf()


df = pd.read_excel('../data.xlsx', sheet_name='emotions')
# удаление neutral, disgust и выбросов
df = df[df['emo'] != 'disgust']
df = df[df['date'] != '27-05']
df = df[((df['date'] == '24-04') | (df['date'] == '25-04')) & (df['emo'] == 'angry') == False]
df = df[((df['date'] == '27-04') | (df['date'] == '28-04')) & (df['emo'] == 'fear') == False]
df = df[((df['date'] == '26-04') & (df['emo'] == 'sad')) == False]

features = list(df.columns)
features.remove('emo')
features.remove('emo value')
features.remove('date')
print(features)

for i in features:
    emo_regplot(i, 'from ' + i, '-from' + i)
