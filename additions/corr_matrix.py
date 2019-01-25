# построение матриц корреляций
import pandas as pd
import seaborn as sns
import os
from matplotlib import pyplot
sns.set_style('white')
sns.set(font_scale=1.5)


def emo_matrix(emo, features, folder):
    df1 = df[['emo', 'emo value'] + features]
    pyplot.figure(figsize=(10, 6))
    corr_matrix = df1[df1['emo'] == emo].corr()
    sns.heatmap(corr_matrix, annot=True)
    if not os.path.exists('diagrams/' + folder): os.makedirs('diagrams/' + folder)
    pyplot.savefig('diagrams/' + folder + '/' + emo + '.png')
    pyplot.clf()


df = pd.read_excel('../data.xlsx', sheet_name='emotions')
df = df[(df['emo'] != 'neutral') & (df['emo'] != 'disgust')]

# удаление neutral, disgust и выбросов
df = df[df['emo'] != 'disgust']
df = df[df['date'] != '27-05']
df = df[(((df['date'] == '24-04') | (df['date'] == '25-04')) & (df['emo'] == 'angry')) == False]
df = df[(((df['date'] == '27-04') | (df['date'] == '28-04')) & (df['emo'] == 'fear')) == False]
# df = df[((df['date'] == '26-04') & (df['emo'] == 'sad')) == False]

# angry_features = ['avg time', 'morning', 'day', 'evening', 'sem-train', 'meeting', 'conference', 'open']
angry_features = ['week day', 'meeting', 'sem-train', 'half-1']
fear_features = ['avg time', 'day', 'rain', 'pressure', 'sem-train', 'for+strat+bus']
sad_features = ['morning', 'lection', 'rain', 'close']
sad_features = ['morning', 'rain', 'lection', 'close']

happy_features = ['week day', 'avg temp', 'pressure','meeting', 'sem-train', 'for+strat+bus']
surprise_features = ['avg time', 'cloud', 'rain', 'lection', 'close']
d = {'angry': angry_features, 'fear': fear_features, 'happy': happy_features,
     'sad': sad_features, 'surprise': surprise_features}

for i in d.keys():
    emo_matrix(i, d[i], 'heatmaps')

