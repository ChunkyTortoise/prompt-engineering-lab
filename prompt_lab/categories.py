"""Business task categories for prompt engineering benchmarks."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TaskExample:
    """A sample task within a category."""

    name: str
    input_text: str
    expected_output: str
    expected_topics: list[str] = field(default_factory=list)
    context: str = ""


@dataclass
class TaskCategory:
    """A business category with sample tasks."""

    name: str
    description: str
    examples: list[TaskExample] = field(default_factory=list)
    recommended_patterns: list[str] = field(default_factory=list)


class CategoryRegistry:
    """Registry of 7 business task categories."""

    def __init__(self):
        self._categories: dict[str, TaskCategory] = {}
        self._register_builtins()

    def _register_builtins(self):
        """Register 7 business categories with sample tasks."""
        categories = [
            TaskCategory(
                name="classification",
                description="Categorize text into predefined classes",
                recommended_patterns=["few_shot", "chain_of_thought"],
                examples=[
                    TaskExample(
                        name="sentiment_analysis",
                        input_text=("The product quality is amazing but shipping was slow."),
                        expected_output="mixed",
                        expected_topics=["sentiment", "positive", "negative"],
                    ),
                    TaskExample(
                        name="ticket_routing",
                        input_text=("I can't log in to my account. Password reset isn't working."),
                        expected_output="authentication",
                        expected_topics=["category", "authentication"],
                    ),
                ],
            ),
            TaskCategory(
                name="extraction",
                description="Extract structured data from unstructured text",
                recommended_patterns=["structured_output", "few_shot"],
                examples=[
                    TaskExample(
                        name="contact_extraction",
                        input_text="Call John at 555-0123 or email john@example.com",
                        expected_output=('{"name": "John", "phone": "555-0123", "email": "john@example.com"}'),
                        expected_topics=["name", "phone", "email"],
                    ),
                    TaskExample(
                        name="date_extraction",
                        input_text=("The meeting is scheduled for March 15, 2026 at 2pm EST."),
                        expected_output=('{"date": "2026-03-15", "time": "14:00", "timezone": "EST"}'),
                        expected_topics=["date", "time"],
                    ),
                ],
            ),
            TaskCategory(
                name="generation",
                description="Generate creative or business content",
                recommended_patterns=["role_play", "structured_output"],
                examples=[
                    TaskExample(
                        name="email_draft",
                        input_text=("Write a follow-up email after a sales call about our SaaS product."),
                        expected_output="Thank you for taking the time...",
                        expected_topics=["follow-up", "meeting", "next steps"],
                    ),
                ],
            ),
            TaskCategory(
                name="summarization",
                description="Condense long text into key points",
                recommended_patterns=["chain_of_thought", "decomposition"],
                examples=[
                    TaskExample(
                        name="article_summary",
                        input_text=(
                            "A long article about renewable energy trends in 2026, "
                            "covering solar, wind, and battery storage innovations."
                        ),
                        expected_output=(
                            "Key renewable energy trends include solar cost reduction, "
                            "offshore wind expansion, and improved battery storage."
                        ),
                        expected_topics=["solar", "wind", "battery"],
                        context="Renewable energy article content here.",
                    ),
                ],
            ),
            TaskCategory(
                name="qa",
                description="Answer questions from provided context",
                recommended_patterns=["rag", "chain_of_thought"],
                examples=[
                    TaskExample(
                        name="policy_qa",
                        input_text="What is the return policy for electronics?",
                        expected_output=("Electronics can be returned within 30 days with original receipt."),
                        expected_topics=["return", "days", "receipt"],
                        context=(
                            "Our return policy: Electronics 30 days with receipt. "
                            "Clothing 60 days. No returns on sale items."
                        ),
                    ),
                ],
            ),
            TaskCategory(
                name="analysis",
                description="Analyze data, trends, or complex scenarios",
                recommended_patterns=["chain_of_thought", "decomposition"],
                examples=[
                    TaskExample(
                        name="market_analysis",
                        input_text=("Analyze the competitive landscape for AI coding assistants."),
                        expected_output=(
                            "The AI coding assistant market features GitHub Copilot, Cursor, and Claude Code..."
                        ),
                        expected_topics=["competitors", "market", "trends"],
                    ),
                ],
            ),
            TaskCategory(
                name="transformation",
                description="Transform data between formats or styles",
                recommended_patterns=["structured_output", "few_shot"],
                examples=[
                    TaskExample(
                        name="csv_to_json",
                        input_text="name,age,city\nAlice,30,NYC\nBob,25,LA",
                        expected_output=(
                            '[{"name": "Alice", "age": 30, "city": "NYC"}, {"name": "Bob", "age": 25, "city": "LA"}]'
                        ),
                        expected_topics=["name", "age", "city"],
                    ),
                ],
            ),
        ]
        for c in categories:
            self._categories[c.name] = c

    def get(self, name: str) -> TaskCategory | None:
        """Get a category by name."""
        return self._categories.get(name)

    def list_categories(self) -> list[TaskCategory]:
        """List all categories."""
        return list(self._categories.values())

    def get_names(self) -> list[str]:
        """Get all category names."""
        return list(self._categories.keys())

    def get_examples(self, category_name: str) -> list[TaskExample]:
        """Get examples for a category."""
        cat = self._categories.get(category_name)
        return cat.examples if cat else []

    def register(self, category: TaskCategory) -> None:
        """Register a custom category."""
        self._categories[category.name] = category
