# ollama chatbot

1. [Install ollama](https://ollama.com/download) for your operating system.
2. Pull the deepseek-r1:7b model from ollama. `ollama pull deepseek-r1.2:7b`
3. Make a copy of `.env.example`. `cp .env.example .env`
4. If you want to run a different model, you will need to update `LLM_MODEL` in `.env`.
5. Run the application with `streamlit run streamlit_app.py`.

## References

- [ollama-python](https://github.com/ollama/ollama-python)
