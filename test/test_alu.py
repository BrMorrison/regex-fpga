# top = regex::alu::alu_test_harness

import cocotb
from spade import SpadeExt
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge

def to_int(c: str) -> int:
    return int.from_bytes(c.encode('utf-8'))

def _assert_outputs(dut, failure, consume, jump):
    dut.o.failure.assert_eq(failure)
    dut.o.consume.assert_eq(consume)
    dut.o.jump.assert_eq(jump)

def assert_failure(dut):
    _assert_outputs(dut, True, False, False)

def assert_consume(dut):
    _assert_outputs(dut, False, True, False)

def assert_jump(dut):
    _assert_outputs(dut, False, False, True)

def assert_none(dut):
    _assert_outputs(dut, False, False, False)

def _set_inputs(dut, branch: bool, inverted: bool, char_min: str, char_max: str):
    dut.i.i_consume = not branch
    dut.i.i_inverted = inverted
    dut.i.i_char_min = to_int(char_min)
    dut.i.i_char_max = to_int(char_max)

def set_compare(dut, char_min: str, char_max: str):
    _set_inputs(dut, False, False, char_min, char_max)

def set_inv_compare(dut, char_min: str, char_max: str):
    _set_inputs(dut, False, True, char_min, char_max)

def set_branch(dut, char_min: str, char_max: str):
    _set_inputs(dut, True, False, char_min, char_max)

@cocotb.test()
async def test(dut):
    s = SpadeExt(dut)
    clk = dut.clk_i
    await cocotb.start(Clock(
        clk,
        period=10,
        units='ns'
    ).start())

    # Initialize Inputs
    s.i.i_char = 0
    s.i.i_consume = False
    s.i.i_inverted = False
    s.i.i_char_min = 0
    s.i.i_char_max = 0

    await FallingEdge(clk)
    await FallingEdge(clk)

    # Test Compare - Single character equal
    set_compare(s, 'a', 'a')
    s.i.i_char = to_int('a')
    await FallingEdge(clk)
    assert_consume(s)

    # Test Compare Inverted - Single character equal
    set_inv_compare(s, 'a', 'a')
    s.i.i_char = to_int('a')
    await FallingEdge(clk)
    assert_failure(s)

    # Test Compare - Single character not equal
    set_compare(s, 'a', 'a')
    s.i.i_char = to_int('b')
    await FallingEdge(clk)
    assert_failure(s)

    # Test Compare Inverted - Single character not equal
    set_inv_compare(s, 'a', 'a')
    s.i.i_char = to_int('b')
    await FallingEdge(clk)
    assert_consume(s)

    # Test Compare - Character range equal
    set_compare(s, 'a', 'c')
    s.i.i_char = to_int('b')
    await FallingEdge(clk)
    assert_consume(s)

    # Test Branch - Character range equal
    set_branch(s, 'a', 'c')
    s.i.i_char = to_int('b')
    await FallingEdge(clk)
    assert_jump(s)

    # Test Branch - Character range not equal
    set_branch(s, 'a', 'c')
    s.i.i_char = to_int('d')
    await FallingEdge(clk)
    assert_none(s)

    await FallingEdge(clk)
    await FallingEdge(clk)
