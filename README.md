🎓 **AI Study Group Copilot**

**AI Study Group Copilot** is an immersive, multi-agent collaborative platform designed to transform solitary writing and studying into an interactive team experience.

Unlike traditional chatbots, this application adopts a **Split-Screen Workbench** approach: you focus on creating content on the left, while specialized AI agents (**Reviewers**, **Researchers**) provide real-time, task-specific scaffolding on the right.

---

### 🚀 Key Features

- **👥 Multi-Agent System:**
  - **Mark (The Logic Reviewer):** Critiques your logic and argumentation structure without rewriting your text.
  - **Amy (The Researcher):** Fetches relevant data, facts, and citations to support your claims.
  - **Susu (The Visual Designer):** Transforms your text into visual mind maps and flowcharts using Mermaid.js.

- **💾 Context Memory:**
  - Automatically saves all discussion content to maintain continuous conversation history
  - Preserves context after page refresh or re-entry
  - Independent conversation history for each AI agent
  - Clear context button to delete all history records
  - Implementation using browser localStorage for persistent storage
  - JSON serialization for efficient data storage and retrieval
  - Automatic synchronization between session state and localStorage

- **🎨 Visual Diagram Generation:**
  - Automatic generation of Mermaid.js flowcharts or mind maps based on your content
  - Real-time visualization of logical structures and relationships
  - Interactive diagram display with zoom and scroll capabilities
  - Optimized rendering using Mermaid.js v8.14.0 for better compatibility
  - Debugging information showing raw Mermaid code and validation status
  - Fallback mechanisms to ensure diagram generation even when AI output is invalid

- **🖥️ Split-Screen UI:** A distraction-free editor on the left paired with an AI feedback feed on the right.

- **⚡ Powered by Qwen:** Utilizes the fast and cost-effective `qwen-plus` model for near-instant feedback.

- **🔍 Unknown-Free Interaction:** Agents do not chat idly; they only respond when triggered by your content submission.

---

### 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/AI-Study-Group-Copilot.git
   cd AI-Study-Group-Copilot
   ```
2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
3. **Configure Environment Variables**
Create a .env file in the root directory and add your DashScope API Key:
    ```bash
    DASHSCOPE_API_KEY=your_qwen_api_key_here
    ```
4. **Run the Application**
    ```bash
    streamlit run app.py
    ```
    The application will be accessible at http://localhost:8501 by default.

---

### 📂 Project Structure
```bash
    AI-Study-Group-Copilot/
    ├── agents/                 # Agent Logic
    │   ├── base_agent.py       # Base class for Qwen interaction
    │   ├── reviewer.py         # Logic for 'Mark' (Logic Reviewer)
    │   ├── researcher.py       # Logic for 'Amy' (Researcher)
    │   └── visualizer.py       # Logic for 'Susu' (Visual Designer) - Converts text to Mermaid.js diagrams
    ├── app.py                  # Main Streamlit UI application with split-screen interface
    ├── requirements.txt        # Python dependencies
    └── .env                    # API Keys (Not included in repo)
```

### 🧠 Technical Implementation Details

- **Context Memory System:** 
  - Implements localStorage-based persistence to maintain conversation history across page reloads
  - Each agent maintains independent conversation history to preserve context
  - Automatic saving of all discussion content for continuous conversation experience
  - Clear context functionality to reset all conversation histories

- **Visual Diagram Rendering:** 
  - Uses Mermaid.js library (v8.14.0) to render interactive flowcharts and mind maps directly in the browser
  - Custom `VisualizerAgent` class that transforms text into Mermaid code with automatic chart type detection
  - Fallback mechanisms to generate default charts when model output is invalid
  - Real-time visualization with zoom and scroll capabilities in a fixed-height container
  - Debugging information display showing raw Mermaid code and validation status
  - Code sanitization to remove unwanted markdown markers from model outputs

- **Agent Specialization:** 
  - Each agent has customized prompts and processing logic tailored to their specific roles
  - `ReviewerAgent` focuses on logical structure and argumentation critique
  - `ResearcherAgent` specializes in fetching relevant data and citations
  - `VisualizerAgent` converts text content into visual representations using Mermaid.js

- **Error Handling:** 
  - Robust error handling and fallback mechanisms ensure consistent user experience even when individual components fail
  - VisualizerAgent includes multiple fallback strategies for generating valid Mermaid code
  - Input validation and sanitization for all user-provided content
  - Graceful degradation when API calls fail or return unexpected responses
  - Comprehensive exception handling with detailed logging for debugging purposes

### 🎨 VisualizerAgent Implementation Details

The `VisualizerAgent` is responsible for transforming textual content into visual diagrams using Mermaid.js syntax. Key features include:

- **Automatic Chart Type Detection:** Analyzes content structure to determine whether to generate a flowchart (`graph TD`) or mind map (`mindmap`)
- **Content Analysis:** Identifies key concepts, relationships, and hierarchical structures in the text
- **Code Sanitization:** Removes common formatting artifacts like markdown code block markers that may be included by the model
- **Validation & Fallback:** Validates generated Mermaid code and provides default diagrams when validation fails
- **Default Templates:** Includes context-aware default templates (e.g., university-related content generates education-themed mind maps)
- **Error Resilience:** Comprehensive error handling ensures that even if the model produces invalid output, a usable diagram is still generated
