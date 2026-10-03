# XDC File for Artix-7 xc7a35tcpg236-1 (Basys3)
# Complete constraints for arbiter_puf_top_uart project
set_property CFGBVS VCCO [current_design]
set_property CONFIG_VOLTAGE 3.3 [current_design]

# Clock Signal (100 MHz) - Correct pin for xc7a35tcpg236-1
set_property PACKAGE_PIN W5 [get_ports CLK100MHZ]
set_property IOSTANDARD LVCMOS33 [get_ports CLK100MHZ]
create_clock -period 10.000 -name sys_clk_pin -waveform {0 5} [get_ports CLK100MHZ]

# USB-UART Interface
set_property PACKAGE_PIN B18 [get_ports RsRx]
set_property IOSTANDARD LVCMOS33 [get_ports RsRx]

set_property PACKAGE_PIN A18 [get_ports RsTx]
set_property IOSTANDARD LVCMOS33 [get_ports RsTx]

# LED0 (debug: will mirror resp_bit)
set_property PACKAGE_PIN U16 [get_ports LED0]
set_property IOSTANDARD LVCMOS33 [get_ports LED0]


# Reset Button (Using Center Button - active low)
set_property PACKAGE_PIN U18 [get_ports rstn]
set_property IOSTANDARD LVCMOS33 [get_ports rstn]
set_property PULLUP true [get_ports rstn]

# Signal Integrity Settings
set_property DRIVE 8 [get_ports {RsTx}]
set_property SLEW SLOW [get_ports {RsTx}]