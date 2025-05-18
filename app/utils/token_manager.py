import tiktoken
from typing import Dict, Any

class TokenManager:
    def _init_(self):
        self.encoding = tiktoken.get_encoding("cl100k_base")
        self.max_tokens = 800

    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in a text string"""
        return len(self.encoding.encode(text))

    def truncate_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Truncate response content to fit within token limit"""
        content = response["content"]
        tokens = self.count_tokens(content)
        
        if tokens <= self.max_tokens:
            return response

        # Truncate content to fit within token limit
        encoded = self.encoding.encode(content)
        truncated = self.encoding.decode(encoded[:self.max_tokens])
        
        return {
            **response,
            "content": truncated,
            "tokens": self.max_tokens
        }

    def split_into_chunks(self, text: str) -> list[str]:
        """Split text into chunks of max_tokens size"""
        encoded = self.encoding.encode(text)
        chunks = []
        
        for i in range(0, len(encoded), self.max_tokens):
            chunk = self.encoding.decode(encoded[i:i + self.max_tokens])
            chunks.append(chunk)
            
        return chunks