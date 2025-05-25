# top = processor::processor_test_harness

from compiler.instruction import *
from compiler.assembler import assemble

import cocotb
from spade import SpadeExt
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge

def to_int(c: str) -> int:
    return int.from_bytes(c.encode('utf-8'))

@cocotb.test()
async def test(dut):
    s = SpadeExt(dut)
    clk = dut.clk_i
    await cocotb.start(Clock(
        clk,
        period=10,
        units='ns'
    ).start())

    s.i.rst = True
    s.i.instruction = 0
    s.i.string = 0
    await FallingEdge(clk)
    s.i.rst = False

    s.i.instruction = assemble(Branch('a', 'c', 32))
    s.i.string = to_int('b')
    await FallingEdge(clk)
    await FallingEdge(clk)
    await FallingEdge(clk)
