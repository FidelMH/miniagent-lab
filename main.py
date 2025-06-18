from agent import Agent
from tools import FakesearchTool, WeatherTool
from fastapi import FastAPI
from config import OPENWEATHER_API_KEY
import yaml
app = FastAPI()

model = "ollama/gemma3"
base_url = "http://localhost:11434"

# Load system prompt from prompts.yaml file
with open("prompts.yaml", "r",encoding="utf-8") as file:
    system_prompt:str = yaml.safe_load(file)["system_prompt"]
AGENT = Agent( 
    model=model,
    api_base=base_url,
    system_prompt=system_prompt,
    provider="ollama",
)

 
fake_search_tool = FakesearchTool("fakesearch")
weather_tool = WeatherTool("weather", OPENWEATHER_API_KEY)

AGENT.register_tool(fake_search_tool,)
AGENT.register_tool(weather_tool)


@app.get("/ask")
def generate(prompt: str):
    """
    Generate a response based on the provided prompt.
    """ 
     
    return AGENT.ask(prompt) 

