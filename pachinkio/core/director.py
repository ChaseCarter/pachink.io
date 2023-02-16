from openai.embeddings_utils import cosine_similarity
import numpy

from .completion_client import CompletionClient
from .embedding_client import EmbeddingClient

class Director:

    DEFAULT_TEMP = 1.55
    completion_client: CompletionClient
    embedding_client: EmbeddingClient
    
    def __init__(self, completion_client: CompletionClient, embedding_client: EmbeddingClient):
        self.completion_client = completion_client
        self.embedding_client = embedding_client

    def compare_statements(self, statement1: str, statement2: str) -> float:
        base_embeddings = list(self.embedding_client.get_embeddings([statement1, statement2]))
        embedding1 = base_embeddings[0][0]
        embedding2 = base_embeddings[1][0]
        similarity = cosine_similarity(embedding1, embedding2)
        print(statement1, statement2, similarity)

    def interpolate_concepts(self, start_statement: str, target_statement: str, fanout: int,  iterations: int):
        base_embeddings = list(self.embedding_client.get_embeddings([start_statement, target_statement]))
        start_embedding = base_embeddings[0][0] 
        target_embedding = base_embeddings[1][0]
        print("target embedding index:", base_embeddings[1][1])
        next_statement = start_statement
        base_prompt = "Re-word this statement in a different way, for a different audience: '{0}'"
        best_similarity = cosine_similarity(start_embedding, target_embedding)
        iterations_without_progress = 0

        for i in range(iterations):
            completions = list(self.completion_client.get_completions(base_prompt.format(next_statement), n=fanout, temp=Director.DEFAULT_TEMP))
            embeddings = self.embedding_client.get_embeddings(completions)
  
            similarity_to_target = map(lambda embedding: (cosine_similarity(embedding[0], target_embedding), embedding[1]), embeddings)
            best_completion_info = max(similarity_to_target)
            if best_completion_info[0] > best_similarity:
                best_completion_index = best_completion_info[1]
                best_similarity = best_completion_info[0]
                next_statement = completions[best_completion_index]
                iterations_without_progress = 0
            else:
                iterations_without_progress += 1
                if iterations_without_progress > 4:
                    print("*** Ending run early, too many iterations without progress toward target ***")
                    print(f"*** iterations: {i}")
                    break

            print("Completions:", completions)
            print("Best: ", best_similarity, next_statement)

    def run_telephone_game(self, iterations: int):

        base_prompt = "Re-word this sentence in a slightly different way, without changing the meaning: '{0}'"
        prev_result = 'My milkshake brings all the boys to the yard.'
        for i in range(iterations):
            results = self.run_next_cycle(base_prompt.format(prev_result))
            prev_result = next(results)
            print(f"Step {i}, Prompt: {prev_result}")

    def run_next_cycle(self, prompt: str):
        results = self.completion_client.get_completions(prompt, n=1, temp=Director.DEFAULT_TEMP)
        return results