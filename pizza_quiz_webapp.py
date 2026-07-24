import streamlit as st
import random

# 設定網頁標題與圖示
st.set_page_config(page_title="門市食材配方考核系統", page_icon="🍕", layout="centered")

# 完整 17 項配方題庫（後端資料，前端無法直接檢視）
RECIPES = [
    {"name": "松露干貝鮮蝦起司", "sauce": "無", "ingredients": ["起司 1/2", "洋蔥 1/2", "菠菜 1/2", "大蝦仁 10隻", "干貝 10個", "魷魚圈 5圈", "番茄 1/2", "牛肝菌菇醬 橫直各5條", "起司 1/2"]},
    {"name": "千島海鮮盛宴", "sauce": "千島醬 2滿杓(專)", "ingredients": ["起司 1", "鳳梨 1/2", "青椒 1/2", "魷魚圈 5圈", "大蝦仁 5隻", "干貝 5個", "1/2蟹風味棒 5個", "番茄 1/2", "起司 1/2", "明太子醬 Z字來回5次"]},
    {"name": "丸勝日式章魚燒", "sauce": "照燒醬 2平杓(專)", "ingredients": ["起司 1/2", "章魚燒丸子 10顆", "青椒 1/2", "甜不辣 1/2", "章魚 1/2", "起司 1/2"]},
    {"name": "和風章魚燒", "sauce": "照燒醬 2平杓(專)", "ingredients": ["起司 1", "洋蔥 1/2", "青椒 1/2", "甜不辣 1/2", "章魚 1", "起司 1"]},
    {"name": "經典海鮮四重奏", "sauce": "Pizza Sauce 1平杓", "ingredients": ["起司 1", "蟹肉絲 2", "小蝦 1/2", "蛤蜊肉 1/2", "帆立貝 8顆", "番茄 1/2", "起司 1"]},
    {"name": "法式海陸盛宴", "sauce": "卡菲底醬 小藍杓*1平杓", "ingredients": ["起司 1/2", "洋蔥 1/2", "韓國烤肉餡 1(外1圈)", "鱈魚片 5片", "大蝦仁 5隻", "番茄 1/2", "花枝調味粉 均勻分灑", "起司 1/2"]},
    {"name": "韓式泡菜豬五花", "sauce": "無", "ingredients": ["起司 1/2", "韓國泡菜 1", "起司 1", "韓式豬五花 1+1/2", "花枝調味粉 均勻分灑"]},
    {"name": "超級總匯", "sauce": "Pizza Sauce 1平杓", "ingredients": ["起司 1", "PP 9片", "火腿 9片", "洋蔥 1/2", "青椒 1/2", "洋菇 1/2", "豬義混 1", "起司 1"]},
    {"name": "夏威夷", "sauce": "Pizza Sauce 1平杓", "ingredients": ["起司 1", "火腿 26片", "鳳梨 1", "起司 1"]},
    {"name": "超級夏威夷", "sauce": "Pizza Sauce 1平杓", "ingredients": ["起司 1/2", "火腿 14+8片", "培根 10+2片", "午餐肉丁 1", "鳳梨 1", "起司 1"]},
    {"name": "雙層美式臘腸", "sauce": "Pizza Sauce 1平杓", "ingredients": ["起司 1", "PP 16片", "起司 1", "PP 16片", "起司 1/2"]},
    {"name": "泰式檸檬椒麻豬", "sauce": "泰式椒麻醬 1平杓", "ingredients": ["起司 1", "洋蔥 1/2", "菠菜 1/2", "豬腿肉片 150g", "番茄 1/2", "起司 1/2"]},
    {"name": "經典費城起司牛肉", "sauce": "無", "ingredients": ["起司 1", "費城牛肉 225g", "三色絲 1", "起司 1/2"]},
    {"name": "鐵板雙牛", "sauce": "BBQ醬 15cc*1滿匙", "ingredients": ["起司 1", "黑胡椒牛柳 110g", "洋菇 1/2", "菠菜 1", "牛肉丸 10顆", "起司 1/2"]},
    {"name": "韓風醬烤雪花牛", "sauce": "洋釀淋醬 Z字交叉來回7次", "ingredients": ["起司 1", "韭菜 1", "韓式燒牛肉 190g", "起司 1"]},
    {"name": "炙燒明太子嫩雞", "sauce": "照燒醬 2平杓(專)", "ingredients": ["起司 1", "洋菇 1/2", "炭烤雞腿塊 1(滿杯)", "番茄 1/2", "起司 1/2", "明太子醬 Z字來回5次"]},
    {"name": "彩蔬鮮菇", "sauce": "BBQ醬 15cc*3滿匙", "ingredients": ["起司 1", "洋菇 1", "菠菜 1", "番茄 1/2", "起司 1"]}
]

# 初始化 Session State 狀態
if "started" not in st.session_state:
    st.session_state.started = False
if "emp_name" not in st.session_state:
    st.session_state.emp_name = ""
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

# 1. 測驗未開始：輸入名字與設定題數
if not st.session_state.started:
    st.markdown("### 📋 員工測驗登入")
    st.info("請輸入您的姓名/員工編號開始測驗。測驗過程無法查看原始碼或配方解答。")
    
    emp_name = st.text_input("請輸入姓名 / 員工編號：")
    num_q = st.slider("抽考題數：", min_value=3, max_value=len(RECIPES), value=5)
    
    if st.button("🚀 開始測驗", type="primary"):
        if not emp_name.strip():
            st.error("請填寫姓名後再開始！")
        else:
            st.session_state.emp_name = emp_name
            st.session_state.started = True
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.session_state.results = []
            shuffled = RECIPES.copy()
            random.shuffle(shuffled)
            st.session_state.questions = shuffled[:num_q]
            st.rerun()

# 2. 測驗進行中
elif st.session_state.current_q < len(st.session_state.questions):
    total_q = len(st.session_state.questions)
    curr_idx = st.session_state.current_q
    q_data = st.session_state.questions[curr_idx]
    
    st.progress((curr_idx) / total_q, text=f"進度：第 {curr_idx + 1} / {total_q} 題")
    st.subheader(f"第 {curr_idx + 1} 題：【{q_data['name']}】")
    
    with st.form(key=f"q_form_{curr_idx}"):
        st.write("請輸入正確的配方內容（若無底醬請填 '無'）：")
        
        sauce_input = st.text_input("1. 底醬與用量：", key=f"sauce_{curr_idx}")
        
        st.write("2. 請依序填入鋪設配料與用量（例如：`起司 1/2`）：")
        ing_inputs = []
        for j, expected_ing in enumerate(q_data["ingredients"]):
            user_ing = st.text_input(f"   配料 {j+1}：", key=f"ing_{curr_idx}_{j}")
            ing_inputs.append(user_ing.strip())
            
        submitted = st.form_submit_button("提交本題答案", type="primary")
        
        if submitted:
            # 計算該題正確度
            sauce_correct = (sauce_input.strip() == q_data["sauce"])
            ing_correct_count = sum(1 for u, e in zip(ing_inputs, q_data["ingredients"]) if u == e)
            total_items = 1 + len(q_data["ingredients"])
            got_items = (1 if sauce_correct else 0) + ing_correct_count
            
            is_fully_correct = (got_items == total_items)
            if is_fully_correct:
                st.session_state.score += 1
                
            st.session_state.results.append({
                "item": q_data["name"],
                "sauce_user": sauce_input.strip(),
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
    st.success(f"🎉 測驗完成！測驗人：**{st.session_state.emp_name}**")
    st.metric(label="最終得分", value=f"{score} / {total_q} 題", delta=f"正確率 {percentage}%")
    
    if percentage == 100:
        st.write("🌟 **評語：** 非常完美！配方非常熟練，准予獨立上工！")
    elif percentage >= 80:
        st.write("👍 **評語：** 表現良好！部分細節再複習一下會更好。")
    else:
        st.write("⚠️ **評語：** 尚未達標，請繼續熟背配方表後重新測驗。")
        
    st.markdown("---")
    st.subheader("📝 答題檢討明細")
    for idx, res in enumerate(st.session_state.results, 1):
        status_icon = "✅" if res["fully_correct"] else "❌"
        with st.expander(f"{status_icon} 第 {idx} 題：{res['item']}"):
            if not res["sauce_ok"]:
                st.write(f"❌ 底醬填寫：`{res['sauce_user']}` ｜ 正確答案：`{res['sauce_ans']}`")
            else:
                st.write(f"✅ 底醬填寫：`{res['sauce_user']}`")
                
            st.write("**配料比對：**")
            for u_ing, a_ing in zip(res["ing_user"], res["ing_ans"]):
                if u_ing == a_ing:
                    st.write(f"  - ✅ `{u_ing}`")
                else:
                    st.write(f"  - ❌ 您的答案：`{u_ing}` ｜ 正確答案：`{a_ing}`")

    if st.button("🔄 重新開始測驗"):
        st.session_state.started = False
        st.session_state.emp_name = ""
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.results = []
        st.rerun()
