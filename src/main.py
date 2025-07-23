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
@click.option('--languages', '-l', multiple=True, default=['go', 'csharp', 'cpp'],
              help='Target languages: go, csharp, cpp, etc.')
@click.option('--doc-id', type=str, default=None,
              help='Google Docs ID to publish comments')
def cli(module_path, languages, doc_id):
    content = load_module(module_path)
    ai = AIEngine()
    translated = ai.translate_module(content, languages)
    print(translated)

    service_account_file = str(os.getenv("SERVICE_ACCOUNT_FILE_PATH"))
    gdocs = GoogleDocsEngine(service_account_file, doc_id)

    if doc_id:
        gdocs.insert_text(translated)
        click.echo(f"Comments published to Docs ID: {doc_id}")
    else:
        click.echo("\n### Translations:\n")
        click.echo(translated)


if __name__ == "__main__":
    cli()
