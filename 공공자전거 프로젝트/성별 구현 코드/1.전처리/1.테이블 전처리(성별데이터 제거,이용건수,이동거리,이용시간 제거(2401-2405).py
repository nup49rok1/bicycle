import pandas as pd
import time

# 원본 CSV 파일 경로
path = './select/서울특별시 공공자전거 이용정보(시간대별)_2401-2405.csv'

# CSV 파일 읽기 (한글 인코딩 처리)
bicycle = pd.read_csv(path, encoding='utf-8')

# 데이터 정보 출력
print(bicycle.info())
time.sleep(1)

# 필요한 컬럼만 추출 (대여일자, 대여시간, 대여소번호, 대여소명, 성별, 연령대코드, 이용건수, 이동거리, 이용시간)
selected_columns = ['대여일자', '대여시간', '대여구분코드','대여소번호', '대여소명', '성별', '연령대코드', '이용건수', '이동거리(M)', '이용시간(분)']
bicycle_selected = bicycle[selected_columns]

# 결측치 제거
bicycle_selected = bicycle_selected.dropna()

# 중복된 데이터 체크 및 갯수 출력
duplicated_rows = bicycle_selected.duplicated().sum()
if duplicated_rows > 0:
    print(f"중복된 데이터가 {duplicated_rows}개 발견되었습니다.")
else:
    print("중복된 데이터가 없습니다.")

# 중복된 데이터 삭제 (첫 번째 데이터는 유지, 이후 중복된 데이터 삭제)
#bicycle_selected = bicycle_selected.drop_duplicates()

# 이상치 제거: 각 필드별로 이상치 처리 (예: 이동거리와 이용시간이 음수이거나 비정상적인 경우 제거)
# 이용건수, 이동거리, 이용시간은 음수일 수 없으므로 0보다 큰 값만 필터링
bicycle_selected = bicycle_selected[
    (bicycle_selected['이용건수'] > 0) &
    (bicycle_selected['이동거리(M)'] > 0) &
    (bicycle_selected['이용시간(분)'] > 0)
]

# 이상치 처리:
# 1. 이용건수, 이동거리, 이용시간이 모두 0인 데이터 제거
# 2. 이동거리, 이용시간이 있어도 이용건수가 0인 데이터 제거
# 3. 이용건수, 이동거리가 있어도 이용시간이 0인 데이터 제거
# 4. 이용건수, 이용시간이 있어도 이동거리가 0인 데이터 제거
bicycle_selected = bicycle_selected[
    ~((bicycle_selected['이용건수'] == 0) & (bicycle_selected['이동거리(M)'] == 0) & (bicycle_selected['이용시간(분)'] == 0)) &  # 모두 0인 경우
    ~(bicycle_selected['이용건수'] == 0) &  # 이용건수가 0인 경우
    ~(bicycle_selected['이용시간(분)'] == 0) &  # 이용시간이 0인 경우
    ~(bicycle_selected['이동거리(M)'] == 0)  # 이동거리가 0인 경우
]

# # 정리된 데이터프레임을 새로운 CSV 파일로 저장
# output_path = './select/서울특별시 공공자전거 이용정보(시간대별)_2401-2405.csv'
# bicycle_selected.to_csv(output_path, index=False, encoding='utf-8')

# 처리된 데이터 정보 출력
print("처리된 데이터 정보:")
print(bicycle_selected.info())
# print(f"선택된 데이터가 {output_path} 파일에 저장되었습니다.")

'''
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 10545385 entries, 0 to 10545384
Data columns (total 11 columns):
 #   Column      Dtype  
---  ------      -----  
 0   Unnamed: 0  int64  
 1   대여일자        object 
 2   대여시간        int64  
 3   대여구분코드      object 
 4   대여소번호       int64  
 5   대여소명        object 
 6   성별          object 
 7   연령대코드       object 
 8   이용건수        int64  
 9   이동거리(M)     float64
 10  이용시간(분)     int64  
dtypes: float64(1), int64(5), object(5)
memory usage: 885.0+ MB
None
중복된 데이터가 270개 발견되었습니다.
처리된 데이터 정보:
<class 'pandas.core.frame.DataFrame'>
Index: 10545115 entries, 0 to 10545384
Data columns (total 10 columns):
 #   Column   Dtype
---  ------   -----
 0   대여일자     object
 1   대여시간     int64
 2   대여구분코드   object
 3   대여소번호    int64
 4   대여소명     object
 5   성별       object
 6   연령대코드    object
 7   이용건수     int64
 8   이동거리(M)  float64
 9   이용시간(분)  int64
dtypes: float64(1), int64(4), object(5)
memory usage: 885.0+ MB
None
선택된 데이터가 ./select/서울특별시 공공자전거 이용정보(시간대별)_2401-2405.csv 파일에 저장되었습니다.
'''
