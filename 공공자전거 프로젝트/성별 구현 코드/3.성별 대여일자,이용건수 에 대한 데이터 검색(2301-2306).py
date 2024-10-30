import pandas as pd

# 파일 경로
path = './select/서울특별시 공공자전거 이용정보(시간대별)_2301-2306.csv'

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

# 'M'과 'F' 데이터를 각각 분리
male_data = gender_date_stats[gender_date_stats['성별'] == 'M']
female_data = gender_date_stats[gender_date_stats['성별'] == 'F']

# 남성이 자전거를 가장 많이 이용한 날짜 (최대 이용건수)
max_male_usage = male_data[male_data['total_rentals'] == male_data['total_rentals'].max()]

# 남성이 자전거를 가장 적게 이용한 날짜 (최소 이용건수)
min_male_usage = male_data[male_data['total_rentals'] == male_data['total_rentals'].min()]

# 여성이 자전거를 가장 많이 이용한 날짜 (최대 이용건수)
max_female_usage = female_data[female_data['total_rentals'] == female_data['total_rentals'].max()]

# 여성이 자전거를 가장 적게 이용한 날짜 (최소 이용건수)
min_female_usage = female_data[female_data['total_rentals'] == female_data['total_rentals'].min()]

# 성별별로 최대, 최소, 평균 이용건수 및 가장 많이/적게 이용한 날짜 출력
print("남성('M')이 자전거를 가장 많이 이용한 날짜와 이용건수:")
print(max_male_usage[['대여일자', 'total_rentals']])
print("\n남성('M')이 자전거를 가장 적게 이용한 날짜와 이용건수:")
print(min_male_usage[['대여일자', 'total_rentals']])

print("\n여성('F')이 자전거를 가장 많이 이용한 날짜와 이용건수:")
print(max_female_usage[['대여일자', 'total_rentals']])
print("\n여성('F')이 자전거를 가장 적게 이용한 날짜와 이용건수:")
print(min_female_usage[['대여일자', 'total_rentals']])

# 성별별로 평균 이용건수 출력 (소수점 2자리까지)
print("\n남성('M')의 평균 이용건수:\n", male_data[['대여일자', 'average_rentals']])
print("\n여성('F')의 평균 이용건수:\n", female_data[['대여일자', 'average_rentals']])
'''
See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  bicycle_selected['성별'] = bicycle_selected['성별'].replace({'남성': 'M', '여성': 'F'})
남성('M')이 자전거를 가장 많이 이용한 날짜와 이용건수:
           대여일자  total_rentals
344  2023-06-13          84505

남성('M')이 자전거를 가장 적게 이용한 날짜와 이용건수:
           대여일자  total_rentals
328  2023-05-28           2697

여성('F')이 자전거를 가장 많이 이용한 날짜와 이용건수:
           대여일자  total_rentals
163  2023-06-13          55488

여성('F')이 자전거를 가장 적게 이용한 날짜와 이용건수:
           대여일자  total_rentals
147  2023-05-28            760

남성('M')의 평균 이용건수:
            대여일자  average_rentals
181  2023-01-01             1.05
182  2023-01-02             1.08
183  2023-01-03             1.08
184  2023-01-04             1.08
185  2023-01-05             1.09
..          ...              ...
357  2023-06-26             1.10
358  2023-06-27             1.17
359  2023-06-28             1.16
360  2023-06-29             1.07
361  2023-06-30             1.14

[181 rows x 2 columns]

여성('F')의 평균 이용건수:
            대여일자  average_rentals
0    2023-01-01             1.05
1    2023-01-02             1.06
2    2023-01-03             1.06
3    2023-01-04             1.06
4    2023-01-05             1.06
..          ...              ...
176  2023-06-26             1.06
177  2023-06-27             1.14
178  2023-06-28             1.13
179  2023-06-29             1.04
180  2023-06-30             1.11

[181 rows x 2 columns]
'''