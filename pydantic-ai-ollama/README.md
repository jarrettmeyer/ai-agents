# Pydantic AI with Ollama

This example runs [Pydantic AI](https://ai.pydantic.dev/) with [Ollama](https://ollama.com/) models hosted **locally**.

1. [Install Ollama](https://ollama.com/download) for your operating system.

2. Get the latest version of [llama3.2](https://ollama.com/library/llama3.2). The 3b model is 2.0 GB.
    ```bash
    ollama pull llama3.2
    ```

3. Create a `.env` file. Make any necessary changes.
    ```bash
    cp .env.example .env
    ```

4. Install required packages.
    ```bash
    pip install -r requirements.txt
    ```

5. Run the Python script.
    ```bash
    python ollama_example.py "Tell me about yourself."
    ```
