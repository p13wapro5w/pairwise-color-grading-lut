import pytest
import math
from render import color_grading_lut as mod

CASES = [
    ("clamp", 'm.domain_clamp(1.2, 0, 1) == 1.0'),
    ("size", 'm.cube_size(4) == 16'),
    ("alpha", 'm.apply_alpha(2, 0.5) == approx(1.0)'),
    ("once", 'm.tonemap_once(True) is False'),
    ("cdl", 'm.cdl_order("cdl-then-lut") == "cdl-then-lut"'),
    ("cache", 'm.cache_key("a.cube", 3) == "a.cube:3"'),
    ("transfer", 'm.transfer(0.5, 2) == approx(0.25)'),
    ("float", 'm.float_sample(0.5) == 0.5'),
    ("edge", 'm.lut_edge(1.0) is True'),
    ("index", 'm.cube_index(1, 2, 3, 4) == 27'),
    ("tetra", 'm.tetra_count(0) == 6'),
    ("key", 'm.color_key(3, 2) == "3:2"'),
    ("sat", 'm.saturation(0.2, 0.8, 0.4) == approx(0.6)'),
    ("linear", 'm.is_linear("linear") is True'),
    ("decode", 'm.gamma_decode(0.5) == approx(0.2176, abs=1e-3)')
]

@pytest.mark.parametrize("name,expr", CASES, ids=[c[0] for c in CASES])
def test_contract(name, expr):
    assert eval(expr, {"m": mod, "approx": pytest.approx, "math": math})
