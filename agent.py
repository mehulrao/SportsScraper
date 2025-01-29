from smolagents import CodeAgent, OpenAIServerModel, Tool
import os
from dotenv import load_dotenv
from tools import NavigateTool, NavigateBackTool, ClickTool, ExtractTextTool, ExtractHyperlinksTool, GetElementsTool, CurrentPageTool

from smolagents.prompts import CODE_SYSTEM_PROMPT


modified_system_prompt = CODE_SYSTEM_PROMPT + "\nPrefer to use the browser tools rather than requests\
        or bs4. Feel free to navigate around the website if you have to."

load_dotenv()

api_key = os.getenv("KEY")

model = OpenAIServerModel(
    model_id="deepseek-chat",
    #api_base="https://api.deepseek.com",
    api_base="http://localhost:1234/v1",
    api_key=api_key,
)

agent = CodeAgent(
    tools=[NavigateTool(), NavigateBackTool(), ClickTool(), ExtractTextTool(), ExtractHyperlinksTool(), GetElementsTool(), CurrentPageTool()],
    model=model,
    add_base_tools=False,
    additional_authorized_imports=['requests', 'bs4']
)

agent.run(
        "Can you find the current stock price for apple?"
)
