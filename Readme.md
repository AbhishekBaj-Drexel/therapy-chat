Clone the repo or copy main.py into a new directory.

Create a Python 3.10+ virtual environment:

python -m venv venv  
    source venv/bin/activate   # (or `venv\Scripts\activate` on Windows)  

Install dependencies:


    pip install chainlit openai python-dotenv


Create a .env file in the same directory with:
    OPENAI_API_KEY=sk-<your_key_here>

Run the app:

    chainlit run main.py

Tech Stack

Language: Python 3.10+

Framework: Chainlit (async chat UI)

LLM Client: Deepseek (via OpenRouter)

Env Management: python-dotenv

Hosting: local or any server that supports Python/Chainlit

Modifications to Patient Prompts

Added “Language: English. Please reply in English.” at the top of each prompt to prevent non-English output.

Removed all leading indentation inside the triple-quoted strings so there are no stray spaces.

Stripped out example/meta-instruction text that had been pasted after Aisha’s narrative—only the actual backstory, narrative, and role instructions remain.

Collapsed filler-example blocks into a single “Role” section that explicitly instructs Aisha to deflect/disclose only when asked.

Justification: Ensures the model stays in character, replies in English, and does not leak staging or meta instructions.