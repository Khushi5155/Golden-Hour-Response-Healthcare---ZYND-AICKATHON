from abc import ABC, abstractmethod
from datetime import datetime

class BaseAgent(ABC):

    def __init__(self, did: str, name: str):
        self.did = did
        self.name = name

    @abstractmethod
    def execute(self, payload: dict) -> dict:
        pass

    def _meta(self):
        return {
            "agent": self.name,
            "did": self.did,
            "timestamp": datetime.utcnow().isoformat()
        }
