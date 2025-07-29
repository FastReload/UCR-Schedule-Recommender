

"""CS scheduling agent using RAG for course information."""

import os

from google.adk.agents import Agent
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag
from dotenv import load_dotenv

from . import prompt

load_dotenv()

cs_course_retrieval = VertexAiRagRetrieval(
    name='retrieve_cs_course_info',
    description=(
        'Use this tool to retrieve course information, prerequisites, and degree requirements for CS courses from the RAG corpus.'
    ),
    rag_resources=[
        rag.RagResource(
            rag_corpus=os.environ.get("CS_CORPUS")
        )
    ],
    similarity_top_k=20,
    vector_distance_threshold=0.6,
)

cs_agent = Agent(
    model='gemini-2.5-pro',
    name='CS_agent',
    instruction=prompt.CS_PROMPT,
    tools=[
        cs_course_retrieval,
    ]
)
