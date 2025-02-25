# crawl4ai-rag

- [crawl4ai.com](https://crawl4ai.com/mkdocs/) is a LLM-friendly web crawler. It converts web pages into human and machine-readable markdown.
- [Pydantic AI](https://ai.pydantic.dev/) is a model-agnostic library for GenAI app development.

## Instructions

Install [Supabase for local development](https://supabase.com/docs/guides/local-development/cli/getting-started).

```bash
# Create a new local project.
supabase init

# Launch services.
supabase start
```

Once your Supabase project is running, you can access the Studio panel at [localhost:54323](http://localhost:54323/). From the Studio, open the SQL Editor. Run the script `create_site_pages.sql`. This script will create the `site_pages` table and a `match_site_pages` function.

```bash
# Install requirements.
pip install -r requirements.txt

# Install playwright headless browser.
playwright install

# Run the crawler to populate the database.
python crawl_site_pages.py

# Run the Streamlit app.
streamlit run streamlit_app.py
```
