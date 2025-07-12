"""
    (b) 整数制約モデル
"""
import pulp

def solve_integer_model():
   
    #-----------------------------------------------------
    # 1. データ定義
    #-----------------------------------------------------
    menu_names = [
        "ご飯","白がゆ","玄米ごはん","きつねうどん","冷奴","納豆","枝豆","ほうれん草のお浸し","きんぴら","うなぎ（蒲焼き）",
        "カボチャの含め煮","大学いも","焼きとり","しゃぶしゃぶ","さんまの塩焼き","ぶりの照り焼き","かつおのたたき","だし巻き卵",
        "さしみ","ゆでカニ","みそ汁（豆腐・油揚げ）","ほっけの塩焼き","魚肉ソーセージ","めかぶ（三杯酢）","ガーリックライス",
        "オムライス","食パン","フランスパン","バターロール","鳥唐揚げ"
    ]
    n = len(menu_names)

    # メニューごとの費用 c_i
    cost_c = [
        40.0,10.0,40.0,31.0,15.0, 6.0,18.0,26.0,13.0,53.0,
        21.0,12.0,103.0,172.0,49.0,38.0,40.0, 9.0,43.0,58.0,
         8.0,45.0,10.0,116.0,46.0,70.0, 3.0, 4.0, 4.0,49.0
    ]
    
    # メニューごとの自給率指標 d_i
    self_suff_d = [
        98.0,98.0,98.0,21.0,27.0,24.0,38.0,67.0,38.0,32.0,
        62.0,42.0, 6.0,13.0,99.0,96.0,77.0,15.0,40.0,32.0,
        26.0,91.0,37.0,53.0,76.0,42.0,13.0,12.0,12.0,16.0
    ]
    
    # 栄養係数
    energy_a = [
        250, 62,243,401, 98, 85, 63, 17, 75,285,
        111,177,241,658,344,210,131, 83, 81, 87,
         67,110, 32, 14,327,464,184,231,247,327
    ]
    protein_a = [
         4,  1,  4,16,10, 7, 6, 2, 2,23,
         3,  1,14,36,22,18,20, 6,17,14,
         6, 18, 2, 1, 4,20, 5, 8, 8,20
    ]
    fat_a = [
         0,  0, 2,10, 5, 4, 3, 0, 3,21,
         0,  8,14,51,31,14, 5, 5, 1, 0,
         4,  4, 1, 0, 9,25, 7, 1, 7,23
    ]
    vitaminA_a = [
         0,   0,   0,   0,   0,   0,   0,   0,   0,1500,
         0,   0,  13,   3,  13,  34,  4,  80, 34,   0,
         0,  20,   0,   0,   0, 223,  0,   0,  0,  50
    ]
    vitaminD_a = [
         0,  0,  0,  0,  0,  0,  0,  0,  0,19,
         0,  0,  0,  0,15.6,4.3,3.2,1.4, 2, 0,
         0,  3,0.2,  0,  0,3.8, 0,   0,0.1, 0
    ]
    vitaminE_a = [
         0,  0,  0,1.2,3.7,4,4.4,2.1,0.4, 5,
         4.3,0.8,0.2,1.8,1.2,1.7,0.2,0.8, 1 ,2.6,
         1.3,0.7,0,0.1,0,1.8,0.6,0.3,1.3,0.1
    ]
    vitaminB1_a = [
        0.03,1.0,0.03,0.07,0.17,
        0.05,0.12,0.03,0.03,0.75,
        0.06,0.06,0.08,0.08,0.0,
        0.19,0.1, 0.03,0.04,0.21,
        0.04,0.1, 0.04,0.02,0.03,
        0.11,0.04,0.06,0.08,0.06
    ]
    vitaminB2_a = [
        0.02,0.01,0.02,0.07,0.08,
        0.12,0.07,0.08,0.02,0.74,
        0.03,0.02,0.23,0.24,0.36,
        0.31,0.14,0.16,0.03,0.57,
        0.22,0.27,0.12,0.02,0.02,
        0.36,0.03,0.04,0.05,0.1
    ]

    # ----------------- 下限/上限の数値 ---------------------
    min_energy = 2000.0
    min_protein = 50.0
    min_vitA, max_vitA = 650.0, 2700.0
    min_vitD, max_vitD = 8.5, 100.0
    min_vitE, max_vitE = 5.0, 650.0
    min_vitB1 = 1.1
    min_vitB2 = 1.2

    # メニュー1日あたり最大回数
    max_units = [2]*n

    # 多目的パラメータ
    w_s = 1.0
    w_c = 1.0

    #-----------------------------------------------------
    # 2. PuLPのMaximize問題
    #-----------------------------------------------------
    problem = pulp.LpProblem("IntegerModel", pulp.LpMaximize)

    #-----------------------------------------------------
    # 3. 決定変数 x_i (整数変数, >=0)
    #-----------------------------------------------------
    # cat = pulp.LpInteger に変更
    x_vars = [pulp.LpVariable(f"x_{i}", lowBound=0, cat=pulp.LpInteger)
              for i in range(n)]
    
    #-----------------------------------------------------
    # 4. 目的関数 (w_s * sum(d_i x_i) - w_c * sum(c_i x_i))
    #-----------------------------------------------------
    total_self_suff = pulp.lpSum(self_suff_d[i] * x_vars[i] for i in range(n))
    total_cost      = pulp.lpSum(cost_c[i]      * x_vars[i] for i in range(n))
    problem += w_s*total_self_suff - w_c*total_cost, "Objective"

    #-----------------------------------------------------
    # 5. 制約
    #-----------------------------------------------------

    # メニュー回数上限
    for i in range(n):
        problem += x_vars[i] <= max_units[i], f"MaxUnit_{i}"

    # エネルギー >= 2000
    problem += pulp.lpSum(energy_a[i]*x_vars[i] for i in range(n)) >= min_energy, "MinEnergy"

    # タンパク質 >= 50
    problem += pulp.lpSum(protein_a[i]*x_vars[i] for i in range(n)) >= min_protein, "MinProtein"

    # たんぱく質 (13~20)% of totalEnergy
    totalE_expr = pulp.lpSum(energy_a[i]*x_vars[i] for i in range(n))
    P_kcal_expr = 4 * pulp.lpSum(protein_a[i]*x_vars[i] for i in range(n))
    problem += P_kcal_expr >= 0.13*totalE_expr, "ProteinRatioLower"
    problem += P_kcal_expr <= 0.20*totalE_expr, "ProteinRatioUpper"

    # 脂質 (20~30)% of totalEnergy
    F_kcal_expr = 9 * pulp.lpSum(fat_a[i]*x_vars[i] for i in range(n))
    problem += F_kcal_expr >= 0.20*totalE_expr, "FatRatioLower"
    problem += F_kcal_expr <= 0.30*totalE_expr, "FatRatioUpper"

    # ビタミンA (650 ~ 2700)
    vitA_expr = pulp.lpSum(vitaminA_a[i]*x_vars[i] for i in range(n))
    problem += vitA_expr >= min_vitA, "VitaminA_min"
    problem += vitA_expr <= max_vitA, "VitaminA_max"

    # ビタミンD (8.5 ~ 100)
    vitD_expr = pulp.lpSum(vitaminD_a[i]*x_vars[i] for i in range(n))
    problem += vitD_expr >= min_vitD, "VitaminD_min"
    problem += vitD_expr <= max_vitD, "VitaminD_max"

    # ビタミンE (5 ~ 650)
    vitE_expr = pulp.lpSum(vitaminE_a[i]*x_vars[i] for i in range(n))
    problem += vitE_expr >= min_vitE, "VitaminE_min"
    problem += vitE_expr <= max_vitE, "VitaminE_max"

    # ビタミンB1 >= 1.1
    vitB1_expr = pulp.lpSum(vitaminB1_a[i]*x_vars[i] for i in range(n))
    problem += vitB1_expr >= min_vitB1, "VitaminB1_min"

    # ビタミンB2 >= 1.2
    vitB2_expr = pulp.lpSum(vitaminB2_a[i]*x_vars[i] for i in range(n))
    problem += vitB2_expr >= min_vitB2, "VitaminB2_min"

    #-----------------------------------------------------
    # 6. ソルバー実行
    #-----------------------------------------------------
    solution_status = problem.solve(pulp.PULP_CBC_CMD(msg=0))

    #-----------------------------------------------------
    # 7. 結果の出力
    #-----------------------------------------------------
    print("=== (b) Integer Model Results ===")
    print("Status:", pulp.LpStatus[solution_status])
    
    if pulp.value(problem.objective) is not None:
        print("Objective Value =", pulp.value(problem.objective))
    else:
        print("Objective Value = None (Infeasible かも)")

    # 決定変数の表示
    for i in range(n):
        val = x_vars[i].varValue
        if val is not None and abs(val)>1e-6:
            print(f"{menu_names[i]} = {val:.1f} (integer)")

    # 付加情報の出力
    if pulp.LpStatus[solution_status]=="Optimal":
        chosen_cost = sum(cost_c[i]*x_vars[i].varValue for i in range(n))
        chosen_self_suff = sum(self_suff_d[i]*x_vars[i].varValue for i in range(n))
        print(f"Total Cost       = {chosen_cost:8.2f}")
        print(f"Total Self-Suff  = {chosen_self_suff:8.2f}")

# 実行テスト例
if __name__ == "__main__":
    solve_integer_model()