# top = regex::processor::processor_test_harness

import recompile.instruction as inst
from recompile.assembler import assemble

_op_consume = assemble(inst.Branch(True, False, 0, 0x00, 0xff))
_op_die = assemble(inst.Branch(True, True, 0, 0x00, 0xff))
_op_match = assemble(inst.Save(0, True))
def _op_jump(dest: int) -> int:
    return assemble(inst.Branch(False, False, dest, 0x00, 0xff))

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

    s.i.instruction = _op_jump(100) #  in: 0

    await FallingEdge(clk)
    s.i.instruction = _op_consume   #  in: 1

    await FallingEdge(clk)
    s.i.instruction = _op_consume   #  in: 2
    s.o.stopped.assert_eq(False)    # out: 0
    s.o.success.assert_eq(False)    # out: 0
    s.o.pc.assert_eq(100)           # out: 0
    s.o.sc.assert_eq(0)             # out: 0

    await FallingEdge(clk)
    s.i.instruction = _op_match     #  in: 3
    s.o.stopped.assert_eq(False)    # out: 1
    s.o.success.assert_eq(False)    # out: 1
    s.o.pc.assert_eq(101)           # out: 1
    s.o.sc.assert_eq(1)             # out: 1

    await FallingEdge(clk)
    s.i.instruction = _op_consume   #  in: 4
    s.o.stopped.assert_eq(False)    # out: 1
    s.o.success.assert_eq(False)    # out: 1
    s.o.pc.assert_eq(102)           # out: 2
    s.o.sc.assert_eq(2)             # out: 2

    await FallingEdge(clk)
    s.i.instruction = _op_die       #  in: 5
    s.o.stopped.assert_eq(True)     # out: 3
    s.o.success.assert_eq(True)     # out: 3
    s.o.pc.assert_eq(102)           # out: 3
    s.o.sc.assert_eq(2)             # out: 3

    await FallingEdge(clk)
    s.o.stopped.assert_eq(True)     # out: 4
    s.o.success.assert_eq(True)     # out: 4
    s.o.pc.assert_eq(102)           # out: 4
    s.o.sc.assert_eq(2)             # out: 4

    await FallingEdge(clk)
    s.o.stopped.assert_eq(True)     # out: 5
    s.o.success.assert_eq(True)     # out: 5
    s.o.pc.assert_eq(102)           # out: 5
    s.o.sc.assert_eq(2)             # out: 5

    await FallingEdge(clk)