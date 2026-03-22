# Agent Learning Journey

## Sprint 1: Agent Fundamentals

### Week 1: Calculator Agent

A multi-tool agent that understands math questions and uses a calculator tool to solve them.

**Features:**
- Extracts math operations from natural language
- Chains multiple tool calls for complex problems
- Handles errors gracefully (division by zero)
- Full conversation history maintained

**How to Run:**
```bash
source venv/bin/activate
python3 calculator_agent.py
```

**Example:**
- Input: "What is 100 + 50, then divide by 3?"
- Agent calls: add(100, 50) → 150
- Agent calls: divide(150, 3) → 50
- Output: "The answer is 50"

**Key Learnings:**
- Agents decide which tools to use based on understanding
- Tool definitions tell Claude what's available
- Message history allows Claude to track context
- Multiple tool calls are chained together

**Next:**
- Add weather tool
- Explore advanced patterns
- Build production-quality agents
