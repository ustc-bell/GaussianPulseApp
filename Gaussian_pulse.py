# gaussian_pulse_app.py

from PIL import Image
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 设置页面为宽屏 + 标题
st.set_page_config(layout="wide", page_title="Tempo Optics Pulse Visualizer")


# Logo + 标题横幅
# col1, col2 = st.columns([1, 5])
# with col1:
#     st.image("tempo_logo.png", width=250)
    # right side
col1, col2 = st.columns([5, 1])
with col2:
    st.image("tempo_logo.png", width=250)

st.title("Visualization of a Gaussian Pulse (Time & Frequency Domains)")

# 📌 用户通过滑块调节脉宽
fwhm = st.slider("Set FWHM (Unit- ps)", min_value=0.1, max_value=5.0, value=1.0, step=0.1)

# 📐 FWHM → sigma
sigma = fwhm / 2.3548

# 🕒 构造时间轴（单位：ps）
t_max = 10  # 时间窗口大小
n_points = 1025  # 更高精度频谱
t = np.linspace(-t_max, t_max, n_points)
dt = t[1] - t[0]  # 采样间隔

# 📈 计算时域脉冲
I_t = np.exp(-t**2 / (2 * sigma**2))

# 📊 频域分析（使用 numpy FFT）
I_f = np.fft.fft(I_t)
I_f = np.fft.fftshift(I_f)  # 把零频移到中心
#freq = np.fft.fftfreq(n_points, dt)
#freq = np.fft.fftshift(freq)  # 同样频率轴也要居中
# By using the directly definations
W_max=0.5/dt
freq=np.linspace(-W_max, W_max, n_points)

spectrum = np.abs(I_f)**2  # 频率强度谱

# 🎨 创建左右双图
fig, axes = plt.subplots(1, 2, figsize=(10, 3))
#st.pyplot(fig, dpi=150)

# 🟦 左图：时域
axes[0].plot(t, I_t, color='blue', label=f'FWHM = {fwhm} ps')
axes[0].set_title("Time Domain")
axes[0].set_xlabel("Time (ps)")
axes[0].set_ylabel("Intensity (a.u.)")
axes[0].grid(True)
axes[0].legend()

# 🟥 右图：频域
axes[1].plot(freq, spectrum, color='red')
axes[1].set_title("Frequency Domain")
axes[1].set_xlabel("Frequency (THz)")
axes[1].set_ylabel("Spectral Intensity (a.u.)")
axes[1].grid(True)

# ⬇️ 显示图形
st.pyplot(fig)
