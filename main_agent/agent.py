from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
import os
from .sub_agents.CS import cs_agent
from .sub_agents.ME import me_agent
from .sub_agents.ONLINE import online_agent
from google.adk.tools import FunctionTool
from google.cloud import bigquery
from dotenv import load_dotenv



MODEL = "gemini-2.5-pro"

load_dotenv()

client = bigquery.Client()

def student_data_retrieval(student_id: str) -> str:
    """
    Retrieves student information from BigQuery based on student ID.

    Args:
        student_id: The ID of the student to search for.

    Returns:
        A formatted string containing the student information, or a message if not found.
    """
    
    table_id = os.environ.get("BIGQUERY_STUDENT_INFO_TABLE", "ucr-student-schedule-recommend.course_demand.student_course_history")
    if not table_id:
        return "Error: BigQuery table ID for student data not configured. Please set BIGQUERY_STUDENT_INFO_TABLE in your .env file."

    student_info_query = f"""
        SELECT Student_UID, PROGRAM_LEVEL_DESC, FIRST_MAJOR_CODE, SECOND_MAJOR_CODE
        FROM `{table_id}`
        WHERE Student_UID = FROM_BASE64('{student_id}')
        LIMIT 1
    """

    # courses student completed + grades, academic standing (number quarters attending), credits
    student_class_query = f"""
        SELECT TERM_CODE, COURSE_ID, COURSE_CREDITS, FINAL_GRADE
        FROM `{table_id}`
        WHERE Student_UID = FROM_BASE64('{student_id}')
        AND COURSE_CREDITS > 0
        AND FINAL_GRADE != "W"
        GROUP BY TERM_CODE, COURSE_ID, FINAL_GRADE, COURSE_CREDITS
        LIMIT 200
    """
    
    try:
        class_query_job = client.query(student_class_query)
        class_results = class_query_job.result()

        output = []
        total_credits = 0
        if class_results.total_rows == 0:
            output.append("No class information found for the specified student ID.")
        else:
            for row in class_results:
                output.append(f"Class ID: {row.COURSE_ID}\n"
                              f"Credits: {row.COURSE_CREDITS}\n"
                              f"Final Grade: {row.FINAL_GRADE}\n"
                              f"Term Code: {row.TERM_CODE}\n")
                total_credits += row.COURSE_CREDITS

        query_job = client.query(student_info_query)
        results = query_job.result()
        
        if results.total_rows == 0:
            return f"No student information found for student ID: {student_id}."
        
        for row in results:
            output.append(f"Student ID: {row.Student_UID}\n"
                          f"Program Level: {row.PROGRAM_LEVEL_DESC}\n"
                          f"First Major: {row.FIRST_MAJOR_CODE}\n"
                          f"Second Major: {row.SECOND_MAJOR_CODE}\n"
                          f"Total Credits Completed: {total_credits}\n")
        if total_credits < 45:
            output.append("Standing: Freshman\n")
        elif total_credits >= 45 and total_credits < 90:
            output.append("Standing: Sophomore\n")
        elif total_credits >= 90 and total_credits < 135:
            output.append("Standing: Junior\n")
        else:
            output.append("Standing: Senior\n")

    except Exception as e:
        return f"Error retrieving student information: {e}"
    
    return "Found the following student information:\n" + "\n".join(output)


student_data_tool = FunctionTool(func=student_data_retrieval)


schedule_recommender = LlmAgent(
    name="Schedule_Recommender",
    model=MODEL,
    description=(
        "Guide UCR students to the appropriate scheduler agent once they "
        "confirm their major or student ID. This main recommender agent helps students "
        "navigate the scheduling process by directing them to a specialized "
        "agent tailored to their academic field."
    ),
    instruction=prompt.MAIN_PROMPT,
    output_key="schedule_recommender_output",
    tools=[
        AgentTool(agent=cs_agent),
        AgentTool(agent=me_agent),
        AgentTool(agent=online_agent),
        student_data_tool
    ]
)

root_agent = schedule_recommender