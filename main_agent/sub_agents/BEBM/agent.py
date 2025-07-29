import os

from google.adk.agents import Agent
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag
from dotenv import load_dotenv

from . import prompt

load_dotenv()

bebm_course_retrieval = VertexAiRagRetrieval(
    name='retrieve_bebm_course_info',
    description=(
        'Use this tool to retrieve course information, prerequisites, degree requirements for Bioengineering BS + MS courses, and availble section information from the RAG corpus.'
    ),
    rag_resources=[
        rag.RagResource(

            rag_corpus=os.environ.get("BEBM_CORPUS")
        )
    ],
    similarity_top_k=20,
    vector_distance_threshold=0.6,
)

bebm_agent = Agent(
    model='gemini-2.5-pro',
    name='BEBM_agent',
    instruction=prompt.BEBM_PROMPT,
    tools=[
        bebm_course_retrieval,
    ]
)
