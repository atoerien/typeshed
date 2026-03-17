"""
behave is behaviour-driven development, Python style

Behavior-driven development (or BDD) is an agile software development
technique that encourages collaboration between developers, QA and
non-technical or business participants in a software project.

*behave* uses tests written in a natural language style, backed up by Python
code.

To get started, we recommend the `tutorial`_ and then the `test language`_ and
`api`_ references.

.. _`tutorial`: tutorial.html
.. _`test language`: gherkin.html
.. _`api`: api.html
"""

from behave.fixture import fixture as fixture, use_fixture as use_fixture
from behave.step_registry import (
    Given as Given,
    Step as Step,
    Then as Then,
    When as When,
    given as given,
    step as step,
    then as then,
    when as when,
)

__all__ = ["given", "when", "then", "step", "Given", "When", "Then", "Step", "use_fixture", "fixture"]
