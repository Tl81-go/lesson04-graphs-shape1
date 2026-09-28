
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

# 제작 국가가 여러 개라면 첫 번째 국가만 사용
df["제작 국가"] = (
    df["nation"]
    .fillna("")
    .astype(str)
    .str.split("|")
    .str[0]
)

# 숫자 데이터 변환
df["total_audi"] = pd.to_numeric(
    df["total_audi"],
    errors="coerce"
)

df["first_scrn"] = pd.to_numeric(
    df["first_scrn"],
    errors="coerce"
)

df["first_week_audi"] = pd.to_numeric(
    df["first_week_audi"],
    errors="coerce"
)

# 필요한 데이터가 없는 행 제거
df = df[
    (df["장르"] != "") &
    (df["제작 국가"] != "") &
    (df["total_audi"].notna()) &
    (df["first_scrn"].notna()) &
    (df["first_week_audi"].notna())
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
st.write(
    "여기에 장르별 영화 편수에 대해 알 수 있는 내용을 한 문장으로 작성하세요."
)


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
st.write(
    "여기에 장르별 영화의 총 관객 규모에 대해 알 수 있는 내용을 한 문장으로 작성하세요."
)


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

most_audience_movie = df.loc[
    df["total_audi"].idxmax()
]

counts, bin_edges = np.histogram(
    df["total_audi"],
    bins=20
)

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
# 그래프 4. 개봉일 스크린수와 총 관객의 관계
# ==========================================

st.divider()
st.header("그래프 4. 개봉일 스크린수와 총 관객의 관계")

fig4 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="장르",
    hover_name="movieNm",
    title="개봉일 스크린수와 총 관객의 관계",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객",
        "장르": "장르"
    }
)

fig4.update_traces(
    marker=dict(size=9),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린수: %{x:,.0f}개<br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig4.update_layout(
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객",
    legend_title="장르"
)

st.plotly_chart(fig4, use_container_width=True)

st.subheader("이 그래프로 알 수 있는 것")
st.write(
    "여기에 개봉일 스크린수와 총 관객의 관계에 대해 알 수 있는 내용을 한 문장으로 작성하세요."
)


# ==========================================
# 그래프 5. 장르별 총 관객 상자 그림
# ==========================================

st.divider()
st.header("그래프 5. 장르별 총 관객 분포")

genre_movie_count = df["장르"].value_counts()

valid_genres = genre_movie_count[
    genre_movie_count >= 10
].index

box_df = df[
    df["장르"].isin(valid_genres)
].copy()

fig5 = px.box(
    box_df,
    x="장르",
    y="total_audi",
    color="장르",
    points="outliers",
    custom_data=["movieNm"],
    title="영화가 10편 이상인 장르의 총 관객 분포",
    labels={
        "장르": "장르",
        "total_audi": "총 관객"
    }
)

fig5.update_traces(
    hovertemplate=(
        "<b>%{customdata[0]}</b><br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig5.update_layout(
    xaxis_title="장르",
    yaxis_title="총 관객",
    showlegend=False
)

st.plotly_chart(fig5, use_container_width=True)

st.subheader("이 그래프로 알 수 있는 것")
st.write(
    "영화가 10편 이상인 장르들의 총 관객 분포와 "
    "장르별 관객의 중앙값 및 이상치를 비교할 수 있습니다."
)


# ==========================================
# 그래프 6. 개봉일 스크린수와 총 관객의 버블 그래프
# ==========================================

st.divider()
st.header("그래프 6. 첫 주 관객을 크기로 나타낸 버블 그래프")

fig6 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="장르",
    hover_name="movieNm",
    size_max=45,
    title="개봉일 스크린수 · 첫 주 관객 · 총 관객의 관계",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객",
        "first_week_audi": "첫 주 관객",
        "장르": "장르"
    }
)

fig6.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린수: %{x:,.0f}개<br>"
        "총 관객: %{y:,.0f}명<br>"
        "첫 주 관객: %{marker.size:,.0f}명"
        "<extra></extra>"
    )
)

fig6.update_layout(
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객",
    legend_title="장르"
)

st.plotly_chart(fig6, use_container_width=True)

st.subheader("이 그래프로 알 수 있는 것")
st.write(
    "점의 크기를 통해 첫 주 관객이 많은 영화가 "
    "개봉일 스크린수와 총 관객에서 어떤 위치에 있는지 살펴볼 수 있습니다."
)


# ==========================================
# 그래프 7. 제작 국가 → 장르 선버스트
# ==========================================

st.divider()
st.header("그래프 7. 제작 국가와 장르별 영화 분포")

# 제작 국가 → 장르별 영화 편수 계산
sunburst_df = (
    df.groupby(["제작 국가", "장르"])
    .size()
    .reset_index(name="영화편수")
)

fig7 = px.sunburst(
    sunburst_df,
    path=["제작 국가", "장르"],
    values="영화편수",
    title="제작 국가에서 장르로 내려가는 영화 분포"
)

fig7.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편"
        "<extra></extra>"
    )
)

fig7.update_layout(
    margin=dict(t=50, l=10, r=10, b=10)
)

st.plotly_chart(fig7, use_container_width=True)

st.subheader("이 그래프로 알 수 있는 것")
st.write(
    "제작 국가별로 어떤 장르의 영화가 많이 포함되어 있는지와 "
    "각 국가와 장르의 영화 편수 비중을 비교할 수 있습니다."
)


# ==========================================
# 앞으로 추가할 그래프
# ==========================================

st.divider()
st.header("그래프 8")
st.write("다음 그래프를 여기에 추가하세요.")
