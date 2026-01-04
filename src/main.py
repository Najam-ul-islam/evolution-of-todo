"""Main entry point for the Todo Console Application."""

from todo.cli import TodoCLI


def main():
    """Run the Todo Console Application."""
    app = TodoCLI()
    app.run()


if __name__ == "__main__":
    main()