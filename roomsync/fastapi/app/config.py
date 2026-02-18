import json
import logging
import os
from pathlib import Path
from pydantic import validator
from pydantic_settings import BaseSettings, EnvSettingsSource, SettingsConfigDict
from typing import List, Optional, Any, Callable, Union
from dotenv import load_dotenv

ENV_PATH = next(
    (parent / ".env" for parent in Path(__file__).resolve().parents if (parent / ".env").exists()),
    None,
)
if ENV_PATH:
    load_dotenv(ENV_PATH, override=True)

logging.basicConfig(level=logging.INFO)


class CustomEnvSettingsSource(EnvSettingsSource):
    def __init__(self, settings_cls, env_nested_delimiter: str | None = None, env_prefix: str = ""):
        super().__init__(settings_cls,
                         env_nested_delimiter=env_nested_delimiter, env_prefix=env_prefix)

    def __call__(self) -> dict[str, Any]:
        # Use os.environ directly or a method to get env vars, since _env_vars isn’t available
        env_vars = os.environ
        out = {}
        for field_name, field in self.settings_cls.model_fields.items():
            env_key = f"{self.env_prefix}{field_name.upper()}"
            env_val = env_vars.get(env_key)
            if env_val is not None and env_val != "":
                # Pass raw string without parsing
                out[field_name] = env_val
        return out


class Settings(BaseSettings):
    debug: bool = True
    jwt_secret_key: str = "my_jwt_secret"
    jwt_token_location: List[str] = ["cookies"]
    jwt_access_cookie_name: str = "jwt"
    jwt_cookie_secure: bool = False
    jwt_cookie_samesite: str = "Lax"
    jwt_cookie_csrf_protect: bool = False
    secret_key: str = "df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506"
    json_as_ascii: bool = False
    database_url: str = "sqlite:///./app.db"  # Default; overridden by .env
    use_supabase: bool = False
    supabase_db_url: Optional[str] = None

    @validator("database_url", pre=True, always=True)
    def check_supabase_url(cls, v, values):
        # We need to access the raw environment variables or the values dict
        # Since 'use_supabase' might not be in 'values' yet if it's validated later,
        # we check the environment variable directly or rely on field order.
        # Pydantic V1/V2 validation order can be tricky.
        # Safest is checking os.environ or ensure use_supabase is defined before.
        use_supabase = values.get("use_supabase")
        # If use_supabase was not in values (maybe distinct validation order), check env
        if use_supabase is None:
             use_supabase = os.getenv("USE_SUPABASE", "false").lower() == "true"
        
        if use_supabase:
            supabase_url = values.get("supabase_db_url") or os.getenv("SUPABASE_DB_URL")
            if supabase_url:
                logging.info("USE_SUPABASE is True: Swapping DATABASE_URL to SUPABASE_DB_URL")
                return supabase_url
            else:
                logging.warning("USE_SUPABASE is True but SUPABASE_DB_URL is missing!")
        return v
    allowed_origins: Union[List[str], str, None] = ["*"]
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None
    google_discovery_url: Optional[str] = None
    frontend_login_success_uri: str = "http://localhost:8080/login-success"  # Default
    frontend_login_failure_uri: str = "http://localhost:8080/login-failed"  # Default

    @validator("allowed_origins", pre=True, always=True)
    def assemble_allowed_origins(cls, v):
        logging.info(f"Raw value for allowed_origins: {v!r}")
        if v is None:
            logging.info("None value detected, returning ['*']")
            return ["*"]
        if isinstance(v, list):
            logging.info(f"Value already a list: {v}")
            return v
        if isinstance(v, str):
            if not v.strip():
                logging.info("Empty string detected, returning ['*']")
                return ["*"]
            if v.startswith("[") and v.endswith("]"):
                try:
                    parsed = json.loads(v)
                    logging.info(f"Successfully parsed JSON: {parsed}")
                    return parsed
                except json.JSONDecodeError as e:
                    logging.error(f"Error decoding JSON: {e}")
            result = [i.strip() for i in v.split(",") if i.strip()]
            logging.info(f"Parsed as comma-separated string: {result}")
            return result if result else ["*"]
        logging.info(f"Unexpected type, returning ['*']")
        return ["*"]

    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH) if ENV_PATH else None,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings: Callable[[], dict[str, Any]],
        env_settings: Callable[[], dict[str, Any]],
        dotenv_settings: Callable[[], dict[str, Any]],
        file_secret_settings: Callable[[], dict[str, Any]],
    ):
        return (init_settings, CustomEnvSettingsSource(settings_cls), dotenv_settings, file_secret_settings)


try:
    settings = Settings()
    logging.info(f"Settings loaded successfully")
    logging.info(f"Final allowed_origins: {settings.allowed_origins}")
    logging.info(f"Database URL: {settings.database_url}")
    logging.info(f"Google Client ID: {settings.google_client_id}")
    logging.info(f"Google Client Secret: {settings.google_client_secret[:10] if settings.google_client_secret else 'NOT SET'}...")
except Exception as e:
    logging.error(f"Error loading settings: {e}")
    raise
