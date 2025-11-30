# app.py
import streamlit as st
from agents.reviewer import ReviewerAgent
from agents.researcher import ResearcherAgent

# 1. 页面配置
st.set_page_config(page_title="AI 小组讨论室", layout="wide")

st.title("🎓 AI 沉浸式学习小组")
st.markdown("---")

# 2. 初始化智能体 (模拟组队)
if 'agents' not in st.session_state:
    st.session_state.agents = {
        "mark": ReviewerAgent(name="马克", role="逻辑审核员"),
        "amy": ResearcherAgent(name="艾米", role="数据资料员")
    }

# 3. 布局：双栏设计
col_editor, col_feedback = st.columns([1, 1]) # 1:1 比例

# --- 左侧：用户编辑区 ---
with col_editor:
    st.subheader("📝 你的工作台")
    # 获取用户输入
    user_draft = st.text_area(
        "在此撰写你的报告/演讲稿...",
        height=400,
        placeholder="开始输入你的想法，例如：AI虽然取代了部分工作，但也创造了新的机会..."
    )
    
    # 触发按钮
    start_review = st.button("📤 发送给小组 (请求反馈)")

# --- 右侧：AI 反馈区 ---
with col_feedback:
    st.subheader("💬 小组反馈")
    
    if start_review and user_draft:
        with st.spinner("小组正在阅读你的草稿..."):
            # 并行调用智能体 (简单起见这里用顺序调用，后续可改为并行)
            review_feedback = st.session_state.agents['mark'].process(user_draft)
            data_feedback = st.session_state.agents['amy'].process(user_draft)
            
        # 展示马克的反馈
        st.info(f"🧐 **{st.session_state.agents['mark'].name} ({st.session_state.agents['mark'].role})** 说：")
        st.markdown(review_feedback)
        
        st.markdown("---")
        
        # 展示艾米的反馈
        st.success(f"📚 **{st.session_state.agents['amy'].name} ({st.session_state.agents['amy'].role})** 说：")
        st.markdown(data_feedback)
        
    elif start_review and not user_draft:
        st.warning("请先在左侧写点东西，我们才能给你建议哦！")
    else:
        st.markdown("*等待提交...*")
        st.info("💡 提示：写完一段后，点击左侧按钮，看看马克和艾米会说什么。")