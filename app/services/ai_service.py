"""Google Gemini API integration for code explanation"""

from google import genai
from google.genai.types import GenerateContentConfig, GoogleSearch
from typing import Callable, Optional, List, Dict
import time
from app.config.constants import GEMINI_MODEL, GEMINI_TEMPERATURE, GEMINI_MAX_OUTPUT_TOKENS
from .prompt_builder import PromptBuilder


class AIService:
    """Handles all AI interactions using Google Gemini API"""

    def __init__(self, api_key: str):
        """
        Initialize AI service with API key

        Args:
            api_key: Google Gemini API key
        """
        # Use v1beta (default) which supports Gemini 2.0/2.5 models
        self.client = genai.Client(api_key=api_key)
        self.model_id = GEMINI_MODEL
        self.last_request_time = 0
        # Free tier allows 15 requests/minute = 4 seconds between requests minimum
        self.min_request_interval = 4.0  # Minimum 4 seconds between requests for free tier

    def _rate_limit(self):
        """Enforce rate limiting between requests"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last_request
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()

    def _make_request_with_retry(self, request_func, max_retries=3):
        """
        Make API request with exponential backoff retry logic
        
        Args:
            request_func: Function that makes the API request
            max_retries: Maximum number of retry attempts
            
        Returns:
            API response
            
        Raises:
            Exception: If all retries fail
        """
        for attempt in range(max_retries):
            try:
                return request_func()
            except Exception as e:
                error_str = str(e)
                
                # Check if it's a rate limit error (429)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    # Extract retry delay from error message if available
                    retry_delay = None
                    if "retry in" in error_str.lower():
                        try:
                            # Try to extract the retry delay (e.g., "52.736287719s")
                            import re
                            match = re.search(r'retry in (\d+\.?\d*)s', error_str.lower())
                            if match:
                                retry_delay = float(match.group(1))
                        except:
                            pass
                    
                    # If we couldn't extract delay, use exponential backoff
                    if retry_delay is None:
                        retry_delay = (2 ** attempt) * 5  # 5s, 10s, 20s
                    
                    if attempt < max_retries - 1:
                        print(f"Rate limit hit. Retrying in {retry_delay:.1f} seconds... (attempt {attempt + 1}/{max_retries})")
                        time.sleep(retry_delay)
                        continue
                
                # For non-rate-limit errors or last attempt, raise the exception
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
        """
        Generate code explanation

        Args:
            code: Code to explain
            language: Programming language
            mode: Explanation mode (overview, line_by_line, beginner, advanced, security, refactor)
            stream: Whether to stream the response
            on_chunk: Callback function for streaming chunks

        Returns:
            Full explanation text
        """
        self._rate_limit()  # Enforce rate limiting
        
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
        """
        Send a chat message with context

        Args:
            message: User's question
            code: Original code being discussed
            explanation: Previous explanation
            history: Chat history in Gemini format [{"role": "user"|"model", "parts": [{"text": str}]}]
            stream: Whether to stream the response
            on_chunk: Callback function for streaming chunks

        Returns:
            AI response text
        """
        self._rate_limit()  # Enforce rate limiting
        
        context_message = PromptBuilder.build_chat_context(code, explanation, message)

        # Convert history to new format if needed
        formatted_history = []
        for msg in history:
            role = msg.get("role", "user")
            parts = msg.get("parts", [])
            # Handle both old format (list of strings) and new format (list of dicts)
            if parts and isinstance(parts[0], str):
                formatted_history.append({"role": role, "parts": [{"text": parts[0]}]})
            else:
                formatted_history.append(msg)

        # Add the new message
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
        """
        Test if API key is valid and connection works
        Note: This should only be called when explicitly testing, not on startup

        Returns:
            True if connection successful, False otherwise
        """
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
            print(f"API Connection Error: {e}")
            return False
