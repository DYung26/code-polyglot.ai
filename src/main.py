from src.ai.engine import AIEngine
import click
import os
from src.gdocs.engine import GoogleDocsEngine
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

def load_module(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

@click.command()
@click.argument('module_path', type=click.Path(exists=True))
@click.option(
    '--current-language', '-c',
    type=click.Choice(['cpp', 'csharp', 'go', 'js', 'javascript', 'python', 'php', 'java'], case_sensitive=False),
    required=True,
    help='The source language of the code snippets'
)
@click.option(
    '--target-languages', '-t',
    type=click.Choice(['cpp', 'csharp', 'go', 'js', 'javascript', 'python', 'php', 'java'], case_sensitive=False),
    multiple=True,
    default=['python'],
    show_default=True,
    help='Target languages(s) to convert to: go, csharp, cpp, etc. Can be used multiple times.'
)
@click.option(
    '--action', '-a',
    type=click.Choice(['translate', 'instruct'], case_sensitive=False),
    multiple=True,
    default=['translate'],
    show_default=True,
    help='Target languages(s) to convert to: go, csharp, cpp, etc. Can be used multiple times.'
)
@click.option(
    '--doc-id', type=str, default=None,
    help='Google Docs ID to publish comments'
)
def cli(module_path, current_language, target_languages, action, doc_id):
    content = load_module(module_path)
    ai = AIEngine()

    text_to_insert = ""
    if action[0] == "translate":
        translated = ai.translate_module(content, current_language, target_languages)
        text_to_insert = translated
        # print(translated)
    elif action[0] == "instruct":
        instructed = ai.instruction_module(content, current_language, target_languages)
        text_to_insert = instructed

    service_account_file = str(os.getenv("SERVICE_ACCOUNT_FILE_PATH"))
    gdocs = GoogleDocsEngine(service_account_file, doc_id)

    if doc_id:
        gdocs.insert_text(text_to_insert)
        click.echo(f"Document published to Docs ID: {doc_id}")
    else:
        click.echo("\n### Translations:\n")
        click.echo(text_to_insert)


if __name__ == "__main__":
    cli()
