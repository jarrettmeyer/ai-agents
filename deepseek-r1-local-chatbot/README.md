# Deepseek-R1 Local Chatbot

1. [Install ollama](https://ollama.com/download) for your operating system.

2. Pull the [deepseek-r1:7b](https://ollama.com/library/deepseek-r1) model from ollama. This model is 4.7 GB. If you have a slow internet connection, you can try a smaller model.
    ```bash
    ollama pull deepseek-r1:7b
    ```

3. Run the ollama server.
    ```bash
    ollama serve
    ```

4. Install Python packages.
    ```bash
    pip install -r requirements.txt
    ```

5. Make a copy of `.env.example`. Make updates to this file as needed.
    ```bash
    cp .env.example .env
    ```

6. Run the application.
    ```bash
    streamlit run streamlit_app.py
    ```

## Links and References

- [ollama-python](https://github.com/ollama/ollama-python)
