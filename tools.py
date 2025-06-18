from tool import Tool
import requests
import ast
import operator


SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
    ast.FloorDiv: operator.floordiv,
}


def safe_eval(expr: str):
    """Safely evaluate a simple arithmetic expression."""

    def _eval(node):
        if isinstance(node, ast.Num):  # type: ignore[attr-defined]
            return node.n
        if isinstance(node, ast.BinOp) and type(node.op) in SAFE_OPERATORS:
            return SAFE_OPERATORS[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in SAFE_OPERATORS:
            return SAFE_OPERATORS[type(node.op)](_eval(node.operand))
        raise ValueError("Unsupported expression")

    tree = ast.parse(expr, mode="eval")
    return _eval(tree.body)



class GoogleSearchTool(Tool):
    """Tool for performing Google searches."""
    def __init__(self, name: str, api_key: str, cse_id: str):
        super().__init__(name)
        self.name = name
        self.api_key = api_key
        self.cse_id = cse_id
    def run(self, args: str) -> list:
        """Perform a Google search with the given arguments."""
        response = requests.get(

            url="https://www.googleapis.com/customsearch/v1",
            params={
                "key": self.api_key,
                "cx": self.cse_id,
                "q": args
            }
        )
        if response.status_code != 200:
            raise Exception(f"Google search failed with status code {response.status_code}: {response.text}")
        data = response.json()
        if "items" not in data: 
            return []
        items = data["items"]
        results = []
        for item in items:
            title = item.get("title", "No title")
            link = item.get("link", "No link")
            snippet = item.get("snippet", "No snippet")
            results.append({"title": title, "link": link, "snippet": snippet})
        return results


class CalculatorTool(Tool):
    """Tool for performing basic arithmetic operations."""
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name

    def run(self, expr: str) -> str:
        """
        Perform a calculation based on the provided arguments.
        Args:
            expr (str): The expression to evaluate, e.g., "2 + 2" or "3 * (4 - 1)".
        """
        try:
            result = safe_eval(expr)
            return str(result)
        except Exception as e:
            raise Exception(f"Calculation failed: {str(e)}")

class FakesearchTool(Tool):
    """Tool for performing fake searches."""
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name

    def run(self, args: dict) -> str:
        """
        Return a fake search result.
        Args:
            query (str): The search query.
        """
        query = args.get("query", "")
        if not query:
            return "No query provided for fake search."
        if 'capital of france' in query.lower():
            return "The capital of France is Paris."
        if 'bocchi the rock' in query.lower():
            return "Bocchi the Rock is a popular anime about a girl who struggles with social anxiety but finds friends "
        return "No results found for your query."

class WeatherTool(Tool):
    """Tool for fetching weather information."""
    def __init__(self, name: str, api_key: str):
        super().__init__(name)
        self.name = name
        self.api_key = api_key

    def run(self, args):
        """Fetch the current weather for the given location.

        Args:
            args (str | dict): Either the location as a string or a dictionary
                containing a ``location`` field.
        """
        if isinstance(args, dict):
            location = args.get("location", "")
        else:
            location = args
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": location,
                "appid": self.api_key,
                "units": "metric"  # Use metric units for temperature
            }

        )
        if response.status_code != 200:
            raise Exception(f"Weather API request failed with status code {response.status_code}: {response.text}")
        data = response.json()
        return f"The current temperature in {location} is {data['main']['temp']}°C with {data['weather'][0]['description']}."
