import os

from google.adk.agents import Agent
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag
from dotenv import load_dotenv

from . import prompt

load_dotenv()

ds_course_retrieval = VertexAiRagRetrieval(
    name='retrieve_ds_course_info',
    description=(
        'Use this tool to retrieve course information, prerequisites, degree requirements for Data Science courses, and availble section information from the RAG corpus.'
    ),
    rag_resources=[
        rag.RagResource(

            rag_corpus=os.environ.get("DS_CORPUS")
        )
    ],
    similarity_top_k=20,
    vector_distance_threshold=0.6,
)

ds_agent = Agent(
    model='gemini-2.5-pro',
    name='DS_agent',
    instruction=prompt.DS_PROMPT,
    tools=[
        ds_course_retrieval,
    ]
)
