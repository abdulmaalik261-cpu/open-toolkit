"""
toolkit fizzbuzz — FizzBuzzEnterpriseEdition(TM), the Python port.

A satirical, wildly over-engineered FizzBuzz: abstract factories, a
strategy registry, a visitor, dependency "injection" via a container,
and a plugin system. It still just prints Fizz, Buzz, and FizzBuzz.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional


# ---------------------------------------------------------------------------
# Domain layer (yes, FizzBuzz has a domain layer now)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class NumberPrintedEvent:
    value: int
    rendered: str


class OutputStrategy(ABC):
    @abstractmethod
    def matches(self, n: int) -> bool: ...

    @abstractmethod
    def render(self, n: int) -> str: ...


class DivisibilityStrategy(OutputStrategy):
    """A strategy that fires when n is divisible by `divisor`."""

    def __init__(self, divisor: int, word: str):
        self._divisor = divisor
        self._word = word

    def matches(self, n: int) -> bool:
        return n % self._divisor == 0

    def render(self, n: int) -> str:
        return self._word


class IdentityStrategy(OutputStrategy):
    """The strategy of last resort: just say the number."""

    def matches(self, n: int) -> bool:
        return True

    def render(self, n: int) -> str:
        return str(n)


# ---------------------------------------------------------------------------
# Strategy registry / "plugin system"
# ---------------------------------------------------------------------------

class StrategyRegistry:
    def __init__(self):
        self._strategies: List[OutputStrategy] = []

    def register(self, strategy: OutputStrategy) -> "StrategyRegistry":
        self._strategies.append(strategy)
        return self

    def resolve(self, n: int) -> OutputStrategy:
        for strategy in self._strategies:
            if not isinstance(strategy, IdentityStrategy) and strategy.matches(n):
                return strategy
        return IdentityStrategy()


# ---------------------------------------------------------------------------
# Abstract factory for strategies, because `if` statements are not enterprise
# ---------------------------------------------------------------------------

class AbstractStrategyFactory(ABC):
    @abstractmethod
    def create(self) -> OutputStrategy: ...


class FizzStrategyFactory(AbstractStrategyFactory):
    def create(self) -> OutputStrategy:
        return DivisibilityStrategy(3, "Fizz")


class BuzzStrategyFactory(AbstractStrategyFactory):
    def create(self) -> OutputStrategy:
        return DivisibilityStrategy(5, "Buzz")


class FizzBuzzStrategyFactory(AbstractStrategyFactory):
    def create(self) -> OutputStrategy:
        return DivisibilityStrategy(15, "FizzBuzz")


DEFAULT_FACTORIES: List[AbstractStrategyFactory] = [
    FizzBuzzStrategyFactory(),  # order matters: 15 before 3 or 5
    FizzStrategyFactory(),
    BuzzStrategyFactory(),
]


# ---------------------------------------------------------------------------
# "Dependency injection" container
# ---------------------------------------------------------------------------

@dataclass
class FizzBuzzContainer:
    factories: List[AbstractStrategyFactory] = field(default_factory=lambda: list(DEFAULT_FACTORIES))
    on_event: Optional[Callable[[NumberPrintedEvent], None]] = None

    def build_registry(self) -> StrategyRegistry:
        registry = StrategyRegistry()
        for factory in self.factories:
            registry.register(factory.create())
        return registry


# ---------------------------------------------------------------------------
# Orchestrator / visitor
# ---------------------------------------------------------------------------

class FizzBuzzOrchestrationEngine:
    """The single responsibility of this class is to have way too many responsibilities."""

    def __init__(self, container: Optional[FizzBuzzContainer] = None):
        self._container = container or FizzBuzzContainer()
        self._registry = self._container.build_registry()

    def process(self, n: int) -> str:
        strategy = self._registry.resolve(n)
        rendered = strategy.render(n)
        if self._container.on_event:
            self._container.on_event(NumberPrintedEvent(value=n, rendered=rendered))
        return rendered

    def execute(self, start: int, end: int) -> List[str]:
        return [self.process(n) for n in range(start, end + 1)]


def run(args) -> int:
    engine = FizzBuzzOrchestrationEngine()
    for line in engine.execute(args.start, args.end):
        print(line)
    return 0


def add_subparser(subparsers):
    p = subparsers.add_parser(
        "fizzbuzz",
        help="Run the over-engineered Enterprise FizzBuzz (for fun)",
    )
    p.add_argument("start", nargs="?", type=int, default=1)
    p.add_argument("end", nargs="?", type=int, default=100)
    p.set_defaults(func=run)
