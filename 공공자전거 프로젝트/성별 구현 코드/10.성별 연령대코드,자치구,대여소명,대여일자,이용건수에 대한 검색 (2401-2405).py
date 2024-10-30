import pandas as pd

# 파일 경로 설정
path_bicycle = './select/서울특별시 공공자전거 이용정보(시간대별)_2401-2405.csv'
path_station = './select/서울특별시 공공자전거 대여소별 이용정보(월별)_24.1-6.csv'

# 데이터 불러오기
bicycle = pd.read_csv(path_bicycle, encoding='utf-8')
station = pd.read_csv(path_station, encoding='cp949')

# 두 데이터프레임 병합 ('대여소명'을 기준으로 병합)
merged_data = pd.merge(bicycle, station[['대여소명', '자치구']], on='대여소명', how='left')

# NaN 값이 있는 행 제거
merged_data.dropna(subset=['자치구'], inplace=True)

# 열이 존재하는지 확인하고 선택
columns_to_select = ['성별', '대여일자', '이용건수', '연령대코드', '자치구', '대여소명']
if '이동거리' in merged_data.columns:
    columns_to_select.append('이동거리')
if '이용시간' in merged_data.columns:
    columns_to_select.append('이용시간')

# 필요한 열만 선택
selected_data = merged_data[columns_to_select]

# 집계할 열 설정
agg_dict = {'이용건수': 'sum'}
if '이동거리' in selected_data.columns:
    agg_dict['이동거리'] = 'sum'
if '이용시간' in selected_data.columns:
    agg_dict['이용시간'] = 'sum'

# 성별, 연령대코드, 자치구, 대여소명, 대여일자별로 통계 처리
grouped_data = selected_data.groupby(['성별', '연령대코드', '자치구', '대여소명', '대여일자']).agg(agg_dict).reset_index()

# 성별 및 대여소명별로 가장 많이 이용된 대여일자 추출 (연령대코드 포함)
top_usage_by_group = grouped_data.loc[grouped_data.groupby(['성별', '연령대코드', '자치구', '대여소명'])['이용건수'].idxmax()]

# 전체에서 가장 많이 이용한 대여소명, 이동거리, 이용시간 통계
most_used_station = grouped_data.loc[grouped_data['이용건수'].idxmax()]
most_used_distance = grouped_data.loc[grouped_data['이동거리'].idxmax()] if '이동거리' in grouped_data.columns else None
most_used_time = grouped_data.loc[grouped_data['이용시간'].idxmax()] if '이용시간' in grouped_data.columns else None

# 전체에서 가장 적게 이용한 대여소명
least_used_station = grouped_data.loc[grouped_data['이용건수'].idxmin()]

# 평균적으로 이용된 대여소 계산
average_usage = grouped_data['이용건수'].mean()
closest_to_mean_station = grouped_data.iloc[(grouped_data['이용건수'] - average_usage).abs().argsort()[:1]]

# 결과 출력
print("성별, 연령대코드, 자치구, 대여소명별로 가장 많이 이용된 대여일자 통계:")
print(top_usage_by_group)

print("\n전체에서 가장 많이 이용한 대여소명 (이용건수 기준):")
print(most_used_station)

if most_used_distance is not None:
    print("\n전체에서 가장 많이 이동한 거리 (이동거리 기준):")
    print(most_used_distance)

if most_used_time is not None:
    print("\n전체에서 가장 많이 이용한 시간 (이용시간 기준):")
    print(most_used_time)

print("\n전체에서 가장 적게 이용한 대여소명 (이용건수 기준):")
print(least_used_station)

print("\n평균적으로 이용된 대여소명 (이용건수 기준):")
print(closest_to_mean_station)

'''
성별, 연령대코드, 자치구, 대여소명별로 가장 많이 이용된 대여일자 통계:
        성별 연령대코드  자치구                            대여소명        대여일자  이용건수
56       F   20대  강남구                2301. 현대고등학교 건너편  2024-03-24   200
215      F   20대  강남구  2302. 교보타워 버스정류장(신논현역 3번출구 후면)  2024-05-03    60
351      F   20대  강남구                 2303. 논현역 10번출구  2024-05-17    80
408      F   20대  강남구                    2304. 대현그린타워  2024-05-14    20
494      F   20대  강남구              2305. MCM 본사 직영점 앞  2024-05-14    20
...     ..   ...  ...                             ...         ...   ...
3327590  M    기타  중랑구                4840. 서울시 북부병원 앞  2024-05-30    15
3327659  M    기타  중랑구                    4841. 중화수경공원  2024-04-09    35
3327740  M    기타  중랑구              4842. 면목라온프라이빗 아파트  2024-05-19    20
3327802  M    기타  중랑구                4843. 봉화산역 4번 출구  2024-02-27    30
3327878  M    기타  중랑구            4845. 신내역금강펜테리움센트럴파크  2024-02-28     5

[42862 rows x 6 columns]

전체에서 가장 많이 이용한 대여소명 (이용건수 기준):
성별                             F
연령대코드                        20대
자치구                          광진구
대여소명     502. 자양(뚝섬한강공원)역 1번출구 앞
대여일자                  2024-03-24
이용건수                        1295
Name: 72571, dtype: object

전체에서 가장 적게 이용한 대여소명 (이용건수 기준):
성별                   F
연령대코드              20대
자치구                강남구
대여소명     4935. 도곡삼성래미안
대여일자        2024-05-30
이용건수                 1
Name: 15352, dtype: object

평균적으로 이용된 대여소명 (이용건수 기준):
        성별 연령대코드   자치구                    대여소명        대여일자  이용건수
1535279  M   20대  동대문구  4136. 롯데캐슬SKY-L65 D동 앞  2024-05-08    18
'''