"""Builds mode-specific prompts for AI code explanation"""

from typing import Dict


class PromptBuilder:
    """Constructs prompts for different explanation modes"""

    MODE_PROMPTS: Dict[str, str] = {
        "overview": """You are a code explanation assistant. Provide a clear, concise overview of what this code does.

Format your response with:
1. **Purpose**: What is the main goal of this code? (2-3 sentences)
2. **Key Components**: What are the main parts or functions?
3. **How It Works**: Brief explanation of the logic flow
4. **Output/Result**: What does this code produce or accomplish?

Keep it high-level and accessible. Avoid line-by-line details.

Please explain this {language} code:

```{language}
{code}
```""",
        "line_by_line": """You are a code explanation assistant. Provide a detailed line-by-line or block-by-block explanation of this code.

Format your response with:
1. **Overview**: Brief summary (1-2 sentences)
2. **Detailed Walkthrough**: Explain each meaningful line or logical block
   - Use line numbers or code snippets to reference specific parts
   - Explain what each section does and why
   - Highlight important variables, functions, or logic

Be thorough but clear. Group related lines together when appropriate.

Please explain this {language} code:

```{language}
{code}
```""",
        "beginner": """You are a patient coding teacher explaining code to a complete beginner who is just learning to program.

Use simple English. Avoid technical jargon. When you must use technical terms, explain them immediately.
Use real-world analogies to make concepts relatable.

Format your response with:
1. **What This Code Does**: Explain in plain English (like explaining to a friend)
2. **Key Concepts**: Explain any programming concepts used (variables, loops, functions, etc.)
3. **Step-by-Step Walkthrough**: Break down the code in simple terms
4. **One Thing to Watch Out For**: A common mistake or important detail

Remember: Your audience is learning. Be encouraging and clear.

Please explain this {language} code:

```{language}
{code}
```""",
        "advanced": """You are an expert software engineer providing advanced technical analysis of this code.

Format your response with:
1. **Code Overview**: Brief summary of functionality
2. **Design Patterns**: Identify any design patterns used
3. **Complexity Analysis**: Time and space complexity (Big-O notation)
4. **Architecture**: How this code fits into larger systems
5. **Potential Issues**: Edge cases, scalability concerns, or technical debt
6. **Best Practices**: What's done well and what could be improved

Be technical and precise. Assume the reader is an experienced developer.

Please analyze this {language} code:

```{language}
{code}
```""",
        "security": """You are a security expert conducting a code security audit.

Format your response with:
1. **Security Overview**: Initial security assessment
2. **Vulnerabilities Found**: List specific security issues
   - SQL injection risks
   - XSS vulnerabilities
   - Authentication/authorization issues
   - Input validation problems
   - Sensitive data exposure
   - Insecure dependencies
3. **Severity Ratings**: Rate each issue (Critical/High/Medium/Low)
4. **Recommendations**: Specific fixes for each vulnerability
5. **Best Practices**: Security improvements to implement

Be thorough and specific. Flag even potential risks.

Please audit this {language} code for security issues:

```{language}
{code}
```""",
        "refactor": """You are a code quality expert providing refactoring suggestions.

Format your response with:
1. **Current State**: Brief assessment of the code quality
2. **Code Smells**: Identify issues
   - Duplicated code
   - Long functions/methods
   - Poor naming
   - Tight coupling
   - Magic numbers
   - Lack of error handling
3. **Refactoring Suggestions**: Specific improvements with examples
4. **Refactored Code**: Show improved version of key sections
5. **Benefits**: Explain why these changes improve the code

Provide concrete, actionable suggestions with code examples.

Please suggest refactorings for this {language} code:

```{language}
{code}
```""",
    }

    @staticmethod
    def build(code: str, language: str, mode: str) -> str:
        """
        Build a prompt for the specified mode

        Args:
            code: The code to explain
            language: Programming language
            mode: Explanation mode

        Returns:
            Formatted prompt string
        """
        if mode not in PromptBuilder.MODE_PROMPTS:
            mode = "overview"

        template = PromptBuilder.MODE_PROMPTS[mode]
        return template.format(code=code, language=language)

    @staticmethod
    def build_chat_context(code: str, explanation: str, question: str) -> str:
        """
        Build context for follow-up chat questions

        Args:
            code: Original code
            explanation: Previous explanation
            question: User's question

        Returns:
            Formatted context string
        """
        return f"""You are helping a user understand code. Here's the context:

**Original Code:**
```
{code[:500]}{"..." if len(code) > 500 else ""}
```

**Previous Explanation Summary:**
{explanation[:300]}{"..." if len(explanation) > 300 else ""}

**User's Question:**
{question}

Please answer the question clearly and concisely, referencing the code and previous explanation as needed."""
