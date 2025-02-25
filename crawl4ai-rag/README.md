# crawl4ai-rag

This project uses RAG to answer questions about web pages.

- [crawl4ai.com](https://crawl4ai.com/mkdocs/) is a LLM-friendly web crawler. It converts web pages into human and machine-readable markdown.
- [Pydantic AI](https://ai.pydantic.dev/) is a model-agnostic library for GenAI app development.
- [Supabase](https://supabase.com/docs) is an open source Firebase alternative built on top of PostgreSQL.

## Instructions

### Supabase

Install [Supabase for local development](https://supabase.com/docs/guides/local-development/cli/getting-started).

```bash
# Create a new local project.
supabase init

# Launch services.
supabase start
```

Once your Supabase project is running, you can access the Studio panel at [localhost:54323](http://localhost:54323/). From the Studio, open the SQL Editor. Run the script `create_site_pages.sql`. This script will create the `site_pages` table and a `match_site_pages` function.

### OpenAI API Keys

Generate a new API key from the OpenAI dashboard. Add this OpenAI key to the `.env` file.

### Run the app

```bash
# Install requirements.
pip install -r requirements.txt

# Install playwright headless browser.
playwright install

# Create a new .env file.
# Make changes to the .env file as needed.
cp .env.example .env

# Run the crawler to populate the database.
python crawl_site_pages.py

# Run the Streamlit app.
streamlit run streamlit_app.py
```
