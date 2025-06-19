from agent import Agent
from tools import FakesearchTool, WeatherTool,CalculatorTool,DefineWordTool
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

calculator_tool = CalculatorTool("calculator")
fake_search_tool = FakesearchTool("fakesearch")
weather_tool = WeatherTool("weather", OPENWEATHER_API_KEY)
define_word = DefineWordTool("define_word")
AGENT.register_tool(fake_search_tool,)
AGENT.register_tool(weather_tool)
AGENT.register_tool(calculator_tool)
AGENT.register_tool(define_word)


@app.get("/ask")
async def generate(prompt: str):
    return AGENT.ask(prompt)

