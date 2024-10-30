import pandas as pd

# 파일 경로
path = './select/서울특별시 공공자전거 이용정보(시간대별)_2401-2405.csv'

# CSV 파일 읽기 (한글 인코딩 처리)
bicycle = pd.read_csv(path, encoding='utf-8')

# 필요한 컬럼만 추출 (성별, 대여일자, 이용건수, 이동거리)
bicycle_selected = bicycle[['성별', '대여일자', '이용건수', '이동거리(M)']]

# 성별 'M'과 'F'로 처리하기 (남성 'M', 여성 'F')
bicycle_selected['성별'] = bicycle_selected['성별'].replace({'남성': 'M', '여성': 'F'})

# 대여일자를 datetime 형식으로 변환
bicycle_selected['대여일자'] = pd.to_datetime(bicycle_selected['대여일자'], format='%Y-%m-%d')

# 대여일자를 통해 요일을 구하기 (0=월요일, 6=일요일)
bicycle_selected['요일'] = bicycle_selected['대여일자'].dt.dayofweek

# 요일을 한글로 변환 (선택사항: 필요에 따라 요일 이름을 넣을 수 있음)
weekday_map = {0: '월요일', 1: '화요일', 2: '수요일', 3: '목요일', 4: '금요일', 5: '토요일', 6: '일요일'}
bicycle_selected['요일명'] = bicycle_selected['요일'].map(weekday_map)

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

# --- 추가된 부분 ---
# 요일별 대여 횟수 빈도수 계산
weekday_counts = bicycle_selected['요일명'].value_counts()

# 가장 많이 대여한 요일과 가장 적게 대여한 요일
most_common_day = weekday_counts.idxmax()  # 대여가 가장 많은 요일
least_common_day = weekday_counts.idxmin()  # 대여가 가장 적은 요일

# 요일별로 이용건수, 이동거리 계산 (최대, 최소, 평균)
weekday_stats = bicycle_selected.groupby('요일명').agg(
    total_rentals=('이용건수', 'sum'),
    average_rentals=('이용건수', 'mean'),
    max_rentals=('이용건수', 'max'),
    min_rentals=('이용건수', 'min'),
    total_distance=('이동거리(M)', 'sum'),
    average_distance=('이동거리(M)', 'mean'),
    max_distance=('이동거리(M)', 'max'),
    min_distance=('이동거리(M)', 'min')
).reset_index()

# 요일별로 가장 많이 대여한 요일과 가장 적게 대여한 요일의 빈도수 출력
print(f"\n대여가 가장 많은 요일: {most_common_day}, 빈도수: {weekday_counts[most_common_day]}")
print(f"대여가 가장 적은 요일: {least_common_day}, 빈도수: {weekday_counts[least_common_day]}")

'''
 남성('M')이 자전거를 가장 많이 이용한 날짜와 이용건수:
          대여일자  total_rentals
300 2024-05-28          84252

남성('M')이 자전거를 가장 적게 이용한 날짜와 이용건수:
          대여일자  total_rentals
203 2024-02-21           5459

여성('F')이 자전거를 가장 많이 이용한 날짜와 이용건수:
          대여일자  total_rentals
148 2024-05-28          53934

여성('F')이 자전거를 가장 적게 이용한 날짜와 이용건수:
         대여일자  total_rentals
51 2024-02-21           1549

남성('M')이 자전거를 가장 멀리 이동한 날짜와 이동거리:
          대여일자  total_distance
273 2024-05-01    2.234420e+08

남성('M')이 자전거를 가장 적게 이동한 날짜와 이동거리:
          대여일자  total_distance
203 2024-02-21       9869104.3

남성('M')의 평균 이동거리가 가장 높은 날짜와 이동거리:
          대여일자  average_distance
235 2024-03-24            3878.8

여성('F')이 자전거를 가장 멀리 이동한 날짜와 이동거리:
          대여일자  total_distance
121 2024-05-01    1.629193e+08

여성('F')이 자전거를 가장 적게 이동한 날짜와 이동거리:
         대여일자  total_distance
51 2024-02-21      2651452.56

여성('F')의 평균 이동거리가 가장 높은 날짜와 이동거리:
         대여일자  average_distance
83 2024-03-24           4423.35

남성('M')의 평균 이용건수와 평균 이동거리:
           대여일자  average_rentals  average_distance
152 2024-01-01             1.06           2526.73
153 2024-01-02             1.10           2204.18
154 2024-01-03             1.09           2111.02
155 2024-01-04             1.10           2180.48
156 2024-01-05             1.09           2163.00
..         ...              ...               ...
299 2024-05-27             1.16           2936.56
300 2024-05-28             1.16           2949.46
301 2024-05-29             1.15           2884.50
302 2024-05-30             1.15           2880.27
303 2024-05-31             1.15           2853.86

[152 rows x 3 columns]

여성('F')의 평균 이용건수와 평균 이동거리:
           대여일자  average_rentals  average_distance
0   2024-01-01             1.04           2509.55
1   2024-01-02             1.06           2030.68
2   2024-01-03             1.06           1947.10
3   2024-01-04             1.07           2009.51
4   2024-01-05             1.07           2027.40
..         ...              ...               ...
147 2024-05-27             1.12           2905.26
148 2024-05-28             1.12           2934.49
149 2024-05-29             1.12           2849.72
150 2024-05-30             1.12           2789.63
151 2024-05-31             1.11           2729.31

[152 rows x 3 columns]

대여가 가장 많은 요일: 금요일, 빈도수: 1759671
대여가 가장 적은 요일: 일요일, 빈도수: 1160974
'''