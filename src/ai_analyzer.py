import anthropic
from typing import Tuple, Dict
import json

class AIAnalyzer:
    """Uses Claude API to analyze screenshots and determine if user is on task"""

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def analyze_screenshot(self, screenshot_base64: str, current_task: str) -> Tuple[bool, str, float]:
        """
        Analyze a screenshot to determine if user is working on their stated task

        Args:
            screenshot_base64: Base64 encoded screenshot image
            current_task: Description of what the user should be working on

        Returns:
            (is_on_task, analysis_text, confidence_score)
        """

        prompt = f"""You are analyzing a screenshot to determine if the user is focused on their stated task.

Current Task: "{current_task}"

Please analyze the screenshot and determine:
1. Is the user working on the stated task? (yes/no)
2. What are they actually doing based on what you see?
3. How confident are you in this assessment? (0.0 to 1.0)

Respond in JSON format:
{{
    "is_on_task": true/false,
    "what_user_is_doing": "brief description",
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation"
}}

Be generous in your interpretation - if the activity could plausibly relate to the task, consider it on-task.
For example, if task is "writing report" and they're researching online, that's on-task.
"""

        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": screenshot_base64,
                                },
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ],
                    }
                ],
            )

            # Parse response
            response_text = message.content[0].text

            # Try to extract JSON from response
            try:
                # Find JSON in response (might be wrapped in markdown code blocks)
                if "```json" in response_text:
                    json_start = response_text.find("```json") + 7
                    json_end = response_text.find("```", json_start)
                    json_str = response_text[json_start:json_end].strip()
                elif "```" in response_text:
                    json_start = response_text.find("```") + 3
                    json_end = response_text.find("```", json_start)
                    json_str = response_text[json_start:json_end].strip()
                else:
                    json_str = response_text

                result = json.loads(json_str)

                is_on_task = result.get("is_on_task", False)
                confidence = result.get("confidence", 0.5)
                what_doing = result.get("what_user_is_doing", "Unknown")
                reasoning = result.get("reasoning", "")

                analysis = f"{what_doing}. {reasoning}"

                return is_on_task, analysis, confidence

            except json.JSONDecodeError:
                # If JSON parsing fails, fall back to simple analysis
                is_on_task = "true" in response_text.lower() or "yes" in response_text.lower()
                return is_on_task, response_text[:200], 0.5

        except Exception as e:
            print(f"Error analyzing screenshot: {e}")
            return False, f"Error: {str(e)}", 0.0

    def analyze_with_inactivity_check(self, screenshot_base64: str,
                                     current_task: str,
                                     is_inactive: bool,
                                     similarity: float) -> Tuple[bool, str, float]:
        """
        Analyze screenshot with consideration for inactivity

        Args:
            screenshot_base64: Base64 encoded screenshot
            current_task: User's stated task
            is_inactive: Whether screen appears unchanged from previous
            similarity: Similarity score to previous screenshot (0.0-1.0)

        Returns:
            (is_on_task, analysis_text, confidence_score)
        """

        if is_inactive:
            # Screen hasn't changed - user likely away or inactive
            analysis = f"Screen unchanged (similarity: {similarity:.2%}). User appears inactive."
            return False, analysis, 0.9
        else:
            # Screen has changed - analyze with AI
            return self.analyze_screenshot(screenshot_base64, current_task)
