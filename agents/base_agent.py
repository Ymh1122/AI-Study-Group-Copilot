# agents/base_agent.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置 Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class BaseAgent:
    def __init__(self, name, role, model="gemini-1.5-flash"):
        self.name = name
        self.role = role
        self.model_name = model
        # 初始化模型
        self.model = genai.GenerativeModel(self.model_name)

    def get_system_prompt(self):
        """需要子类重写"""
        return "You are a helpful assistant."

    def process(self, user_content):
        """核心处理逻辑：接收用户文档，返回反馈"""
        try:
            # Gemini 的 system prompt 通常放在 generation_config 或者直接拼在 prompt 前面
            # 这里我们采用拼接的方式，或者利用 system_instruction (如果是 1.5 Pro/Flash)
            
            # 创建带 System Instruction 的新模型实例（建议做法）
            model = genai.GenerativeModel(
                self.model_name,
                system_instruction=self.get_system_prompt()
            )
            
            response = model.generate_content(
                f"用户正在撰写的文档内容如下：\n\n{user_content}\n\n请根据你的角色给出简短、具体的反馈。"
            )
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"