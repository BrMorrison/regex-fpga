module synchronous_fifo #(parameter DEPTH=8) (
  input clk, rst,
  input w_en, r_en,
  input [7:0] data_in,
  output reg [7:0] data_out,
  output full,
  output empty
);

  reg [$clog2(DEPTH)-1:0] w_ptr, r_ptr;
  reg [7:0] fifo[DEPTH];

  assign full = ((w_ptr+1'b1) == r_ptr);
  assign empty = (w_ptr == r_ptr);
  
  // To write data to FIFO
  always@(posedge clk) begin
    if (rst) begin
      w_ptr <= 0;
    end else if(w_en & !full)begin
      fifo[w_ptr] <= data_in;
      w_ptr <= w_ptr + 1;
    end
  end
  
  // To read data from FIFO
  always@(posedge clk) begin
    if (rst) begin
      r_ptr <= 0;
      data_out <= 0;
    end else if(r_en & !empty) begin
      data_out <= fifo[r_ptr];
      r_ptr <= r_ptr + 1;
    end
  end

endmodule
