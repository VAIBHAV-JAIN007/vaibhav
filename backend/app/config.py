from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_name: str = "Global AI Trading Intelligence API"
    database_url: str = "sqlite:///./gati.db"
    jwt_secret: str = "CHANGE_THIS_SECRET_BEFORE_DEPLOYMENT"
    jwt_minutes: int = 60
    cors_origins: str = "http://localhost:5173,http://localhost:8000,http://localhost:8080,https://vaibhav-jain007.github.io"
    binance_base_url: str = "https://api.binance.com"

settings = Settings()
