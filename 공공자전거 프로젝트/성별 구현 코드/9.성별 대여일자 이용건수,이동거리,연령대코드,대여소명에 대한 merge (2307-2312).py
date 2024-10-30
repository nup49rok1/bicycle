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

# 병합된 데이터를 새로운 CSV 파일로 저장
output_path = './select/merge/서울특별시 공공자전거 대여소별_이용정보(월별)_2307-2312.csv'
merged_data.to_csv(output_path, index=False, encoding='utf-8')

# 완료 메시지 출력
print(f"병합된 데이터가 {output_path} 파일에 저장되었습니다.")
# path = './select/merge/서울특별시 공공자전거 대여소별_이용정보(월별)_2307-2312.csv'

# bimerge = pd.read_csv(output_path,encoding='utf-8')
# print('bimerge.info()=>',bimerge.info())