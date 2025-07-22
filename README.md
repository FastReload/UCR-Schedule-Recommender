
# 📅 UCR Schedule Recommender

A modular, multi-agent recommendation system designed to assist undergraduate students at the University of California, Riverside (UCR) in planning their class schedules. Built using Google's Agent Development Kit (ADK), this tool provides tailored course guidance based on the student’s major, year, and completed coursework.

---

## 🚀 Features

- 🔍 **Multi-agent architecture**: Root agent delegates scheduling tasks to sub-agents based on the student's major (e.g., CS, ME).
- 📚 **Major-specific subagents**: Supports domain-specific course planning logic for Computer Science (CS) and Mechanical Engineering (ME).
- 🌐 **Online resource agent**: Fetches professor reviews and external academic resources.
- 🧠 **Prompt-driven reasoning**: Each agent includes a structured prompt to drive decision-making and interaction flow.
- 🛠️ **Configurable & scalable**: Easily extendable to other majors and schools using the same agent design.

---

## 🧩 Project Structure

```
UCR_Schedule_Recommender/
│
├── pyproject.toml          # Project dependencies and settings
├── poetry.lock             # Locked dependency versions
├── .env                    # Environment variables (API keys, etc.)
│
├── Root_Agent/
│   ├── agent.py            # Root agent logic: delegates to sub-agents
│   ├── prompt.py           # Root agent prompt template
│   └── sub_agents/
│       ├── CS/
│       │   ├── agent.py    # CS-specific scheduling logic
│       │   └── prompt.py   # CS-specific system prompt
│       ├── ME/
│       │   ├── agent.py    # ME-specific scheduling logic
│       │   └── prompt.py   # ME-specific system prompt
│       └── ONLINE/
│           ├── agent.py    # Online resource agent (reviews, external tools)
│           └── prompt.py   # ONLINE-specific prompt
```

---

## 🧠 How It Works

1. **Root Agent** receives user input about their major, academic year, and goals.
2. **Delegation**: Based on the major (e.g., CS or ME), control is passed to a specialized sub-agent.
3. **Sub-Agent** processes the input, filters course offerings, and recommends an optimal schedule using a major-specific prompt template.
4. **ONLINE Agent** handles requests for professor reviews, external academic tools, or supplemental resources.
5. **Response** is returned to the user through the Root Agent interface.

---

## 🛠️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/UCR_Schedule_Recommender.git
cd UCR_Schedule_Recommender/UCR_Schedule_Recommender
```

### 2. Install dependencies
```bash
poetry install
```

### 3. Add your environment variables
Create a `.env` file with the required API keys (e.g., for ADK and Gemini):
```
GEMINI_API_KEY=your_key
ADK_PROJECT_ID=your_project_id
```

### 4. Run the agent
```bash
adk run rag
```

---

## 🧪 Example Use

```python
from Root_Agent.agent import ScheduleRecommenderAgent

agent = ScheduleRecommenderAgent()
response = agent.run({
    "major": "CS",
    "year": "Sophomore",
    "term": "Fall",
    "completed_courses": ["CS010A", "CS010B"]
})
print(response)
```

---

## 🧱 Built With

- [Google Agent Development Kit (ADK)](https://github.com/google/agent-development-kit)
- Python 3.11+
- [Poetry](https://python-poetry.org/) for dependency management

---

## 📈 Future Enhancements

- Add support for additional majors (e.g., Business, Biology)
- Integrate professor/course reviews from external sources
- Frontend chatbot interface (Streamlit / React)
- Course prerequisite validation using historical data

