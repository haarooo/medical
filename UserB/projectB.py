import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import koreanfont



# 데이터 불러오기

b_time = pd.read_csv('./UserB/팀B_접근성이용률_시계열.csv', encoding='utf-8')
b_change = pd.read_csv('./UserB/팀B_접근성이용률_5년치변화분석.csv', encoding='utf-8')
c_time = pd.read_csv('./UserC/팀C_수요건강결과_시계열.csv', encoding='utf-8')


# 결측치 확인
print("[B 시계열] 결측치")
print(b_time.isnull().sum())
print("\n[B 5년 변화] 결측치")
print(b_change.isnull().sum())
print("\n[C 시계열] 결측치")
print(c_time.isnull().sum())


# 가설 1
# 2019~2023년 사이 응급실·분만실 관내이용률(uu27, uu28)의 하락폭은
# 수도권보다 비수도권 시군구에서 더 클 것이다.

# 수도권/비수도권 구분 컬럼 추가
수도권_목록 = ['서울특별시', '인천광역시', '경기도']

df1 = b_time.copy()
df1['지역구분'] = df1['명칭'].apply(
    lambda x: '수도권' if x in 수도권_목록 else '비수도권'
)

# 연도별 평균 관내이용률 (수도권 vs 비수도권)
year_average = df1.groupby(['기준연도', '지역구분'])[
    ['uu27_응급실관내이용률', 'uu28_분만실관내이용률']
].mean().reset_index()

print("\n[가설1] 연도별 평균 관내이용률")
print(year_average)


# 5년 변화율 비교 (수도권 vs 비수도권)
df2 = b_change.copy()
df2['지역구분'] = df2['시도'].apply(
    lambda x: '수도권' if x in 수도권_목록 else '비수도권'
)

# 0값은 분만실이 없는 지역이라 제외하고 평균
change_comparison = df2.groupby('지역구분')[
    ['응급실관내이용률_변화율%', '분만실관내이용률_변화율%']
].mean()

print("\n[가설1] 수도권 vs 비수도권 5년 변화율 평균(%)")
print(change_comparison)


# 그래프 1-1: 연도별 응급실 관내이용률 추이
plt.figure(figsize=(10, 5))
sns.lineplot(
    data=year_average,
    x='기준연도', y='uu27_응급실관내이용률',
    hue='지역구분', marker='o'
)
plt.title('연도별 응급실 관내이용률 (수도권 vs 비수도권)')
plt.ylabel('응급실 관내이용률 (%)')
plt.grid(alpha=0.3)
plt.show()


# 그래프 1-2: 연도별 분만실 관내이용률 추이 (0값 제외)
df1_no_zero = df1[df1['uu28_분만실관내이용률'] > 0]
Annual_average_birth = df1_no_zero.groupby(['기준연도', '지역구분'])[
    'uu28_분만실관내이용률'
].mean().reset_index()

plt.figure(figsize=(10, 5))
sns.lineplot(
    data=Annual_average_birth,
    x='기준연도', y='uu28_분만실관내이용률',
    hue='지역구분', marker='o'
)
plt.title('연도별 분만실 관내이용률 (수도권 vs 비수도권, 0값 제외)')
plt.ylabel('분만실 관내이용률 (%)')
plt.grid(alpha=0.3)
plt.show()


# 그래프 1-3: 5년 변화율 박스플롯
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
sns.boxplot(
    data=df2, x='지역구분', y='응급실관내이용률_변화율%', ax=axes[0]
)
axes[0].set_title('응급실 관내이용률 변화율 (2019→2023)')
axes[0].axhline(0, color='red', linestyle='--', alpha=0.5)

sns.boxplot(
    data=df2[df2['분만실관내이용률_변화율%'].notna()],
    x='지역구분', y='분만실관내이용률_변화율%', ax=axes[1]
)
axes[1].set_title('분만실 관내이용률 변화율 (2019→2023)')
axes[1].axhline(0, color='red', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()





# 가설 2
# 노인인구비율(dsp03)이 높은 시군구일수록
# 응급실 30분 도달률(ra27)과 응급실 관내이용률(uu27)이 낮을 것이다.

# B 시계열 + C 시계열 병합 (sd_cd, 기준연도 기준)
merged = pd.merge(
    b_time[['sd_cd', '기준연도', '명칭', 'sd_nm2',
            'ra27_응급실30분도달', 'uu27_응급실관내이용률']],
    c_time[['sd_cd', '기준연도', 'dsp03_노인인구비율']],
    on=['sd_cd', '기준연도'],
    how='inner'
)
print(f"\n[가설2] 병합 후 행 수: {len(merged)}")


