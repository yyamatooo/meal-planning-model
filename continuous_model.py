"""
    (a) 連続変数モデル
"""

import pulp

def solve_continuous_model():
    

    #-----------------------------------------------------
    # 1. データ定義
    #-----------------------------------------------------
    menu_names = [
        "ご飯", "白がゆ", "玄米ごはん", "きつねうどん", "冷奴", "納豆", "枝豆", "ほうれん草のお浸し", "きんぴら", "うなぎ（蒲焼き）",
        "カボチャの含め煮", "大学いも", "焼きとり", "しゃぶしゃぶ", "さんまの塩焼き", "ぶりの照り焼き", "かつおのたたき",
        "だし巻き卵", "さしみ", "ゆでカニ", "みそ汁（豆腐・油揚げ）", "ほっけの塩焼き", "魚肉ソーセージ", "めかぶ（三杯酢）",
        "ガーリックライス", "オムライス", "食パン", "フランスパン", "バターロール", "鳥唐揚げ"
    ]
    n = len(menu_names)

    # メニューごとの費用 c_i
    cost_c = [
        40.0, 10.0, 40.0, 31.0, 15.0,  6.0, 18.0, 26.0, 13.0, 53.0,
        21.0, 12.0, 103.0,172.0, 49.0, 38.0, 40.0,  9.0, 43.0, 58.0,
         8.0, 45.0, 10.0,116.0, 46.0, 70.0,  3.0,  4.0,  4.0, 49.0
    ]  
    
    # メニューごとの自給率指標 d_i
    self_suff_d = [
        98.0, 98.0, 98.0, 21.0, 27.0, 24.0, 38.0, 67.0, 38.0, 32.0,
        62.0, 42.0,  6.0, 13.0, 99.0, 96.0, 77.0, 15.0, 40.0, 32.0,
        26.0, 91.0, 37.0, 53.0, 76.0, 42.0, 13.0, 12.0, 12.0, 16.0
    ] 

    # 栄養係数
    energy_a = [
        250, 62, 243, 401,  98, 85, 63, 17, 75, 285,
        111,177,241,658, 344,210,131, 83, 81,  87,
         67,110, 32, 14, 327,464,184,231,247, 327
    ]  # kcal

    protein_a = [
         4,  1,  4, 16, 10,  7,  6,  2,  2, 23,
         3,  1, 14, 36, 22, 18, 20,  6, 17, 14,
         6, 18,  2,  1,  4, 20,  5,  8,  8, 20
    ]  # g

    fat_a = [
         0,  0,  2, 10,  5,  4,  3,  0,  3, 21,
         0,  8, 14, 51, 31, 14,  5,  5,  1,  0,
         4,  4,  1,  0,  9, 25,  7,  1,  7, 23
    ]  # g

    vitaminA_a = [
         0,   0,   0,   0,   0,   0,   0,   0,   0, 1500,
         0,   0,  13,   3,  13,  34,   4,  80,  34,   0,
         0,  20,   0,   0,   0, 223,   0,   0,   0,  50
    ]  # μg

    vitaminD_a = [
         0,   0,   0,   0,   0,   0,   0,   0,   0, 19,
         0,   0,   0,   0, 15.6,4.3, 3.2,1.4,  2,   0,
         0,   3, 0.2,   0,   0, 3.8,   0,   0,0.1,   0
    ]  # μg

    vitaminE_a = [
         0,  0,  0, 1.2, 3.7, 4, 4.4, 2.1, 0.4,   5,
         4.3,0.8,0.2,1.8,1.2,1.7,0.2,0.8,  1 ,2.6,
         1.3,0.7, 0, 0.1,  0 ,1.8,0.6,0.3,1.3,0.1
    ]  # mg

    vitaminB1_a = [
         0.03,1.0, 0.03,0.07,0.17,
         0.05,0.12,0.03,0.03,0.75,
         0.06,0.06,0.08,0.08,0.0,
         0.19,0.1, 0.03,0.04,0.21,
         0.04,0.1, 0.04,0.02,0.03,
         0.11,0.04,0.06,0.08,0.06
    ]  # mg

    vitaminB2_a = [
        0.02,0.01,0.02,0.07,0.08,
        0.12,0.07,0.08,0.02,0.74,
        0.03,0.02,0.23,0.24,0.36,
        0.31,0.14,0.16,0.03,0.57,
        0.22,0.27,0.12,0.02,0.02,
        0.36,0.03,0.04,0.05,0.1
    ]  # mg

    # ----------------- 下限/上限の数値---------------------
    min_energy   = 2000.0  # kcal
    min_protein  =   50.0  # g

    min_vitA  =  650.0
    max_vitA  = 2700.0

    min_vitD  =    8.5
    max_vitD  =  100.0

    min_vitE  =    5.0
    max_vitE  =  650.0

    min_vitB1 =    1.1
    min_vitB2 =    1.2
    # ----------------------------------------------------------

    # メニュー消費量の上限(1日あたり何回まで)
    max_units = [2]*n  # 全メニュー一律で2回まで 
    
    # 多目的の重みパラメータ (例: 自給率 - 費用)
    w_s = 1.0
    w_c = 1.0

    #-----------------------------------------------------
    # 2. PuLPのMaximize
    #-----------------------------------------------------
    problem = pulp.LpProblem("ContinuousModel", pulp.LpMaximize)

    #-----------------------------------------------------
    # 3. 決定変数 x_i (連続変数, >=0)
    #-----------------------------------------------------
    x_vars = [pulp.LpVariable(f"x_{i}", lowBound=0.0, cat=pulp.LpContinuous) for i in range(n)]
    
    #-----------------------------------------------------
    # 4. 目的関数 (w_s * sum(d_i x_i) - w_c * sum(c_i x_i))
    #-----------------------------------------------------
    total_self_suff = pulp.lpSum(self_suff_d[i] * x_vars[i] for i in range(n))
    total_cost      = pulp.lpSum(cost_c[i]      * x_vars[i] for i in range(n))

    # 自給率を最大化 & 費用を最小化 => maximize( sum(d_i x_i) - sum(c_i x_i) )
    problem += w_s*total_self_suff - w_c*total_cost, "Objective"

    #-----------------------------------------------------
    # 5. 各種制約
    #-----------------------------------------------------

    # (11) x_i <= alpha_i^max  
    for i in range(n):
        problem += x_vars[i] <= max_units[i], f"MaxUnit_{i}"

    # (12)  エネルギー>= 2000kcal
    problem += pulp.lpSum(energy_a[i]*x_vars[i] for i in range(n)) >= min_energy, "MinEnergy"

    # (13)  たんぱく質>= 50g
    problem += pulp.lpSum(protein_a[i]*x_vars[i] for i in range(n)) >= min_protein, "MinProtein"

    # (14)  たんぱく質が (13~20)% of totalEnergy

    totalE_expr = pulp.lpSum(energy_a[i]*x_vars[i] for i in range(n))
    P_kcal_expr = 4 * pulp.lpSum(protein_a[i]*x_vars[i] for i in range(n))
    problem += P_kcal_expr >= 0.13*totalE_expr, "ProteinRatioLower"
    problem += P_kcal_expr <= 0.20*totalE_expr, "ProteinRatioUpper"


    # (15)  脂質が (20~30)% of totalEnergy

    F_kcal_expr = 9 * pulp.lpSum(fat_a[i]*x_vars[i] for i in range(n))
    problem += F_kcal_expr >= 0.20*totalE_expr, "FatRatioLower"
    problem += F_kcal_expr <= 0.30*totalE_expr, "FatRatioUpper"


    # (16) ビタミンA: 650 <= sum(...) <= 2700
    vitA_expr = pulp.lpSum(vitaminA_a[i]*x_vars[i] for i in range(n))
    problem += vitA_expr >= min_vitA, "VitaminA_Min"
    problem += vitA_expr <= max_vitA, "VitaminA_Max"

    # (17) ビタミンD: 8.5 <= sum(...) <= 100
    vitD_expr = pulp.lpSum(vitaminD_a[i]*x_vars[i] for i in range(n))
    problem += vitD_expr >= min_vitD, "VitaminD_Min"
    problem += vitD_expr <= max_vitD, "VitaminD_Max"

    # (18) ビタミンE: 5 <= sum(...) <= 650
    vitE_expr = pulp.lpSum(vitaminE_a[i]*x_vars[i] for i in range(n))
    problem += vitE_expr >= min_vitE, "VitaminE_Min"
    problem += vitE_expr <= max_vitE, "VitaminE_Max"

    # (19) ビタミンB1: >= 1.1
    vitB1_expr = pulp.lpSum(vitaminB1_a[i]*x_vars[i] for i in range(n))
    problem += vitB1_expr >= min_vitB1, "VitaminB1_Min"

    # (20) ビタミンB2: >= 1.2
    vitB2_expr = pulp.lpSum(vitaminB2_a[i]*x_vars[i] for i in range(n))
    problem += vitB2_expr >= min_vitB2, "VitaminB2_Min"
    
    #-----------------------------------------------------
    # 6. ソルバー実行
    #-----------------------------------------------------
    solution_status = problem.solve(pulp.PULP_CBC_CMD(msg=0))
    
    #-----------------------------------------------------
    # 7. 結果の出力
    #-----------------------------------------------------
    print("=== (a) Continuous Model Results ===")
    print("Status:", pulp.LpStatus[solution_status])
    
    # 目的関数値
    if pulp.value(problem.objective) is not None:
        print("Objective Value =", pulp.value(problem.objective))
    else:
        print("Objective Value = None (可能性としてInfeasible)")

    # 変数値の表示
    for i in range(n):
        val = x_vars[i].varValue
        if val is not None and abs(val)>1e-6:
            print(f"{menu_names[i]} = {val:.3f}")

    # 付加情報: 
    if solution_status == pulp.LpStatusOptimal or pulp.LpStatus[solution_status]=="Optimal":
        chosen_cost = sum(cost_c[i]*x_vars[i].varValue for i in range(n))
        chosen_self_suff = sum(self_suff_d[i]*x_vars[i].varValue for i in range(n))
        print(f"Total Cost       =  {chosen_cost:8.2f}")
        print(f"Total Self-Suff  =  {chosen_self_suff:8.2f}")
       

if __name__ == "__main__":
    solve_continuous_model()