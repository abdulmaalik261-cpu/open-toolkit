from open_toolkit.commands.fizzbuzz import FizzBuzzOrchestrationEngine


def test_standard_cases():
    engine = FizzBuzzOrchestrationEngine()
    assert engine.process(1) == "1"
    assert engine.process(3) == "Fizz"
    assert engine.process(5) == "Buzz"
    assert engine.process(15) == "FizzBuzz"
    assert engine.process(7) == "7"


def test_execute_range():
    engine = FizzBuzzOrchestrationEngine()
    result = engine.execute(1, 15)
    assert result == [
        "1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8",
        "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz",
    ]
