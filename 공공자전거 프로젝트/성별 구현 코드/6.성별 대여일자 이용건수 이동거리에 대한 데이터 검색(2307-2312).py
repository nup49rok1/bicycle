import pandas as pd

# 파일 경로
path = './select/서울특별시 공공자전거 이용정보(시간대별)_2307-2312.csv'

# CSV 파일 읽기 (한글 인코딩 처리)
bicycle = pd.read_csv(path, encoding='utf-8')

# 필요한 컬럼만 추출 (성별, 대여일자, 이용건수, 이동거리)
bicycle_selected = bicycle[['성별', '대여일자', '이용건수', '이동거리(M)']]

# 성별 'M'과 'F'로 처리하기 (남성 'M', 여성 'F')
bicycle_selected['성별'] = bicycle_selected['성별'].replace({'남성': 'M', '여성': 'F'})

# 성별과 대여일자별로 이용건수 및 이동거리를 그룹화하여 합계, 평균, 최대, 최소 계산
gender_date_stats = bicycle_selected.groupby(['성별', '대여일자']).agg(
    total_rentals=('이용건수', 'sum'),
    average_rentals=('이용건수', 'mean'),
    max_rentals=('이용건수', 'max'),
    min_rentals=('이용건수', 'min'),
    total_distance=('이동거리(M)', 'sum'),
    average_distance=('이동거리(M)', 'mean'),
    max_distance=('이동거리(M)', 'max'),
    min_distance=('이동거리(M)', 'min')
).reset_index()

# 소수점 둘째 자리까지 표시하도록 변환
gender_date_stats['average_rentals'] = gender_date_stats['average_rentals'].round(2)
gender_date_stats['total_rentals'] = gender_date_stats['total_rentals'].round(2)
gender_date_stats['max_rentals'] = gender_date_stats['max_rentals'].round(2)
gender_date_stats['min_rentals'] = gender_date_stats['min_rentals'].round(2)
gender_date_stats['total_distance'] = gender_date_stats['total_distance'].round(2)
gender_date_stats['average_distance'] = gender_date_stats['average_distance'].round(2)
gender_date_stats['max_distance'] = gender_date_stats['max_distance'].round(2)
gender_date_stats['min_distance'] = gender_date_stats['min_distance'].round(2)

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

# 남성의 이동거리가 가장 긴 날짜
max_male_distance = male_data[male_data['total_distance'] == male_data['total_distance'].max()]

# 남성의 이동거리가 가장 짧은 날짜
min_male_distance = male_data[male_data['total_distance'] == male_data['total_distance'].min()]

# 남성의 평균 이동거리가 가장 높은 날짜
avg_male_distance = male_data[male_data['average_distance'] == male_data['average_distance'].max()]

# 여성의 이동거리가 가장 긴 날짜
max_female_distance = female_data[female_data['total_distance'] == female_data['total_distance'].max()]

# 여성의 이동거리가 가장 짧은 날짜
min_female_distance = female_data[female_data['total_distance'] == female_data['total_distance'].min()]

# 여성의 평균 이동거리가 가장 높은 날짜
avg_female_distance = female_data[female_data['average_distance'] == female_data['average_distance'].max()]

# 성별별로 최대, 최소, 평균 이용건수 및 가장 많이/적게 이용한 날짜 출력
print("남성('M')이 자전거를 가장 많이 이용한 날짜와 이용건수:")
print(max_male_usage[['대여일자', 'total_rentals']])
print("\n남성('M')이 자전거를 가장 적게 이용한 날짜와 이용건수:")
print(min_male_usage[['대여일자', 'total_rentals']])

print("\n여성('F')이 자전거를 가장 많이 이용한 날짜와 이용건수:")
print(max_female_usage[['대여일자', 'total_rentals']])
print("\n여성('F')이 자전거를 가장 적게 이용한 날짜와 이용건수:")
print(min_female_usage[['대여일자', 'total_rentals']])

# 이동거리 관련 출력
print("\n남성('M')이 자전거를 가장 멀리 이동한 날짜와 이동거리:")
print(max_male_distance[['대여일자', 'total_distance']])
print("\n남성('M')이 자전거를 가장 적게 이동한 날짜와 이동거리:")
print(min_male_distance[['대여일자', 'total_distance']])
print("\n남성('M')의 평균 이동거리가 가장 높은 날짜와 이동거리:")
print(avg_male_distance[['대여일자', 'average_distance']])

print("\n여성('F')이 자전거를 가장 멀리 이동한 날짜와 이동거리:")
print(max_female_distance[['대여일자', 'total_distance']])
print("\n여성('F')이 자전거를 가장 적게 이동한 날짜와 이동거리:")
print(min_female_distance[['대여일자', 'total_distance']])
print("\n여성('F')의 평균 이동거리가 가장 높은 날짜와 이동거리:")
print(avg_female_distance[['대여일자', 'average_distance']])

# 성별별로 평균 이용건수와 이동거리 출력 (소수점 2자리까지)
print("\n남성('M')의 평균 이용건수와 평균 이동거리:\n", male_data[['대여일자', 'average_rentals', 'average_distance']])
print("\n여성('F')의 평균 이용건수와 평균 이동거리:\n", female_data[['대여일자', 'average_rentals', 'average_distance']])

'''
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

남성('M')이 자전거를 가장 멀리 이동한 날짜와 이동거리:
           대여일자  total_distance
267  2023-09-22    2.202908e+08

남성('M')이 자전거를 가장 적게 이동한 날짜와 이동거리:
           대여일자  total_distance
224  2023-08-10      9763971.28

남성('M')의 평균 이동거리가 가장 높은 날짜와 이동거리:
           대여일자  average_distance
274  2023-09-29           3622.58

여성('F')이 자전거를 가장 멀리 이동한 날짜와 이동거리:
          대여일자  total_distance
93  2023-10-02    1.613690e+08

여성('F')이 자전거를 가장 적게 이동한 날짜와 이동거리:
          대여일자  total_distance
40  2023-08-10      2183208.74

여성('F')의 평균 이동거리가 가장 높은 날짜와 이동거리:
          대여일자  average_distance
90  2023-09-29           4202.88

남성('M')의 평균 이용건수와 평균 이동거리:
            대여일자  average_rentals  average_distance
184  2023-07-01             1.10           2910.17
185  2023-07-02             1.10           3096.10
186  2023-07-03             1.16           2757.63
187  2023-07-04             1.13           2354.44
188  2023-07-05             1.16           2943.44
..          ...              ...               ...
363  2023-12-27             1.09           2125.58
364  2023-12-28             1.08           2100.12
365  2023-12-29             1.08           2150.48
366  2023-12-30             1.03           1960.28
367  2023-12-31             1.04           2162.16

[184 rows x 3 columns]

여성('F')의 평균 이용건수와 평균 이동거리:
            대여일자  average_rentals  average_distance
0    2023-07-01             1.09           2963.52
1    2023-07-02             1.09           3232.66
2    2023-07-03             1.13           2650.18
3    2023-07-04             1.10           2147.93
4    2023-07-05             1.14           2902.03
..          ...              ...               ...
179  2023-12-27             1.06           1934.82
180  2023-12-28             1.06           1930.24
181  2023-12-29             1.06           1955.34
182  2023-12-30             1.01           1718.24
183  2023-12-31             1.03           1957.50

[184 rows x 3 columns]
'''