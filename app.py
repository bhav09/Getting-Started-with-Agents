import os
import streamlit as st
import asyncio
import base64
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools import google_search
from google.genai import types
import vertexai

# Load environment variables
load_dotenv()
PROJECT_ID  = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION    = os.getenv("GOOGLE_CLOUD_LOCATION")
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
MODEL_GEMINI_FLASH = 'gemini-2.0-flash'

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Define Agents
artifact_recognition_agent = Agent(
    model=MODEL_GEMINI_FLASH,
    name="artifact_recognition_agent",
    description="Identifies cultural artifacts from images.",
    instruction="Identify the cultural artifact in the image.",
    tools=[google_search],
    generate_content_config=types.GenerateContentConfig(
        max_output_tokens=512,
        temperature=0.2,
        top_p=0.95,
    ),
)

historical_context_agent = Agent(
    model=MODEL_GEMINI_FLASH,
    name="historical_context_agent",
    description="Provides historical background of the artifact.",
    instruction="Provide historical context for the identified artifact.",
    tools=[google_search],
    generate_content_config=types.GenerateContentConfig(
        max_output_tokens=1024,
        temperature=0.2,
        top_p=0.95,
    ),
)

cultural_significance_agent = Agent(
    model=MODEL_GEMINI_FLASH,
    name="cultural_significance_agent",
    description="Explains the cultural significance of the artifact.",
    instruction="Explain the cultural significance of the artifact.",
    tools=[google_search],
    generate_content_config=types.GenerateContentConfig(
        max_output_tokens=1024,
        temperature=0.2,
        top_p=0.95,
    ),
)

# Root Agent
root_agent = Agent(
    model=MODEL_GEMINI_FLASH,
    name="culture_explorer_agent",
    description="Explores cultural artifacts through images.",
    instruction="""
    1. Use artifact_recognition_agent to identify the artifact from the image.
    2. Use historical_context_agent to provide background information.
    3. Use cultural_significance_agent to explain its cultural importance.
    """,
    sub_agents=[
        artifact_recognition_agent,
        historical_context_agent,
        cultural_significance_agent,
    ],
)

# Session Service and Runner
APP_NAME = "culture_explorer_app"
USER_ID = "user_1"
SESSION_ID = "session_1"

session_service = InMemorySessionService()
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

# Streamlit Interface
st.title("🌍 CultureLens")
st.write("Upload an image of a cultural artifact to learn about its history and significance.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
    if st.button("Analyze Artifact"):
        image_bytes = uploaded_file.read()
        image_b64 = base64.b64encode(image_bytes).decode()

        async def process_image():
            parts = [types.Part(text="Analyze this cultural artifact.")]
            parts.append(types.Part.from_bytes(data=image_bytes, mime_type="image/png"))
            content = types.Content(role="user", parts=parts)

            await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)

            async for ev in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
                if ev.is_final_response() and ev.content and ev.content.parts:
                    st.markdown("### 🖼️ Identified Artifact")
                    st.write(ev.content.parts[0].text)
                    # Additional sections for historical context and cultural significance can be added here
                    break

        asyncio.run(process_image())