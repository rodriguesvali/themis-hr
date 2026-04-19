from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from themis_hr_api.core.config import settings
import os

# Configura a variável de ambiente global para o LiteLLM
if settings.google_api_key:
    os.environ["GEMINI_API_KEY"] = settings.google_api_key # CrewAI (litellm base) expects GEMINI_API_KEY for google

@CrewBase
class ThemisHRCrew:
    """Themis HR multi-agent orchestration crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        # Passar a string de conexão LiteLLM suportada pro CrewAI resolver o Provider dele
        self.llm = f"gemini/{settings.crewai_model}"

    @agent
    def intake_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['intake_agent'],
            llm=self.llm,
            verbose=True
        )

    @agent
    def router_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['router_agent'],
            llm=self.llm,
            verbose=True
        )

    @agent
    def expert_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['expert_agent'],
            llm=self.llm,
            verbose=True
        )

    @agent
    def response_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['response_agent'],
            llm=self.llm,
            verbose=True
        )

    @agent
    def sentiment_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['sentiment_agent'],
            llm=self.llm,
            verbose=True
        )

    @agent
    def escalation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['escalation_agent'],
            llm=self.llm,
            verbose=True
        )

    @task
    def intake_task(self) -> Task:
        return Task(
            config=self.tasks_config['intake_task'],
            agent=self.intake_agent()
        )

    @task
    def classification_task(self) -> Task:
        return Task(
            config=self.tasks_config['classification_task'],
            agent=self.router_agent()
        )

    @task
    def knowledge_task(self) -> Task:
        return Task(
            config=self.tasks_config['knowledge_task'],
            agent=self.expert_agent()
        )

    @task
    def response_task(self) -> Task:
        return Task(
            config=self.tasks_config['response_task'],
            agent=self.response_agent()
        )

    @task
    def sentiment_task(self) -> Task:
        return Task(
            config=self.tasks_config['sentiment_task'],
            agent=self.sentiment_agent()
        )

    @task
    def escalation_task(self) -> Task:
        return Task(
            config=self.tasks_config['escalation_task'],
            agent=self.escalation_agent()
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Themis HR crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            # memory=True, # No MVP vamos manter memory off pra economizar requests se não configurar embedders locais
        )
