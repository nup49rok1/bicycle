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

# 기상청 날씨 데이터 읽기
path_weather = './select/기상청날씨정보(2301-2312).csv'
try:
    weather_data = pd.read_csv(path_weather, encoding='utf-8')
except UnicodeDecodeError:
    weather_data = pd.read_csv(path_weather, encoding='latin1')

# 컬럼 이름 확인
print("날씨 데이터의 컬럼 이름:", weather_data.columns)

# 3번째 항목을 '일시'로 부여
if len(weather_data.columns) > 2:
    weather_data['일시'] = weather_data.iloc[:, 2]  # 3번째 항목을 '일시'로 설정
else:
    raise KeyError("3번째 항목이 존재하지 않습니다.")

# 강수량(mm)과 기온(°C) 임시 필드 설정
if len(weather_data.columns) > 4:
    weather_data['강수량(mm)'] = weather_data.iloc[:, 3]  # 4번째 항목을 '강수량(mm)'으로 설정
    weather_data['기온(°C)'] = weather_data.iloc[:, 4]  # 5번째 항목을 '기온(°C)'으로 설정
else:
    raise KeyError("4번째 또는 5번째 항목이 존재하지 않습니다.")

# '일시' 컬럼을 datetime으로 변환
weather_data['일시'] = pd.to_datetime(weather_data['일시'], errors='coerce')

# 오류가 발생한 데이터 출력
invalid_dates = weather_data[weather_data['일시'].isna()]
if not invalid_dates.empty:
    print("형식이 맞지 않는 데이터:\n", invalid_dates)

# 오전 6시부터 오후 11시까지의 데이터만 필터링
filtered_weather = weather_data[(weather_data['일시'].dt.hour >= 6) & (weather_data['일시'].dt.hour <= 23)]

# 필터링된 데이터 확인
if filtered_weather.empty:
    print("필터링된 날씨 데이터가 없습니다.")
else:
    print("필터링된 날씨 데이터:\n", filtered_weather)

# 필요한 컬럼 선택 (성별, 대여일자, 대여시간, 연령대코드)
data_subset = data[['성별', '대여일자', '대여시간', '연령대코드']]

# 결측치 제거
data_subset.dropna(inplace=True)

# 성별 '남성'을 'M', '여성'을 'F'로 변경
data_subset['성별'] = data_subset['성별'].replace({'남성': 'M', '여성': 'F'})

# 날짜를 datetime으로 변환
data_subset['대여일자'] = pd.to_datetime(data_subset['대여일자'])

# 요일로 변환
data_subset['요일'] = data_subset['대여일자'].dt.day_name()
day_translation = {
    'Monday': '월요일',
    'Tuesday': '화요일',
    'Wednesday': '수요일',
    'Thursday': '목요일',
    'Friday': '금요일',
    'Saturday': '토요일',
    'Sunday': '일요일'
}
data_subset['요일'] = data_subset['요일'].map(day_translation)

# 성별과 연령대코드별로 대여시간을 합산
grouped_data = data_subset.groupby(['성별', '연령대코드']).agg({'대여시간': 'sum'}).reset_index()

# 요일별 대여시간 합산
weekday_data = data_subset.groupby(['요일', '성별']).agg({'대여시간': 'sum'}).reset_index()

# 요일 순서 지정
weekday_data['요일'] = pd.Categorical(weekday_data['요일'], 
                                      categories=['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일'], 
                                      ordered=True)

# 날씨 데이터에서 요일별 기온과 강수량 추가
filtered_weather['요일'] = filtered_weather['일시'].dt.day_name().map(day_translation)

# 요일별 평균 기온과 강수량 계산
weather_summary = filtered_weather.groupby('요일').agg({'기온(°C)': 'mean', '강수량(mm)': 'mean'}).reset_index()

# 요일 데이터 병합
combined_data = pd.merge(weekday_data, weather_summary, on='요일', how='outer')

# 그래프 그리기
plt.figure(figsize=(14, 8))

# 첫 번째 그래프: 연령대코드별 대여시간 (막대 그래프)
sns.barplot(data=grouped_data, 
            x='연령대코드', y='대여시간', 
            hue='성별', 
            palette='muted', 
            alpha=0.6)

# 각 막대 위에 수치 표시
for p in plt.gca().patches:
    value = int(p.get_height())
    plt.annotate(f'{value:,}', 
                 (p.get_x() + p.get_width() / 2., p.get_height()), 
                 ha='center', va='bottom', fontsize=10)

# 두 번째 그래프: 요일별 대여시간 (선 그래프)
ax2 = plt.gca().twinx()  # y축을 공유하기 위한 설정
sns.lineplot(data=combined_data, 
             x='요일', y='대여시간', 
             hue='성별', 
             marker='o', 
             ax=ax2)

# 날씨 정보 표시
for index, row in combined_data.iterrows():
    if pd.notna(row['기온(°C)']):
        plt.axhline(y=row['기온(°C)'], color='gray', linestyle='--', alpha=0.5)
        plt.text(0, row['기온(°C)'], f"{row['기온(°C)']}°C", color='gray', ha='right', va='bottom')

# y축 라벨 및 타이틀 설정
plt.title('성별에 따른 연령대코드별 대여시간과 요일별 대여시간 및 날씨 정보')
plt.ylabel('대여시간 (막대 그래프)')
ax2.set_ylabel('요일별 대여시간')  # 선 그래프 y축 라벨 설정

plt.xticks(rotation=45)  # x축 라벨 회전

# 범례 설정
bar_legend = plt.legend(title='성별', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
line_legend = ax2.legend(title='요일별 대여시간', loc='upper center', bbox_to_anchor=(0.5, -0.1), fontsize=10)

plt.tight_layout()
plt.show()
