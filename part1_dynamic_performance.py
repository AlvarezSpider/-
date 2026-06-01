"""
汽车理论课程设计一（习题1.3）
轻型货车动力性能计算 —— 五档变速器
"""
import numpy as np
from scipy import integrate, interpolate
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# ============ 已知参数 ============
m_total = 3880       # 总质量 (kg)
m_load = 2000        # 装载质量 (kg)
m_curb = 1800        # 整备质量 (kg)
r_wheel = 0.367      # 车轮半径 (m)
eta_t = 0.85         # 传动系机械效率
f = 0.013            # 滚动阻力系数
CD_A = 2.77          # 空气阻力系数×迎风面积 (m²)
i0 = 5.83            # 主减速器传动比
If = 0.218           # 飞轮转动惯量 (kg·m²)
Iw1 = 1.798          # 二前轮转动惯量 (kg·m²)
Iw2 = 3.598          # 四后轮转动惯量 (kg·m²)
Iw_total = Iw1 + Iw2 # 总车轮转动惯量
L = 3.2              # 轴距 (m)
a = 1.947            # 质心至前轴距离（满载）(m)
hg = 0.9             # 质心高（满载）(m)
g = 9.8              # 重力加速度

# 五档变速器传动比
ig_list = np.array([5.56, 2.769, 1.644, 1.00, 0.793])
gear_labels = ['1档', '2档', '3档', '4档', '5档']

n_min, n_max = 600, 4000  # 发动机转速范围 (r/min)
n = np.linspace(n_min, n_max, 500)


def engine_torque(n):
    """发动机外特性转矩 Tq (N·m), n in r/min"""
    x = n / 1000.0
    return -19.313 + 295.27 * x - 165.44 * x**2 + 40.874 * x**3 - 3.8445 * x**4


def vehicle_speed(n, ig):
    """车速 ua (km/h)"""
    return 0.377 * r_wheel * n / (ig * i0)


def driving_force(n, ig):
    """驱动力 Ft (N)"""
    Tq = engine_torque(n)
    return Tq * ig * i0 * eta_t / r_wheel


def rolling_resistance():
    """滚动阻力 Ff (N)"""
    return m_total * g * f


def air_resistance(ua):
    """空气阻力 Fw (N), ua in km/h"""
    return CD_A * ua**2 / 21.15


def rotating_mass_factor(ig):
    """旋转质量换算系数 δ"""
    Iw_sum = Iw_total
    delta = 1 + (Iw_sum + If * ig**2 * i0**2 * eta_t) / (m_total * r_wheel**2)
    return delta


# ============ 1. 绘制驱动力-行驶阻力平衡图 ============
print("=" * 50)
print("题目一：轻型货车动力性能计算")
print("=" * 50)

plt.figure(figsize=(10, 7))

# 绘制各档驱动力曲线
max_ua = 0
for idx, ig in enumerate(ig_list):
    ua = vehicle_speed(n, ig)
    Ft = driving_force(n, ig)
    plt.plot(ua, Ft / 1000.0, label=f'Ft {gear_labels[idx]} (ig={ig})')
    max_ua = max(max_ua, ua[-1])

# 绘制阻力曲线
ua_range = np.linspace(0, max_ua * 1.05, 500)
Ff = np.full_like(ua_range, rolling_resistance())
Fw = air_resistance(ua_range)
F_total = (Ff + Fw) / 1000.0
Ff_plot = Ff / 1000.0

plt.plot(ua_range, Ff_plot, 'k--', label='滚动阻力 Ff', linewidth=1.5)
plt.plot(ua_range, (Ff + Fw) / 1000.0, 'k-', label='总阻力 Ff+Fw', linewidth=1.5)

plt.xlabel('车速 ua (km/h)', fontsize=12)
plt.ylabel('力 (kN)', fontsize=12)
plt.title('汽车驱动力-行驶阻力平衡图（五档变速器）', fontsize=14)
plt.legend(fontsize=9, loc='upper left')
plt.grid(True, alpha=0.3)
plt.xlim(0, ua_range[-1])
plt.ylim(0, None)
plt.tight_layout()
plt.savefig('fig1_driving_resistance_balance.png', dpi=150)
plt.close()
print("图1已保存：fig1_driving_resistance_balance.png")

# ============ 2. 求最高车速 ============
# 最高车速发生在最高档（5档）驱动力与总阻力曲线的交点
ig5 = ig_list[-1]
ua5 = vehicle_speed(n, ig5)
Ft5 = driving_force(n, ig5)
F_resist = rolling_resistance() + air_resistance(ua5)

# 寻找交点（驱动力 >= 阻力的最大车速）
diff = Ft5 - F_resist
# 找到从正到负的转折点
cross_idx = None
for i in range(len(diff) - 1):
    if diff[i] >= 0 and diff[i + 1] < 0:
        cross_idx = i
        break

if cross_idx is not None:
    # 线性插值精确求交点
    ua_max = ua5[cross_idx] + (ua5[cross_idx + 1] - ua5[cross_idx]) * \
             (0 - diff[cross_idx]) / (diff[cross_idx + 1] - diff[cross_idx])
else:
    ua_max = ua5[-1]

print(f"\n最高车速 ua_max = {ua_max:.2f} km/h")

# 最大转矩点
Tq_max = engine_torque(n)
Tq_max_val = np.max(Tq_max)
n_Tq_max = n[np.argmax(Tq_max)]
print(f"发动机最大转矩 Tq_max = {Tq_max_val:.2f} N·m @ n = {n_Tq_max:.0f} r/min")

# 最大功率点
Pe = engine_torque(n) * n / 9550.0
Pe_max = np.max(Pe)
n_Pe_max = n[np.argmax(Pe)]
print(f"发动机最大功率 Pe_max = {Pe_max:.2f} kW @ n = {n_Pe_max:.0f} r/min")

# ============ 3. 求最大爬坡度 ============
# 使用1档计算最大爬坡度
ig1 = ig_list[0]
ua1 = vehicle_speed(n, ig1)
Ft1 = driving_force(n, ig1)
Ff_val = rolling_resistance()

# 在1档最低稳定车速处计算最大爬坡度（通常在最大转矩点附近的车速）
# 取1档发动机最低转速以上范围
for i, ua_val in enumerate(ua1):
    if ua_val > 10:  # 从10km/h以上开始（绕过很低车速不稳定的区域）
        idx_start = i
        break
else:
    idx_start = 0

# 取最大转矩对应的转速附近
idx_tq_max = np.argmax(engine_torque(n))
ua_at_max_Tq_1st = ua1[idx_tq_max]

# 计算各车速下的爬坡度
Ft1_sub = Ft1[idx_start:]
ua1_sub = ua1[idx_start:]
Fw1_sub = air_resistance(ua1_sub)

sin_alpha = (Ft1_sub - Ff_val - Fw1_sub) / (m_total * g)
sin_alpha = np.clip(sin_alpha, -1.0, 1.0)
alpha = np.arcsin(sin_alpha)
grade = np.tan(alpha)  # i = tan(alpha)

max_grade_idx = np.argmax(grade)
max_grade = grade[max_grade_idx]
max_grade_ua = ua1_sub[max_grade_idx]
max_grade_alpha = np.degrees(alpha[max_grade_idx])

print(f"\n最大爬坡度（1档）：")
print(f"  最大爬坡度 i = {max_grade:.4f} = {max_grade * 100:.2f}%")
print(f"  爬坡角度 α = {max_grade_alpha:.2f}°")
print(f"  对应车速 ua = {max_grade_ua:.2f} km/h")

# ============ 4. 计算最大爬坡度时的附着率 ============
# 后轮驱动货车，附着率 Cφ2 = Fx2 / Fz2
# Fx2 = Ft - Ff - Fw（后轮驱动力）
# Fz2 = mg*a/L*cos(α) + (Ff+Fw)*hg/L + m*g*hg*sin(α)/L ...

# 在最大爬坡度时
alpha_max = alpha[max_grade_idx]
Ft_at_max_grade = Ft1_sub[max_grade_idx]
Fw_at_max_grade = Fw1_sub[max_grade_idx]

# 后轴法向反力
Fz2 = (m_total * g * a * np.cos(alpha_max) +
       (Ft_at_max_grade - Ff_val - Fw_at_max_grade) * hg +
       m_total * g * hg * np.sin(alpha_max)) / L
# 后轮驱动力
Fx2 = Ft_at_max_grade - Ff_val - Fw_at_max_grade
C_phi2 = Fx2 / Fz2

print(f"\n最大爬坡度时的附着率：")
print(f"  后轴法向反力 Fz2 = {Fz2:.2f} N")
print(f"  后轮驱动力 Fx2 = {Fx2:.2f} N")
print(f"  附着率 Cφ2 = {C_phi2:.4f}")

# 不出现滑转的条件：Cφ2 < φ（附着系数）
# 一般干燥良好路面 φ≈0.7-0.8

# ============ 5. 加速度倒数曲线和加速时间 ============
# 2档起步加速至70 km/h
ig2 = ig_list[1]
ua2 = vehicle_speed(n, ig2)
Ft2 = driving_force(n, ig2)
delta2 = rotating_mass_factor(ig2)

# 加速度计算
Ff_val = rolling_resistance()
Fw2 = air_resistance(ua2)
a2 = (Ft2 - Ff_val - Fw2) / (delta2 * m_total)

# 只取加速度为正的部分，且2档起步（最低稳定车速以上）
valid_mask = (a2 > 0.001) & (ua2 >= ua2[0])
ua2_valid = ua2[valid_mask]
a2_valid = a2[valid_mask]

# 加速度倒数
inv_a2 = 1.0 / a2_valid

# 绘制加速度倒数曲线
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# 各档加速度曲线
ax1.set_title('各档加速度曲线', fontsize=12)
for idx, ig in enumerate(ig_list):
    ua_g = vehicle_speed(n, ig)
    Ft_g = driving_force(n, ig)
    Fw_g = air_resistance(ua_g)
    delta_g = rotating_mass_factor(ig)
    a_g = (Ft_g - Ff_val - Fw_g) / (delta_g * m_total)
    a_g = np.clip(a_g, 0, None)
    ax1.plot(ua_g, a_g, label=f'{gear_labels[idx]}')

ax1.set_xlabel('车速 ua (km/h)', fontsize=11)
ax1.set_ylabel('加速度 a (m/s²)', fontsize=11)
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, ua_range[-1])

# 加速度倒数曲线（2档）
ax2.set_title('2档加速度倒数曲线', fontsize=12)
ax2.plot(ua2_valid, inv_a2, 'b-', linewidth=1.5)
ax2.set_xlabel('车速 ua (km/h)', fontsize=11)
ax2.set_ylabel('1/a (s²/m)', fontsize=11)
ax2.grid(True, alpha=0.3)

# 图解积分：计算从起步加速到70km/h的时间
target_speed = 70.0  # km/h
mask_70 = ua2_valid <= target_speed
ua_accel = ua2_valid[mask_70]
inv_a_accel = inv_a2[mask_70]

# 数值积分求加速时间（将速度单位转换为m/s再积分）
# t = ∫(1/a) du, 其中 u in m/s
# dt = (1/a) * du, du in m/s
# ua in km/h → u in m/s: u = ua/3.6
# t = ∫(1/a) * (1/3.6) du_a [km/h]
t_accel = integrate.trapezoid(inv_a_accel, ua_accel) / 3.6

# 填充积分区域
ax2.fill_between(ua_accel, 0, inv_a_accel, alpha=0.3, color='blue')
ax2.axvline(x=target_speed, color='r', linestyle='--', label=f'目标车速={target_speed} km/h')
ax2.legend(fontsize=9)
ax2.set_xlim(ua2_valid[0], ua2_valid[-1])
ax2.set_ylim(0, None)

plt.tight_layout()
plt.savefig('fig2_acceleration_curves.png', dpi=150)
plt.close()

# 打印加速时间
# 找到2档加速到70km/h过程中是否需要换挡
# 2档车速范围
ua2_min = ua2[0]
ua2_max = ua2[-1]

print(f"\n2档车速范围：{ua2_min:.1f} ~ {ua2_max:.1f} km/h")

# 检查2档是否能覆盖0-70km/h
# 如果2档最高车速 < 70，需要换3档
if ua2_max < target_speed:
    # 需要先在2档加速到2档最高车速，然后换3档
    print("2档无法直接达到70km/h，需要换3档继续加速")

    # 2档加速到换挡车速
    mask_2nd = ua2_valid <= ua2_max
    ua_2nd_seg = ua2_valid[mask_2nd]
    inv_a_2nd_seg = inv_a2[mask_2nd]
    t_2nd = integrate.trapezoid(inv_a_2nd_seg, ua_2nd_seg) / 3.6

    # 3档从相应车速继续加速
    ig3 = ig_list[2]
    ua3 = vehicle_speed(n, ig3)
    Ft3 = driving_force(n, ig3)
    Fw3 = air_resistance(ua3)
    delta3 = rotating_mass_factor(ig3)
    a3 = (Ft3 - Ff_val - Fw3) / (delta3 * m_total)

    valid_mask3 = (a3 > 0.001) & (ua3 <= target_speed) & (ua3 >= ua2_max)
    ua3_valid = ua3[valid_mask3]
    inv_a3 = 1.0 / a3[valid_mask3]
    t_3rd = integrate.trapezoid(inv_a3, ua3_valid) / 3.6

    # 加上换挡时间（通常0.5-1s）
    t_shift = 0.8
    t_total = t_2nd + t_3rd + t_shift

    print(f"  2档加速段时间：{t_2nd:.2f} s")
    print(f"  换挡时间：{t_shift:.2f} s")
    print(f"  3档加速段时间：{t_3rd:.2f} s")
    print(f"  2档起步加速至70km/h总时间：{t_total:.2f} s")
else:
    print(f"\n2档起步加速至{target_speed} km/h的时间：")
    print(f"  图解积分法（梯形法则）：t = {t_accel:.2f} s")

    # 也用Simpson法则验证
    if len(ua_accel) >= 3:
        t_accel_simpson = integrate.simpson(inv_a_accel, ua_accel) / 3.6
        print(f"  图解积分法（Simpson法则）：t = {t_accel_simpson:.2f} s")

print("\n" + "=" * 50)
print("题目一计算完成！")
print("=" * 50)
