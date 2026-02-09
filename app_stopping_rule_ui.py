import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams

from reliability.stopping_rule import (
    minimal_total_time_to_pass,
    extra_time_needed,
)

# Configure Chinese font fallback for matplotlib labels.
def _setup_matplotlib_chinese_font() -> None:
    candidate_fonts = [
        "Microsoft YaHei",
        "SimHei",
        "Noto Sans CJK SC",
        "Source Han Sans SC",
        "PingFang SC",
        "WenQuanYi Zen Hei",
    ]
    installed = {f.name for f in font_manager.fontManager.ttflist}
    selected = next((name for name in candidate_fonts if name in installed), None)
    if selected:
        rcParams["font.sans-serif"] = [selected] + rcParams.get("font.sans-serif", [])
    rcParams["axes.unicode_minus"] = False


_setup_matplotlib_chinese_font()

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="贝叶斯停止规则（Poisson–Gamma）", layout="wide")
st.title("贝叶斯停止规则：表格 + 曲线 + 事故后补测时间")

with st.sidebar:
    st.header("可靠性要求")
    lam0 = st.number_input("λ₀（目标失效率）", value=1e-3, format="%.6g")
    alpha = st.number_input("α（置信度 = 1-α）", value=1e-2, format="%.6g")

    st.header("先验（Gamma(a,b)）")
    a = st.number_input("a（先验失败次数 + 1）", value=1.0, min_value=1e-9)
    b = st.number_input("b（先验时间信用）", value=0.0, min_value=0.0)

    st.header("表格设置")
    r_max = st.slider("最大失败次数（r_max）", 0, 30, 10)

    st.header("当前/事故状态")
    r_current = st.number_input("当前失败次数 r", value=1, min_value=0, step=1)
    T_current = st.number_input("当前总测试时间 T", value=2033.0, min_value=0.0)

# -------------------------
# Table computation
# -------------------------
rows = []
for r in range(0, r_max + 1):
    T_req = minimal_total_time_to_pass(lam0, alpha, r, a, b)
    rows.append(
        {
            "失败次数 r": r,
            "所需总测试时间 T": T_req,
            "从当前起需补充时间": max(0.0, T_req - T_current),
        }
    )
df = pd.DataFrame(rows)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("停止规则表")
    st.dataframe(df, width="stretch")

    dt = extra_time_needed(lam0, alpha, r_current, a, b, T_current)
    st.subheader("事故后需补测时间")
    st.metric("ΔT（所需无事故补测时间）", f"{dt:.1f}")

with col2:
    st.subheader("曲线：所需总测试时间随失败次数变化")
    fig = plt.figure()
    plt.plot(df["失败次数 r"], df["所需总测试时间 T"], marker="o")
    plt.xlabel("失败次数（r）")
    plt.ylabel("所需总测试时间 T")
    plt.grid(True)
    st.pyplot(fig)
