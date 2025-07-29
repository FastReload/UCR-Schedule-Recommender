from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
from .sub_agents.CS import cs_agent
from .sub_agents.ME import me_agent
from .sub_agents.DS import ds_agent
from .sub_agents.ONLINE import online_agent
from .sub_agents.BEBM import bebm_agent
from .sub_agents.BIEN import bien_agent
from .sub_agents.CEN import cen_agent
from .sub_agents.CHBM import chbm_agent
from .sub_agents.CHEN import chen_agent
from .sub_agents.CNBM import cnbm_agent
from .sub_agents.CSBA import csba_agent
from .sub_agents.CSBM import csbm_agent
from .sub_agents.EEBM import eebm_agent
from .sub_agents.ELEN import elen_agent
from .sub_agents.ENBM import enbm_agent
from .sub_agents.ENEN import enen_agent
from .sub_agents.ENRB import enrb_agent
from .sub_agents.ENUN import enun_agent
from .sub_agents.MCBM import mcbm_agent
from .sub_agents.MSE import mse_agent
from .sub_agents.ENGR import engr_agent


MODEL = "gemini-2.5-pro"


schedule_recommender = LlmAgent(
    name="Schedule_Recommender",
    model=MODEL,
    description=(
        "Guide UCR students to the appropriate scheduler agent once they "
        "confirm their major. This main recommender agent helps students "
        "navigate the scheduling process by directing them to a specialized "
        "agent tailored to their academic field."
    ),
    instruction=prompt.MAIN_PROMPT,
    output_key="schedule_recommender_output",
    tools=[
        AgentTool(agent=cs_agent),
        AgentTool(agent=me_agent),
        AgentTool(agent=online_agent),
        AgentTool(agent=ds_agent),
        AgentTool(agent=bien_agent),
        AgentTool(agent=cen_agent),
        AgentTool(agent=chbm_agent),
        AgentTool(agent=chen_agent),
        AgentTool(agent=cnbm_agent),
        AgentTool(agent=bebm_agent),
        AgentTool(agent=csba_agent),
        AgentTool(agent=csbm_agent),
        AgentTool(agent=eebm_agent),
        AgentTool(agent=elen_agent),
        AgentTool(agent=enbm_agent),
        AgentTool(agent=enen_agent),
        AgentTool(agent=enrb_agent),
        AgentTool(agent=enun_agent),
        AgentTool(agent=mcbm_agent),
        AgentTool(agent=mse_agent),
        AgentTool(agent=engr_agent)
    ]
)

root_agent = schedule_recommender
