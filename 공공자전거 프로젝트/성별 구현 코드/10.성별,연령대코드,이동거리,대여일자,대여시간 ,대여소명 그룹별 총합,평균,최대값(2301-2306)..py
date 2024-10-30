import pandas as pd
from geopy.geocoders import Nominatim
import folium

# Load the dataset
path = './missingvalue/서울특별시 공공자전거 이용정보(시간대별)_2301-2306missing.csv'
bicyclesung = pd.read_csv(path, encoding='utf-8')

# Handle missing values by dropping rows with missing '성별', '연령대코드', '이동거리(M)', '대여일자', '대여시간', and '대여소명'
bicyclesung = bicyclesung.dropna(subset=['성별', '연령대코드', '이동거리(M)', '대여일자', '대여시간', '대여소명'])

# Convert '이동거리(M)' to numeric in case there are any non-numeric values
bicyclesung['이동거리(M)'] = pd.to_numeric(bicyclesung['이동거리(M)'], errors='coerce')

# Group by '대여일자', '대여시간', '대여소명', '성별', and '연령대코드', then calculate sum, mean, max, and min for '이동거리(M)'
distance_stats = bicyclesung.groupby(['대여일자', '대여시간', '대여소명', '성별', '연령대코드'])['이동거리(M)'].agg(['sum', 'mean', 'max', 'min']).reset_index()

# Round the values to 2 decimal places
distance_stats = distance_stats.round({'sum': 2, 'mean': 2, 'max': 2, 'min': 2})

# Print the result
print(distance_stats)
'''
,평균,최대값(2301-2306)..py"
                대여일자  대여시간                       대여소명 성별 연령대코드      sum     mean      max      min
0         2023-01-01     0  1001. 광진교 남단 사거리(천호공원 방면)  F   20대  8311.19  8311.19  8311.19  8311.19
1         2023-01-01     0  1001. 광진교 남단 사거리(천호공원 방면)  M    기타  1341.21  1341.21  1341.21  1341.21
2         2023-01-01     0       1009. 천호역4번출구(현대백화점)  M   20대  1095.88  1095.88  1095.88  1095.88
3         2023-01-01     0                1010. 강동세무서  M   50대   349.26   349.26   349.26   349.26
4         2023-01-01     0           1011. LIGA 아파트 앞  F   40대  5270.00  5270.00  5270.00  5270.00
...              ...   ...                        ... ..   ...      ...      ...      ...      ...
11740185  2023-06-30    23         996.응암역2번출구 국민은행 앞  M   20대  3054.69  1527.34  2530.00   524.69
11740186  2023-06-30    23         996.응암역2번출구 국민은행 앞  M   30대  1565.18  1565.18  1565.18  1565.18
11740187  2023-06-30    23         996.응암역2번출구 국민은행 앞  M   40대   750.00   750.00   750.00   750.00
11740188  2023-06-30    23         996.응암역2번출구 국민은행 앞  M   50대   490.00   490.00   490.00   490.00
11740189  2023-06-30    23         996.응암역2번출구 국민은행 앞  M   60대   670.00   670.00   670.00   670.00

[11740190 rows x 9 columns]
'''
