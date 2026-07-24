import streamlit as st
import random

# 設定網頁標題與圖示
st.set_page_config(page_title="門市食材配方考核系統", page_icon="🍕", layout="centered")

# 餅皮種類選項
CRUST_OPTIONS = ["大厚", "大芝心", "大薄", "大舊"]

# 定義下拉選單選項
ALL_SAUCES = [
    "(請選擇)", "無", "千島醬 2滿杓(專)", "照燒醬 2平杓(專)", "Pizza Sauce 1平杓", 
    "卡菲底醬 小藍杓*1平杓", "BBQ醬 15cc*1滿匙", 
    "洋釀淋醬 Z字交叉來回7次", "BBQ醬 15cc*3滿匙"
]

ALL_INGREDIENTS = [
    "(請選擇)", "1/2蟹風味棒", "PP", "三色絲", "午餐肉丁", "大蝦仁", "干貝", 
    "小蝦", "帆立貝", "明太子醬", "洋蔥", "洋菇", "炭烤雞腿塊", "牛肝菌菇醬", 
    "牛肉丸", "甜不辣", "番茄", "章魚", "培根", "蛤蜊肉", 
    "起司", "費城牛肉", "韓國泡菜", "韓國烤肉餡", "韓式燒牛肉", "韓式豬五花", 
    "韭菜", "魷魚圈", "鱈魚片", "火腿", "豬義混", "青椒", "黑胡椒牛柳", 
    "菠菜", "鳳梨", "蟹肉絲", "花枝調味粉"
]

ALL_QUANTITIES = [
    "(請選擇)", "1/2", "1", "1+1/2", "2", "5個", "5圈", "5片", "5隻", 
    "8顆", "9片", "10個", "10顆", "10隻", "10+2片", "14+8片", "16片", "26片", 
    "1(外1圈)", "1(滿杯)", "均勻分灑", "橫直各5條", "Z字來回5次", "Z字交叉來回7次", 
    "克數填寫(g)"
]

# 將題庫改寫為結構化資料
RECIPES = [
    {"name": "松露干貝鮮蝦起司", "sauce": "無", "ingredients": [
        {"n": "起司", "q": "1/2", "g": ""}, {"n": "洋蔥", "q": "1/2", "g": ""}, {"n": "菠菜", "q": "1/2", "g": ""}, {"n": "大蝦仁", "q": "10隻", "g": ""}, {"n": "干貝", "q": "10個", "g": ""}, {"n": "魷魚圈", "q": "5圈", "g": ""}, {"n": "番茄", "q": "1/2", "g": ""}, {"n": "牛肝菌菇醬", "q": "橫直各5條", "g": ""}, {"n": "起司", "q": "1/2", "g": ""}
    ]},
    {"name": "千島海鮮盛宴", "sauce": "千島醬 2滿杓(專)", "ingredients": [
        {"n": "起司", "q": "1", "g": ""}, {"n": "鳳梨", "q": "1/2", "g": ""}, {"n": "青椒", "q": "1/2", "g": ""}, {"n": "魷魚圈", "q": "5圈", "g": ""}, {"n": "大蝦仁", "q": "5隻", "g": ""}, {"n": "干貝", "q": "5個", "g": ""}, {"n": "1/2蟹風味棒", "q": "5個", "g": ""}, {"n": "番茄", "q": "1/2", "g": ""}, {"n": "起司", "q": "1/2", "g": ""}, {"n": "明太子醬", "q": "Z字來回5次", "g": ""}
    ]},
    {"name": "和風章魚燒", "sauce": "照燒醬 2平杓(專)", "ingredients": [
        {"n": "起司", "q": "1", "g": ""}, {"n": "洋蔥", "q": "1/2", "g": ""}, {"n": "青椒", "q": "1/2", "g": ""}, {"n": "甜不辣", "q": "1/2", "g": ""}, {"n": "章魚", "q": "1", "g": ""}, {"n": "起司", "q": "1", "g": ""}
    ]},
    {"name": "經典海鮮四重奏", "sauce": "Pizza Sauce 1平杓", "ingredients": [
        {"n": "起司", "q": "1", "g": ""}, {"n": "蟹肉絲", "q": "2", "g": ""}, {"n": "小蝦", "q": "1/2", "g": ""}, {"n": "蛤蜊肉", "q": "1/2", "g": ""}, {"n": "帆立貝", "q": "8顆", "g": ""}, {"n": "番茄", "q": "1/2", "g": ""}, {"n": "起司", "q": "1", "g": ""}
    ]},
    {"name": "法式海陸盛宴", "sauce": "卡菲底醬 小藍杓*1平杓", "ingredients": [
        {"n": "起司", "q": "1/2", "g": ""}, {"n": "洋蔥", "q": "1/2", "g": ""}, {"n": "韓國烤肉餡", "q": "1(外1圈)", "g": ""}, {"n": "鱈魚片", "q": "5片", "g": ""}, {"n": "大蝦仁", "q": "5隻", "g": ""}, {"n": "番茄", "q": "1/2", "g": ""}, {"n": "花枝調味粉", "q": "均勻分灑", "g": ""}, {"n": "起司", "q": "1/2", "g": ""}
    ]},
    {"name": "韓式泡菜豬五花", "sauce": "無", "ingredients": [
        {"n": "起司", "q": "1/2", "g": ""}, {"n": "韓國泡菜", "q": "1", "g": ""}, {"n": "起司", "q": "1", "g": ""}, {"n": "韓式豬五花", "q": "1+1/2", "g": ""}, {"n": "花枝調味粉", "q": "均勻分灑", "g": ""}
    ]},
    {"name": "超級總匯", "sauce": "Pizza Sauce 1平杓", "ingredients": [
        {"n": "起司", "q": "1", "g": ""}, {"n": "PP", "q": "9片", "g": ""}, {"n": "火腿", "q": "9片", "g": ""}, {"n": "洋蔥", "q": "1/2", "g": ""}, {"n": "青椒", "q": "1/2", "g": ""}, {"n": "洋菇", "q": "1/2", "g": ""}, {"n": "豬義混", "q": "1", "g": ""}, {"n": "起司", "q": "1", "g": ""}
    ]},
    {"name": "夏威夷", "sauce": "Pizza Sauce 1平杓", "ingredients": [
        {"n": "起司", "q": "1", "g": ""}, {"n": "火腿", "q": "26片", "g": ""}, {"n": "鳳梨", "q": "1", "g": ""}, {"n": "起司", "q": "1", "g": ""}
    ]},
    {"name": "超級夏威夷", "sauce": "Pizza Sauce 1平杓", "ingredients": [
        {"n": "起司", "q": "1/2", "g": ""}, {"n": "火腿", "q": "14+8片", "g": ""}, {"n": "培根", "q": "10+2片", "g": ""}, {"n": "午餐肉丁", "q": "1", "g": ""}, {"n": "鳳梨", "q": "1", "g": ""}, {"n": "起司", "q": "1", "g": ""}
    ]},
    {"name": "雙層美式臘腸", "sauce": "Pizza Sauce 1平杓", "ingredients": [
        {"n": "起司", "q": "1", "g": ""}, {"n": "PP", "q": "16片", "g": ""}, {"n": "起司", "q": "1", "g": ""}, {"n": "PP", "q": "16片", "g": ""}, {"n": "起司", "q": "1/2", "g": ""}
    ]},
    {"name": "經典費城起司牛肉", "sauce": "無", "ingredients": [
        {"n": "起司", "q": "1", "g": ""}, {"n": "費城牛肉", "q": "克數填寫(g)", "g": "225"}, {"n": "三色絲", "q": "1", "g": ""}, {"n": "起司", "q": "1/2", "g": ""}
    ]},
    {"name": "鐵板雙牛", "sauce": "BBQ醬 15cc*1滿匙", "ingredients": [
        {"n": "起司", "q": "1", "g": ""}, {"n": "黑胡椒牛柳", "q": "克數填寫(g)", "g": "110"}, {"n": "洋菇", "q": "1/2", "g": ""}, {"n": "菠菜", "q": "1", "g": ""}, {"n": "牛肉丸", "q": "10顆", "g": ""}, {"n": "起司", "q": "1/2", "g": ""}
    ]},
    {"name": "韓風醬烤雪花牛", "sauce": "洋釀淋醬 Z字交叉來回7次", "ingredients": [
        {"n": "起司", "q": "1", "g": ""}, {"n": "韭菜", "q": "1", "g": ""}, {"n": "韓式燒牛肉", "q": "克數填寫(g)", "g": "190"}, {"n": "起司", "q": "1", "g": ""}
    ]},
    {"name": "炙燒明太子嫩雞", "sauce": "照燒醬 2平杓(專)", "ingredients": [
        {"n": "起司", "q": "1", "g": ""}, {"n": "洋菇", "q": "1/2", "g": ""}, {"n": "炭烤雞腿塊", "q": "1(滿杯)", "g": ""}, {"n": "番茄", "q": "1/2", "g": ""}, {"n": "起司", "q": "1/2", "g": ""}, {"n": "明太子醬", "q": "Z字來回5次", "g": ""}
    ]},
    {"name": "彩蔬鮮菇", "sauce": "BBQ醬 15cc*3滿匙", "ingredients": [
        {"n": "起司", "q": "1", "g": ""}, {"n": "洋菇", "q": "1", "g": ""}, {"n": "菠菜", "q": "1", "g": ""}, {"n": "番茄", "q": "1/2", "g": ""}, {"n": "起司", "q": "1", "g": ""}
    ]}
]

# 初始化 Session State 狀態
if "started" not in st.session_state:
    st.session_state.started = False
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "questions" not in st.session_state:
    st.session_state.questions = []
if "results" not in st.session_state:
    st.session_state.results = []

# 標題區
st.title("🍕 門市食材配方考核系統")

# 1. 測驗未開始：設定題數並生成題目
if not st.session_state.started:
    st.markdown("### 📋 測驗設定")
    num_q = st.slider("抽考題數：", min_value=3, max_value=len(RECIPES), value=5)
    
    if st.button("🚀 開始測驗", type="primary"):
        st.session_state.started = True
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.results = []
        
        shuffled = RECIPES.copy()
        random.shuffle(shuffled)
        
        selected_questions = []
        for recipe in shuffled[:num_q]:
            # 隨機抽取餅皮
            crust = random.choice(CRUST_OPTIONS)
            ings = [dict(item) for item in recipe["ingredients"]]
            
            # 【大舊餅皮特殊規則】若第一項食材是起司，移至最後一項
            if crust == "大舊" and ings and ings[0]["n"] == "起司":
                first_cheese = ings.pop(0)
                ings.append(first_cheese)
                
            selected_questions.append({
                "name": f"{crust} - {recipe['name']}",
                "crust": crust,
                "sauce": recipe["sauce"],
                "ingredients": ings
            })
            
        st.session_state.questions = selected_questions
        st.rerun()

# 2. 測驗進行中
elif st.session_state.current_q < len(st.session_state.questions):
    total_q = len(st.session_state.questions)
    curr_idx = st.session_state.current_q
    q_data = st.session_state.questions[curr_idx]
    
    st.progress((curr_idx) / total_q, text=f"進度：第 {curr_idx + 1} / {total_q} 題")
    st.subheader(f"第 {curr_idx + 1} 題：【{q_data['name']}】")
    
    with st.form(key=f"q_form_{curr_idx}"):
        st.write("1. 底醬與用量：")
        sauce_input = st.selectbox("底醬選擇", ALL_SAUCES, key=f"sauce_{curr_idx}", label_visibility="collapsed")
        
        st.write("2. 請依序選擇鋪設配料與份量：")
        st.info("💡 提示：若為「大舊」餅皮，請注意底層起司順序調整喔！")
        
        # 標題列排版
        header_cols = st.columns([4, 4, 3])
        header_cols[0].markdown("**配料名稱**")
        header_cols[1].markdown("**份量單位**")
        header_cols[2].markdown("**克數 (g)**")
        
        ing_inputs = []
        for j in range(len(q_data["ingredients"])):
            cols = st.columns([4, 4, 3])
            
            with cols[0]:
                sel_n = st.selectbox(f"配料 {j}", ALL_INGREDIENTS, key=f"ing_n_{curr_idx}_{j}", label_visibility="collapsed")
            with cols[1]:
                sel_q = st.selectbox(f"份量 {j}", ALL_QUANTITIES, key=f"ing_q_{curr_idx}_{j}", label_visibility="collapsed")
            with cols[2]:
                text_g = st.text_input(f"克數 {j}", key=f"ing_g_{curr_idx}_{j}", label_visibility="collapsed", placeholder="輸入數字")
                
            ing_inputs.append({"n": sel_n, "q": sel_q, "g": text_g.strip()})
            
        submitted = st.form_submit_button("提交本題答案", type="primary")
        
        if submitted:
            # 驗證底醬
            sauce_correct = (sauce_input == q_data["sauce"])
            
            # 驗證配料
            ing_correct_count = 0
            for u, e in zip(ing_inputs, q_data["ingredients"]):
                is_n_correct = (u["n"] == e["n"])
                is_q_correct = (u["q"] == e["q"])
                is_g_correct = (u["g"] == e["g"]) if e["q"] == "克數填寫(g)" else True
                
                if is_n_correct and is_q_correct and is_g_correct:
                    ing_correct_count += 1
                    
            total_items = 1 + len(q_data["ingredients"])
            got_items = (1 if sauce_correct else 0) + ing_correct_count
            
            is_fully_correct = (got_items == total_items)
            if is_fully_correct:
                st.session_state.score += 1
                
            st.session_state.results.append({
                "item": q_data["name"],
                "sauce_user": sauce_input,
                "sauce_ans": q_data["sauce"],
                "sauce_ok": sauce_correct,
                "ing_user": ing_inputs,
                "ing_ans": q_data["ingredients"],
                "fully_correct": is_fully_correct
            })
            
            st.session_state.current_q += 1
            st.rerun()

# 3. 測驗完成結果頁面
else:
    total_q = len(st.session_state.questions)
    score = st.session_state.score
    percentage = int((score / total_q) * 100)
    
    st.balloons()
    st.success("🎉 測驗完成！")
    st.metric(label="最終得分", value=f"{score} / {total_q} 題", delta=f"正確率 {percentage}%")
    
    if percentage == 100:
        st.write("🌟 **評語：** 非常完美！連餅皮特殊規則都掌握得很好，准予獨立上工！")
    elif percentage >= 80:
        st.write("👍 **評語：** 表現良好！部分細節再複習一下會更好。")
    else:
        st.write("⚠️ **評語：** 尚未達標，請繼續熟背配方表後重新測驗。")
        
    st.markdown("---")
    st.subheader("📝 答題檢討明細")
    for idx, res in enumerate(st.session_state.results, 1):
        status_icon = "✅" if res["fully_correct"] else "❌"
        with st.expander(f"{status_icon} 第 {idx} 題：{res['item']}"):
            
            u_sauce = res['sauce_user'] if res['sauce_user'] != "(請選擇)" else "(未選底醬)"
            if not res["sauce_ok"]:
                st.write(f"❌ 底醬選擇：`{u_sauce}` ｜ 正確答案：`{res['sauce_ans']}`")
            else:
                st.write(f"✅ 底醬選擇：`{u_sauce}`")
                
            st.write("**配料比對：**")
            for u, e in zip(res["ing_user"], res["ing_ans"]):
                # 組合正確答案字串
                ans_str = f"{e['n']} {e['g']}g" if e['q'] == "克數填寫(g)" else f"{e['n']} {e['q']}"
                
                # 組合使用者作答字串
                u_n = u['n'] if u['n'] != "(請選擇)" else "(未選配料)"
                u_q = u['q'] if u['q'] != "(請選擇)" else "(未選份量)"
                user_str = f"{u_n} {u['g']}g" if u['q'] == "克數填寫(g)" else f"{u_n} {u_q}"
                
                # 驗證該行是否全對
                is_correct = (u["n"] == e["n"]) and (u["q"] == e["q"]) and (u["q"] != "克數填寫(g)" or u["g"] == e["g"])
                
                if is_correct:
                    st.write(f"  - ✅ `{ans_str}`")
                else:
                    st.write(f"  - ❌ 您的答案：`{user_str}` ｜ 正確答案：`{ans_str}`")

    if st.button("🔄 重新開始測驗"):
        st.session_state.started = False
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.results = []
        st.rerun()

