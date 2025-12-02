# app.py
import streamlit as st
import streamlit.components.v1 as components
import json
from agents.reviewer import ReviewerAgent
from agents.researcher import ResearcherAgent
from agents.visualizer import VisualizerAgent  # 导入新角色

# --- 辅助函数：渲染 Mermaid 图表 ---
def render_mermaid(code, sender_info=None, debug=False):
    """
    在 Streamlit 中渲染 Mermaid 图表
    使用更简单直接的方式
    """
    if debug:
        # 显示调试信息
        st.write("**Mermaid代码调试信息：**")
        st.write(f"- 代码长度: {len(code)} 字符")
        st.write(f"- 代码格式: {'有效' if code.strip().startswith(('graph', 'mindmap')) else '无效'}")
        st.code(code, language='mermaid')
    
    # 检查代码是否为空
    if not code or code.strip() == '':
        if debug:
            st.warning("没有生成有效的Mermaid代码")
        return
        
    # 确保代码包含正确的图表类型声明
    if not (code.strip().startswith('graph') or code.strip().startswith('mindmap')):
        if debug:
            st.warning("Mermaid代码格式不正确，请检查是否包含 'graph' 或 'mindmap' 声明")
    
    # 准备头部信息
    header_html = ""
    box_style = ""
    if sender_info:
        name = sender_info.get('name', '苏苏')
        role = sender_info.get('role', '视觉设计师')
        timestamp = sender_info.get('timestamp', '')
        
        # 使用新的CSS类样式
        header_html = f"""
            <div class="bubble-header">
                <span class="avatar" style="background-color: #fff3e0;">🎨</span>
                <strong style="color: #f57c00;">{name}</strong>
                <span style="background-color: #fff3e0; color: #f57c00; padding: 2px 8px; border-radius: 10px; font-size: 0.8em; margin-left: 8px;">{role}</span>
                <small style="color: gray; margin-left: auto;">{timestamp}</small>
            </div>
        """
        # 使用新的CSS类样式
        box_class = "chat-bubble assistant-bubble role-susu"
    else:
        box_class = "mermaid"
    
    # 估算高度：基础高度 + 每行代码增加的高度
    # 这是一个简单的启发式方法，避免固定高度导致的巨大空白
    line_count = len(code.strip().split('\n'))
    estimated_height = max(200, min(600, line_count * 40 + 100))
    
    # 使用最简单直接的方式加载mermaid.js
    # 简化HTML代码，避免复杂的DOM加载事件
    # 注意：我们需要将CSS样式注入到iframe中，因为iframe不继承父页面的样式
    html_code = f"""
    <style>
        body {{
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 10px;
            overflow: hidden; /* 隐藏滚动条，除非必要 */
        }}
        /* 聊天气泡基础样式 */
        .chat-bubble {{
            padding: 15px;
            border-radius: 15px;
            margin-bottom: 0; /* 移除内部margin，由iframe高度控制 */
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            position: relative;
        }}
        
        /* 助手气泡通用 */
        .assistant-bubble {{
            background-color: #ffffff;
            border-bottom-left-radius: 2px;
            margin-right: 10%;
            border: 1px solid #f0f0f0;
        }}
        
        /* 角色特定样式 */
        .role-susu {{ border-left: 4px solid #ff9800; }}
        
        /* 头部信息 */
        .bubble-header {{
            display: flex;
            align-items: center;
            margin-bottom: 8px;
            font-size: 0.9em;
        }}
        
        .avatar {{
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-right: 8px;
            font-size: 14px;
        }}
    </style>
    <div class="{box_class}">
        {header_html}
        <div class="mermaid">
        {code}
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.0/dist/mermaid.min.js"></script>
    <script>
        // 直接初始化，不等待DOM加载完成
        mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
        mermaid.init();
    </script>
    """
    
    # 使用估算的高度
    if debug:
        st.write(f"**图表渲染结果 (高度: {estimated_height}px)：**")
    components.html(html_code, height=estimated_height, scrolling=True)

# --- 辅助函数：本地存储对话历史 ---
def save_conversation_history():
    """将对话历史保存到localStorage"""
    # 保存统一的聊天记录格式
    conversation_data = {
        "mark": st.session_state.conversation_history["mark"],
        "amy": st.session_state.conversation_history["amy"],
        "susu": st.session_state.conversation_history["susu"],
        "chat": st.session_state.chat_history  # 保存统一的聊天记录
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
            # 加载统一的聊天记录
            st.session_state.chat_history = conversation_data.get("chat", [])
        except:
            st.session_state.conversation_history = {
                "mark": [],
                "amy": [],
                "susu": []
            }
            st.session_state.chat_history = []

def clear_conversation_history():
    """清除对话历史"""
    st.session_state.conversation_history = {
        "mark": [],
        "amy": [],
        "susu": []
    }
    st.session_state.chat_history = []  # 清除统一的聊天记录
    st.session_state.storage_data = ""
    st.session_state.context_cleared = True
    save_conversation_history()

# 1. 页面配置
st.set_page_config(page_title="AI 小组讨论室", layout="wide", page_icon="🎓")

# --- 自定义 CSS ---
st.markdown("""
<style>
    /* 全局字体优化 */
    body {
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    }
    
    /* 聊天气泡基础样式 */
    .chat-bubble {
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 10px; /* 减小间距 */
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        position: relative;
        animation: fadeIn 0.3s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* 用户气泡 */
    .user-bubble {
        background-color: #e3f2fd;
        border-bottom-right-radius: 2px;
        margin-left: 20%;
        border: 1px solid #bbdefb;
    }
    
    /* 助手气泡通用 */
    .assistant-bubble {
        background-color: #ffffff;
        border-bottom-left-radius: 2px;
        margin-right: 10%;
        border: 1px solid #f0f0f0;
    }
    
    /* 角色特定样式 */
    .role-mark { border-left: 4px solid #2196f3; }
    .role-amy { border-left: 4px solid #4caf50; }
    .role-susu { border-left: 4px solid #ff9800; }
    
    /* 头部信息 */
    .bubble-header {
        display: flex;
        align-items: center;
        margin-bottom: 8px;
        font-size: 0.9em;
    }
    
    .avatar {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-right: 8px;
        font-size: 14px;
    }
    
    /* 按钮美化 */
    .stButton button {
        border-radius: 20px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* 输入框美化 */
    .stTextArea textarea {
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        padding: 15px;
        font-size: 16px;
    }
    
    .stTextArea textarea:focus {
        border-color: #2196f3;
        box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2);
    }
    
    /* 标题美化 */
    h1 {
        color: #1a237e;
        font-weight: 700;
    }
    
    .stExpander {
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        background-color: #fafafa;
        color: #333333; /* 强制深色字体 */
    }
    
    .stExpander p, .stExpander li {
        color: #333333 !important; /* 强制深色字体 */
    }
</style>
""", unsafe_allow_html=True)

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

# 初始化统一聊天历史
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

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
    # 文件上传功能
    uploaded_file = st.file_uploader("📁 上传文件", type=["txt", "pdf", "md"], key="file_uploader")
    
    # 如果用户上传了文件，读取文件内容
    file_content = ""
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.pdf'):
                # 处理PDF文件
                import PyPDF2
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                file_content = ""
                for page in pdf_reader.pages:
                    file_content += page.extract_text() + "\n"
            else:
                # 处理文本文件
                file_content = uploaded_file.read().decode("utf-8")
            
            st.success(f"✅ 文件 {uploaded_file.name} 上传成功！")
        except Exception as e:
            st.error(f"❌ 文件处理出错: {str(e)}")
            file_content = ""
    
    user_draft = st.text_area(
        "在此撰写内容...",
        height=400,
        placeholder="例如：工业革命不仅带来了蒸汽机，还改变了社会结构，导致了城市化进程加快...",
        value=file_content
    )
    
    # 创建按钮列布局
    button_col1, button_col2 = st.columns([3, 1])
    
    with button_col1:
        start_review = st.button("🚀 发送给小组", type="primary", use_container_width=True)
    
    with button_col2:
        if st.button("🗑️ 清除聊天记录"):
            clear_conversation_history()
            st.rerun()
    
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
    st.subheader("💬 小组讨论记录")
    
    # 显示聊天历史
    chat_container = st.container()
    
    with chat_container:
        # 如果有聊天历史，则显示
        if st.session_state.chat_history:
            for message in st.session_state.chat_history:
                sender = message["sender"]
                name = message["name"]
                content = message["content"]
                timestamp = message["timestamp"]
                
                # 根据发送者设置不同的样式
                if sender == "user":
                    st.markdown(f"""
                    <div class="chat-bubble user-bubble">
                        <div class="bubble-header" style="justify-content: flex-end;">
                            <small style="color: gray; margin-right: 8px;">{timestamp}</small>
                            <strong style="color: #1565c0;">{name}</strong>
                            <span class="avatar" style="background-color: #bbdefb; margin-left: 8px; margin-right: 0;">👤</span>
                        </div>
                        <div style="color: #333; text-align: right;">{content}</div>
                    </div>
                    """, unsafe_allow_html=True)
                elif sender == "mark":
                    st.markdown(f"""
                    <div class="chat-bubble assistant-bubble role-mark">
                        <div class="bubble-header">
                            <span class="avatar" style="background-color: #e3f2fd;">🧠</span>
                            <strong style="color: #1976d2;">{name}</strong> 
                            <span style="background-color: #e3f2fd; color: #1976d2; padding: 2px 8px; border-radius: 10px; font-size: 0.8em; margin-left: 8px;">逻辑审核员</span>
                            <small style="color: gray; margin-left: auto;">{timestamp}</small>
                        </div>
                        <div style="color: #333; line-height: 1.6;">{content}</div>
                    </div>
                    """, unsafe_allow_html=True)
                elif sender == "amy":
                    st.markdown(f"""
                    <div class="chat-bubble assistant-bubble role-amy">
                        <div class="bubble-header">
                            <span class="avatar" style="background-color: #e8f5e9;">📊</span>
                            <strong style="color: #388e3c;">{name}</strong>
                            <span style="background-color: #e8f5e9; color: #388e3c; padding: 2px 8px; border-radius: 10px; font-size: 0.8em; margin-left: 8px;">数据资料员</span>
                            <small style="color: gray; margin-left: auto;">{timestamp}</small>
                        </div>
                        <div style="color: #333; line-height: 1.6;">{content}</div>
                    </div>
                    """, unsafe_allow_html=True)
                elif sender == "susu":
                    # 渲染 Mermaid 图表，包含发送者信息以便包装在同一个框内
                    render_mermaid(content, sender_info={"name": name, "role": "视觉设计师", "timestamp": timestamp}, debug=False)
        else:
            st.info("还没有讨论记录，提交草稿开始与AI助手们的对话吧！")
    
    # 处理用户提交
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
            
            # 添加到统一聊天历史
            st.session_state.chat_history.append({"sender": "user", "name": "你", "content": user_draft, "timestamp": "刚刚"})
            st.session_state.chat_history.append({"sender": "mark", "name": st.session_state.agents['mark'].name, "content": review_res, "timestamp": "刚刚"})
            st.session_state.chat_history.append({"sender": "amy", "name": st.session_state.agents['amy'].name, "content": data_res, "timestamp": "刚刚"})
            st.session_state.chat_history.append({"sender": "susu", "name": st.session_state.agents['susu'].name, "content": visual_res, "timestamp": "刚刚"})
            
            # 保存到localStorage
            save_conversation_history()
            
            # 重新运行以更新界面
            st.rerun()