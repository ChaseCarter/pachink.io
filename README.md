# Pachink.io
A toy app for using structured prompts with language models. Currently configured to use the OpenAI API, but other LLMs could be integrated with different implementations of `CompletionClient` and `EmbeddingClient`. 

## Flows
* **Telephone Game**: Iteratively re-word the given *statement*, like in the children's game 'Telephone'. 
    * This is interesting as a proxy for how rumors can evolve.
    * Also demonstrates how some semantic information can be safely mutated whereas other information (like proper names) is permantently lost if it is omitted from a single step of the chain.
* **Interpolate Concepts**: Atempt to evolve from *start_statement* to *target_statement* by iteratively re-wording the statement and choosing the completion with the closest embedding to the *target_statement* embedding. 
    * Current implementation doesn't work as well as I'd hoped due to the fact that non-conceptual things like sentence structure are also encoded in the embeddings. This makes raw embedding similarity an insufficient proxy for conceptual similiarity, at least for use in a naive selection process as implemented. To get the behavior I was looking for would probably require isolating various axes in embedding space which more closely reflect the conceptual axes I want to interpolate across.
* **Chain of Intuition**:  Similar to Chain of Thought prompting, performs Chain of Intuition prompting attempting to answer the query in discrete steps. At each step, multiple completions are presented to choose from, then the user picks one or writes their own. *(Currently only implemented for use in console)*.
    * The core idea here is that what LLMs do when generating completions is more akin to intuition than thought. So rather than try to force the process into the mold of cleanly defined and logically connected 'thoughts', allow more leeway for the LLM to explore it's space of word-associations. 
    * In practice this will tend to quickly devolve into absurdity, so COI is implemented here as a collaborative process shared by the user and the LLM, roughly in the spirit of [Loom](https://github.com/socketteer/loom).

See `Pachinki.io.postman_collection.json` for example API calls.

##  Setup
* Activate virtual environment from `requirements.txt`.
* Create a `.env` file and populate with your OpenAI API account info, e.g.: 
    ```
    [open-ai]
    organization-id=<OpenAI API org-id>
    api-key=<OpenAI API api-key>
    engine=text-davinci-003
    ```
* **Unit Tests**:
    * Create a `test.env` file mirroring the `.env` file above, but can use a different engine (such as `text-babbage-001`, for example) for cheaper runs.
    * Run unit tests with `pytest -s tests`.
* **Running**:
    * To start Flask API in dev mode, run `python app.py`.
    * Alternatively, run directly, without Flask, with `python main.py`; this additionally enables Chain of Intuition mode, which is not exposed in the API.
* **Prompts**:
    * To change base-prompts, either modify the prompts in `pachinkio.prompts.prompts_v1.ini`,
    or create a new version of the prompts.ini and point to it when initializing `PromptsModule` (see `app.py`).

