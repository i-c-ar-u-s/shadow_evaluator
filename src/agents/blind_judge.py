from rich.console import Console

console = Console()

class BlindJudgeAgent:
    def __init__(self, config):
        self.config = config
        self.name = config['name']
        self.role = config['role']
        console.print(f"[bold green]Initialized {self.name} ({self.role})[/bold green]")

    def evaluate(self, sanitized_script, rubric):
        """
        Grade anonymous script vs rubric. Return Score, Confidence, Reasoning.
        """
        console.print(f"[cyan]{self.name} is evaluating script...[/cyan]")
        # Placeholder
        return {
            "score": 85, 
            "confidence": 0.95, 
            "reasoning": "Matches key points in rubric."
        }
