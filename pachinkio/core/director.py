from .completion_client import CompletionClient

class Director:

    completion_client: CompletionClient
    
    def __init__(self, completion_client: CompletionClient):
        self.completion_client = completion_client

    def run_cycles(self, n: int):

        base_prompt = "Re-word this sentence in a slightly different way, without changing the meaning: '{0}'"
        prev_result = 'Chloe accused Joe of minor voyeurism.'
        for i in range(n):
            results = self.run_next_cycle(base_prompt.format(prev_result))
            prev_result = next(results)
            print(f"Step {i}, Prompt: {prev_result}")

    def run_next_cycle(self, prompt: str):
        results = self.completion_client.get_completions(prompt, n=1, temp=0.9)
        return results