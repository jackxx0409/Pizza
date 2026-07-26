import streamlit as st
import random
import re
import time
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# 設定網頁標題與圖示
st.set_page_config(page_title="食材配方考核系統", page_icon="🍕", layout="centered")

# 餅皮種類選項
CRUST_OPTIONS = ["大厚", "大芝心", "大薄", "大舊", "大火山", "大歐火"]

# 定義底醬選單
ALL_SAUCES = [
    "(請選擇)", 
    "無", 
    "Pizza Sauce 1平杓", 
    "照燒醬 2平杓(專)", 
    "千島醬 2滿杓(專)", 
    "BBQ醬 15cc*1滿匙", 
    "BBQ醬 15cc*3滿匙", 
    "卡菲底醬 小藍杓*1平杓", 
    "洋釀淋醬 Z字交叉來回7次",
    "洋釀淋醬 2圈"
]

# 定義食材選單
ALL_INGREDIENTS = [
    "(請選擇)",
    "起司",
    "洋蔥", "洋菇", "青椒", "菠菜", "番茄", "鳳梨", "韭菜", "三色絲", "韓國泡菜",
    "大蝦仁", "小蝦", "干貝", "魷魚圈", "章魚", "蛤蜊肉", "鱈魚片", "蟹肉絲", "1/2蟹風味棒", "花枝條",
    "火腿", "培根", "PP", "午餐肉丁", "豬義混", "炭烤雞腿塊", "牛肉丸", "費城牛肉", "黑胡椒牛柳", "韓式燒牛肉", "韓式豬五花", "韓國烤肉餡", "甜不辣",
    "明太子醬", "牛肝菌菇醬", "花枝調味粉"
]

# 數量選單
ALL_QUANTITIES = [
    "(請選擇)", "1/2", "1", "1+1/2", "2", "5", 
    "8", "9", "10", "10+2", "14+8", "16", "26", 
    "1(外1圈)", "1(滿杯)", "均勻分灑", "橫直各5條", "Z字來回5次", "Z字交叉來回7次", 
    "2圈", "克數填寫(g)"
]

# 題庫資料
RECIPES = [
    {"name": "松露干貝鮮蝦起司", "sauce": "無", "ingredients": [
        {"n": "起司", "q": "1/2", "g": ""}, {"n": "洋蔥", "q": "1/2", "g": ""}, {"n": "菠菜", "q": "1/2", "g": ""}, {"n": "大蝦仁", "q": "10", "g": ""}, {"n": "干貝", "q": "10", "g": ""}, {"n": "魷魚圈", "q": "5", "g": ""}, {"n": "番茄", "q": "1/2", "g": ""}, {"n": "牛肝菌菇醬", "q": "橫直各5條", "g": ""}, {"n": "起司", "q": "1/2", "g": ""}
    ]},
    {"name": "千島海鮮盛宴", "sauce": "千島醬 2滿杓(專)", "ingredients": [
        {"n": "起司", "q": "1", "g": ""}, {"n": "鳳梨", "q": "1/2", "g": ""}, {"n": "青椒", "q": "1/2", "g": ""}, {"n": "魷魚圈", "q": "5", "g": ""}, {"n": "大蝦仁", "q": "5", "g": ""}, {"n": "干貝", "q": "5", "g": ""}, {"n": "1/2蟹風味棒", "q": "5", "g": ""}, {"n": "番茄", "q": "1/2", "g": ""}, {"n": "起司", "q": "1/2", "g": ""}, {"n": "明太子醬", "q": "Z字來回5次", "g": ""}
    ]},
    {"name": "和風章魚燒", "sauce": "照燒醬 2平杓(專)", "ingredients": [
        {"n": "起司", "q": "1", "g": ""}, {"n": "洋蔥", "q": "1/2", "g": ""}, {"n": "青椒", "q": "1/2", "g": ""}, {"n": "甜不辣", "q": "1/2", "g": ""}, {"n": "章魚", "q": "1", "g": ""}, {"n": "起司", "q": "1", "g": ""}
    ]},
    {"name": "經典海鮮四重奏", "sauce": "Pizza Sauce 1平杓", "ingredients": [
        {"n": "起司", "q": "1/2", "g": ""}, {"n": "蟹肉絲", "q": "2", "g": ""}, {"n": "花枝條", "q": "1/2", "g": ""}, {"n": "小蝦", "q": "1/2", "g": ""}, {"n": "蛤蜊肉", "q": "1/2", "g": ""}, {"n": "番茄", "q": "1/2", "g": ""}, {"n": "起司", "q": "1", "g": ""}
    ]},
    {"name": "法式海陸盛宴", "sauce": "卡菲底醬 小藍杓*1平杓", "ingredients": [
        {"n": "起司", "q": "1/2", "g": ""}, {"n": "洋蔥", "q": "1/2", "g": ""}, {"n": "韓國烤肉餡", "q": "1(外1圈)", "g": ""}, {"n": "鱈魚片", "q": "5", "g": ""}, {"n": "大蝦仁", "q": "5", "g": ""}, {"n": "番茄", "q": "1/2", "g": ""}, {"n": "花枝調味粉", "q": "均勻分灑", "g": ""}, {"n": "起司", "q": "1/2", "g": ""}
    ]},
    {"name": "韓式泡菜豬五花", "sauce": "無", "ingredients": [
        {"n": "起司", "q": "1/2", "g": ""}, {"n": "韓國泡菜", "q": "1", "g": ""}, {"n": "起司", "q": "1", "g": ""}, {"n": "韓式豬五花", "q": "1+1/2", "g": ""}, {"n": "花枝調味粉", "q": "均勻分灑", "g": ""}
    ]},
    {"name": "超級總匯", "sauce": "Pizza Sauce 1平杓", "ingredients": [
        {"n": "起司", "q": "1", "g": ""}, {"n": "PP", "q": "9", "g": ""}, {"n": "火腿", "q": "9", "g": ""}, {"n": "洋蔥", "q": "1/2", "g": ""}, {"n": "青椒", "q": "1/2", "g": ""}, {"n": "洋菇", "q": "1/2", "g": ""}, {"n": "豬義混", "q": "1", "g": ""}, {"n": "起司", "q": "1", "g": ""}
    ]},
    {"name": "夏威夷", "sauce": "Pizza Sauce 1平杓", "ingredients": [
        {"n": "起司", "q": "1", "g": ""}, {"n": "火腿", "q": "26", "g": ""}, {"n": "鳳梨", "q": "1", "g": ""}, {"n": "起司", "q": "1", "g": ""}
    ]},
    {"name": "超級夏威夷", "sauce": "Pizza Sauce 1平杓", "ingredients": [
        {"n": "起司", "q": "1/2", "g": ""}, {"n": "火腿", "q": "14+8", "g": ""}, {"n": "培根", "q": "10+2", "g": ""}, {"n": "午餐肉丁", "q": "1", "g": ""}, {"n": "鳳梨", "q": "1", "g": ""}, {"n": "起司", "q": "1", "g": ""}
    ]},
    {"name": "雙層美式臘腸", "sauce": "Pizza Sauce 1平杓", "ingredients": [
        {"n": "起司", "q": "1", "g": ""}, {"n": "PP", "q": "16", "g": ""}, {"n": "起司", "q": "1", "g": ""}, {"n": "PP", "q": "16", "g": ""}, {"n": "起司", "q": "1/2", "g": ""}
    ]},
    {"name": "經典費城起司牛肉", "sauce": "無", "ingredients": [
        {"n": "起司", "q": "1", "g": ""}, {"n": "費城牛肉", "q": "克數填寫(g)", "g": "225"}, {"n": "三色絲", "q": "1", "g": ""}, {"n": "起司", "q": "1/2", "g": ""}
    ]},
    {"name": "鐵板雙牛", "sauce": "BBQ醬 15cc*1滿匙", "ingredients": [
        {"n": "起司", "q": "1", "g": ""}, {"n": "黑胡椒牛柳", "q": "克數填寫(g)", "g": "110"}, {"n": "洋菇", "q": "1/2", "g": ""}, {"n": "菠菜", "q": "1", "g": ""}, {"n": "牛肉丸", "q": "10", "g": ""}, {"n": "起司", "q": "1/2", "g": ""}
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

# 初始化 Session State
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
if "q_start_time" not in st.session_state:
    st.session_state.q_start_time = 0
if "staff_name" not in st.session_state:
    st.session_state.staff_name = ""
if "uploaded" not in st.session_state:
    st.session_state.uploaded = False

st.title("🍕 食材配方考核系統")

# 1. 測驗未開始
if not st.session_state.started:
    st.markdown("### 📋 測驗設定")
    staff_name_input = st.text_input("👤 請輸入您的大名 (必填)：", value=st.session_state.staff_name)
    num_q = st.slider("🎯 抽考題數：", min_value=3, max_value=len(RECIPES), value=5)
    
    if st.button("🚀 開始測驗", type="primary"):
        if not staff_name_input.strip():
            st.error("❌ 提醒：請先輸入姓名才能開始測驗喔！")
        else:
            st.session_state.staff_name = staff_name_input.strip()
            st.session_state.started = True
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.session_state.results = []
            st.session_state.uploaded = False
            
            shuffled = RECIPES.copy()
            random.shuffle(shuffled)
            
            selected_questions = []
            for recipe in shuffled[:num_q]:
                no_thin_old_list = ["松露干貝鮮蝦起司", "千島海鮮盛宴", "法式海陸盛宴"]
                if recipe["name"] in no_thin_old_list:
                    available_crusts = ["大厚", "大芝心", "大火山", "大歐火"]
                else:
                    available_crusts = CRUST_OPTIONS
                    
                crust = random.choice(available_crusts)
                sauce = recipe["sauce"]
                ings = [dict(item) for item in recipe["ingredients"]]
                
                if crust in ["大火山", "大歐火"]:
                    if not any(keyword in sauce for keyword in ["杓", "勺", "匙"]):
                        if sauce == "洋釀淋醬 Z字交叉來回7次":
                            sauce = "洋釀淋醬 2圈"
                    for ing in ings:
                        if ing["n"] in ["明太子醬", "牛肝菌菇醬"]:
                            ing["q"] = "2圈"
                
                if crust == "大舊" and ings and ings[0]["n"] == "起司":
                    first_cheese = ings.pop(0)
                    ings.append(first_cheese)
                    
                selected_questions.append({
                    "name": f"{crust} - {recipe['name']}",
                    "crust": crust,
                    "sauce": sauce,
                    "ingredients": ings
                })
                
            st.session_state.questions = selected_questions
            st.session_state.q_start_time = time.time()
            st.rerun()

# 2. 測驗進行中
elif st.session_state.current_q < len(st.session_state.questions):
    total_q = len(st.session_state.questions)
    curr_idx = st.session_state.current_q
    q_data = st.session_state.questions[curr_idx]
    
    st.progress((curr_idx) / total_q, text=f"進度：第 {curr_idx + 1} / {total_q} 題 (受測者：{st.session_state.staff_name})")
    st.subheader(f"第 {curr_idx + 1} 題：【{q_data['name']}】")
    
    with st.form(key=f"q_form_{curr_idx}"):
        st.write("1. 底醬與用量：")
        sauce_input = st.selectbox("底醬選擇", ALL_SAUCES, key=f"sauce_{curr_idx}", label_visibility="collapsed")
        
        st.write("2. 請依序選擇鋪設配料與份量：")
        if q_data["crust"] == "大舊":
            st.warning("💡 提示：本題為「大舊」餅皮，請注意底層起司順序調整！")
        elif q_data["crust"] in ["大火山", "大歐火"]:
            st.warning("💡 提示：本題為「大火山/大歐火」，非勺/匙計算之淋醬請改為 2 圈！")
        else:
            st.info("💡 提示：所有欄位皆為必填！")
        
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
            has_error = False
            error_messages = []
            if sauce_input == "(請選擇)":
                has_error = True
                error_messages.append("❌ 請選擇「底醬與用量」！")
            for j, u in enumerate(ing_inputs, 1):
                if u["n"] == "(請選擇)":
                    has_error = True
                    error_messages.append(f"❌ 第 {j} 項配料的「名稱」尚未選擇！")
                if u["q"] == "(請選擇)":
                    has_error = True
                    error_messages.append(f"❌ 第 {j} 項配料的「份量單位」尚未選擇！")
                if u["q"] == "克數填寫(g)" and not u["g"]:
                    has_error = True
                    error_messages.append(f"❌ 第 {j} 項配料選擇了克數填寫，但未輸入數字！")
                    
            if has_error:
                for err in error_messages:
                    st.error(err)
            else:
                elapsed_time = round(time.time() - st.session_state.q_start_time, 1)
                sauce_correct = (sauce_input == q_data["sauce"])
                
                ing_correct_count = 0
                for u, e in zip(ing_inputs, q_data["ingredients"]):
                    is_n_correct = (u["n"] == e["n"])
                    is_q_correct = (u["q"] == e["q"])
                    if e["q"] == "克數填寫(g)":
                        user_g_clean = re.sub(r'\D', '', u["g"])
                        is_g_correct = (user_g_clean == e["g"])
                    else:
                        is_g_correct = True
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
                    "fully_correct": is_fully_correct,
                    "time_spent": elapsed_time
                })
                st.session_state.current_q += 1
                st.session_state.q_start_time = time.time()
                st.rerun()

# 3. 測驗完成結果頁面
else:
    total_q = len(st.session_state.questions)
    score = st.session_state.score
    percentage = int((score / total_q) * 100)
    
    st.balloons()
    st.success(f"🎉 測驗完成！辛苦了，{st.session_state.staff_name}！")
    st.metric(label="最終得分", value=f"{score} / {total_q} 題", delta=f"正確率 {percentage}%")
    
    if percentage == 100:
        st.write("🌟 **評語：** 非常完美！你根本內場小天才吧")
    elif percentage >= 80:
        st.write("👍 **評語：** 表現良好！部分細節再複習一下會更好")
    else:
        st.write("⚠️ **評語：** 尚未達標，壞小孩快去看神奇的配方表啊")
        
    st.markdown("---")
    st.subheader("☁️ 成績資料同步狀態")
    
    if not st.session_state.uploaded:
        with st.spinner("正在自動將成績上傳至雲端試算表..."):
            try:
                creds_dict = dict(st.secrets["gcp_service_account"])
                scopes = [
                    "https://www.googleapis.com/auth/spreadsheets",
                    "https://www.googleapis.com/auth/drive"
                ]
                creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
                client = gspread.authorize(creds)
                
                sheet = client.open("披薩考核成績紀錄").sheet1
                
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                total_time = sum([r["time_spent"] for r in st.session_state.results])
                
                row_data = [
                    current_time,
                    st.session_state.staff_name,
                    total_q,
                    score,
                    f"{percentage}%",
                    round(total_time, 1)
                ]
                
                sheet.append_row(row_data)
                st.session_state.uploaded = True
                st.success("✅ 太棒了！本次成績已經成功寫入「披薩考核成績紀錄」試算表中！")
                
            except Exception as e:
                st.error(f"❌ 上傳失敗。詳細錯誤：{e}")
    else:
        st.success("✅ 本次成績已成功保存在試算表中。")

    st.markdown("---")
    st.subheader("📝 答題檢討明細與所花時間")
    for idx, res in enumerate(st.session_state.results, 1):
        status_icon = "✅" if res["fully_correct"] else "❌"
        with st.expander(f"{status_icon} 第 {idx} 題：{res['item']} (⏱️ 耗時 {res['time_spent']} 秒)"):
            u_sauce = res['sauce_user'] if res['sauce_user'] != "(請選擇)" else "(未選底醬)"
            if not res["sauce_ok"]:
                st.write(f"❌ 底醬選擇：`{u_sauce}` ｜ 正確答案：`{res['sauce_ans']}`")
            else:
                st.write(f"✅ 底醬選擇：`{u_sauce}`")
                
            st.write("**配料比對：**")
            for u, e in zip(res["ing_user"], res["ing_ans"]):
                ans_str = f"{e['n']} {e['g']}g" if e['q'] == "克數填寫(g)" else f"{e['n']} {e['q']}"
                u_n = u['n'] if u['n'] != "(請選擇)" else "(未選配料)"
                u_q = u['q'] if u['q'] != "(請選擇)" else "(未選份量)"
                user_str = f"{u_n} {u['g']}" if e['q'] == "克數填寫(g)" else f"{u_n} {u_q}"
                
                if e["q"] == "克數填寫(g)":
                    user_g_clean = re.sub(r'\D', '', u["g"])
                    is_g_correct = (user_g_clean == e["g"])
                else:
                    is_g_correct = True
                    
                is_correct = (u["n"] == e["n"]) and (u["q"] == e["q"]) and is_g_correct
                
                if is_correct:
                    st.write(f"  - ✅ `{ans_str}`")
                else:
                    st.write(f"  - ❌ 您的答案：`{user_str}` ｜ 正確答案：`{ans_str}`")

    if st.button("🔄 重新開始測驗"):
        st.session_state.started = False
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.results = []
        st.session_state.uploaded = False
        st.rerun()

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray; font-size: 14px;'>© 版權歸必勝客所有</p>", unsafe_allow_html=True)
