# APUF-IoT-Hardware-Security

A hardware-assisted IoT authentication prototype based on Arbiter PUFs implemented on a Basys 3 (Xilinx Artix-7) FPGA.

## Implementations

- `fpga/` â€” Verilog APUF and UART hardware design.
- `implementations/fpga_32bit/` â€” 32-bit APUF version using live FPGA responses over UART.
- `implementations/protocol_simulation/` â€” software/network-oriented authentication implementation from the thesis work.
- `data/crp/` â€” enrolled challenge-response pairs.
- `docs/` â€” thesis and project presentation.

## Important

The two Python implementations are intentionally kept separate because they implement different versions of the authentication flow.
