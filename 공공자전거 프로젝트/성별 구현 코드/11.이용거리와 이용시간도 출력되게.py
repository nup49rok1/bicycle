
import pandas as pd

# 파일 경로 설정
path_bicycle = './select/서울특별시 공공자전거 이용정보(시간대별)_2301-2306.csv'
path_station = './select/서울특별시 공공자전거 대여소별 이용정보(월별)_23.1-6.csv'

# 데이터 불러오기
bicycle = pd.read_csv(path_bicycle, encoding='utf-8')
station = pd.read_csv(path_station, encoding='cp949')

# 두 데이터프레임 병합 ('대여일자'와 '대여소명'을 기준으로 병합)
merged_data = pd.merge(bicycle, station[['대여소명', '자치구', '이동거리', '이동시간']], on=['대여소명', '대여일자'], how='left')

# NaN 값이 있는 행 제거
merged_data.dropna(subset=['자치구'], inplace=True)

# 필요한 열만 선택
selected_data = merged_data[['성별', '대여일자', '이용건수', '이동거리', '이동시간', '연령대코드', '자치구', '대여소명']]

# 성별, 연령대코드, 자치구, 대여소명, 대여일자별로 통계 처리
grouped_data = selected_data.groupby(['성별', '연령대코드', '자치구', '대여소명', '대여일자']).agg({
    '이용건수': 'sum', 
    '이동거리': 'sum', 
    '이동시간': 'sum'
}).reset_index()

# 성별 및 대여소명별로 가장 많이 이용된 대여일자 추출 (연령대코드 포함)
top_usage_by_group = grouped_data.loc[grouped_data.groupby(['성별', '연령대코드', '자치구', '대여소명'])['이용건수'].idxmax()]

# 전체에서 가장 많이 이용한 대여소명, 이동거리, 이용시간 통계
most_used_station = grouped_data.loc[grouped_data['이용건수'].idxmax()]
most_used_distance = grouped_data.loc[grouped_data['이동거리'].idxmax()] if '이동거리' in grouped_data.columns else None
most_used_time = grouped_data.loc[grouped_data['이용시간'].idxmax()] if '이동시간' in grouped_data.columns else None

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
