# top = util::mem::fifo_test_harness

import cocotb
from spade import SpadeExt
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge


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
    s.i.rst = True
    s.i.w_en = False
    s.i.r_en = False
    s.i.data_in = 0

    await FallingEdge(clk)
    s.i.rst = False
    s.o.empty.assert_eq(True)
    s.o.full.assert_eq(False)

    # Fill the FIFO
    s.i.w_en = True
    s.i.data_in = 1
    await FallingEdge(clk)
    s.o.empty.assert_eq(False)
    s.i.data_in = 2
    await FallingEdge(clk)
    s.i.data_in = 3
    await FallingEdge(clk)
    s.o.full.assert_eq(True)
    s.i.data_in = 4
    await FallingEdge(clk)
    s.i.w_en = False
    await FallingEdge(clk)

    # Drain the FIFO
    s.i.r_en = True
    await FallingEdge(clk)
    s.o.full.assert_eq(False)
    s.o.data.assert_eq(1)
    await FallingEdge(clk)
    s.o.data.assert_eq(2)
    await FallingEdge(clk)
    s.o.data.assert_eq(3)
    s.o.empty.assert_eq(True)

    # Simultaneous Read/Write
    s.i.w_en = True
    s.i.data_in = 4
    await FallingEdge(clk)
    s.o.empty.assert_eq(False)
    s.o.full.assert_eq(False)
    s.i.data_in = 5
    await FallingEdge(clk)
    s.o.empty.assert_eq(False)
    s.o.full.assert_eq(False)
    s.o.data.assert_eq(4)
    s.i.data_in = 6
    await FallingEdge(clk)
    s.o.empty.assert_eq(False)
    s.o.full.assert_eq(False)
    s.o.data.assert_eq(5)
    s.i.data_in = 7
    await FallingEdge(clk)
    s.o.empty.assert_eq(False)
    s.o.full.assert_eq(False)
    s.o.data.assert_eq(6)
    s.i.w_en = False
    await FallingEdge(clk)
    s.o.empty.assert_eq(True)
    s.o.data.assert_eq(7)

    await FallingEdge(clk)
    await FallingEdge(clk)
