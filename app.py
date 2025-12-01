# app.py
import streamlit as st
import streamlit.components.v1 as components
import json
from agents.reviewer import ReviewerAgent
from agents.researcher import ResearcherAgent
from agents.visualizer import VisualizerAgent  # 导入新角色

# --- 辅助函数：渲染 Mermaid 图表 ---
def render_mermaid(code):
    """
    在 Streamlit 中渲染 Mermaid 图表
    使用更简单直接的方式
    """
    # 显示调试信息
    st.write("**Mermaid代码调试信息：**")
    st.write(f"- 代码长度: {len(code)} 字符")
    st.write(f"- 代码格式: {'有效' if code.strip().startswith(('graph', 'mindmap')) else '无效'}")
    st.code(code, language='mermaid')
    
    # 检查代码是否为空
    if not code or code.strip() == '':
        st.warning("没有生成有效的Mermaid代码")
        return
        
    # 确保代码包含正确的图表类型声明
    if not (code.strip().startswith('graph') or code.strip().startswith('mindmap')):
        st.warning("Mermaid代码格式不正确，请检查是否包含 'graph' 或 'mindmap' 声明")
    
    # 使用最简单直接的方式加载mermaid.js
    # 简化HTML代码，避免复杂的DOM加载事件
    html_code = f"""
    <div class="mermaid">
    {code}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@8.14.0/dist/mermaid.min.js"></script>
    <script>
        // 直接初始化，不等待DOM加载完成
        mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
        mermaid.init();
    </script>
    """
    
    # 使用固定高度
    st.write("**图表渲染结果：**")
    components.html(html_code, height=600, scrolling=True)

# --- 辅助函数：本地存储对话历史 ---
def save_conversation_history():
    """将对话历史保存到localStorage"""
    conversation_data = {
        "mark": st.session_state.conversation_history["mark"],
        "amy": st.session_state.conversation_history["amy"],
        "susu": st.session_state.conversation_history["susu"]
    }
    st.session_state.storage_data = json.dumps(conversation_data)

def load_conversation_history():
    """从localStorage加载对话历史"""
    if "storage_data" in st.session_state and st.session_state.storage_data:
        try:
            conversation_data = json.loads(st.session_state.storage_data)
            st.session_state.conversation_history = {
                "mark": conversation_data.get("mark", []),
                "amy": conversation_data.get("amy", []),
                "susu": conversation_data.get("susu", [])
            }
        except:
            st.session_state.conversation_history = {
                "mark": [],
                "amy": [],
                "susu": []
            }

def clear_conversation_history():
    """清除对话历史"""
    st.session_state.conversation_history = {
        "mark": [],
        "amy": [],
        "susu": []
    }
    st.session_state.storage_data = ""
    st.session_state.context_cleared = True
    save_conversation_history()

# 1. 页面配置
st.set_page_config(page_title="AI 小组讨论室", layout="wide")

st.title("🎓 AI 沉浸式学习小组")
st.caption("你的全能虚拟助教团队：马克（逻辑）、艾米（数据）、苏苏（视觉）")
st.markdown("---")

# 2. 初始化智能体和对话历史
if 'agents' not in st.session_state:
    st.session_state.agents = {
        "mark": ReviewerAgent(name="马克", role="逻辑审核员"),
        "amy": ResearcherAgent(name="艾米", role="数据资料员"),
        "susu": VisualizerAgent(name="苏苏", role="视觉设计师") # 新增苏苏
    }

# 初始化对话历史
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = {
        "mark": [],
        "amy": [],
        "susu": []
    }

# 初始化存储数据
if 'storage_data' not in st.session_state:
    st.session_state.storage_data = ""

# 初始化上下文清除状态
if 'context_cleared' not in st.session_state:
    st.session_state.context_cleared = False

# 加载对话历史
load_conversation_history()

# 3. 布局：双栏设计
col_editor, col_feedback = st.columns([1, 1]) 

# --- 左侧：用户编辑区 ---
with col_editor:
    st.subheader("📝 你的工作台")
    
    # 显示上下文状态
    if st.session_state.context_cleared:
        st.success("✅ 上下文已清除")
        st.session_state.context_cleared = False
    else:
        total_messages = sum(len(history) for history in st.session_state.conversation_history.values())
        if total_messages > 0:
            st.info(f"💾 上下文已保存 ({total_messages} 条消息)")
    
    user_draft = st.text_area(
        "在此撰写内容...",
        height=500,
        placeholder="例如：工业革命不仅带来了蒸汽机，还改变了社会结构，导致了城市化进程加快..."
    )
    
    # 创建按钮列布局
    button_col1, button_col2 = st.columns([3, 1])
    
    with button_col1:
        start_review = st.button("📤 发送给小组 (请求反馈)", type="primary")
    
    with button_col2:
        if st.button("🗑️ 清除上下文"):
            clear_conversation_history()
            st.experimental_rerun()
    
    # 添加用户提示
    with st.expander("ℹ️ 关于上下文记忆功能"):
        st.markdown("""
        **上下文记忆功能说明：**
        - 您的所有讨论内容将被自动保存，形成连续的对话历史
        - 页面刷新或重新进入时，上下文将保持不变
        - 只有点击"清除上下文"按钮才会删除所有历史记录
        - 每个AI助手都有独立的对话历史
        """)

# --- 右侧：AI 反馈区 ---
with col_feedback:
    st.subheader("💬 小组反馈")
    
    # 使用 Tabs 整理界面
    tab_logic, tab_data, tab_visual = st.tabs(["🧠 逻辑检查", "📊 数据补充", "🎨 逻辑图示"])
    
    if start_review and user_draft:
        with st.spinner("小组正在头脑风暴中..."):
            # 获取每个agent的历史对话
            mark_history = st.session_state.conversation_history["mark"]
            amy_history = st.session_state.conversation_history["amy"]
            susu_history = st.session_state.conversation_history["susu"]
            
            # 并行处理（在简单的 Streamlit 结构中顺序执行即可，速度很快）
            review_res = st.session_state.agents['mark'].process(user_draft, conversation_history=mark_history)
            data_res = st.session_state.agents['amy'].process(user_draft, conversation_history=amy_history)
            visual_res = st.session_state.agents['susu'].process(user_draft, conversation_history=susu_history)
            
            # 保存对话历史
            st.session_state.conversation_history["mark"].append({"role": "user", "content": user_draft})
            st.session_state.conversation_history["mark"].append({"role": "assistant", "content": review_res})
            
            st.session_state.conversation_history["amy"].append({"role": "user", "content": user_draft})
            st.session_state.conversation_history["amy"].append({"role": "assistant", "content": data_res})
            
            st.session_state.conversation_history["susu"].append({"role": "user", "content": user_draft})
            st.session_state.conversation_history["susu"].append({"role": "assistant", "content": visual_res})
            
            # 保存到localStorage
            save_conversation_history()
            
        # 填充内容
        with tab_logic:
            st.info(f"🧐 **{st.session_state.agents['mark'].name}** 的批注：")
            st.markdown(review_res)
            
        with tab_data:
            st.success(f"📚 **{st.session_state.agents['amy'].name}** 的资料：")
            st.markdown(data_res)
            
        with tab_visual:
                st.warning(f"🎨 **{st.session_state.agents['susu'].name}** 的绘图：")
                st.caption("基于你的文本生成的结构图：")
                # 显示原始生成的代码（用于调试）
                st.write("**原始生成代码：**")
                st.code(visual_res)
                # 调用渲染函数
                render_mermaid(visual_res)
                
    elif not start_review:
        # 空闲状态显示占位符
        with tab_logic:
            st.info("等待提交草稿...")
        with tab_data:
            st.info("等待提交草稿...")
        with tab_visual:
            st.info("等待提交草稿...")