import pandas as pd

# 파일 경로
path = './select/서울특별시 공공자전거 이용정보(시간대별)_2307-2312.csv'

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
성별, 연령대코드별 대여 및 이동거리 통계:
   성별  연령대코드 total_rentals average_rentals max_rentals min_rentals    total_distance average_distance max_distance min_distance
0   F    20대   2,076,478.0            1.16        24.0         1.0  4,734,407,558.22         2,649.87   130,956.22          0.1
1   F    30대   1,446,458.0            1.11        27.0         1.0  3,417,656,960.22          2,612.7   131,273.11          0.1
2   F    40대     847,952.0            1.07        19.0         1.0  2,137,436,926.82         2,694.12   165,543.73          0.1
3   F    50대     582,198.0            1.04         8.0         1.0  1,576,638,490.53         2,829.34   100,646.51          0.1
4   F    60대     128,772.0            1.02         6.0         1.0    371,056,826.68         2,932.65     65,360.0          0.1
5   F  70대이상      21,314.0            1.01         9.0         1.0     52,436,252.96         2,485.13     41,280.0          0.1
6   F   ~10대     391,289.0            1.14        29.0         1.0    815,364,084.35         2,385.47   201,131.24          0.1
7   F     기타     480,762.0            1.04        26.0         1.0  1,112,668,540.87         2,406.06   151,032.56          0.1
8   M    20대   2,723,376.0            1.17        20.0         1.0  5,965,722,924.81          2,553.2   328,043.56          0.1
9   M    30대   2,409,676.0            1.15        28.0         1.0  5,524,610,936.51         2,632.71   291,158.01          0.1
10  M    40대   1,630,280.0             1.1        25.0         1.0  4,196,763,854.56         2,844.32   147,921.25          0.1
11  M    50대   1,115,260.0            1.07        16.0         1.0  2,971,836,950.75          2,846.0   177,698.55          0.1
12  M    60대     423,192.0            1.03        11.0         1.0  1,137,446,909.03         2,765.73    66,626.12          0.1
13  M  70대이상      61,119.0            1.01         3.0         1.0    165,828,314.85         2,740.92     54,110.0          0.1
14  M   ~10대   1,051,439.0            1.23        24.0         1.0  2,110,594,709.63         2,477.91    180,715.4          0.1
15  M     기타     739,992.0            1.05        30.0         1.0  1,737,502,475.45         2,462.89   242,591.14          0.1

남성('M')이 자전거를 가장 많이 이용한 연령대코드와 이용건수:
   연령대코드
15    기타
   total_rentals
15     739,992.0

남성('M')이 자전거를 가장 적게 이용한 연령대코드와 이용건수:
   연령대코드
14  ~10대
   total_rentals
14   1,051,439.0

여성('F')이 자전거를 가장 많이 이용한 연령대코드와 이용건수:
  연령대코드
2   40대
  total_rentals
2     847,952.0

여성('F')이 자전거를 가장 적게 이용한 연령대코드와 이용건수:
  연령대코드
1   30대
  total_rentals
1   1,446,458.0
'''