from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Dynamic Pricing and Promotion Simulation System"
    database_url: str = "sqlite:///./pricing_simulation.db"
    api_prefix: str = "/api"
    random_seed: int = 20261022
    secret_key: str = "CHANGE_THIS_TO_A_LONG_RANDOM_SECRET_BEFORE_DEPLOYMENT"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
