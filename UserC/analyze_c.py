
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from common import koreanfont
import numpy as np

data1 = pd.read_csv('./UserC/팀C_수요건강결과_5년치변화분석.csv', encoding='utf-8')
data2 = pd.read_csv('./UserA/팀A_의료자원공급_5년치변화분석.csv', encoding='utf-8')


# 결측치 확인
print(data1)
print(data1.isnull().sum())

print(data2)
print(data2.isnull().sum())


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

# 가설 1 
# 2019년부터 2023년 사이 분만 건수가 감소한 시군구에서는분만실 밀집도도 함께 감소했을 것이다.



# 데이터 합치기
df = pd.merge(df1, df2, on=['sd_cd', '시도', '시군구'], how='inner')

# 확인할 연도
years = [2019, 2020, 2021, 2022, 2023]

result = []

for year in years:
    old_col = f'노인인구비율_{year}'
    doctor_col = f'전체의사_{year}'

    # 필요한 컬럼
    temp = df[['시도', '시군구', old_col, doctor_col]]

    # 숫자로 변환
    temp[old_col] = pd.to_numeric(temp[old_col], errors='coerce')
    temp[doctor_col] = pd.to_numeric(temp[doctor_col], errors='coerce')

    # 결측치 제거
    temp = temp.dropna()

    # 노인인구비율 상위 25%, 하위 25% 기준값
    high_cut = temp[old_col].quantile(0.75)
    low_cut = temp[old_col].quantile(0.25)

    # 고령화 상위/하위 지역 나누기
    high_old = temp[temp[old_col] >= high_cut]
    low_old = temp[temp[old_col] <= low_cut]

    # 평균 의사 수
    high_doctor_mean = high_old[doctor_col].mean()
    low_doctor_mean = low_old[doctor_col].mean()

    # 결과 저장
    result.append({
        '연도': year,
        '고령화_상위25_평균의사수': high_doctor_mean,
        '고령화_하위25_평균의사수': low_doctor_mean,
        '격차_하위25_minus_상위25': low_doctor_mean - high_doctor_mean
    })

# 결과표
result_df = pd.DataFrame(result)

print(result_df)

# 1. 고령화 상위/하위 평균 의사 수 비교

plt.figure(figsize=(10, 6))

plt.plot(
    result_df['연도'],
    result_df['고령화_상위25_평균의사수'],
    marker='o',
    label='고령화 상위 25%'
)

plt.plot(
    result_df['연도'],
    result_df['고령화_하위25_평균의사수'],
    marker='o',
    label='고령화 하위 25%'
)

plt.title('고령화 수준별 평균 의사 수 비교', fontsize=15)
plt.xlabel('연도')
plt.ylabel('평균 전체의사 수')
plt.legend()
plt.grid(True)
plt.show()


# =========================
# 2. 의사 수 격차 변화
# =========================

plt.figure(figsize=(10, 6))

plt.plot(
    result_df['연도'],
    result_df['격차_하위25_minus_상위25'],
    marker='o'
)

plt.axhline(0, linestyle='--')

plt.title('고령화 하위 25%와 상위 25%의 의사 수 격차', fontsize=15)
plt.xlabel('연도')
plt.ylabel('의사 수 격차\n하위 25% - 상위 25%')
plt.grid(True)
plt.show()
