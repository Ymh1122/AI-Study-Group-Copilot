# agents/base_agent.py
import os
import dashscope
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置 DashScope API
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

class BaseAgent:
    def __init__(self, name, role, model="qwen-plus"):
        self.name = name
        self.role = role
        self.model_name = model

    def get_system_prompt(self):
        """需要子类重写"""
        return "You are a helpful assistant."

    def process(self, user_content, context_material=None, conversation_history=None):
        """
        核心处理逻辑
        :param user_content: 用户的草稿
        :param context_material: 上传的参考资料（可选）
        :param conversation_history: 对话历史（可选）
        """
        try:
            # 构造消息列表
            messages = [
                {"role": "system", "content": self.get_system_prompt()}
            ]
            
            # 如果有参考资料，注入到消息中
            if context_material:
                messages.append({
                    "role": "system", 
                    "content": (
                        "【参考资料/背景知识】\n"
                        "请优先基于以下提供的资料内容进行分析。如果用户的内容与资料冲突，请指出。\n"
                        f"---开始资料---\n{context_material}\n---结束资料---\n\n"
                    )
                })
            
            # 添加对话历史（如果有）
            if conversation_history:
                messages.extend(conversation_history)
            
            # 添加当前用户内容
            messages.append({
                "role": "user",
                "content": f"【用户正在撰写的文档】\n{user_content}\n\n请根据你的角色给出反馈。"
            })
            
            # 发送请求
            response = dashscope.Generation.call(
                model=self.model_name,
                messages=messages,
                result_format='message'
            )
            
            # 处理响应
            if response.status_code == 200:
                ai_response = response.output.choices[0]['message']['content']
                # 返回结果和更新后的对话历史
                return ai_response
            else:
                return f"Error: {response.message}"
        except Exception as e:
            return f"Error: {str(e)}"