"""
汽车理论课程设计二（习题2.7）
轻型货车燃油经济性计算 —— 功率平衡图 + 等速百公里油耗 + 六工况循环
"""
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# ============ 已知参数（与题目一相同） ============
m_total = 3880
r_wheel = 0.367
eta_t = 0.85
f = 0.013
CD_A = 2.77
i0 = 5.83
g = 9.8

# 五档变速器
ig_list = np.array([5.56, 2.769, 1.644, 1.00, 0.793])
gear_labels = ['1档', '2档', '3档', '4档', '5档']

n_min, n_max = 600, 4000
n = np.linspace(n_min, n_max, 500)

# 汽油参数 (93#)
rho_gasoline = 0.715   # 密度 (kg/L)
gamma_gasoline = rho_gasoline * g  # 重度 (N/L)


def engine_torque(n):
    x = n / 1000.0
    return -19.313 + 295.27 * x - 165.44 * x**2 + 40.874 * x**3 - 3.8445 * x**4


def engine_power(n):
    """发动机净功率 Pe (kW)"""
    Tq = engine_torque(n)
    return Tq * n / 9550.0


def vehicle_speed(n, ig):
    return 0.377 * r_wheel * n / (ig * i0)


def engine_speed_from_ua(ua, ig):
    """由车速反算发动机转速"""
    return ua * ig * i0 / (0.377 * r_wheel)


def rolling_resistance():
    return m_total * g * f


def air_resistance(ua):
    return CD_A * ua**2 / 21.15


def resistance_power(ua):
    """阻力功率 (kW)"""
    Ff = rolling_resistance()
    Fw = air_resistance(ua)
    return (Ff + Fw) * ua / (3600.0 * eta_t)


# ============ 负荷特性数据 ============
# 转速 (r/min) 和对应的拟合系数 B0~B4
load_data = {
    815:  [1326.8, -416.46, 72.379,   -5.8629,   0.17768],
    1207: [1354.7, -303.98, 36.657,   -2.0553,   0.043072],
    1614: [1284.4, -189.75, 14.524,   -0.51184,  0.0068164],
    2012: [1122.9, -121.59, 7.0035,   -0.18517,  0.0018555],
    2603: [1141.0, -98.893, 4.4763,   -0.091077, 0.00068906],
    3006: [1051.2, -73.714, 2.8593,   -0.05138,  0.00035032],
    3403: [1233.9, -84.478, 2.9788,   -0.047449, 0.00028230],
    3804: [1129.7, -45.291, 0.71113,  -0.00075215, -0.000038568],
}

n_list = np.array(sorted(load_data.keys()))


def fuel_consumption_rate(Pe, n_target):
    """
    燃油消耗率 b [g/(kW·h)]
    Pe: 发动机功率 (kW)
    n_target: 发动机转速 (r/min)
    用相邻转速曲线插值法求得
    """
    # 找到相邻的两条转速曲线
    if n_target <= n_list[0]:
        n_low, n_high = n_list[0], n_list[1]
    elif n_target >= n_list[-1]:
        n_low, n_high = n_list[-2], n_list[-1]
    else:
        idx = np.searchsorted(n_list, n_target) - 1
        n_low, n_high = n_list[idx], n_list[idx + 1]

    # 在两条转速曲线上分别计算b值
    b_low = np.polyval(load_data[n_low][::-1], Pe)
    b_high = np.polyval(load_data[n_high][::-1], Pe)

    # 线性插值
    if n_high == n_low:
        return b_low
    b = b_low + (b_high - b_low) * (n_target - n_low) / (n_high - n_low)
    return b


# ============ 1. 功率平衡图 ============
print("=" * 50)
print("题目二：轻型货车燃油经济性计算")
print("=" * 50)

plt.figure(figsize=(10, 7))

# 发动机功率曲线
Pe_engine = engine_power(n)
plt.plot(n, Pe_engine, 'r-', linewidth=2, label='发动机功率 Pe')

# 绘制各档等速行驶时发动机功率（即阻力功率换算到发动机端）
ua_range = np.linspace(10, 120, 500)
# 阻力功率曲线（换算到发动机转速）
n_range = np.linspace(n_min, n_max, 500)
Pe_resist = resistance_power(vehicle_speed(n_range, ig_list[-1]))  # 5档阻力功率

# 各档阻力功率 vs 车速
for idx, ig in enumerate(ig_list):
    ua_g = vehicle_speed(n, ig)
    Pe_r = resistance_power(ua_g)
    plt.plot(n, Pe_r, '--', label=f'{gear_labels[idx]}阻力功率', alpha=0.7)

# 发动机外特性功率
plt.plot(n, Pe_engine, 'r-', linewidth=2.5, label='发动机功率 Pe')

plt.xlabel('发动机转速 n (r/min)', fontsize=12)
plt.ylabel('功率 (kW)', fontsize=12)
plt.title('汽车功率平衡图', fontsize=14)
plt.legend(fontsize=8, loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('fig3_power_balance.png', dpi=150)
plt.close()
print("图3已保存：fig3_power_balance.png")

# ============ 2. 等速百公里油耗曲线（最高档和次高档） ============
# 最高档 = 5档 (ig=0.793), 次高档 = 4档 (ig=1.00)

plt.figure(figsize=(9, 6))

for gear_idx, gear_name in [(4, '5档（最高档）'), (3, '4档（次高档）')]:
    ig = ig_list[gear_idx]
    # 计算该档位下不同车速对应的等速油耗
    ua_list_gear = np.linspace(20, vehicle_speed(n_max, ig), 100)

    Qs_list = []
    for ua_val in ua_list_gear:
        n_e = engine_speed_from_ua(ua_val, ig)
        if n_e < n_min or n_e > n_max:
            Qs_list.append(np.nan)
            continue

        Pe_req = resistance_power(ua_val)
        Pe_max_avail = engine_power(n_e)  # 发动机在当前转速下的最大功率
        if Pe_req > Pe_max_avail * 0.95:  # 需求功率超过可用功率
            Qs_list.append(np.nan)
            continue

        b_val = fuel_consumption_rate(Pe_req, n_e)
        Qs = Pe_req * b_val / (1.02 * ua_val * gamma_gasoline)
        Qs_list.append(Qs)

    Qs_list = np.array(Qs_list)
    valid = ~np.isnan(Qs_list)
    if valid.any():
        plt.plot(ua_list_gear[valid], Qs_list[valid], linewidth=2, label=gear_name)

plt.xlabel('车速 ua (km/h)', fontsize=12)
plt.ylabel('等速百公里油耗 Qs (L/100km)', fontsize=12)
plt.title('最高档与次高档等速百公里油耗曲线', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('fig4_constant_speed_fuel.png', dpi=150)
plt.close()
print("图4已保存：fig4_constant_speed_fuel.png")

# 打印一些特征值
for gear_idx, gear_name in [(4, '5档（最高档）'), (3, '4档（次高档）')]:
    ig = ig_list[gear_idx]
    ua_list_gear = np.linspace(30, vehicle_speed(n_max, ig), 200)
    Qs_min = float('inf')
    ua_best = 0
    Qs_60 = None
    Qs_80 = None

    for ua_val in ua_list_gear:
        n_e = engine_speed_from_ua(ua_val, ig)
        if n_e < n_min or n_e > n_max:
            continue
        Pe_req = resistance_power(ua_val)
        if Pe_req > engine_power(n_e) * 0.95:
            continue
        b_val = fuel_consumption_rate(Pe_req, n_e)
        Qs = Pe_req * b_val / (1.02 * ua_val * gamma_gasoline)

        if Qs < Qs_min:
            Qs_min = Qs
            ua_best = ua_val
        if abs(ua_val - 60) < 0.5:
            Qs_60 = Qs
        if abs(ua_val - 80) < 0.5:
            Qs_80 = Qs

    print(f"\n{gear_name}：")
    print(f"  最低油耗 {Qs_min:.2f} L/100km @ {ua_best:.0f} km/h")
    if Qs_60:
        print(f"  60km/h等速油耗：{Qs_60:.2f} L/100km")
    if Qs_80:
        print(f"  80km/h等速油耗：{Qs_80:.2f} L/100km")

# ============ 3. 六工况循环百公里油耗 ============
print(f"\n{'='*30}")
print("六工况循环百公里油耗计算")
print(f"{'='*30}")

# 六工况参数
# 工况, 累计行程(m), 时间(s), 累计时间(s), 车速范围(km/h), 说明
cycle = [
    {"name": "I",   "dist": 50,   "time": 7.2,  "v_start": 25, "v_end": 25, "accel": 0},
    {"name": "II",  "dist": 150,  "time": 16.7, "v_start": 25, "v_end": 40, "accel": 0.25},
    {"name": "III", "dist": 250,  "time": 22.5, "v_start": 40, "v_end": 40, "accel": 0},
    {"name": "IV",  "dist": 175,  "time": 14.0, "v_start": 40, "v_end": 50, "accel": 0.2},
    {"name": "V",   "dist": 250,  "time": 18.0, "v_start": 50, "v_end": 50, "accel": 0},
    {"name": "VI",  "dist": 200,  "time": 19.3, "v_start": 50, "v_end": 25, "accel": -0.36},
]

total_distance = 1075.0  # m
total_fuel_ml = 0.0

print("\n逐工况计算：")
for seg in cycle:
    t_seg = seg["time"]
    n_steps = max(int(t_seg * 10), 50)  # 每个工况至少50步
    t_arr = np.linspace(0, t_seg, n_steps)
    dt = t_arr[1] - t_arr[0]

    fuel_seg = 0.0

    for t_val in t_arr:
        # 当前车速 (km/h)
        if seg["accel"] == 0:
            v_kmh = seg["v_start"]
        else:
            v_kmh = seg["v_start"] + seg["accel"] * t_val * 3.6  # m/s² → km/h

        if v_kmh <= 0:
            continue

        # 计算所需发动机功率
        Ff = rolling_resistance()
        Fw = air_resistance(v_kmh)
        P_resist = (Ff + Fw) * v_kmh / (3600.0 * eta_t)  # kW

        # 选挡策略：根据车速选择合适挡位
        # 使用最高挡（5挡）进行等速工况，加速工况可能需降挡
        if seg["accel"] > 0 and v_kmh < 35:
            ig_used = ig_list[2]  # 3挡加速
        elif seg["accel"] > 0 and v_kmh < 45:
            ig_used = ig_list[3]  # 4挡加速
        else:
            ig_used = ig_list[4]  # 5挡

        n_e = engine_speed_from_ua(v_kmh, ig_used)
        if n_e < n_min:
            n_e = n_min
        if n_e > n_max:
            n_e = n_max

        # 发动机需要提供的功率（需考虑附件消耗，简化按等速行驶功率）
        Pe_actual = P_resist

        b_val = fuel_consumption_rate(Pe_actual, n_e)
        # b值不应低于发动机最低燃油消耗率（约250-300 g/(kW·h)）
        if b_val < 200:
            b_val = 200

        # 单位时间燃油消耗量 Qt = Pe * b / (3600 * ρ) [mL/s]
        # Pe [kW] * b [g/(kW·h)] / 3600 = g/s → /ρ [g/mL] = mL/s
        Qt = Pe_actual * b_val / (3600.0 * rho_gasoline)  # mL/s

        fuel_seg += Qt * dt  # mL

    total_fuel_ml += fuel_seg
    print(f"  工况{seg['name']}：车速 {seg['v_start']}→{seg['v_end']} km/h, "
          f"时间 {seg['time']:.1f}s, 油耗 {fuel_seg:.2f} mL")

# 百公里油耗
Qs_cycle = total_fuel_ml * 100.0 / total_distance  # L/100km
total_fuel_L = total_fuel_ml / 1000.0

print(f"\n六工况循环总计：")
print(f"  总行程：{total_distance:.0f} m")
print(f"  总油耗：{total_fuel_ml:.2f} mL = {total_fuel_L:.4f} L")
print(f"  百公里油耗：{Qs_cycle:.2f} L/100km")

print("\n" + "=" * 50)
print("题目二计算完成！")
print("=" * 50)
