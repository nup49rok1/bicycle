
#성별 대여일자,이동거리,이용건수를 확인하는 그래프 작성(2301-2306)
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 한글 폰트 설정
font_path = "C:\\Windows\\Fonts\\malgun.ttf"  # Windows 시스템에서의 Malgun Gothic 폰트 경로
font_prop = fm.FontProperties(fname=font_path, size=12)
plt.rcParams['font.family'] = font_prop.get_name()

# 데이터 읽기
path_bicycle = './select/서울특별시 공공자전거 이용정보(시간대별)_2301-2306.csv'
data = pd.read_csv(path_bicycle, encoding='utf-8')

# 필요한 컬럼 선택 (성별, 대여일자, 이용건수)
data_subset = data[['성별', '대여일자', '이용건수']]

# 결측치 제거
data_subset.dropna(inplace=True)

# 성별 '남성'을 'M', '여성'을 'F'로 변경
data_subset['성별'] = data_subset['성별'].replace({'남성': 'M', '여성': 'F'})

# 성별과 대여일자별로 이용건수를 합산
grouped_data = data_subset.groupby(['성별', '대여일자']).agg({
    '이용건수': 'sum'
}).reset_index()

# 날짜를 datetime으로 변환
grouped_data['대여일자'] = pd.to_datetime(grouped_data['대여일자'])

# 요일로 변환 (한글로 설정)
grouped_data['요일'] = grouped_data['대여일자'].dt.day_name()
day_translation = {
    'Monday': '월요일',
    'Tuesday': '화요일',
    'Wednesday': '수요일',
    'Thursday': '목요일',
    'Friday': '금요일',
    'Saturday': '토요일',
    'Sunday': '일요일'
}
grouped_data['요일'] = grouped_data['요일'].map(day_translation)

# 성별 데이터 분리
male_data = grouped_data[grouped_data['성별'] == 'M']
female_data = grouped_data[grouped_data['성별'] == 'F']

# 이중 축 그래프 생성
plt.figure(figsize=(12, 6))

# 이용건수의 바 그래프
sns.barplot(data=male_data, x='요일', y='이용건수', color='blue', alpha=0.6, label='남성 이용건수')
sns.barplot(data=female_data, x='요일', y='이용건수', color='pink', alpha=0.6, label='여성 이용건수')

# 그래프 꾸미기
plt.title('성별에 따른 요일별 이용건수')
plt.xlabel('요일')
plt.ylabel('이용건수')
plt.xticks(rotation=45)

# 범례 설정
plt.legend()

plt.tight_layout()
plt.show()
