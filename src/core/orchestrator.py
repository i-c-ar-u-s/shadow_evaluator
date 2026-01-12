import yaml
from rich.console import Console
from src.agents.clean_room import CleanRoomAgent
from src.agents.rubric_master import RubricMasterAgent
from src.agents.blind_judge import BlindJudgeAgent
from src.agents.quant_analyst import QuantAnalystAgent
from src.agents.governance_officer import GovernanceOfficerAgent

console = Console()

class Orchestrator:
    def __init__(self, config_path="config/agents.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
        
        self.agents = {
            "clean_room": CleanRoomAgent(self.config['agents']['clean_room']),
            "rubric_master": RubricMasterAgent(self.config['agents']['rubric_master']),
            "blind_judge": BlindJudgeAgent(self.config['agents']['blind_judge']),
            "quant_analyst": QuantAnalystAgent(self.config['agents']['quant_analyst']),
            "governance_officer": GovernanceOfficerAgent(self.config['agents']['governance_officer']),
        }

    def run_pipeline(self, input_pdf, faculty_grade=None):
        console.print("[bold]Starting Evaluation Pipeline...[/bold]")

        # 1. Clean Room
        clean_data = self.agents['clean_room'].process(input_pdf)
        
        # 2. Rubric Master
        rubric = self.agents['rubric_master'].generate_rubric(clean_data['sanitized_text']) # Simplified flow
        
        # 3. Blind Judge
        evaluation = self.agents['blind_judge'].evaluate(clean_data['sanitized_text'], rubric['rubric'])
        
        # 4. Quant Analyst (if faculty grade provided)
        if faculty_grade is not None:
            stats = self.agents['quant_analyst'].analyze(faculty_grade, evaluation['score'], None)
            
            # 5. Governance Officer
            report = self.agents['governance_officer'].report(stats)
            console.print(f"\n[bold red]Final Report:[/bold red] {report}")
        else:
            console.print(f"\n[bold green]AI Score:[/bold green] {evaluation['score']}")
