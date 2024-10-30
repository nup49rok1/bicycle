import pandas as pd

# 파일 경로
path = './select/서울특별시 공공자전거 이용정보(시간대별)_2401-2405.csv'

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
gender_age_stats[columns_to_format] = gender_age_stats[columns_to_format].applymap('{:,}'.format)

성별, 연령대코드별 대여 및 이동거리 통계:
   성별  연령대코드 total_rentals average_rentals max_rentals min_rentals    total_distance average_distance max_distance min_distance
0   F    20대     1,377,140            1.13          39           1  3,443,382,742.04         2,836.03   289,400.62          0.1
1   F    30대     1,130,496             1.1          16           1  2,871,641,729.19         2,799.14   116,622.56          0.1
2   F    40대       663,856            1.07          16           1  1,737,771,369.39         2,793.22    182,520.0          0.1
3   F    50대       464,268            1.04           6           1  1,252,691,889.04         2,813.39   187,993.08          0.1
4   F    60대       113,942            1.02           4           1     329,592,047.8         2,936.76    76,236.21          0.1
5   F  70대이상        18,568            1.01           3           1     47,654,174.48         2,592.01     36,280.0          0.1
6   F   ~10대       238,714            1.16          21           1    525,939,251.74         2,545.12    84,252.39          0.1
7   F     기타       326,620            1.03           6           1    810,569,638.76         2,566.97    103,111.1          0.1
8   M    20대     1,782,119            1.13          25           1  4,144,287,803.67         2,632.78   153,658.74          0.1
9   M    30대     1,826,834            1.13          21           1  4,327,987,385.59         2,686.84   147,300.63          0.1
10  M    40대     1,251,471             1.1          16           1  3,288,486,451.11         2,886.34   142,690.46          0.1
11  M    50대       901,061            1.07          16           1  2,459,073,526.39         2,914.83   153,288.88          0.1
12  M    60대       360,587            1.03           8           1    973,232,776.81         2,775.12    120,459.2          0.1
13  M  70대이상        62,059            1.01           3           1    168,719,368.18         2,746.17    53,449.84          0.1
14  M   ~10대       646,128            1.23          30           1  1,362,947,209.77         2,593.25   151,070.15          0.1
15  M     기타       497,325            1.04           7           1  1,218,615,994.97         2,542.49    125,030.0          0.1

남성('M')이 자전거를 가장 많이 이용한 연령대코드와 이용건수:
   연령대코드
11   50대
   total_rentals
11       901,061

남성('M')이 자전거를 가장 적게 이용한 연령대코드와 이용건수:
   연령대코드
10   40대
   total_rentals
10     1,251,471

여성('F')이 자전거를 가장 많이 이용한 연령대코드와 이용건수:
  연령대코드
2   40대
  total_rentals
2       663,856

여성('F')이 자전거를 가장 적게 이용한 연령대코드와 이용건수:
  연령대코드
1   30대
  total_rentals
1     1,130,496
'''