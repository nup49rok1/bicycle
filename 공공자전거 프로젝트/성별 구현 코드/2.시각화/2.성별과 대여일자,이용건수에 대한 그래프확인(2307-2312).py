import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 한글 폰트 설정
font_path = "C:\\Windows\\Fonts\\malgun.ttf"  # Windows 시스템에서의 Malgun Gothic 폰트 경로
font_prop = fm.FontProperties(fname=font_path, size=12)
plt.rcParams['font.family'] = font_prop.get_name()

# 파일 경로
path = './select/서울특별시 공공자전거 이용정보(시간대별)_2307-2312.csv'

# CSV 파일 읽기 (한글 인코딩 처리)
bicycle = pd.read_csv(path, encoding='utf-8')

# 필요한 컬럼만 추출 (성별, 대여일자, 이용건수)
bicycle_selected = bicycle[['성별', '대여일자', '이용건수']]

# 성별 'M'과 'F'로 처리하기 (남성 'M', 여성 'F')
bicycle_selected['성별'] = bicycle_selected['성별'].replace({'남성': 'M', '여성': 'F'})

# 성별과 대여일자별로 이용건수를 그룹화하여 합계, 평균, 최대, 최소 계산
gender_date_stats = bicycle_selected.groupby(['성별', '대여일자']).agg(
    total_rentals=('이용건수', 'sum'),
    average_rentals=('이용건수', 'mean'),
    max_rentals=('이용건수', 'max'),
    min_rentals=('이용건수', 'min')
).reset_index()

# 소수점 둘째 자리까지 표시하도록 변환
gender_date_stats['average_rentals'] = gender_date_stats['average_rentals'].round(2)
gender_date_stats['total_rentals'] = gender_date_stats['total_rentals'].round(2)
gender_date_stats['max_rentals'] = gender_date_stats['max_rentals'].round(2)
gender_date_stats['min_rentals'] = gender_date_stats['min_rentals'].round(2)

# 성별별 총 이용건수와 평균 이용건수를 시각화
plt.figure(figsize=(12, 6))

# 총 이용건수 바 그래프
plt.subplot(1, 2, 1)
total_rentals_data = gender_date_stats.groupby('성별').agg(total_rentals=('total_rentals', 'sum')).reset_index()
bar_total = sns.barplot(data=total_rentals_data, x='성별', y='total_rentals', palette='Set2')
plt.title('성별 총 이용건수')
plt.xlabel('성별')
plt.ylabel('총 이용건수')

# 수치 표시
for p in bar_total.patches:
    bar_total.annotate(f'{p.get_height():,.0f}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                       ha='center', va='bottom', fontsize=10, color='black')

# 평균 이용건수 바 그래프
plt.subplot(1, 2, 2)
average_rentals_data = gender_date_stats.groupby('성별').agg(average_rentals=('average_rentals', 'mean')).reset_index()
bar_average = sns.barplot(data=average_rentals_data, x='성별', y='average_rentals', palette='Set2')
plt.title('성별 평균 이용건수(2307-2312)')
plt.xlabel('성별')
plt.ylabel('평균 이용건수')

# 수치 표시
for p in bar_average.patches:
    bar_average.annotate(f'{p.get_height():,.2f}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                         ha='center', va='bottom', fontsize=10, color='black')

plt.tight_layout()
plt.show()
