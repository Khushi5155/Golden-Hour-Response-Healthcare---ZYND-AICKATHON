# src/mock_zynd.py
from typing import Any, Callable, Dict

class MockZyndRegistry:
    """
    Minimal in-process stand‑in for Zynd Protocol.
    You can later swap this for the real Zynd SDK client.
    """
    def __init__(self):
        self._agents: Dict[str, Callable[[dict], Any]] = {}

    def register_agent(self, did: str, handler: Callable[[dict], Any]):
        self._agents[did] = handler

    async def call(self, did: str, payload: dict):
        if did not in self._agents:
            raise ValueError(f"Agent with DID {did} not registered")
        handler = self._agents[did]
        result = handler(payload)
        if hasattr(result, "__await__"):
            return await result
        return result


zynd_registry = MockZyndRegistry()
