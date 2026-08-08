from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    whisper_model: str = "small"
    whisper_device: str = "cpu"
    whisper_compute_type: str = "int8"
    languages: str = "es-AR,en-US"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def supported_languages(self) -> list[str]:
        return [lang.strip() for lang in self.languages.split(",") if lang.strip()]


settings = Settings()
