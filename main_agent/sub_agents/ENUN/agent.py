import os

from google.adk.agents import Agent
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag
from dotenv import load_dotenv

from . import prompt

load_dotenv()

enun_course_retrieval = VertexAiRagRetrieval(
    name='retrieve_enun_course_info',
    description=(
        'Use this tool to retrieve course information, prerequisites, degree requirements for Engineering (Undeclared) courses, and availble section information from the RAG corpus.'
    ),
    rag_resources=[
        rag.RagResource(

            rag_corpus=os.environ.get("ENUN_CORPUS")
        )
    ],
    similarity_top_k=20,
    vector_distance_threshold=0.6,
)

enun_agent = Agent(
    model='gemini-2.5-pro',
    name='ENUN_agent',
    instruction=prompt.ENUN_PROMPT,
    tools=[
        enun_course_retrieval,
    ]
)
