(* keep_hierarchy = "yes" *)
module arbiter_puf_core(
    input  wire        clk,
    input  wire        rstn,
    input  wire [31:0] challenge,
    input  wire        start,
    output reg         resp_bit,
    output reg         done
);

    // 32-stage delay paths
    wire [32:0] top;
    wire [32:0] bottom;

    // Initial values
    assign top[0]    = 1'b0;
    assign bottom[0] = 1'b1;

    genvar i;
    generate
        for (i = 0; i < 32; i = i + 1) begin : puf_stages
            // Simple 2:1 mux behavior
            assign top[i+1] =
                (challenge[i]) ? bottom[i] : top[i];

            assign bottom[i+1] =
                (challenge[i]) ? top[i] : bottom[i];
        end
    endgenerate

    // Arbiter logic
    reg start_d;

    always @(posedge clk or negedge rstn) begin
        if (!rstn) begin
            resp_bit <= 1'b0;
            done     <= 1'b0;
            start_d  <= 1'b0;
        end else begin
            start_d <= start;
            done    <= 1'b0;

            // Rising edge of start
            if (start && !start_d) begin
                resp_bit <= top[32]; // faster path wins
                done     <= 1'b1;
            end
        end
    end
endmodule