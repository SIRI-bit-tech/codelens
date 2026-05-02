"""Token count estimation utility"""

from app.config.constants import TOKEN_ESTIMATE_CHARS_PER_TOKEN


class TokenCounter:
    """Estimates token count for text"""

    @staticmethod
    def estimate_tokens(text: str) -> int:
        """Estimate token count based on character count"""
        return len(text) // TOKEN_ESTIMATE_CHARS_PER_TOKEN

    @staticmethod
    def estimate_tokens_for_code_explanation(code: str, mode: str) -> int:
        """Estimate total tokens for a code explanation request"""
        prompt_overhead = 200
        code_tokens = TokenCounter.estimate_tokens(code)
        return code_tokens + prompt_overhead
