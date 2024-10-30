import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 한글 폰트 설정
font_path = "C:\\Windows\\Fonts\\malgun.ttf"  # Windows 시스템에서의 Malgun Gothic 폰트 경로
font_prop = fm.FontProperties(fname=font_path, size=12)
plt.rcParams['font.family'] = font_prop.get_name()

# 데이터 읽기
path_bicycle = './select/서울특별시 공공자전거 이용정보(시간대별)_2307-2312.csv'
data = pd.read_csv(path_bicycle, encoding='utf-8')

# 필요한 컬럼 선택 (성별, 대여일자, 이용건수, 연령대코드)
data_subset = data[['성별', '대여일자', '이용건수', '연령대코드']]

# 결측치 제거
data_subset.dropna(inplace=True)

# 성별 '남성'을 'M', '여성'을 'F'로 변경
data_subset['성별'] = data_subset['성별'].replace({'남성': 'M', '여성': 'F'})

# 성별, 연령대코드, 대여일자별로 이용건수를 합산
grouped_data = data_subset.groupby(['성별', '연령대코드', '대여일자']).agg({
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

# 그래프 그리기
plt.figure(figsize=(14, 8))

# 성별과 연령대코드를 기준으로 그래프 그리기
for gender in ['M', 'F']:
    gender_data = grouped_data[grouped_data['성별'] == gender]
    
    # 연령대코드별로 이용건수를 요약
    sns.lineplot(data=gender_data, 
                 x='연령대코드', y='이용건수', 
                 label='남성' if gender == 'M' else '여성',
                 marker='o')

# 그래프 꾸미기
plt.title('성별 및 연령대에 따른 이용건수 (선 그래프) 2307-2312')
plt.xlabel('연령대 코드')
plt.ylabel('이용건수')
plt.xticks(rotation=45)  # x축 라벨 회전
plt.legend(title='성별', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()
