"""OpenAI provider implementation"""

from openai import OpenAI
from typing import Callable, Optional, List, Dict
from app.config.constants import OPENAI_MODEL, OPENAI_TEMPERATURE, OPENAI_MAX_OUTPUT_TOKENS
from app.services.prompt_builder import PromptBuilder


class OpenAIProvider:
    """OpenAI API provider"""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model_id = OPENAI_MODEL

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

        messages = [{"role": "user", "content": prompt}]

        if stream:
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                temperature=OPENAI_TEMPERATURE,
                max_tokens=OPENAI_MAX_OUTPUT_TOKENS,
                stream=True
            )
            
            full_text = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    text = chunk.choices[0].delta.content
                    full_text += text
                    if on_chunk:
                        on_chunk(text)
            return full_text
        else:
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                temperature=OPENAI_TEMPERATURE,
                max_tokens=OPENAI_MAX_OUTPUT_TOKENS,
            )
            return response.choices[0].message.content

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

        # Convert history to OpenAI format
        messages = []
        for msg in history:
            role = msg.get("role", "user")
            parts = msg.get("parts", [])
            
            # Map Gemini roles to OpenAI roles
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
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                temperature=OPENAI_TEMPERATURE,
                max_tokens=OPENAI_MAX_OUTPUT_TOKENS,
                stream=True
            )
            
            full_text = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    text = chunk.choices[0].delta.content
                    full_text += text
                    if on_chunk:
                        on_chunk(text)
            return full_text
        else:
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                temperature=OPENAI_TEMPERATURE,
                max_tokens=OPENAI_MAX_OUTPUT_TOKENS,
            )
            return response.choices[0].message.content

    def test_connection(self) -> bool:
        """Test if API key is valid"""
        try:
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=[{"role": "user", "content": "Say OK"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            print(f"OpenAI API Connection Error: {e}")
            return False
