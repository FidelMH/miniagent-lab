
import json
import re
from tool import Tool
from typing import  Dict, List, Optional
import litellm
from logger import logger

class Agent:
    """Agent IA class for managing interactions with a language model."""

    def __init__(
            self,
            # LLM parameters
            provider: str = "openai", # Provider for the language model, e.g., "ollama", "openai"
            api_key: Optional[str] = None, # API key for authentication with the language model service
            model: str = "gpt-3.5-turbo", # Default model to use for completions
            api_base: Optional[str] = None, # ex. "http://localhost:11434" pour Ollama
            temperature: float = 0.7, # Temperature for controlling randomness in responses

            # Personality
            system_prompt: Optional[str] =None , # System prompt to set the agent's personality


    ) -> None:
        """Initialize the Agent with API key, model, and personality."""
        self.model = model
        self.api_base = api_base
        self.temperature = temperature
        self.system_prompt = system_prompt
        self.api_key = api_key
        self.provider = provider

        if api_key or provider != "ollama":
            litellm.api_key = self.api_key
        
        self.memory : List[Dict[str, str]] = [
            {
                "role": "system",
                "content": self.system_prompt or 
                    """
                    Tu es un assistant personnel non amical et inutile.
                    """
            }
        ]
        self.tools: Dict[str, Tool] = {}
    
    def ask(self, user_input: str) -> str:
        logger.info(f"User input: {user_input}")
        if not user_input:
            raise ValueError("User input cannot be empty.")
        self.memory.append({"role": "user", "content": user_input})
        
        while True:
            assistant_reply = self._chat()
            logger.info(f"Assistant reply: {assistant_reply}")
            print(f"Assistant reply: {assistant_reply}")
            self.memory.append({"role": "assistant", "content": assistant_reply})
            if "Final Answer:" in assistant_reply:
                logger.info("Final answer detected in the response.")
                # If the response contains "Final Answer:", we assume it's the end of the conversation
                return assistant_reply.split("Final Answer:")[-1].strip()
            json_blob = self._extract_json(assistant_reply)
            if not json_blob:
                raise ValueError("No valid JSON found in the response.")
            # If a JSON blob is found, we execute the tool
            try:
                result = self.execute_tool(json_blob)
                logger.info(f"Tool execution result: {result}")
                self.memory.append({"role": "system", "content": f"Observation: {result}"})
            except ValueError as e:
                # If the tool execution fails, we continue the conversation
                self.memory.append({"role": "error", "content": str(e)})
                continue
  

    def _chat(self) -> str:
        kwargs = {
            "model": self.model,
            "messages": self.memory,
            "temperature": self.temperature,
            "stop": ["Observation:"]
        }
        
        if self.api_base:
            kwargs["base_url"] = self.api_base
        if self.api_key and self.provider != "ollama":
            kwargs["api_key"] = self.api_key
        if self.provider:
            kwargs["provider"] = self.provider
        response = litellm.completion(**kwargs)
        return response["choices"][0]["message"]["content"] # type: ignore[no-any-return]
    
    def register_tool(self, tool):
        """Register an external tool for the agent to use."""
        
        self.tools[tool.name] = tool
    def execute_tool(self, data) -> str:
        """Execute a registered tool with the given arguments."""
        action:str = data.get("action") 
        args = data.get("action_input", "")
        if action in self.tools:
            return self.tools[action].run(args)
        else:
            raise ValueError(f"Tool '{action}' not found.")
        
    def _extract_json(self, text: str) -> Optional[dict]:
        match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                return None
        return None
