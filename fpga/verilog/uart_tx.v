module uart_tx (
    input wire clk,
    input wire rstn,
    input wire start_tx,        // start transmission
    input wire [7:0] tx_data,   // data to transmit
    output reg txd,             // UART TX line
    output reg busy             // high while transmitting
);

    parameter BAUD_DIV = 10416; // 100MHz / 9600 baud

    reg [13:0] baud_cnt;
    reg [3:0] bit_cnt;
    reg [9:0] shift_reg;

    always @(posedge clk or negedge rstn) begin
        if (!rstn) begin
            txd <= 1;
            busy <= 0;
            baud_cnt <= 0;
            bit_cnt <= 0;
            shift_reg <= 10'b1111111111;
        end else begin
            if (start_tx && !busy) begin
                shift_reg <= {1'b1, tx_data, 1'b0}; // stop, data, start
                busy <= 1;
                baud_cnt <= 0;
                bit_cnt <= 0;
            end else if (busy) begin
                if (baud_cnt == BAUD_DIV-1) begin
                    baud_cnt <= 0;
                    txd <= shift_reg[0];
                    shift_reg <= {1'b1, shift_reg[9:1]};
                    bit_cnt <= bit_cnt + 1;
                    if (bit_cnt == 9) begin
                        busy <= 0;
                    end
                end else begin
                    baud_cnt <= baud_cnt + 1;
                end
            end
        end
    end
endmodule