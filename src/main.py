import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.progress import track
from rich import print as rprint
from pathlib import Path

from database import init_db, save_transaction, get_all_transactions, get_summary_by_category
from classifier import classify_transaction

console = Console()

DATA_PATH = Path(__file__).parent.parent / "data" / "transactions.csv"


def load_transactions(path: Path) -> pd.DataFrame:

    if not path.exists():
        console.print(f"[red]Error:[/red] No se encontró el archivo {path}")
        raise FileNotFoundError(f"No existe: {path}")
    
    df = pd.read_csv(path)
    console.print(f"[green]✓[/green] {len(df)} transacciones cargadas desde CSV")
    return df


def print_results_table(transactions: list) -> None:

    table = Table(title="Transacciones Clasificadas", show_lines=True)
    
    table.add_column("Fecha",        style="cyan",    no_wrap=True)
    table.add_column("Descripción",  style="white",   max_width=30)
    table.add_column("Monto",        style="yellow",  justify="right")
    table.add_column("Categoría",    style="magenta")
    table.add_column("Confianza",    justify="center")
    
    confidence_style = {
        "alta":  "[green]alta[/green]",
        "media": "[yellow]media[/yellow]",
        "baja":  "[red]baja[/red]"
    }
    
    for tx in transactions:
        conf = confidence_style.get(tx["confidence"], tx["confidence"])
        table.add_row(
            tx["date"],
            tx["description"],
            f"${tx['amount']:,.2f}",
            tx["category"],
            conf
        )
    
    console.print(table)


def print_summary_table(summary: list) -> None:

    table = Table(title="Resumen por Categoría", show_lines=True)
    
    table.add_column("Categoría",        style="magenta")
    table.add_column("Transacciones",    justify="center", style="cyan")
    table.add_column("Gasto Total",      justify="right",  style="yellow")
    table.add_column("Gasto Promedio",   justify="right",  style="white")
    
    for row in summary:
        table.add_row(
            row["category"],
            str(row["total_transacciones"]),
            f"${row['gasto_total']:,.2f}",
            f"${row['gasto_promedio']:,.2f}"
        )
    
    console.print(table)


def main():
    console.rule("[bold blue]TX-CLASSIFIER — Clasificador de Transacciones[/bold blue]")
    
    console.print("\n[bold]Paso 1:[/bold] Inicializando base de datos...")
    init_db()
    
    console.print("\n[bold]Paso 2:[/bold] Cargando transacciones...")
    df = load_transactions(DATA_PATH)
    
    console.print("\n[bold]Paso 3:[/bold] Clasificando con IA local...\n")
    
    classified = []
    
    for _, row in track(df.iterrows(), total=len(df), description="Procesando..."):
        result = classify_transaction(row["description"], row["amount"])
        
        tx = {
            "date":        row["date"],
            "description": row["description"],
            "amount":      row["amount"],
            "currency":    row["currency"],
            "category":    result["category"],
            "confidence":  result["confidence"]
        }
        classified.append(tx)
        
        save_transaction(**tx)
    
    console.print("\n[bold]Paso 4:[/bold] Resultados\n")
    print_results_table(classified)
    
    console.print("\n[bold]Paso 5:[/bold] Resumen por categoría (consulta SQL)\n")
    summary_raw = get_summary_by_category()
    
    summary = [dict(row) for row in summary_raw]
    print_summary_table(summary)
    
    total = sum(tx["amount"] for tx in classified)
    console.print(f"\n[bold green]Total procesado:[/bold green] ${total:,.2f} MXN")
    console.rule("[bold blue]Proceso completado[/bold blue]")


if __name__ == "__main__":

    main()