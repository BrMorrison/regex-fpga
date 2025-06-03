module memory #(parameter ADDR_BITS=8, parameter DATA_BITS=8) (
  input clk, rst,
  input w_en, r_en,
  input [ADDR_BITS-1:0] r_addr, w_addr,
  input [DATA_BITS-1:0] w_data,
  output reg [DATA_BITS-1:0] r_data
);

  reg [DATA_BITS-1:0] data[2 ** ADDR_BITS];

  // Write data to memory
  always@(posedge clk) begin
    if (w_en) begin
      data[w_addr] <= w_data;
    end
  end
  
  // Read Data from memory
  always@(posedge clk) begin
    if (rst) begin
      r_data <= 0;
    end else if (r_en) begin
      r_data <= data[r_addr];
    end else begin
      r_data <= r_data;
    end
  end

endmodule
