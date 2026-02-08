"""Prompt Engineering Lab: Pattern Library, Evaluate, A/B Compare, Benchmarks."""

import streamlit as st

from prompt_lab.ab_tester import ABTester
from prompt_lab.benchmark import BenchmarkRunner
from prompt_lab.categories import CategoryRegistry
from prompt_lab.evaluator import PromptEvaluator
from prompt_lab.patterns import PatternLibrary
from prompt_lab.report_generator import ReportGenerator


def main():
    st.set_page_config(page_title="Prompt Engineering Lab", page_icon="🔬", layout="wide")
    st.title("🔬 Prompt Engineering Lab")
    st.caption("Pattern library, evaluation, and A/B testing for prompt engineering")

    library = PatternLibrary()
    evaluator = PromptEvaluator()
    categories = CategoryRegistry()

    tab_patterns, tab_evaluate, tab_ab, tab_benchmarks = st.tabs(
        ["📚 Pattern Library", "📊 Evaluate", "⚖️ A/B Compare", "🏆 Benchmarks"]
    )

    # Tab 1: Pattern Library
    with tab_patterns:
        st.subheader("Prompt Pattern Library")
        pattern_names = library.get_names()
        selected = st.selectbox("Select Pattern:", pattern_names)
        pattern = library.get(selected)
        if pattern:
            st.markdown(f"**Description**: {pattern.description}")
            st.markdown(f"**Variables**: {', '.join(pattern.variables)}")
            st.markdown(f"**Tags**: {', '.join(pattern.tags)}")
            st.code(pattern.template, language="text")

            if pattern.example_input:
                st.markdown("**Example:**")
                rendered = pattern.render_example()
                st.code(rendered, language="text")
                if pattern.example_output:
                    st.markdown(f"**Expected Output**: {pattern.example_output}")

    # Tab 2: Evaluate
    with tab_evaluate:
        st.subheader("Evaluate Prompt Output")
        query = st.text_area("Query/Input:", "What is the return policy?")
        context = st.text_area(
            "Context:", "Return policy: 30 days for electronics, 60 days for clothing."
        )
        output = st.text_area("LLM Output:", "Electronics can be returned within 30 days.")
        topics = st.text_input("Expected Topics (comma-separated):", "return, days, electronics")

        if st.button("Evaluate"):
            topic_list = [t.strip() for t in topics.split(",") if t.strip()]
            result = evaluator.evaluate(
                output, query=query, context=context, expected_topics=topic_list
            )
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Faithfulness", f"{result.faithfulness:.2%}")
            col2.metric("Relevance", f"{result.relevance:.2%}")
            col3.metric("Completeness", f"{result.completeness:.2%}")
            col4.metric("Overall", f"{result.overall:.2%}")

    # Tab 3: A/B Compare
    with tab_ab:
        st.subheader("A/B Pattern Comparison")
        col1, col2 = st.columns(2)
        pattern_a = col1.selectbox("Pattern A:", pattern_names, key="ab_a")
        pattern_b = col2.selectbox("Pattern B:", pattern_names, index=1, key="ab_b")

        cat_names = categories.get_names()
        selected_cat = st.selectbox("Test Category:", cat_names)

        if st.button("Run A/B Test"):
            examples = categories.get_examples(selected_cat)
            if not examples:
                st.warning("No examples in this category.")
            else:
                scores_a = []
                scores_b = []
                for ex in examples:
                    eval_a = evaluator.evaluate(
                        ex.expected_output,
                        query=ex.input_text,
                        context=ex.context,
                        expected_topics=ex.expected_topics,
                    )
                    eval_b = evaluator.evaluate(
                        ex.expected_output,
                        query=ex.input_text,
                        context=ex.context,
                        expected_topics=ex.expected_topics,
                    )
                    scores_a.append(eval_a.overall)
                    scores_b.append(eval_b.overall)

                tester = ABTester()
                result = tester.compare(scores_a, scores_b, pattern_a, pattern_b)

                reporter = ReportGenerator()
                st.markdown(reporter.ab_test_report(result))

    # Tab 4: Benchmarks
    with tab_benchmarks:
        st.subheader("Pattern Benchmarks")
        if st.button("Run Benchmarks"):
            runner = BenchmarkRunner()
            patterns = library.list_patterns()

            tasks = []
            for cat in categories.list_categories():
                for ex in cat.examples:
                    task = {
                        "name": f"{cat.name}/{ex.name}",
                        "query": ex.input_text,
                        "context": ex.context,
                        "expected_topics": ex.expected_topics,
                        "default_output": ex.expected_output,
                        "variables": {},
                        "mock_outputs": {},
                    }
                    for p in patterns:
                        if "problem" in p.variables:
                            task["variables"][p.name] = {"problem": ex.input_text}
                        elif "question" in p.variables and "context" in p.variables:
                            task["variables"][p.name] = {
                                "question": ex.input_text,
                                "context": ex.context or "No context provided.",
                            }
                        elif "task" in p.variables and "tools" not in p.variables:
                            task["variables"][p.name] = {"task": ex.input_text}
                        task["mock_outputs"][p.name] = ex.expected_output
                    tasks.append(task)

            report = runner.run_comparison(patterns, tasks)
            reporter = ReportGenerator()
            st.markdown(reporter.summary_table(report))
            st.markdown("---")
            st.markdown(reporter.benchmark_table(report))


if __name__ == "__main__":
    main()
