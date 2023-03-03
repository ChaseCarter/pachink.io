from injector import inject
from openai.embeddings_utils import cosine_similarity

from .completion_client import CompletionClient
from .embedding_client import EmbeddingClient
from .prompts import Prompts

class Director:

    DEFAULT_TEMP = 1.3
    completion_client: CompletionClient
    embedding_client: EmbeddingClient
    
    @inject
    def __init__(self, completion_client: CompletionClient, embedding_client: EmbeddingClient, prompts: Prompts) -> None:
        self.completion_client = completion_client
        self.embedding_client = embedding_client
        self.prompts = prompts
        print("Initializing Director")

    def chain_of_intuition(self, query: str, fanout: int = 1, prompt_override = False) -> None:
        
        if prompt_override:
            prompt = query
        else:
            prompt = self.prompts.COI_base_prompt.format(query)
        print("Prompt:", prompt)

        while True:
            completions = list(self.completion_client.get_completions(prompt, n=fanout, temp=Director.DEFAULT_TEMP, stop=">>> "))
            for i, completion in enumerate(completions):
                print(f"({i}): {completion}")
            selected_index = input()
            if selected_index.isdigit():
                chosen_completion = completions[int(selected_index)]
            elif selected_index == "exit":
                print("Exiting chain of intuition")
                break
            elif selected_index == "":
                # TODO: don't modify prompt 
                pass
            else:
                chosen_completion = selected_index

            prompt = prompt + chosen_completion + ", \n>>> "
            print("Next Prompt:", prompt)

    def compare_statements(self, statement1: str, statement2: str) -> float:
        base_embeddings = list(self.embedding_client.get_embeddings([statement1, statement2]))
        embedding1 = base_embeddings[0][0]
        embedding2 = base_embeddings[1][0]
        similarity = cosine_similarity(embedding1, embedding2)
        print(statement1, statement2, similarity)
        return similarity

    # Returns (list[(step_result, similarity-to-original)], temination-reason)
    def interpolate_concepts(self, start_statement: str, target_statement: str, fanout: int,  iterations: int) -> tuple[list[tuple[str, float]], str]:
        base_embeddings = list(self.embedding_client.get_embeddings([start_statement, target_statement]))
        start_embedding = base_embeddings[0][0] 
        target_embedding = base_embeddings[1][0]
        print("target embedding index:", base_embeddings[1][1])
        next_statement = start_statement
        best_similarity = cosine_similarity(start_embedding, target_embedding)
        iterations_without_progress = 0
        temp = Director.DEFAULT_TEMP
        results = [(start_statement, best_similarity)]
        termination_reason = "finished"

        for i in range(iterations):
            print("Temp:", temp)
            completions = list(self.completion_client.get_completions(self.prompts.interpolate_concepts_base_prompt.format(next_statement), n=fanout, temp=temp))
            embeddings = self.embedding_client.get_embeddings(completions)
  
            similarity_to_target = map(lambda embedding: (cosine_similarity(embedding[0], target_embedding), embedding[1]), embeddings)
            best_completion_info = max(similarity_to_target)
            if best_completion_info[0] > best_similarity:
                best_completion_index = best_completion_info[1]
                best_similarity = best_completion_info[0]
                next_statement = completions[best_completion_index]
                iterations_without_progress = 0
                temp = max(Director.DEFAULT_TEMP, temp * 0.9)
                results.append((completions[best_completion_index], best_similarity))
            else:
                iterations_without_progress += 1
                temp = min(temp * 1.1, 2.0)
                if iterations_without_progress > 5:
                    termination_reason = "slow progress"
                    print("*** Ending run early, too many iterations without progress toward target ***")
                    print(f"*** iterations: {i}")
                    break

            print("Completions:", completions)
            print("Best: ", best_similarity, next_statement)
        
        return (results, termination_reason)

    def run_telephone_game(self, statement: str, iterations: int = 2, temperature: float = DEFAULT_TEMP) -> list[str]:

        prev_result = statement
        step_results = [prev_result]
        for i in range(iterations):
            results = self.completion_client.get_completions(self.prompts.telephone_base_prompt.format(prev_result), n=1, temp=temperature)
            prev_result = next(results)
            step_results.append(prev_result)
            print(f"Step {i}, Prompt: {prev_result}")
        
        return step_results
