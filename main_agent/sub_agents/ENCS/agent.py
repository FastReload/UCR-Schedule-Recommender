import os

from google.adk.agents import Agent
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag
from dotenv import load_dotenv

from . import prompt

load_dotenv()

encs_course_retrieval = VertexAiRagRetrieval(
    name='retrieve_encs_course_info',
    description=(
        'Use this tool to retrieve course information, prerequisites, degree requirements for Date Science coursesm, and availble section information from the RAG corpus.'
    ),
    rag_resources=[
        rag.RagResource(

            rag_corpus=os.environ.get("ENCS_CORPUS")
        )
    ],
    similarity_top_k=20,
    vector_distance_threshold=0.6,
)

encs_agent = Agent(
    model='gemini-2.5-pro',
    name='ENCS_agent',
    instruction=prompt.ENCS_PROMPT,
    tools=[
        encs_course_retrieval,
    ]
)
