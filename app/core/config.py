# app/core/config.py
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Azure Service Principal
    AZURE_CLIENT_ID: str
    AZURE_CLIENT_SECRET: str
    AZURE_TENANT_ID: str

    # Subscriptions to monitor (comma-separated in .env)
    AZURE_SUBSCRIPTION_IDS: str

    # PostgreSQL
    DATABASE_URL: str

    # Azure OpenAI
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_DEPLOYMENT: str = "gpt-4o"

    # Teams
    TEAMS_WEBHOOK_URL: str = ""

    # Agent thresholds
    CPU_THRESHOLD_PCT: float = 10.0
    MEMORY_THRESHOLD_PCT: float = 20.0
    LOOKBACK_DAYS: int = 30

    @property
    def subscription_ids(self) -> List[str]:
        """Parse comma-separated subscription IDs into a list."""
        return [s.strip() for s in self.AZURE_SUBSCRIPTION_IDS.split(",")]

    class Config:
        env_file = ".env"
        extra = "ignore"


# single instance imported everywhere
settings = Settings()