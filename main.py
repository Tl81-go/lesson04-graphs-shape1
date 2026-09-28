import streamlit as st
import pandas as pd
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

# 장르가 여러 개라면 첫 번째 장르만 사용
df["장르"] = df["genre"].fillna("").astype(str).str.split("|").str[0]

# 빈 장르 제거
genre_df = df[df["장르"] != ""].copy()

# 장르별 영화 편수 계산
genre_count = (
    genre_df["장르"]
    .value_counts()
    .reset_index()
)

genre_count.columns = ["장르", "영화편수"]


# ==========================================
# 그래프 1. 장르별 영화 편수
# ==========================================

st.divider()
st.header("그래프 1. 장르별 영화 편수")

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


# ==========================================
# 그래프로 알 수 있는 것
# ==========================================

st.subheader("이 그래프로 알 수 있는 것")
st.write("여기에 이 그래프를 보고 알 수 있는 내용을 한 문장으로 작성하세요.")


# ==========================================
# 앞으로 추가할 그래프
# ==========================================

st.divider()
st.header("그래프 2")
st.write("다음 그래프를 여기에 추가하세요.")

st.divider()
st.header("그래프 3")
st.write("다음 그래프를 여기에 추가하세요.")
