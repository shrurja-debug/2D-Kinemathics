from project import get_values
from project import get_result
from project import get_units
import pytest
import sympy
# input validation


def test_values_valid_and_questionconversion(monkeypatch):
    inputs = iter([
        "30",  # theta
        "40",  # vi
        "?",   # vix
        "?",   # viy
        "1",   # vf
        "?",   # vfx
        "?",   # vfy
        "-10",  # a
        "?",   # ax
        "?",   # ay
        "-35",  # d
        "?",   # dx
        "?",   # dy
        "?",   # t
        "t"    # solve
    ])

    def fake_input(prompt):
        return next(inputs)
    monkeypatch.setattr("builtins.input", fake_input)
    result = get_values()
    assert result["theta"] == 30.0
    assert result["vi"] == 40.0
    assert result["vix"] == None
    assert result["viy"] == None
    assert result["vf"] == 1.0
    assert result["vfx"] == None
    assert result["vfy"] == None
    assert result["a"] == -10.0
    assert result["ax"] == None
    assert result["ay"] == None
    assert result["d"] == -35.0
    assert result["dx"] == None
    assert result["dy"] == None
    assert result["t"] == None
    assert result["solve"] == "t"


def test_values_invalid(monkeypatch):
    inputs = iter([
        "A",  # theta
        "B",  # vi
        "C",   # vix
        "D",   # viy
        "1",   # vf
        "?",   # vfx
        "?",   # vfy
        "-10",  # a
        "?",   # ax
        "?",   # ay
        "-35",  # d
        "?",   # dx
        "?",   # dy
        "?",   # t
        "t"    # solve
    ])

    def fake_input(prompt):
        return next(inputs)
    monkeypatch.setattr("builtins.input", fake_input)
    with pytest.raises(SystemExit):
        get_values()
# get_result calculations


def test_simple_acceleration_from_rest():
    values = {
        "theta": None,
        "vi": 0,
        "vix": None,
        "viy": None,
        "vf": None,
        "vfx": None,
        "vfy": None,
        "a": 10,
        "ax": None,
        "ay": None,
        "d": 50,
        "dx": None,
        "dy": None,
        "t": None,
        "solve": "vf"
    }
    solved, _ = get_result(values)
    assert solved[0] == -10*sympy.sqrt(10)


def test_time_with_zero_acceleration():
    values = {
        "theta": None,
        "vi": 5,
        "vix": None,
        "viy": None,
        "vf": 5,
        "vfx": None,
        "vfy": None,
        "a": 0,
        "ax": None,
        "ay": None,
        "d": 25,
        "dx": None,
        "dy": None,
        "t": None,
        "solve": "t"
    }
    solved, _ = get_result(values)
    # d=1/2at^2 +vit
    # 25=5t
    # t=5
    assert solved[0] == pytest.approx(5.0)


def test_projectile_max_height():
    values = {
        "theta": None,
        "vi": None,
        "vix": None,
        "viy": 14.14,  # 20*sin(45)
        "vf": None,
        "vfx": None,
        "vfy": 0,      # At max height
        "a": None,
        "ax": None,
        "ay": -9.8,
        "d": None,
        "dx": None,
        "dy": None,
        "t": None,
        "solve": "dy"
    }
    solved, _ = get_result(values)
    assert solved[0] == pytest.approx(10.20, rel=0.01)


def test_horizontal_launch():
    values = {
        "theta": None,
        "vi": None,
        "vix": 0,
        "viy": 0,
        "vf": None,
        "vfx": None,
        "vfy": None,
        "a": None,
        "ax": 0,
        "ay": -9.8,
        "d": None,
        "dx": 50,
        "dy": -20,
        "t": None,
        "solve": "t"
    }
    solved, _ = get_result(values)
    assert solved[0] == pytest.approx(2.02, rel=0.01)


def test_negative_time_solutions():
    values = {
        "theta": None,
        "vi": 10,
        "vix": None,
        "viy": None,
        "vf": 0,
        "vfx": None,
        "vfy": None,
        "a": -5,
        "ax": None,
        "ay": None,
        "d": None,
        "dx": None,
        "dy": None,
        "t": None,
        "solve": "t"
    }
    solved, _ = get_result(values)
    assert len(solved) == 1
    assert solved[0] == pytest.approx(2.00, rel=0.01)


def test_quadratic_two_positive_solutions():
    values = {
        "theta": None,
        "vi": 0,
        "vix": None,
        "viy": None,
        "vf": None,
        "vfx": None,
        "vfy": None,
        "a": 2,
        "ax": None,
        "ay": None,
        "d": 10,
        "dx": None,
        "dy": None,
        "t": None,
        "solve": "t"
    }
    solved, _ = get_result(values)
    assert solved[0] == pytest.approx(3.16, rel=0.01)
# component tests


def test_solving_for_vix_component():
    values = {
        "theta": None,
        "vi": None,
        "vix": None,
        "viy": None,
        "vf": None,
        "vfx": None,
        "vfy": None,
        "a": None,
        "ax": 2,
        "ay": None,
        "d": None,
        "dx": 20,
        "dy": None,
        "t": 4,
        "solve": "vix"
    }
    solved, _ = get_result(values)
    # dx = vix*t + 0.5*ax*t^2
    # 20 = vix*4 + 0.5*2*16
    # vix = 1
    assert solved[0] == pytest.approx(1.00, rel=0.01)


def test_solving_for_vfy_component():
    values = {
        "theta": None,
        "vi": None,
        "vix": None,
        "viy": 0,
        "vf": None,
        "vfx": None,
        "vfy": None,
        "a": None,
        "ax": None,
        "ay": -9.8,
        "d": None,
        "dx": None,
        "dy": -20,
        "t": None,
        "solve": "vfy"
    }
    solved, _ = get_result(values)
    # vfy^2 = viy^2 + 2*ay*dy
    # vfy^2 = 0 + 2*(-9.8)*(-20) = 392
    # vfy = -19.80
    assert solved[0] == pytest.approx(-19.80, rel=0.01)


def test_conflict_givenvx_with_theta():
    values = {
        "theta": 45,
        "vi": 20,
        "vix": 10,  # should be 20*cos(45)=14.14
        "viy": None,
        "vf": None,
        "vfx": None,
        "vfy": None,
        "a": None,
        "ax": None,
        "ay": -9.8,
        "d": None,
        "dx": None,
        "dy": None,
        "t": None,
        "solve": "dy"
    }
    with pytest.raises(SystemExit):
        get_result(values)
# Units


def test_units_for_each_variable():
    """Test that get_units returns correct units"""
    assert get_units({"solve": "vi"}) == "m/s"
    assert get_units({"solve": "vix"}) == "m/s"
    assert get_units({"solve": "vf"}) == "m/s"
    assert get_units({"solve": "a"}) == "m/s^2"
    assert get_units({"solve": "ax"}) == "m/s^2"
    assert get_units({"solve": "d"}) == "m"
    assert get_units({"solve": "dx"}) == "m"
    assert get_units({"solve": "t"}) == "s"
