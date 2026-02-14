"""DevKB Snippets - Code Snippet Manager"""
import json
import os
import sqlite3
from pathlib import Path

import click
from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table

console = Console()
DB_PATH = os.getenv("DATABASE_PATH", "./data/snippets.db")


def get_db():
    """Get database connection"""
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS snippets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL,
            language TEXT,
            title TEXT,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


@click.group()
def cli():
    """DevKB Snippets - Manage code snippets"""
    init_db()


@cli.command()
@click.option("--code", "-c", required=True, help="Code content")
@click.option("--language", "-l", help="Programming language")
@click.option("--title", "-t", help="Snippet title")
@click.option("--tags", help="Comma-separated tags")
def add(code, language, title, tags):
    """Add a new snippet"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO snippets (code, language, title, tags) VALUES (?, ?, ?, ?)",
        (code, language, title, tags)
    )
    conn.commit()
    snippet_id = cursor.lastrowid
    conn.close()
    console.print(f"[green]Added snippet ID: {snippet_id}[/green]")


@cli.command()
@click.argument("tag")
def tag(tag):
    """Search snippets by tag"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM snippets WHERE tags LIKE ?", (f"%{tag}%",)
    )
    results = cursor.fetchall()
    conn.close()
    
    table = Table(title=f"Snippets tagged: {tag}")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="green")
    table.add_column("Language", style="yellow")
    
    for row in results:
        table.add_row(str(row["id"]), row["title"] or "Untitled", row["language"] or "N/A")
    
    console.print(table)


@cli.command()
def list():
    """List all snippets"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM snippets ORDER BY created_at DESC")
    results = cursor.fetchall()
    conn.close()
    
    table = Table(title="All Snippets")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="green")
    table.add_column("Language", style="yellow")
    table.add_column("Tags", style="magenta")
    
    for row in results:
        table.add_row(
            str(row["id"]), 
            row["title"] or "Untitled", 
            row["language"] or "N/A",
            row["tags"] or ""
        )
    
    console.print(table)


@cli.command()
@click.argument("snippet_id", type=int)
def view(snippet_id):
    """View a snippet"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM snippets WHERE id = ?", (snippet_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        console.print(f"[red]Snippet {snippet_id} not found[/red]")
        return
    
    console.print(f"\n[bold]{row['title'] or 'Untitled'}[/bold]")
    console.print(f"Language: {row['language'] or 'N/A'}")
    console.print(f"Tags: {row['tags'] or 'None'}")
    console.print("\n[bold]Code:[/bold]")
    syntax = Syntax(row["code"], row["language"] or "text", theme="monokai")
    console.print(syntax)


@cli.command()
@click.argument("snippet_id", type=int)
def delete(snippet_id):
    """Delete a snippet"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM snippets WHERE id = ?", (snippet_id,))
    conn.commit()
    conn.close()
    console.print(f"[red]Deleted snippet {snippet_id}[/red]")


if __name__ == "__main__":
    cli()
