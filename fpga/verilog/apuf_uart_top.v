module apuf_uart_top (
    input  wire CLK100MHZ,
    input  wire RsRx,     // UART RX from PC
    output wire RsTx,     // UART TX to PC
    output wire LED0,     // Debug LED
    input  wire rstn
);

    // UART RX signals
    wire [7:0]  last_byte;
    wire [31:0] challenge;
    wire        byte_valid;
    wire        data_valid;

    reg         ack;
    wire        resp_bit;
    reg         resp_valid;

    // ================= UART RX =================
    uart_rx RX (
        .clk(CLK100MHZ),
        .rstn(rstn),
        .rxd(RsRx),
        .ack(ack),
        .last_byte(last_byte),
        .data_out(challenge),   // 32-bit
        .byte_valid(byte_valid),
        .data_valid(data_valid)
    );

    // ================= UART TX =================
    reg        start_tx;
    reg [7:0]  tx_data;
    wire       busy;

    uart_tx TX (
        .clk(CLK100MHZ),
        .rstn(rstn),
        .start_tx(start_tx),
        .tx_data(tx_data),
        .txd(RsTx),
        .busy(busy)
    );

    // ================= 32-bit APUF =================
    reg  puf_start;
    wire puf_done;

    arbiter_puf_core PUF (
        .clk(CLK100MHZ),
        .rstn(rstn),
        .challenge(challenge),
        .start(puf_start),
        .resp_bit(resp_bit),
        .done(puf_done)
    );

    assign LED0 = resp_bit;  // response on LED

    // ================= FSM =================
    reg [3:0] state;

    always @(posedge CLK100MHZ or negedge rstn) begin
        if (!rstn) begin
            state      <= 0;
            start_tx   <= 0;
            tx_data    <= 8'h00;
            ack        <= 0;
            puf_start  <= 0;
            resp_valid <= 0;
        end else begin
            start_tx <= 0;

            case (state)
                // Print "Rdy\n"
                0: if (!busy) begin tx_data <= "R"; start_tx <= 1; state <= 1; end
                1: if (!busy) begin tx_data <= "d"; start_tx <= 1; state <= 2; end
                2: if (!busy) begin tx_data <= "y"; start_tx <= 1; state <= 3; end
                3: if (!busy) begin tx_data <= "\n"; start_tx <= 1; state <= 4; end

                // Wait for 32-bit challenge
                4: begin
                    if (data_valid) begin
                        puf_start <= 1;
                        ack <= 1;
                        state <= 5;
                    end else begin
                        ack <= 0;
                    end
                end

                // Wait for PUF result
                5: begin
                    puf_start <= 0;
                    ack <= 0;
                    if (puf_done) begin
                        resp_valid <= 1;
                        state <= 6;
                    end
                end

                // Send response bit
                6: begin
                    if (!busy && resp_valid) begin
                        tx_data <= (resp_bit ? "1" : "0");
                        start_tx <= 1;
                        resp_valid <= 0;
                        state <= 4;
                    end
                end
            endcase
        end
    end
endmodule