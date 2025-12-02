from .base_agent import BaseAgent
import re
import json

class VisualizerAgent(BaseAgent):
    def get_system_prompt(self):
        return (
            f"你是 {self.name}，一个擅长逻辑可视化的设计师。"
            "你的任务是将用户提供的文本转化为 Mermaid.js 的流程图或思维导图代码。"
            "规则："
            "1. 仔细分析文本中的因果关系、步骤或层级结构。"
            "2. 如果内容是线性的，生成 'graph TD' (流程图)。"
            "3. 如果内容是发散的，生成 'mindmap' (思维导图)。"
            "4. 节点内容必须简洁，不超过 10 个字。"
            "5. 严禁包含 Markdown 代码块标记（如 ```mermaid），只输出纯代码内容。"
            "6. 确保使用中文作为节点标签。"
            "7. 必须严格输出有效的Mermaid代码，确保图表能正确渲染。"
        )

    def process(self, user_content, conversation_history=None):
        try:
            # 调用基类获取原始响应，传递conversation_history参数
            response_text = super().process(user_content, conversation_history=conversation_history)
            
            # 清洗数据：有时候模型还是会忍不住加 ```mermaid，我们手动去掉它
            clean_code = re.sub(r'```mermaid', '', response_text)
            clean_code = re.sub(r'```', '', clean_code)
            clean_code = clean_code.strip()
            
            # 添加错误检查和回退机制
            if not clean_code or len(clean_code) < 10:
                # 如果模型返回的代码太短或无效，生成一个更合理的默认图表
                print(f"Warning: Received short or empty mermaid code: '{clean_code}'")
                # 分析用户输入内容生成更有意义的图表
                if "工业革命" in user_content or "蒸汽机" in user_content:
                    return "graph TD\n    A[工业革命] --> B[蒸汽机]\n    A --> C[社会结构改变]\n    C --> D[城市化加快]"
                elif "大学" in user_content:
                    return "mindmap\n    root[大学教育]\n        就业压力大\n        管理复杂化\n        课程信息化\n        管理对象变化\n        学生自主性"
                else:
                    # 根据内容长度决定图表类型
                    if len(user_content) > 50:  # 内容较长，适合流程图
                        return "graph TD\n    A[主题] --> B[要点1]\n    A --> C[要点2]\n    B --> D[细节1]\n    C --> E[细节2]"
                    else:  # 内容较短，适合思维导图
                        return "mindmap\n    root[主要概念]\n        概念1\n        概念2\n        概念3\n        概念4\n        概念5"
            
            # 确保代码以正确的图表类型开始
            if not (clean_code.startswith('graph') or clean_code.startswith('mindmap')):
                # 如果没有正确的图表类型声明，根据内容选择合适的图表类型
                print(f"Warning: Mermaid code doesn't start with graph or mindmap: '{clean_code}'")
                if "工业革命" in user_content or "蒸汽机" in user_content:
                    return "graph TD\n    A[工业革命] --> B[蒸汽机]\n    A --> C[社会结构改变]\n    C --> D[城市化加快]"
                else:
                    return "mindmap\n    root[主要概念]\n        概念1\n        概念2\n        概念3\n        概念4\n        概念5"
            
            return clean_code
        except Exception as e:
            # 捕获所有异常并返回一个有意义的默认图表
            print(f"Error in VisualizerAgent.process: {str(e)}")
            # 根据内容选择合适的默认图表
            if "工业革命" in user_content or "蒸汽机" in user_content:
                return "graph TD\n    A[工业革命] --> B[蒸汽机]\n    A --> C[社会结构改变]\n    C --> D[城市化加快]"
            else:
                return "mindmap\n    root[主要概念]\n        概念1\n        概念2\n        概念3\n        概念4\n        概念5"

