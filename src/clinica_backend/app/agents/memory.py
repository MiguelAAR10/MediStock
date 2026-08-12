from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Deque, Dict, List


@dataclass
class ChatTurn:
    role: str
    content: str


class SessionMemory:
    def __init__(self, max_turns: int = 8) -> None:
        self.max_turns = max_turns
        self._store: Dict[str, Deque[ChatTurn]] = defaultdict(
            lambda: deque(maxlen=self.max_turns)
        )

    def get_history(self, session_id: str) -> List[dict]:
        if not session_id:
            return []
        return [
            {"role": turn.role, "content": turn.content}
            for turn in self._store[session_id]
        ]

    def append_user(self, session_id: str, message: str) -> None:
        if session_id and message:
            self._store[session_id].append(ChatTurn(role="user", content=message))

    def append_assistant(self, session_id: str, message: str) -> None:
        if session_id and message:
            self._store[session_id].append(ChatTurn(role="assistant", content=message))


session_memory = SessionMemory(max_turns=10)
