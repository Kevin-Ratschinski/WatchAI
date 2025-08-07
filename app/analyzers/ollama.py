import ollama


class OllamaAnalyzer:
    def __init__(self, config):
        self.ollama_host = config.ollama.host
        self.ollama_model = config.ollama.model
        print(
            f"OllamaAnalyzer initialized with Host: {self.ollama_host}, Model: {self.ollama_model}")

    def analyze(self, prompt: str, image: str | None = None, data: str | None = None) -> str:
        """Sends data and prompt to Ollama and returns the response."""
        print("OllamaAnalyzer: Sending request to Ollama...")
        analyze_str = f"{prompt}\n{data}" if data else prompt
        try:
            response = ollama.generate(model=self.ollama_model, prompt=analyze_str, images=[
                image] if image else [], stream=False)
            print("OllamaAnalyzer: Response received from Ollama.")
            return response.get('response', 'No response from LLM received.')
        except ollama.RequestError as e:
            print(f"Error in Ollama request: {e}")
            return f"Error in Ollama request: {e}"
        except ollama.ResponseError as e:
            print(f"Error in Ollama response: {e}")
            return f"Error in Ollama response: {e}"
