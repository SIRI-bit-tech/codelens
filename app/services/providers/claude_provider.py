"""Anthropic Claude provider implementation"""

from anthropic import Anthropic
from typing import Callable, Optional, List, Dict
from app.config.constants import CLAUDE_MODEL, CLAUDE_TEMPERATURE, CLAUDE_MAX_OUTPUT_TOKENS
from app.services.prompt_builder import PromptBuilder


class ClaudeProvider:
    """Anthropic Claude API provider"""

    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.model_id = CLAUDE_MODEL

    def explain_code(
        self,
        code: str,
        language: str,
        mode: str,
        stream: bool = True,
        on_chunk: Optional[Callable[[str], None]] = None,
    ) -> str:
        """Generate code explanation"""
        prompt = PromptBuilder.build(code, language, mode)

        if stream:
            full_text = ""
            with self.client.messages.stream(
                model=self.model_id,
                max_tokens=CLAUDE_MAX_OUTPUT_TOKENS,
                temperature=CLAUDE_TEMPERATURE,
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                for text in stream.text_stream:
                    full_text += text
                    if on_chunk:
                        on_chunk(text)
            return full_text
        else:
            response = self.client.messages.create(
                model=self.model_id,
                max_tokens=CLAUDE_MAX_OUTPUT_TOKENS,
                temperature=CLAUDE_TEMPERATURE,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text

    def chat(
        self,
        message: str,
        code: str,
        explanation: str,
        history: List[Dict],
        stream: bool = True,
        on_chunk: Optional[Callable[[str], None]] = None,
    ) -> str:
        """Send a chat message with context"""
        context_message = PromptBuilder.build_chat_context(code, explanation, message)

        # Convert history to Claude format
        messages = []
        for msg in history:
            role = msg.get("role", "user")
            parts = msg.get("parts", [])
            
            # Map Gemini roles to Claude roles
            if role == "model":
                role = "assistant"
            
            # Extract text content
            if parts:
                if isinstance(parts[0], str):
                    content = parts[0]
                elif isinstance(parts[0], dict) and "text" in parts[0]:
                    content = parts[0]["text"]
                else:
                    content = str(parts[0])
                
                messages.append({"role": role, "content": content})

        # Add the new message
        messages.append({"role": "user", "content": context_message})

        if stream:
            full_text = ""
            with self.client.messages.stream(
                model=self.model_id,
                max_tokens=CLAUDE_MAX_OUTPUT_TOKENS,
                temperature=CLAUDE_TEMPERATURE,
                messages=messages
            ) as stream:
                for text in stream.text_stream:
                    full_text += text
                    if on_chunk:
                        on_chunk(text)
            return full_text
        else:
            response = self.client.messages.create(
                model=self.model_id,
                max_tokens=CLAUDE_MAX_OUTPUT_TOKENS,
                temperature=CLAUDE_TEMPERATURE,
                messages=messages
            )
            return response.content[0].text

    def test_connection(self) -> bool:
        """Test if API key is valid"""
        try:
            response = self.client.messages.create(
                model=self.model_id,
                max_tokens=5,
                messages=[{"role": "user", "content": "Say OK"}]
            )
            return True
        except Exception as e:
            print(f"Claude API Connection Error: {e}")
            return False
