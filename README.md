# Getting-Started-with-Agents

## ADK Tutorial Overview

The Agent Development Kit (ADK) is Google's framework for building AI agents with Gemini models. Key concepts covered:

### Simple Agents
- Basic building blocks that wrap LLMs with instructions and personality
- Stateful by default, maintaining conversation context

### Agents with Tools
- Tools allow agents to perform actions beyond their knowledge cutoff
- Built-in tools (google_search, code_execution) extend agent capabilities
- Custom function tools enable domain-specific actions

### Multi-Modal Agents
- Can process and respond to both text and images
- Combine visual analysis with text-based tools

### Agent Teams
- Root agents orchestrate specialists (sub-agents)
- Each sub-agent focuses on specific tasks
- Enables modular, reusable agent components

### Sequential Agents
- Process steps in a defined order (pipeline)
- Each agent receives the previous agent's output

### Parallel Agents
- Run multiple sub-agents concurrently for speed
- Useful for independent tasks that can be performed simultaneously

## CultureLens Streamlit Application

The Streamlit app applies ADK concepts to create a cultural artifact analyzer:

### Implementation Details
- Uses a SequentialAgent architecture with three specialists:
  1. artifact_recognition_agent: Identifies items from images
  2. historical_context_agent: Provides historical background
  3. cultural_significance_agent: Explains cultural meaning

### Features
- Accepts image uploads of cultural artifacts
- Processes images with multi-modal capabilities
- Uses Google Search tool for up-to-date information
- Presents analysis in an organized web interface

### How to Run
1. Ensure environment variables are set (GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION)
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`

The application demonstrates how ADK concepts can be applied to create practical, multi-modal AI applications with specialised agents working together.
