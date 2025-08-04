import os

from google.adk.agents import Agent
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag
from dotenv import load_dotenv

from . import prompt

load_dotenv()

enen_course_retrieval = VertexAiRagRetrieval(
    name='retrieve_enen_course_info',
    description=(
        'Use this tool to retrieve course information, prerequisites, degree requirements for Environmental Engineering courses, and availble section information from the RAG corpus.'
    ),
    rag_resources=[
        rag.RagResource(

            rag_corpus=os.environ.get("ENEN_CORPUS")
        )
    ],
    similarity_top_k=20,
    vector_distance_threshold=0.6,
)

enen_agent = Agent(
    model='gemini-2.5-pro',
    name='ENEN_agent',
    instruction=prompt.ENEN_PROMPT,
    tools=[
        enen_course_retrieval,
    ]
)
