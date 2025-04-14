

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.docker", extra="ignore")


    # Application Settings
    app_name: str
    app_env: str

    airflow_db: str
    airflow_base_url: str
    airflow_username: str
    airflow_password: str

    core_base_url : str

    uvicorn_host: str
    uvicorn_port: int



# Instantiate settings
settings = Settings()
