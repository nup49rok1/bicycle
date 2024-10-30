import pandas as pd

# 파일 경로
path = './select/서울특별시 공공자전거 이용정보(시간대별)_2301-2306.csv'

# CSV 파일 읽기 (한글 인코딩 처리)
bicycle = pd.read_csv(path, encoding='utf-8')

# 필요한 컬럼만 추출 (성별, 대여일자, 이용건수, 이동거리, 연령대코드)
bicycle_selected = bicycle[['성별', '대여일자', '이용건수', '이동거리(M)', '연령대코드']]

# 성별 'M'과 'F'로 처리하기 (남성 'M', 여성 'F')
bicycle_selected['성별'] = bicycle_selected['성별'].replace({'남성': 'M', '여성': 'F'})

# 대여일자를 datetime 형식으로 변환
bicycle_selected['대여일자'] = pd.to_datetime(bicycle_selected['대여일자'], format='%Y-%m-%d')

# 성별, 연령대코드별로 이용건수 및 이동거리를 그룹화하여 합계, 평균, 최대, 최소 계산
gender_age_stats = bicycle_selected.groupby(['성별', '연령대코드']).agg(
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
gender_age_stats['average_rentals'] = gender_age_stats['average_rentals'].round(2)
gender_age_stats['total_rentals'] = gender_age_stats['total_rentals'].round(2)
gender_age_stats['max_rentals'] = gender_age_stats['max_rentals'].round(2)
gender_age_stats['min_rentals'] = gender_age_stats['min_rentals'].round(2)
gender_age_stats['total_distance'] = gender_age_stats['total_distance'].round(2)
gender_age_stats['average_distance'] = gender_age_stats['average_distance'].round(2)
gender_age_stats['max_distance'] = gender_age_stats['max_distance'].round(2)
gender_age_stats['min_distance'] = gender_age_stats['min_distance'].round(2)

# 세 자리마다 콤마를 표시하기 위해 숫자 데이터에 포맷 적용
columns_to_format = ['total_rentals', 'average_rentals', 'max_rentals', 'min_rentals', 
                     'total_distance', 'average_distance', 'max_distance', 'min_distance']

# 모든 숫자 컬럼에 대해 세자리마다 콤마 포맷 적용
gender_age_stats[columns_to_format] = gender_age_stats[columns_to_format].applymap('{:,}'.format)

# 성별별로 최대, 최소, 평균 이용건수 및 이동거리 출력
print("\n성별, 연령대코드별 대여 및 이동거리 통계:")
print(gender_age_stats)

# 성별별로 가장 많이 대여한 연령대코드와 가장 적게 대여한 연령대코드 계산
# 남성 'M'과 여성 'F' 데이터로 분리
male_data = gender_age_stats[gender_age_stats['성별'] == 'M']
female_data = gender_age_stats[gender_age_stats['성별'] == 'F']

# 남성: 가장 많이 대여한 연령대코드 (최대 이용건수)
max_male_rental_age = male_data[male_data['total_rentals'] == male_data['total_rentals'].max()]

# 남성: 가장 적게 대여한 연령대코드 (최소 이용건수)
min_male_rental_age = male_data[male_data['total_rentals'] == male_data['total_rentals'].min()]

# 여성: 가장 많이 대여한 연령대코드 (최대 이용건수)
max_female_rental_age = female_data[female_data['total_rentals'] == female_data['total_rentals'].max()]

# 여성: 가장 적게 대여한 연령대코드 (최소 이용건수)
min_female_rental_age = female_data[female_data['total_rentals'] == female_data['total_rentals'].min()]

# 결과 출력 (연령대코드를 포함하여 최대, 최소 출력)
print("\n남성('M')이 자전거를 가장 많이 이용한 연령대코드와 이용건수:")
print(max_male_rental_age[['연령대코드']])
print(max_male_rental_age[['total_rentals']])

print("\n남성('M')이 자전거를 가장 적게 이용한 연령대코드와 이용건수:")
print(min_male_rental_age[['연령대코드']])
print(min_male_rental_age[['total_rentals']])

print("\n여성('F')이 자전거를 가장 많이 이용한 연령대코드와 이용건수:")
print(max_female_rental_age[['연령대코드']])
print(max_female_rental_age[['total_rentals']])

print("\n여성('F')이 자전거를 가장 적게 이용한 연령대코드와 이용건수:")
print(min_female_rental_age[['연령대코드']])
print(min_female_rental_age[['total_rentals']])
'''
stead.
  gender_age_stats[columns_to_format] = gender_age_stats[columns_to_format].applymap('{:,}'.format)

성별, 연령대코드별 대여 및 이동거리 통계:
   성별  연령대코드 total_rentals average_rentals max_rentals min_rentals    total_distance average_distance max_distance min_distance
0   F    20대     1,943,154            1.18          32           1   4,898,305,529.3         2,972.77   183,372.72          0.1
1   F    30대     1,411,900            1.12          24           1  3,635,014,347.74         2,881.52   105,927.85          0.1
2   F    40대       784,346            1.07           9           1  2,123,871,856.48         2,903.28   144,196.74          0.1
3   F    50대       537,484            1.05           5           1   1,512,273,071.6         2,942.25   109,176.84          0.1
4   F    60대       122,898            1.02           5           1    367,161,512.29         3,039.97    50,576.49          0.1
5   F  70대이상        20,661            1.01           4           1     50,201,713.51         2,456.77     54,120.0          0.1
6   F   ~10대       307,172            1.15          23           1    685,288,736.35         2,576.15    98,585.78          0.1
7   F     기타       495,915            1.05           6           1  1,243,442,246.62         2,621.93   134,006.27          0.1
8   M    20대     2,404,448            1.17          28           1   5,702,069,154.2         2,772.53   166,482.21          0.1
9   M    30대     2,187,702            1.16          31           1  5,385,637,299.08         2,846.43   693,418.03          0.1
10  M    40대     1,472,828            1.11          22           1   4,045,804,277.8         3,047.84   179,803.02          0.1
11  M    50대       976,916            1.06          12           1  2,817,501,707.01          3,067.8   138,651.05          0.1
12  M    60대       375,308            1.03           5           1  1,063,956,210.72         2,913.54    117,400.0          0.1
13  M  70대이상        56,718            1.01           5           1    161,860,350.57          2,882.8     42,110.0          0.1
14  M   ~10대       789,032            1.24          28           1  1,685,657,336.72         2,641.34   307,412.44          0.1
15  M     기타       724,946            1.05           9           1  1,810,369,345.14         2,633.06    95,263.26          0.1

남성('M')이 자전거를 가장 많이 이용한 연령대코드와 이용건수:
   연령대코드
11   50대
   total_rentals
11       976,916

남성('M')이 자전거를 가장 적게 이용한 연령대코드와 이용건수:
   연령대코드
10   40대
   total_rentals
10     1,472,828

여성('F')이 자전거를 가장 많이 이용한 연령대코드와 이용건수:
  연령대코드
2   40대
  total_rentals
2       784,346

여성('F')이 자전거를 가장 적게 이용한 연령대코드와 이용건수:
  연령대코드
1   30대
  total_rentals
1     1,411,900
'''