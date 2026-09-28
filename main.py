
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# ==========================================
# 기본 설정
# ==========================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")


# ==========================================
# 데이터 불러오기
# ==========================================

DATA_URL = "https://raw.githubusercontent.com/happykth/data/main/kobis_movies.csv"

df = pd.read_csv(DATA_URL)


# ==========================================
# 데이터 전처리
# ==========================================

# 여러 장르가 있으면 첫 번째 장르만 사용
df["장르"] = (
    df["genre"]
    .fillna("")
    .astype(str)
    .str.split("|")
    .str[0]
)

# 총 관객을 숫자로 변환
df["total_audi"] = pd.to_numeric(
    df["total_audi"],
    errors="coerce"
)

# 장르와 총 관객이 없는 데이터 제거
df = df[
    (df["장르"] != "") &
    (df["total_audi"].notna())
].copy()


# ==========================================
# 그래프 1. 장르별 영화 편수
# ==========================================

st.divider()
st.header("그래프 1. 장르별 영화 편수")

genre_count = (
    df["장르"]
    .value_counts()
    .reset_index()
)

genre_count.columns = ["장르", "영화편수"]

fig1 = px.pie(
    genre_count,
    names="장르",
    values="영화편수",
    hole=0.55,
    title="장르별 영화 편수"
)

fig1.update_traces(
    textinfo="percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}<extra></extra>"
    )
)

fig1.update_layout(
    legend_title_text="장르"
)

st.plotly_chart(fig1, use_container_width=True)

st.subheader("이 그래프로 알 수 있는 것")
st.write("여기에 장르별 영화 편수에 대해 알 수 있는 내용을 한 문장으로 작성하세요.")


# ==========================================
# 그래프 2. 장르별 영화 총 관객 트리맵
# ==========================================

st.divider()
st.header("그래프 2. 장르 안에 들어 있는 영화")

fig2 = px.treemap(
    df,
    path=["장르", "movieNm"],
    values="total_audi",
    title="장르별 영화의 총 관객 트리맵"
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,.0f}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    margin=dict(t=50, l=10, r=10, b=10)
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("이 그래프로 알 수 있는 것")
st.write("여기에 장르별 영화의 총 관객 규모에 대해 알 수 있는 내용을 한 문장으로 작성하세요.")


# ==========================================
# 그래프 3. 총 관객 분포 히스토그램
# ==========================================

st.divider()
st.header("그래프 3. 총 관객 분포")

fig3 = px.histogram(
    df,
    x="total_audi",
    nbins=20,
    title="영화별 총 관객 분포",
    labels={
        "total_audi": "총 관객 수",
        "count": "영화 편수"
    }
)

fig3.update_traces(
    hovertemplate=(
        "총 관객 구간: %{x}<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    )
)

fig3.update_layout(
    xaxis_title="총 관객 수",
    yaxis_title="영화 편수"
)

st.plotly_chart(fig3, use_container_width=True)


# ==========================================
# 그래프 3 해석
# ==========================================

# 가장 관객이 많은 영화
most_audience_movie = df.loc[
    df["total_audi"].idxmax()
]

# numpy를 이용해서 히스토그램 구간 계산
counts, bin_edges = np.histogram(
    df["total_audi"],
    bins=20
)

# 영화가 가장 많이 들어 있는 구간
max_bin_index = counts.argmax()

bin_start = bin_edges[max_bin_index]
bin_end = bin_edges[max_bin_index + 1]


st.subheader("이 그래프로 알 수 있는 것")

st.write(
    f"대부분의 영화는 총 관객 약 "
    f"{bin_start:,.0f}명~{bin_end:,.0f}명 구간에 몰려 있습니다."
)

st.write(
    f"가장 관객이 많은 영화는 "
    f"「{most_audience_movie['movieNm']}」로, "
    f"총 관객은 {most_audience_movie['total_audi']:,.0f}명입니다."
)


# ==========================================
# 앞으로 추가할 그래프
# ==========================================

st.divider()
st.header("그래프 4")
st.write("다음 그래프를 여기에 추가하세요.")
