"""Google Gemini provider implementation"""

from google import genai
from google.genai.types import GenerateContentConfig
from typing import Callable, Optional, List, Dict
import time
from app.config.constants import GEMINI_MODEL, GEMINI_TEMPERATURE, GEMINI_MAX_OUTPUT_TOKENS
from app.services.prompt_builder import PromptBuilder


class GeminiProvider:
    """Google Gemini API provider"""

    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model_id = GEMINI_MODEL

    def _make_request_with_retry(self, request_func, max_retries=3):
        """Make API request with exponential backoff retry logic"""
        for attempt in range(max_retries):
            try:
                return request_func()
            except Exception as e:
                error_str = str(e)
                
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    retry_delay = None
                    if "retry in" in error_str.lower():
                        try:
                            import re
                            match = re.search(r'retry in (\d+\.?\d*)s', error_str.lower())
                            if match:
                                retry_delay = float(match.group(1))
                        except:
                            pass
                    
                    if retry_delay is None:
                        retry_delay = (2 ** attempt) * 5
                    
                    if attempt < max_retries - 1:
                        print(f"Rate limit hit. Retrying in {retry_delay:.1f} seconds...")
                        time.sleep(retry_delay)
                        continue
                
                raise e
        
        raise Exception("Max retries exceeded")

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

        config = GenerateContentConfig(
            temperature=GEMINI_TEMPERATURE,
            max_output_tokens=GEMINI_MAX_OUTPUT_TOKENS,
        )

        def make_request():
            if stream:
                response = self.client.models.generate_content_stream(
                    model=self.model_id,
                    contents=prompt,
                    config=config,
                )
                full_text = ""
                for chunk in response:
                    if chunk.text:
                        text = chunk.text
                        full_text += text
                        if on_chunk:
                            on_chunk(text)
                return full_text
            else:
                response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=prompt,
                    config=config,
                )
                return response.text
        
        return self._make_request_with_retry(make_request)

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

        formatted_history = []
        for msg in history:
            role = msg.get("role", "user")
            parts = msg.get("parts", [])
            if parts and isinstance(parts[0], str):
                formatted_history.append({"role": role, "parts": [{"text": parts[0]}]})
            else:
                formatted_history.append(msg)

        formatted_history.append({"role": "user", "parts": [{"text": context_message}]})

        config = GenerateContentConfig(
            temperature=GEMINI_TEMPERATURE,
            max_output_tokens=GEMINI_MAX_OUTPUT_TOKENS,
        )

        def make_request():
            if stream:
                response = self.client.models.generate_content_stream(
                    model=self.model_id,
                    contents=formatted_history,
                    config=config,
                )
                full_text = ""
                for chunk in response:
                    if chunk.text:
                        text = chunk.text
                        full_text += text
                        if on_chunk:
                            on_chunk(text)
                return full_text
            else:
                response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=formatted_history,
                    config=config,
                )
                return response.text
        
        return self._make_request_with_retry(make_request)

    def test_connection(self) -> bool:
        """Test if API key is valid"""
        try:
            config = GenerateContentConfig(max_output_tokens=5)
            
            def make_request():
                return self.client.models.generate_content(
                    model=self.model_id,
                    contents="Say OK",
                    config=config,
                )
            
            self._make_request_with_retry(make_request)
            return True
        except Exception as e:
            print(f"Gemini API Connection Error: {e}")
            return False
