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
data = pd.read_csv(path_bicycle, encoding='utf-8')

# 필요한 컬럼 선택 (성별, 대여일자, 이용건수, 연령대코드)
data_subset = data[['성별', '대여일자', '이용건수', '연령대코드']]

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

# 성별과 연령대코드별로 이용건수를 합산
grouped_data = data_subset.groupby(['성별', '연령대코드']).agg({'이용건수': 'sum'}).reset_index()

# 요일별 이용건수 합산
weekday_data = data_subset.groupby(['요일', '성별']).agg({'이용건수': 'sum'}).reset_index()

# 요일 순서 지정
weekday_data['요일'] = pd.Categorical(weekday_data['요일'], 
                                      categories=['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일'], 
                                      ordered=True)

# 그래프 그리기
plt.figure(figsize=(14, 8))

# 첫 번째 그래프: 연령대코드별 이용건수 (막대 그래프)
sns.barplot(data=grouped_data, 
            x='연령대코드', y='이용건수', 
            hue='성별', 
            palette='muted', 
            alpha=0.6)

# 각 막대 위에 수치 표시
for p in plt.gca().patches:
    value = int(p.get_height())
    plt.annotate(f'{value:,}', 
                 (p.get_x() + p.get_width() / 2., p.get_height()), 
                 ha='center', va='bottom', fontsize=10)

# 두 번째 그래프: 요일별 이용건수 (선 그래프)
ax2 = plt.gca().twinx()  # y축을 공유하기 위한 설정
sns.lineplot(data=weekday_data, 
             x='요일', y='이용건수', 
             hue='성별', 
             marker='o', 
             ax=ax2)

# y축 라벨 및 타이틀 설정
plt.title('성별에 따른 연령대코드별 이용건수와 요일별 이용건수(2401-2405)')
plt.ylabel('이용건수 (막대 그래프)')
ax2.set_ylabel('요일별 이용건수')  # 선 그래프 y축 라벨 설정

plt.xticks(rotation=45)  # x축 라벨 회전

# 범례 설정
bar_legend = plt.legend(title='성별', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
line_legend = ax2.legend(title='요일별 이용건수', loc='upper center', bbox_to_anchor=(0.5, -0.1), fontsize=10)

plt.tight_layout()
plt.show()

# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# import matplotlib.font_manager as fm

# # 한글 폰트 설정
# font_path = "C:\\Windows\\Fonts\\malgun.ttf"  # Windows 시스템에서의 Malgun Gothic 폰트 경로
# font_prop = fm.FontProperties(fname=font_path, size=12)
# plt.rcParams['font.family'] = font_prop.get_name()

# # 데이터 읽기
# path_bicycle = './select/서울특별시 공공자전거 이용정보(시간대별)_2301-2306.csv'
# data = pd.read_csv(path_bicycle, encoding='utf-8')

# # 필요한 컬럼 선택 (성별, 대여일자, 이용건수, 연령대코드)
# data_subset = data[['성별', '대여일자', '이용건수', '연령대코드']]

# # 결측치 제거
# data_subset.dropna(inplace=True)

# # 성별 '남성'을 'M', '여성'을 'F'로 변경
# data_subset['성별'] = data_subset['성별'].replace({'남성': 'M', '여성': 'F'})

# # 날짜를 datetime으로 변환
# data_subset['대여일자'] = pd.to_datetime(data_subset['대여일자'])

# # 성별과 연령대코드별로 이용건수를 합산
# grouped_data = data_subset.groupby(['성별', '연령대코드']).agg({
#     '이용건수': 'sum'
# }).reset_index()

# # 그래프 그리기
# plt.figure(figsize=(14, 8))

# # 성별을 기준으로 그래프 그리기
# bar_plot = sns.barplot(data=grouped_data, 
#                        x='연령대코드', y='이용건수', 
#                        hue='성별', 
#                        palette='muted',  # 색상 팔레트 설정
#                        alpha=0.6)

# # 각 막대 위에 수치 표시
# for p in bar_plot.patches:
#     value = int(p.get_height())
#     bar_plot.annotate(f'{value:,}',  # 세 자리마다 쉼표 추가
#                       (p.get_x() + p.get_width() / 2., p.get_height()), 
#                       ha='center', va='bottom', fontsize=10)

# # 그래프 꾸미기
# plt.title('성별에 따른 연령대코드별 이용건수 (막대 그래프) 2301-2306')
# plt.xlabel('연령대 코드')
# plt.ylabel('이용건수')
# plt.legend(title='성별', bbox_to_anchor=(1.05, 1), loc='upper left')

# plt.tight_layout()
# plt.show()


# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# import matplotlib.font_manager as fm

# # 한글 폰트 설정
# font_path = "C:\\Windows\\Fonts\\malgun.ttf"  # Windows 시스템에서의 Malgun Gothic 폰트 경로
# font_prop = fm.FontProperties(fname=font_path, size=12)
# plt.rcParams['font.family'] = font_prop.get_name()

# # 데이터 읽기
# path_bicycle = './select/서울특별시 공공자전거 이용정보(시간대별)_2301-2306.csv'
# data = pd.read_csv(path_bicycle, encoding='utf-8')

# # 필요한 컬럼 선택 (성별, 대여일자, 이용건수, 연령대코드)
# data_subset = data[['성별', '대여일자', '이용건수', '연령대코드']]

# # 결측치 제거
# data_subset.dropna(inplace=True)

# # 성별 '남성'을 'M', '여성'을 'F'로 변경
# data_subset['성별'] = data_subset['성별'].replace({'남성': 'M', '여성': 'F'})

# # 날짜를 datetime으로 변환
# data_subset['대여일자'] = pd.to_datetime(data_subset['대여일자'])

# # 요일로 변환 (한글로 설정)
# data_subset['요일'] = data_subset['대여일자'].dt.day_name()
# day_translation = {
#     'Monday': '월요일',
#     'Tuesday': '화요일',
#     'Wednesday': '수요일',
#     'Thursday': '목요일',
#     'Friday': '금요일',
#     'Saturday': '토요일',
#     'Sunday': '일요일'
# }
# data_subset['요일'] = data_subset['요일'].map(day_translation)

# # 성별, 요일별로 이용건수를 합산
# grouped_data = data_subset.groupby(['성별', '요일']).agg({
#     '이용건수': 'sum'
# }).reset_index()

# # 그래프 그리기
# plt.figure(figsize=(14, 8))

# # 성별을 기준으로 그래프 그리기
# bar_plot = sns.barplot(data=grouped_data, 
#                        x='요일', y='이용건수', 
#                        hue='성별', 
#                        palette='muted',  # 색상 팔레트 설정
#                        alpha=0.6)

# # 각 막대 위에 수치 표시
# for p in bar_plot.patches:
#     value = int(p.get_height())
#     bar_plot.annotate(f'{value:,}',  # 세 자리마다 쉼표 추가
#                       (p.get_x() + p.get_width() / 2., p.get_height()), 
#                       ha='center', va='bottom', fontsize=10)

# # 그래프 꾸미기
# plt.title('성별에 따른 요일별 이용건수 (막대 그래프) 2301-2306')
# plt.xlabel('요일')
# plt.ylabel('이용건수')
# plt.legend(title='성별', bbox_to_anchor=(1.05, 1), loc='upper left')

# plt.tight_layout()
# plt.show()
