#성별에 따른 자치구별 대여시간 그래프(2301-2306)
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 한글 폰트 설정
font_path = "C:\\Windows\\Fonts\\malgun.ttf"  # Windows 시스템에서의 Malgun Gothic 폰트 경로
font_prop = fm.FontProperties(fname=font_path, size=12)
plt.rcParams['font.family'] = font_prop.get_name()

# 파일 경로 설정
path_bicycle = './select/서울특별시 공공자전거 이용정보(시간대별)_2307-2312.csv'
path_station = './select/서울특별시 공공자전거 대여소별 이용정보(월별)_23.7-12.csv'

# 데이터 불러오기
bicycle = pd.read_csv(path_bicycle, encoding='utf-8')
station = pd.read_csv(path_station, encoding='cp949')

# 두 데이터프레임 병합 ('대여소명'을 기준으로 병합)
merged_data = pd.merge(bicycle, station[['대여소명', '자치구']], on='대여소명', how='left')

# NaN 값이 있는 행 제거
merged_data.dropna(subset=['자치구'], inplace=True)

# 필요한 컬럼 선택 (성별, 자치구, 대여시간, 연령대코드)
data_subset = merged_data[['성별', '자치구', '대여시간', '연령대코드']]

# 결측치 제거
data_subset.dropna(inplace=True)

# 성별 '남성'을 'M', '여성'을 'F'로 변경
data_subset['성별'] = data_subset['성별'].replace({'남성': 'M', '여성': 'F'})

# 자치구별 대여시간 합산
grouped_data = data_subset.groupby(['자치구', '성별']).agg({'대여시간': 'sum'}).reset_index()

# 그래프 그리기
plt.figure(figsize=(14, 8))

# 첫 번째 그래프: 자치구별 대여시간 (막대 그래프)
sns.barplot(data=grouped_data, 
            x='자치구', y='대여시간', 
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
plt.title('성별에 따른 자치구별 대여시간')
plt.ylabel('대여시간 (시간)')

plt.xticks(rotation=45)  # x축 라벨 회전

# 범례 설정
plt.legend(title='성별', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)

plt.tight_layout()
plt.show()
