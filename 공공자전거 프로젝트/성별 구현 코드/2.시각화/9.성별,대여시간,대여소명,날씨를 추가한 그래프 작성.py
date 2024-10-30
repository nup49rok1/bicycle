import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import requests
from datetime import datetime

# 한글 폰트 설정
font_path = "C:\\Windows\\Fonts\\malgun.ttf"  # Windows 시스템에서의 Malgun Gothic 폰트 경로
font_prop = fm.FontProperties(fname=font_path, size=12)
plt.rcParams['font.family'] = font_prop.get_name()

# 기상청 API 설정
API_KEY = 'xMcVxJh2IMEZhKVnXsN8IHEcB6hHTcenBpHRZPtTBnmKcDmzy1briRf9YrK856b7LwunYhcxyPBre9g0WMAdJw%3D%3D'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'
CITY_NAME = 'Seoul'

# 기상청 날씨 데이터 가져오기
def get_weather_data(date):
    params = {
        'q': CITY_NAME,
        'appid': API_KEY,
        'units': 'metric',
        'dt': int(date.timestamp())
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# 파일 경로 설정
path_bicycle = './select/서울특별시 공공자전거 이용정보(시간대별)_2301-2306.csv'
path_station = './select/서울특별시 공공자전거 대여소별 이용정보(월별)_23.1-6.csv'

# 데이터 불러오기
bicycle = pd.read_csv(path_bicycle, encoding='utf-8')
station = pd.read_csv(path_station, encoding='cp949')

# 두 데이터프레임 병합 ('대여소명'을 기준으로 병합)
merged_data = pd.merge(bicycle, station[['대여소명', '자치구']], on='대여소명', how='left')

# NaN 값이 있는 행 제거
merged_data.dropna(subset=['자치구'], inplace=True)

# 데이터의 컬럼 이름 확인
print("Merged Data Columns:", merged_data.columns)

# 필요한 컬럼 선택 (성별, 대여소명, 대여시간, 대여일시)
if '대여일자' in merged_data.columns:
    data_subset = merged_data[['성별', '대여소명', '대여시간', '대여일자']]
else:
    raise KeyError("Merged data does not contain '대여일시' column. Please check your CSV files.")

# 결측치 제거
data_subset.dropna(inplace=True)

# 성별 '남성'을 'M', '여성'을 'F'로 변경
data_subset['성별'] = data_subset['성별'].replace({'남성': 'M', '여성': 'F'})

# 대여일시를 datetime 형식으로 변환
data_subset['대여일자'] = pd.to_datetime(data_subset['대여일자'])

# 대여일시에서 요일 추출
data_subset['요일'] = data_subset['대여일자'].dt.day_name()

# 대여소명별 대여시간 합산
grouped_data = data_subset.groupby(['대여소명', '성별', '요일', '대여일자']).agg({'대여시간': 'sum'}).reset_index()

# 대여시간 기준으로 상위 20개 대여소명 추출
top_20_stations = grouped_data.groupby('대여소명')['대여시간'].sum().nlargest(20).index
top_20_data = grouped_data[grouped_data['대여소명'].isin(top_20_stations)]

# 날씨 데이터 추가
weather_data = []
for _, row in top_20_data.iterrows():
    date = row['대여일자']
    weather_info = get_weather_data(date)
    if weather_info:
        weather_data.append({
            '대여소명': row['대여소명'],
            '성별': row['성별'],
            '대여시간': row['대여시간'],
            '요일': row['요일'],
            '날씨': weather_info['weather'][0]['description'],
            '온도': weather_info['main']['temp']
        })
    else:
        weather_data.append({
            '대여소명': row['대여소명'],
            '성별': row['성별'],
            '대여시간': row['대여시간'],
            '요일': row['요일'],
            '날씨': None,
            '온도': None
        })

weather_df = pd.DataFrame(weather_data)

# 그래프 그리기
plt.figure(figsize=(14, 8))

# 막대 그래프: 대여소별 대여시간 (성별 기준)
sns.barplot(data=weather_df, 
            x='대여소명', y='대여시간', 
            hue='성별', 
            palette='muted', 
            alpha=0.6)

# 각 막대 위에 수치 표시
for p in plt.gca().patches:
    value = int(p.get_height())
    plt.annotate(f'{value:,}', 
                 (p.get_x() + p.get_width() / 2., p.get_height()), 
                 ha='center', va='bottom', fontsize=10)

# y축 라벨 및 타이틀 설정
plt.title('성별에 따른 상위 20개 대여소별 대여시간 및 날씨')
plt.ylabel('대여시간 (시간)')

plt.xticks(rotation=45)  # x축 라벨 회전

# 범례 설정
plt.legend(title='성별', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)

plt.tight_layout()
plt.show()