module uart_rx (
    input  wire        clk,           // 100 MHz
    input  wire        rstn,          // active low reset
    input  wire        rxd,           // UART RX
    input  wire        ack,           // acknowledge from top
    output reg  [7:0]  last_byte,     // last received byte
    output reg  [31:0] data_out,      // 32-bit challenge
    output reg         byte_valid,    // pulse per byte
    output reg         data_valid     // high when 4 bytes collected
);

    parameter BAUD_DIV   = 10416; // 9600 baud @ 100MHz
    parameter BYTE_COUNT = 4;     // 32-bit challenge

    reg [13:0] baud_cnt;
    reg [3:0]  bit_cnt;
    reg [2:0]  byte_cnt;
    reg [9:0]  rx_shift;
    reg        receiving;

    always @(posedge clk or negedge rstn) begin
        if (!rstn) begin
            baud_cnt   <= 0;
            bit_cnt    <= 0;
            byte_cnt   <= 0;
            rx_shift   <= 0;
            receiving  <= 0;
            last_byte  <= 0;
            data_out   <= 0;
            byte_valid <= 0;
            data_valid <= 0;
        end else begin
            byte_valid <= 0;

            // Clear after ACK
            if (data_valid) begin
                if (ack) begin
                    data_valid <= 0;
                    byte_cnt   <= 0;
                    data_out   <= 0;
                end
            end else begin
                if (!receiving) begin
                    if (rxd == 1'b0) begin   // start bit
                        receiving <= 1;
                        baud_cnt  <= BAUD_DIV / 2;
                        bit_cnt   <= 0;
                    end
                end else begin
                    if (baud_cnt == BAUD_DIV - 1) begin
                        baud_cnt <= 0;
                        bit_cnt  <= bit_cnt + 1;
                        rx_shift <= {rxd, rx_shift[9:1]};

                        if (bit_cnt == 9) begin
                            receiving  <= 0;
                            last_byte  <= rx_shift[8:1];
                            byte_valid <= 1;

                            // Shift into 32-bit register
                            data_out <= {data_out[23:0], rx_shift[8:1]};
                            byte_cnt <= byte_cnt + 1;

                            if (byte_cnt == BYTE_COUNT - 1)
                                data_valid <= 1;
                        end
                    end else begin
                        baud_cnt <= baud_cnt + 1;
                    end
                end
            end
        end
    end
endmodule