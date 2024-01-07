from dataclasses import dataclass
import os


@dataclass
class Config:
    MANAGEMENT_BASE_URL: str = os.environ.get("MANAGEMENT_BASE_URL")
