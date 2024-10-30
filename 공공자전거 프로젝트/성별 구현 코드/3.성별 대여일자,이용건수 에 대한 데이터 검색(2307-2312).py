import pandas as pd

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
A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  bicycle_selected['성별'] = bicycle_selected['성별'].replace({'남성': 'M', '여성': 'F'})
남성('M')이 자전거를 가장 많이 이용한 날짜와 이용건수:
           대여일자  total_rentals
267  2023-09-22        88720.0

남성('M')이 자전거를 가장 적게 이용한 날짜와 이용건수:
           대여일자  total_rentals
224  2023-08-10         5263.0

여성('F')이 자전거를 가장 많이 이용한 날짜와 이용건수:
          대여일자  total_rentals
83  2023-09-22        57957.0

여성('F')이 자전거를 가장 적게 이용한 날짜와 이용건수:
          대여일자  total_rentals
40  2023-08-10         1331.0

남성('M')의 평균 이용건수:
            대여일자  average_rentals
184  2023-07-01             1.10
185  2023-07-02             1.10
186  2023-07-03             1.16
187  2023-07-04             1.13
188  2023-07-05             1.16
..          ...              ...
363  2023-12-27             1.09
364  2023-12-28             1.08
365  2023-12-29             1.08
366  2023-12-30             1.03
367  2023-12-31             1.04

[184 rows x 2 columns]

여성('F')의 평균 이용건수:
            대여일자  average_rentals
0    2023-07-01             1.09
1    2023-07-02             1.09
2    2023-07-03             1.13
3    2023-07-04             1.10
4    2023-07-05             1.14
..          ...              ...
179  2023-12-27             1.06
180  2023-12-28             1.06
181  2023-12-29             1.06
182  2023-12-30             1.01
183  2023-12-31             1.03

[184 rows x 2 columns]
'''