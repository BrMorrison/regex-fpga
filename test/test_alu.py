# top = alu::alu_test_harness

import cocotb
from spade import SpadeExt
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge

from enum import IntEnum

def to_int(c: str) -> int:
    return int.from_bytes(c.encode('utf-8'))

class OpCode(IntEnum):
    Match   = 0
    Die     = 1
    Consume = 2
    Jump    = 3
    Split   = 4
    Compare = 5
    OptCompare = 6

@cocotb.test()
async def test(dut):
    s = SpadeExt(dut)
    clk = dut.clk_i
    await cocotb.start(Clock(
        clk,
        period=10,
        units='ns'
    ).start())

    # Initialize inputs and test Match
    s.i.i_pc = 0
    s.i.i_char = 0
    s.i.i_op = OpCode.Match.value
    s.i.i_inverted_op = False
    s.i.i_char_op1 = 0
    s.i.i_char_op2 = 0
    s.i.i_dest_op1 = 0
    s.i.i_dest_op2 = 0

    await FallingEdge(clk)
    await FallingEdge(clk)
    s.o.success.assert_eq(True)

    # Test Jump
    s.i.i_op = OpCode.Jump.value
    s.i.i_dest_op1 = 123
    await FallingEdge(clk)
    s.o.pc_out.assert_eq(123)

    # Test Split
    s.i.i_op = OpCode.Split.value
    s.i.i_dest_op1 = 45
    s.i.i_dest_op2 = 67
    await FallingEdge(clk)
    s.o.pc_out.assert_eq(45)
    s.o.spawn.assert_eq(True)
    s.o.spawn_addr.assert_eq(67)

    # Test Compare - Single character equal
    s.i.i_op = OpCode.Compare.value
    s.i.i_pc = 99
    s.i.i_inverted_op = False
    s.i.i_char_op1 = to_int('a')
    s.i.i_char_op2 = to_int('a')
    s.i.i_char = to_int('a')
    await FallingEdge(clk)
    s.o.pc_out.assert_eq(100)
    s.o.consume.assert_eq(True)

    # Test Compare Inverted - Single character equal
    s.i.i_op = OpCode.Compare.value
    s.i.i_pc = 100
    s.i.i_inverted_op = True
    s.i.i_char_op1 = to_int('a')
    s.i.i_char_op2 = to_int('a')
    s.i.i_char = to_int('a')
    await FallingEdge(clk)
    s.o.failure.assert_eq(True)

    # Test Compare - Single character not equal
    s.i.i_op = OpCode.Compare.value
    s.i.i_pc = 101
    s.i.i_inverted_op = False
    s.i.i_char_op1 = to_int('a')
    s.i.i_char_op2 = to_int('a')
    s.i.i_char = to_int('b')
    await FallingEdge(clk)
    s.o.failure.assert_eq(True)

    # Test Compare Inverted - Single character not equal
    s.i.i_op = OpCode.Compare.value
    s.i.i_pc = 101
    s.i.i_inverted_op = True
    s.i.i_char_op1 = to_int('a')
    s.i.i_char_op2 = to_int('a')
    s.i.i_char = to_int('b')
    await FallingEdge(clk)
    s.o.consume.assert_eq(True)
    s.o.pc_out.assert_eq(102)

    # Test Compare - Character range equal
    s.i.i_op = OpCode.Compare.value
    s.i.i_pc = 102
    s.i.i_inverted_op = False
    s.i.i_char_op1 = to_int('a')
    s.i.i_char_op2 = to_int('c')
    s.i.i_char = to_int('b')
    await FallingEdge(clk)
    s.o.pc_out.assert_eq(103)
    s.o.consume.assert_eq(True)

    # Test OptCompare - Character range equal
    s.i.i_op = OpCode.OptCompare.value
    s.i.i_pc = 103
    s.i.i_inverted_op = False
    s.i.i_char_op1 = to_int('a')
    s.i.i_char_op2 = to_int('c')
    s.i.i_char = to_int('b')
    s.i.i_dest_op1 = 13
    await FallingEdge(clk)
    s.o.pc_out.assert_eq(13)

    # Test OptCompare - Character range not equal
    s.i.i_op = OpCode.OptCompare.value
    s.i.i_pc = 103
    s.i.i_inverted_op = False
    s.i.i_char_op1 = to_int('a')
    s.i.i_char_op2 = to_int('c')
    s.i.i_char = to_int('d')
    s.i.i_dest_op1 = 13
    await FallingEdge(clk)
    s.o.pc_out.assert_eq(104)

    await FallingEdge(clk)
    await FallingEdge(clk)
