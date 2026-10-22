"""Static checks for resource handling in the package metadata."""

import ast
from pathlib import Path


def test_setup_reads_readme_inside_a_context_manager():
    setup_tree = ast.parse((Path(__file__).parents[1] / "setup.py").read_text())

    readme_contexts = [
        node
        for node in ast.walk(setup_tree)
        if isinstance(node, ast.With)
        and any(
            isinstance(item.context_expr, ast.Call)
            and isinstance(item.context_expr.func, ast.Name)
            and item.context_expr.func.id == "open"
            and item.context_expr.args
            and isinstance(item.context_expr.args[0], ast.Constant)
            and item.context_expr.args[0].value == "README.md"
            for item in node.items
        )
    ]

    assert len(readme_contexts) == 1
    assert any(
        isinstance(node, ast.Assign)
        and isinstance(node.targets[0], ast.Name)
        and node.targets[0].id == "long_description"
        and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Attribute)
        and isinstance(node.value.func.value, ast.Name)
        and node.value.func.value.id == "readme"
        and node.value.func.attr == "read"
        for node in ast.walk(readme_contexts[0])
    )
