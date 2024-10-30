import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 한글 폰트 설정
font_path = "C:\\Windows\\Fonts\\malgun.ttf"  # Windows 시스템에서의 Malgun Gothic 폰트 경로
font_prop = fm.FontProperties(fname=font_path, size=12)
plt.rcParams['font.family'] = font_prop.get_name()

# 데이터 읽기
path_bicycle = './select/서울특별시 공공자전거 이용정보(시간대별)_2401-2405.csv'
data = pd.read_csv(path_bicycle)

# 성별, 대여시간, 이용건수 열 선택
data_subset = data[['성별', '대여시간', '이용건수']]

# 결측치 제거
data_subset.dropna(inplace=True)

# 대여시간을 문자열로 변환 후, 적절한 형식으로 변환
def convert_time_format(time_str):
    try:
        return pd.to_datetime(time_str, format='%H:%M').hour
    except ValueError:
        return None  # 형식이 맞지 않으면 None 반환

data_subset['대여시간'] = data_subset['대여시간'].astype(str).apply(convert_time_format)

# None 값을 제거
data_subset.dropna(inplace=True)

# 성별과 대여시간, 이용건수로 데이터 집계
grouped_data = data_subset.groupby(['성별', '대여시간']).agg({'이용건수': 'sum'}).reset_index()

# 성별과 대여시간의 바 그래프 생성
plt.figure(figsize=(12, 6))
sns.barplot(data=grouped_data, x='대여시간', y='이용건수', hue='성별', palette='Set2')

# 수치 표시
for p in plt.gca().patches:
    plt.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                 ha='center', va='bottom', fontsize=10, color='black')

# 그래프 꾸미기
plt.title('성별에 따른 대여시간별 이용건수')
plt.xlabel('대여시간 (시)')
plt.ylabel('이용건수')
plt.xticks(range(0, 24))  # 0시부터 23시까지 표시
plt.legend(title='성별')
plt.tight_layout()

# 그래프 표시
plt.show()
