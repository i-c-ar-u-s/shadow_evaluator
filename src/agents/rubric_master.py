from rich.console import Console

console = Console()

class RubricMasterAgent:
    def __init__(self, config):
        self.config = config
        self.name = config['name']
        self.role = config['role']
        console.print(f"[bold green]Initialized {self.name} ({self.role})[/bold green]")

    def generate_rubric(self, question_paper_text):
        """
        Analyze question paper, generate strict grading key.
        """
        console.print(f"[cyan]{self.name} is generating rubric...[/cyan]")
        # Placeholder
        return {"rubric": "Sample Rubric Key", "strictness": "high"}
