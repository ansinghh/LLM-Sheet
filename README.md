# LLM-Sheet: Talk to Your Data with Natural Language

**LLM-Sheet** is a command-line tool that lets you upload CSVs and query your data using everyday language — powered by GPT-4 and SQLite.

No need to remember SQL syntax. Just ask:

> “Give me all the customers from Boston.”  
> “Add a product called ‘Flux Capacitor’ priced at $299.”  
> “Which employee joined after 2022?”

---

## Features

- Upload any `.csv` file and auto-create tables in SQLite
- Run natural language queries powered by GPT-4
- Dynamic schema extraction for query generation
- Smart handling of inserts, updates, and selects
- Unit-tested with GitHub Actions CI
- API key stored securely using `.env` in the root folder

---

## How It Works

1. **Upload CSVs** — The CLI lists and ingests CSVs into a SQLite database.
2. **Ask questions** — You enter a natural language query.
3. **AI generates SQL** — The model uses schema info to generate a compatible SQL command.
4. **View Results** — The query is executed, and results are shown instantly.

---

## Installation

Clone the repo and install the dependencies:

```bash
git clone https://github.com/ansinghh/LLM-Sheet.git
cd LLM-Sheet
pip install -r requirements.txt
