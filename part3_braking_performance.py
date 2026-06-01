"""
汽车理论课程设计三（习题4.3）
中型货车制动性能计算 —— 利用附着系数、制动效率、制动距离
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# ============ 已知参数 ============
g = 9.8

# 空载参数
m_empty = 4080
hg_empty = 0.845
L_empty = 3.950
a_empty = 2.100
beta = 0.38  # 制动力分配系数

# 满载参数
m_full = 9290
hg_full = 1.170
L_full = 3.950
a_full = 2.950
beta_full = 0.38

# 制动系参数
tau1 = 0.02   # 制动系反应时间 (s)
tau2 = 0.02   # 制动减速度上升时间 (s)
ua0 = 30.0    # 初始车速 (km/h)
phi_road = 0.80  # 路面附着系数


def calc_adhesion_curves(m, hg, L, a, beta_val):
    """
    计算利用附着系数曲线和制动效率曲线
    返回: z_array, phi_f, phi_r, E_f, E_r
    """
    b = L - a  # 质心至后轴距离
    z = np.linspace(0.01, 1.0, 200)  # 制动强度

    # 利用附着系数
    phi_f = beta_val * z * L / (b + z * hg)
    phi_r = (1 - beta_val) * z * L / (a - z * hg)

    # 制动效率（避免除零）
    with np.errstate(divide='ignore', invalid='ignore'):
        E_f = np.where(phi_f > 1e-10, z / phi_f, 0)
        E_r = np.where(phi_r > 1e-10, z / phi_r, 0)

    return z, phi_f, phi_r, E_f, E_r


def braking_distance(ua_kmh, phi, E, tau1, tau2):
    """
    计算制动距离
    ua_kmh: 初始车速 (km/h)
    phi: 路面附着系数
    E: 制动效率
    """
    ua_ms = ua_kmh / 3.6  # m/s
    a_bmax = E * phi * g  # 最大制动减速度 (m/s²)

    if a_bmax <= 0:
        return float('inf')

    # s = (τ1 + τ2/2) * ua0 / 3.6 + ua0² / (25.92 * a_bmax)
    s = (tau1 + tau2 / 2) * ua_kmh / 3.6 + ua_kmh**2 / (25.92 * a_bmax)
    return s


# ============ 1. 绘制利用附着系数曲线和制动效率曲线 ============
print("=" * 50)
print("题目三：中型货车制动性能计算")
print("=" * 50)

fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# 空载
z_empty, phi_f_empty, phi_r_empty, E_f_empty, E_r_empty = \
    calc_adhesion_curves(m_empty, hg_empty, L_empty, a_empty, beta)

# 满载
z_full, phi_f_full, phi_r_full, E_f_full, E_r_full = \
    calc_adhesion_curves(m_full, hg_full, L_full, a_full, beta_full)

# 利用附着系数——空载
ax = axes[0, 0]
ax.plot(z_empty, phi_f_empty, 'b-', label='前轴 φf (空载)', linewidth=1.5)
ax.plot(z_empty, phi_r_empty, 'r-', label='后轴 φr (空载)', linewidth=1.5)
ax.plot([0, 1], [0, 1], 'k--', linewidth=0.8, alpha=0.5)  # φ=z 参考线
# ECE法规线
z_ECE = np.linspace(0.15, 0.8, 100)
phi_ECE = (z_ECE + 0.07) / 0.85
ax.plot(z_ECE, phi_ECE, 'g--', linewidth=1, alpha=0.7, label='ECE法规')
ax.set_xlabel('制动强度 z', fontsize=11)
ax.set_ylabel('利用附着系数 φ', fontsize=11)
ax.set_title('利用附着系数曲线（空载）', fontsize=12)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 1.0)
ax.set_ylim(0, 1.2)

# 利用附着系数——满载
ax = axes[0, 1]
ax.plot(z_full, phi_f_full, 'b-', label='前轴 φf (满载)', linewidth=1.5)
ax.plot(z_full, phi_r_full, 'r-', label='后轴 φr (满载)', linewidth=1.5)
ax.plot([0, 1], [0, 1], 'k--', linewidth=0.8, alpha=0.5)
ax.plot(z_ECE, phi_ECE, 'g--', linewidth=1, alpha=0.7, label='ECE法规')
ax.set_xlabel('制动强度 z', fontsize=11)
ax.set_ylabel('利用附着系数 φ', fontsize=11)
ax.set_title('利用附着系数曲线（满载）', fontsize=12)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 1.0)
ax.set_ylim(0, 1.2)

# 制动效率——空载
ax = axes[1, 0]
# 只绘制有效范围内的效率（附着系数不超过路面附着系数的典型值）
mask_f_empty = phi_f_empty <= 1.2
mask_r_empty = phi_r_empty <= 1.2
ax.plot(phi_f_empty[mask_f_empty], E_f_empty[mask_f_empty], 'b-', label='前轴效率 Ef', linewidth=1.5)
ax.plot(phi_r_empty[mask_r_empty], E_r_empty[mask_r_empty], 'r-', label='后轴效率 Er', linewidth=1.5)
ax.set_xlabel('附着系数 φ', fontsize=11)
ax.set_ylabel('制动效率 E', fontsize=11)
ax.set_title('制动效率曲线（空载）', fontsize=12)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 1.0)
ax.set_ylim(0, 1.1)

# 制动效率——满载
ax = axes[1, 1]
mask_f_full = phi_f_full <= 1.2
mask_r_full = phi_r_full <= 1.2
ax.plot(phi_f_full[mask_f_full], E_f_full[mask_f_full], 'b-', label='前轴效率 Ef', linewidth=1.5)
ax.plot(phi_r_full[mask_r_full], E_r_full[mask_r_full], 'r-', label='后轴效率 Er', linewidth=1.5)
ax.set_xlabel('附着系数 φ', fontsize=11)
ax.set_ylabel('制动效率 E', fontsize=11)
ax.set_title('制动效率曲线（满载）', fontsize=12)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 1.0)
ax.set_ylim(0, 1.1)

plt.tight_layout()
plt.savefig('fig5_adhesion_efficiency.png', dpi=150)
plt.close()
print("图5已保存：fig5_adhesion_efficiency.png")

# ============ 2. 制动距离计算（满载，Ua=30km/h, φ=0.80） ============
print(f"\n--- 制动距离计算（{ua0}km/h, φ={phi_road}）---")

# 满载时的制动效率
# 找到满载时在φ=0.80路面上对应哪个轴的制动效率
# 前轴：φf = β*z*L/(b+z*hg)，当φf=0.80时求z
b_full = L_full - a_full  # 质心至后轴距离

# 在φ=0.80路面上，前轴先抱死还是后轴先抱死取决于利用附着系数
# 求前轴利用附着系数=0.80时的制动强度z_f
# β*z*L/(b+z*hg) = 0.80
# β*z*L = 0.80*(b+z*hg)
# β*z*L - 0.80*z*hg = 0.80*b
# z*(β*L - 0.80*hg) = 0.80*b
z_f_at_phi = (phi_road * b_full) / (beta * L_full - phi_road * hg_full)
# 后轴利用附着系数=0.80时的制动强度z_r
z_r_at_phi = (phi_road * a_full) / ((1 - beta) * L_full + phi_road * hg_full)

print(f"  前轴在φ=0.80时对应的制动强度 z_f = {z_f_at_phi:.4f}")
print(f"  后轴在φ=0.80时对应的制动强度 z_r = {z_r_at_phi:.4f}")

# 较小者先抱死，决定制动效率
# 找前轴和后轴在φ=0.80时的制动效率
# 插值法
E_f_at_phi = np.interp(phi_road, phi_f_full, E_f_full)
E_r_at_phi = np.interp(phi_road, phi_r_full, E_r_full)

print(f"  满载前轴制动效率 Ef(φ=0.80) = {E_f_at_phi:.4f}")
print(f"  满载后轴制动效率 Er(φ=0.80) = {E_r_at_phi:.4f}")

# 制动效率取较小者（先抱死的轴决定整车制动效率）
E_effective = min(E_f_at_phi, E_r_at_phi)
print(f"  整车有效制动效率 E = {E_effective:.4f}")

# 制动距离
s_normal = braking_distance(ua0, phi_road, E_effective, tau1, tau2)
a_bmax_normal = E_effective * phi_road * g

print(f"\n  正常制动距离：s = {s_normal:.2f} m")
print(f"  最大制动减速度：a_bmax = {a_bmax_normal:.2f} m/s²")

# 空载情况
E_f_empty_phi = np.interp(phi_road, phi_f_empty, E_f_empty)
E_r_empty_phi = np.interp(phi_road, phi_r_empty, E_r_empty)
E_effective_empty = min(E_f_empty_phi, E_r_empty_phi)
s_empty = braking_distance(ua0, phi_road, E_effective_empty, tau1, tau2)
a_bmax_empty = E_effective_empty * phi_road * g

print(f"\n  空载制动距离：s = {s_empty:.2f} m")
print(f"  空载最大制动减速度：a_bmax = {a_bmax_empty:.2f} m/s²")
print(f"  空载制动效率 E = {E_effective_empty:.4f}")

# ============ 3. 管路损坏时的制动距离 ============
print(f"\n--- 制动管路损坏时的制动距离 ---")

# 前部管路损坏：只有后轮制动，β=0
beta_rear_only = 0.0
z_r_fail, phi_f_r_fail, phi_r_r_fail, E_f_r_fail, E_r_r_fail = \
    calc_adhesion_curves(m_full, hg_full, L_full, a_full, beta_rear_only)

# φ=0.80时后轮制动效率
phi_r_rear_fail_at_phi = np.interp(phi_road, phi_r_r_fail, E_r_r_fail) if \
    phi_r_r_fail[-1] >= phi_road else 0

# 对于前部管路损坏，后轴利用附着系数=0.80对应制动强度
# (1-0)*z*L/(a - z*hg) = z*L/(a - z*hg) = 0.80 → z = 0.80*a/(L+0.80*hg)
z_rear_only = (phi_road * a_full) / (L_full + phi_road * hg_full)
E_rear_only = z_rear_only / phi_road
s_rear_fail = braking_distance(ua0, phi_road, E_rear_only, tau1, tau2)
a_bmax_rear_fail = E_rear_only * phi_road * g

print(f"\n【前部管路损坏（仅后轮制动）】")
print(f"  制动强度 z = {z_rear_only:.4f}")
print(f"  制动效率 E = {E_rear_only:.4f}")
print(f"  制动距离 s = {s_rear_fail:.2f} m")
print(f"  最大制动减速度 a_bmax = {a_bmax_rear_fail:.2f} m/s²")

# 后部管路损坏：只有前轮制动，β=1
beta_front_only = 1.0
z_f_fail, phi_f_f_fail, phi_r_f_fail, E_f_f_fail, E_r_f_fail = \
    calc_adhesion_curves(m_full, hg_full, L_full, a_full, beta_front_only)

# β=1时，前轴利用附着系数=0.80对应制动强度
# 1*z*L/(b+z*hg) = 0.80 → z = 0.80*b/(L-0.80*hg)
z_front_only = (phi_road * b_full) / (L_full - phi_road * hg_full)
E_front_only = z_front_only / phi_road
s_front_fail = braking_distance(ua0, phi_road, E_front_only, tau1, tau2)
a_bmax_front_fail = E_front_only * phi_road * g

print(f"\n【后部管路损坏（仅前轮制动）】")
print(f"  制动强度 z = {z_front_only:.4f}")
print(f"  制动效率 E = {E_front_only:.4f}")
print(f"  制动距离 s = {s_front_fail:.2f} m")
print(f"  最大制动减速度 a_bmax = {a_bmax_front_fail:.2f} m/s²")

# 汇总对比
print(f"\n{'='*55}")
print(f"制动距离汇总（{ua0}km/h, φ={phi_road}）：")
print(f"{'='*55}")
print(f"  满载正常制动：    {s_normal:.2f} m")
print(f"  空载正常制动：    {s_empty:.2f} m")
print(f"  前部管路损坏：    {s_rear_fail:.2f} m")
print(f"  后部管路损坏：    {s_front_fail:.2f} m")
print(f"{'='*55}")

# ============ 关键数据点输出 ============
print(f"\n--- 关键附着系数分析 ---")
# 空载同步附着系数
b_empty = L_empty - a_empty
phi0_empty = (L_empty * beta - b_empty) / hg_empty
print(f"空载同步附着系数 φ0 = {phi0_empty:.4f}")

# 满载同步附着系数
b_full = L_full - a_full
phi0_full = (L_full * beta_full - b_full) / hg_full
print(f"满载同步附着系数 φ0 = {phi0_full:.4f}")

# 分析制动稳定性
print(f"\n制动稳定性分析：")
for label, phi0, cond in [("空载", phi0_empty, "空载"), ("满载", phi0_full, "满载")]:
    if phi0 > phi_road:
        print(f"  {label}：φ0={phi0:.2f} > φ={phi_road}，前轮先抱死，制动稳定")
    else:
        print(f"  {label}：φ0={phi0:.2f} < φ={phi_road}，后轮先抱死，存在侧滑风险")

print("\n" + "=" * 50)
print("题目三计算完成！")
print("=" * 50)
