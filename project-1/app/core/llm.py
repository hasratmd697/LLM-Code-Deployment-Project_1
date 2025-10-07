# from openai import OpenAI
from typing import List, Dict, Any
import json
from app.core.config import settings

# Using AIpipe API key with OpenAI-compatible interface
client = PIPE(
    api_key=settings.AIPIPE_API_KEY,
    base_url="https://api.aipipe.io/v1"  # AIpipe's OpenAI-compatible endpoint
)

class LLMCodeGenerator:
    def __init__(self):
        self.client = client

    async def generate_code(self, brief: str, checks: List[str]) -> Dict[str, Any]:
        """Generate code based on the brief and checks using AIpipe."""
        prompt = self._create_prompt(brief, checks)
        
        response = await self.client.chat.completions.create(
            model="gpt-4",  # AIpipe should handle this model name
            messages=[
                {"role": "system", "content": "You are an expert code generator. Generate complete, production-ready code based on the requirements."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return self._parse_response(response.choices[0].message.content)

    def _create_prompt(self, brief: str, checks: List[str]) -> str:
        """Create a detailed prompt for the LLM."""
        return f"""
Please generate a complete web application based on the following requirements:

Brief:
{brief}

Requirements (the application must pass these checks):
{json.dumps(checks, indent=2)}

Generate a complete, production-ready application that:
1. Meets all the specified requirements
2. Is well-structured and maintainable
3. Includes proper error handling
4. Has clear documentation
5. Is ready for deployment to GitHub Pages

Please provide:
1. HTML, CSS, and JavaScript code
2. README.md content
3. Any necessary configuration files
4. Structure for GitHub Pages deployment
"""

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse the LLM response into structured code files."""
        # This is a simplified version - in practice, you'd want to use a more robust parsing method
        files = {
            "index.html": "",
            "style.css": "",
            "script.js": "",
            "README.md": ""
        }
        
        current_file = None
        current_content = []
        
        for line in response.split("\n"):
            if line.startswith("```") and len(line) > 3:
                current_file = line[3:].strip()
                continue
            elif line.startswith("```") and current_file:
                files[current_file] = "\n".join(current_content)
                current_file = None
                current_content = []
                continue
                
            if current_file:
                current_content.append(line)
                
        return files