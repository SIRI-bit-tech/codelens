"""Unified AI service supporting multiple providers (Gemini, OpenAI, Claude)"""

from typing import Callable, Optional, List, Dict
import time


class AIServiceUnified:
    """Unified interface for multiple AI providers"""

    def __init__(self, provider: str, api_key: str):
        """
        Initialize AI service with specific provider

        Args:
            provider: AI provider name ('gemini', 'openai', 'claude')
            api_key: API key for the provider
        """
        self.provider = provider
        self.api_key = api_key
        self.last_request_time = 0
        self.min_request_interval = 4.0  # 4 seconds for free tier rate limiting
        
        # Initialize the appropriate provider
        if provider == "gemini":
            from .providers.gemini_provider import GeminiProvider
            self.provider_instance = GeminiProvider(api_key)
        elif provider == "openai":
            from .providers.openai_provider import OpenAIProvider
            self.provider_instance = OpenAIProvider(api_key)
        elif provider == "claude":
            from .providers.claude_provider import ClaudeProvider
            self.provider_instance = ClaudeProvider(api_key)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def _rate_limit(self):
        """Enforce rate limiting between requests"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last_request
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()

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
            mode: Explanation mode
            stream: Whether to stream the response
            on_chunk: Callback function for streaming chunks

        Returns:
            Full explanation text
        """
        self._rate_limit()
        return self.provider_instance.explain_code(code, language, mode, stream, on_chunk)

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
            history: Chat history
            stream: Whether to stream the response
            on_chunk: Callback function for streaming chunks

        Returns:
            AI response text
        """
        self._rate_limit()
        return self.provider_instance.chat(message, code, explanation, history, stream, on_chunk)

    def test_connection(self) -> bool:
        """
        Test if API key is valid and connection works

        Returns:
            True if connection successful, False otherwise
        """
        try:
            return self.provider_instance.test_connection()
        except Exception as e:
            print(f"API Connection Error: {e}")
            return False
