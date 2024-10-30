import pandas as pd

# 파일 경로 설정
path_bicycle = './select/서울특별시 공공자전거 이용정보(시간대별)_2307-2312.csv'
path_station = './select/서울특별시 공공자전거 대여소별 이용정보(월별)_23.7-12.csv'

# 데이터 불러오기
bicycle = pd.read_csv(path_bicycle, encoding='utf-8')
station = pd.read_csv(path_station, encoding='cp949')

# 두 데이터프레임 병합 ('대여소명'을 기준으로 병합)
merged_data = pd.merge(bicycle, station[['대여소명', '자치구']], on='대여소명', how='left')

# NaN 값이 있는 행 제거
merged_data.dropna(subset=['자치구'], inplace=True)

# '이동거리' 열이 존재하는지 확인
if '이동거리' in merged_data.columns:
    # 성별, 대여일자, 이용건수, 이동거리, 연령대코드, 자치구, 대여소명 필드만 선택
    selected_data = merged_data[['성별', '대여일자', '이용건수', '이동거리', '연령대코드', '자치구', '대여소명']]
else:
    # 이동거리 열이 없는 경우, 나머지 필드만 선택
    selected_data = merged_data[['성별', '대여일자', '이용건수', '연령대코드', '자치구', '대여소명']]

# 성별에 따라 자주 이용한 자치구 및 대여소명
gender_group = selected_data.groupby(['성별', '자치구', '대여소명']).agg({'이용건수': 'sum'}).reset_index()

# 성별별로 이용건수가 가장 많은 자치구, 대여소명 확인
top_usage_by_gender = gender_group.loc[gender_group.groupby('성별')['이용건수'].idxmax()]

# 가장 많이 이용한 대여소, 적게 이용한 대여소, 평균적으로 이용한 대여소 계산
total_usage_by_station = selected_data.groupby('대여소명').agg({'이용건수': 'sum'}).reset_index()

# 가장 많이 이용한 대여소
most_used_station = total_usage_by_station.loc[total_usage_by_station['이용건수'].idxmax()]

# 가장 적게 이용한 대여소
least_used_station = total_usage_by_station.loc[total_usage_by_station['이용건수'].idxmin()]

# 평균적으로 이용한 대여소 (중간값에 가까운 대여소)
mean_usage = total_usage_by_station['이용건수'].mean()
closest_to_mean_station = total_usage_by_station.iloc[(total_usage_by_station['이용건수'] - mean_usage).abs().argsort()[:1]]

# 결과 출력
print("성별에 따라 가장 자주 이용한 자치구 및 대여소:")
print(top_usage_by_gender)

print("\n가장 많이 이용한 대여소명:")
print(f"대여소명: {most_used_station['대여소명']}, 이용건수: {most_used_station['이용건수']:,}")

print("\n가장 적게 이용한 대여소명:")
print(f"대여소명: {least_used_station['대여소명']}, 이용건수: {least_used_station['이용건수']:,}")

print("\n평균적으로 이용한 대여소명:")
print(f"대여소명: {closest_to_mean_station.iloc[0]['대여소명']}, 이용건수: {closest_to_mean_station.iloc[0]['이용건수']:,}")

'''
별에 따라 가장 자주 이용한 자치구 및 대여소:
     성별  자치구               대여소명      이용건수
443   F  강서구  2715.마곡나루역 2번 출구   162756.0
3205  M  강서구  2715.마곡나루역 2번 출구   244530.0

가장 많이 이용한 대여소명:
대여소명: 2715.마곡나루역 2번 출구 , 이용건수: 407,286.0

가장 적게 이용한 대여소명:
대여소명: 4467. 한림연예예술고등학교, 이용건수: 2.0

평균적으로 이용한 대여소명:
대여소명: 1396.래미안장위퍼스트하이(513동), 이용건수: 34,902.0
'''
