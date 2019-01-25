import pandas as pd
from sklearn.tree import DecisionTreeRegressor


# обучение дерева
def emo_predict(emo, target_date, features, depth):
    df1 = df[(df['emo'] == emo) & (df['date'] != target_date)]
    xtrain = df1[features]
    ytrain = df1['emo value']
    rtree = DecisionTreeRegressor(max_depth=depth)
    rtree.fit(xtrain, ytrain)
    target_features = []
    for i in features:
        for j in df[(df['emo'] == emo) & (df['date'] == target_date)][i]:
            target_features.append(j)
    answer = rtree.predict([target_features])[0]
    true_answer = df[(df['emo'] == emo) & (df['date'] == target_date)]['emo value'].values[0]
    return [emo, target_date, round(true_answer,2), round(answer,2), round((true_answer - answer)**2,2)]


# признаки для обучения
angry_features = ['week day', 'meeting', 'sem-train', 'half-1', 7]
fear_features = ['day', 'pressure', 'sem-train', 'for+strat+bus', 'open', 8]
sad_features = ['morning', 'rain', 'lection', 'close', 5]
happy_features = ['week day', 'avg temp', 'pressure', 'meeting', 'sem-train', 'for+strat+bus', 5]
surprise_features = ['avg time', 'cloud', 'lection', 'close', 5]

d = {'angry': angry_features, 'fear': fear_features, 'happy': happy_features,
     'sad': sad_features, 'surprise': surprise_features}
df = pd.read_excel('data.xlsx', sheet_name='emotions')
# удаление neutral, disgust и выбросов
df = df[df['emo'] != 'disgust']
df = df[df['date'] != '27-05']
df = df[((df['date'] == '24-04') | (df['date'] == '25-04')) & (df['emo'] == 'angry') == False]
df = df[((df['date'] == '27-04') | (df['date'] == '28-04')) & (df['emo'] == 'fear') == False]
# df = df[((df['date'] == '26-04') & (df['emo'] == 'sad')) == False]

# вызов функции emo_predict для каждой эмоции, обучение и прогнозирование для 12 мая
emo_day_list = []
k = '12-05'
total_answer = 0

neutral = 100
for i in df[(df['date'] == k) & (df['emo'] != 'neutral')]['emo'].unique():
    x = emo_predict(i,k,d[i][:-1],d[i][-1])
    # выбор только полей "эмоция", "дата", "ответ"
    emo_day_list.append(x[:2] + x[3:4])
    total_answer += x[3]

neutral -= total_answer
if neutral<0: neutral=0
neutral_true = df[(df['emo'] == 'neutral') & (df['date'] == k)]['emo value'].values[0]
emo_day_list.append(['neutral', k, neutral])

# сохранение результатов в файл excel
results = pd.DataFrame(emo_day_list, columns=['emo', 'date', 'answer'])
writer = pd.ExcelWriter('results.xlsx')
results.to_excel(writer,'results')
writer.save()

print(results)