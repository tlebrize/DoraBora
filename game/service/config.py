from dataclasses import dataclass
import os


@dataclass
class Config:
    MANAGEMENT_BASE_URL: str = os.environ.get("MANAGEMENT_BASE_URL")
    SERVER_PORT: int = os.environ.get("SERVER_PORT")
    SERVER_TOKEN: str = os.environ.get("SERVER_TOKEN")
    SERVER_ID: int = os.environ.get("SERVER_ID")
    REDIS_URL: str = os.environ.get("REDIS_URL")
