
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import pymysql
from kiwipiepy import Kiwi
from kiwipiepy.utils import Stopwords
from wordcloud import WordCloud
from PIL import Image

# 데이터베이스에서 크롤링한 목록 가져오기
connection = pymysql.connect(
    host='localhost',
    database='playstore',
    user='root',
    charset='utf8mb4'
)

cursor = connection.cursor()
cursor.execute('SELECT * FROM apps')
results = cursor.fetchall()
cursor.close()

for v in results:
    print(v)

# init 
init = {'mabo':None, 'kokkiri':None, 'calm':None}

# 데이터베이스에서 수집한 리뷰 가져오기
ids = {'mabo':7, 'kokkiri':8, 'calm':11}
reviews = init

cursor = connection.cursor()
for key, value in ids.items():
    cursor.execute('SELECT * FROM reviews WHERE app_id = %s', value)
    result = cursor.fetchall()
    reviews[key] = pd.DataFrame(result)
cursor.close()

# column 이름 바꿔주기
for key,value in reviews.items():
    reviews[key].columns = ['id', 'app_id', 'name', 'rating', 'reviewed_at', 'content', 'useful_count', 'created_at']
    
# reviewed_at date로 변경해주기
for key, value in reviews.items():
    reviews[key]['reviewed_at'] = pd.to_datetime(reviews[key]['reviewed_at'])

# 년, 월별로 리뷰 개수 확인
monthly_count = {'calm':None, 'mabo':None,'kokkiri':None}
df = pd.DataFrame()
for key, value in monthly_count.items():
    monthly_count[key] = reviews[key].groupby(reviews[key]['reviewed_at'].dt.strftime("%Y-%m"))['id'].count()
    df[key] = monthly_count[key]


# 열 <-> 행
df.transpose()

# 정렬
df.sort_index(ascending=True,inplace=True)

# na 드랍.
droped = df.dropna()


# 그래프
fig, ax = plt.subplots(figsize=(15, 2.7), layout='constrained')


ax.plot(droped['mabo'], label='mabo') 
ax.plot(droped['kokkiri'], label='kokkiri')
ax.plot(droped['calm'], label='calm')

# 표 꾸미기
ax.set_xticks(droped['calm'].index[::3]) 
ax.legend()
ax.set_title("Monthly review count")
ax.set_ylabel("review count")
