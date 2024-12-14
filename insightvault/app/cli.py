import click
import asyncio
from typing import Optional
from ..services.database import DatabaseService
import uvicorn
import sys
import asyncio

class InsightVaultCLI:
    def __init__(self) -> None:
        self.db = DatabaseService()
        self.running = False

    async def init(self) -> None:
        """Initialize the database service"""
        await self.db.init()
        
    async def interactive_loop(self) -> None:
        """Run the interactive command loop"""
        self.running = True
        print("Welcome to InsightVault Interactive Mode!")
        print("Type 'help' for commands, 'exit' to quit")
        
        while self.running:
            try:
                command = input("\ninsightvault> ").strip()
                if not command:
                    continue
                    
                if command == "exit":
                    self.running = False
                    continue
                    
                if command == "help":
                    print("\nAvailable commands:")
                    print("  query <text>     - Search the database")
                    print("  add <file_path>  - Add a document")
                    print("  exit            - Exit the program")
                    print("  help            - Show this help")
                    continue
                
                parts = command.split(maxsplit=1)
                if not parts:
                    continue
                    
                cmd = parts[0]
                args = parts[1] if len(parts) > 1 else ""
                
                if cmd == "query":
                    if not args:
                        print("Error: Query text required")
                        continue
                    results = await self.db.query(args)
                    print(f"\nResults for: {args}")
                    # TODO: Format and display results
                    
                elif cmd == "add":
                    if not args:
                        print("Error: File path required")
                        continue
                    # TODO: Implement document addition
                    print(f"Adding document: {args}")
                    
                else:
                    print(f"Unknown command: {cmd}")
                    
            except KeyboardInterrupt:
                self.running = False
            except Exception as e:
                print(f"Error: {str(e)}")

@click.group()
def cli() -> None:
    """InsightVault - Local RAG Pipeline Runner"""
    pass

@cli.command()
def start() -> None:
    """Start InsightVault in interactive mode"""
    cli_app = InsightVaultCLI()
    asyncio.run(cli_app.init())
    asyncio.run(cli_app.interactive_loop())

@cli.command()
@click.option('--host', default='127.0.0.1', help='Host to bind to')
@click.option('--port', default=8000, help='Port to bind to')
def serve(host: str, port: int) -> None:
    """Start the API server"""
    print(f"Starting API server at http://{host}:{port}")
    uvicorn.run("insightvault.app.api:app", host=host, port=port, reload=True)

def main() -> None:
    """Entry point for the CLI"""
    cli()

if __name__ == '__main__':
    main() 