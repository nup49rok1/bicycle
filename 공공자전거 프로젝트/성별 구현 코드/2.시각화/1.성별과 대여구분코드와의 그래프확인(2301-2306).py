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
data = pd.read_csv(path_bicycle)

# 성별과 대여구분코드 열 선택
data_subset = data[['성별', '대여구분코드']]

# 결측치 제거
data_subset.dropna(inplace=True)

# 성별과 대여구분코드의 점 그래프 생성
plt.figure(figsize=(12, 6))
ax = sns.countplot(data=data_subset, x='대여구분코드', hue='성별', palette='Set2')
plt.title('성별에 따른 대여구분코드 분포')
plt.xlabel('대여구분코드')
plt.ylabel('대여건수')
plt.legend(title='성별', labels=['여자', '남자'])
plt.xticks(rotation=45)

# 수치 표시
for p in ax.patches:
    ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='bottom', fontsize=10, color='black')

plt.tight_layout()
plt.show()
