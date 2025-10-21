#!/usr/bin/env python3
"""
Main application for Olympus NDT-35DL communication
"""

from device_communication import DeviceCommunication
from device_testing import DeviceTesting


def print_separator(title, char="=", width=60):
    """Print a formatted separator with title"""
    print(f"\n{char * width}")
    print(f"{title:^{width}}")
    print(f"{char * width}")


def show_menu():
    """Show testing options menu"""
    print("\nTesting Options:")
    print("1. Quick test (basic commands only)")
    print("2. Full command probe (all categories)")
    print("3. Measurement focus (measurement commands only)")
    print("4. File system probe (discover stored files)")
    print("5. Live monitoring (find and monitor live readings)")
    print("6. Custom command test")
    print("7. Exit")
    print("8. Recall Stored Data by Index (NEW)")
    return input("Select option (1-8): ").strip()


def main():
    print_separator("Olympus NDT-35DL Communication Tool")
    
    # Initialize communication
    comm = DeviceCommunication()
    
    # Find and connect to device
    print("Searching for devices...")
    devices = comm.find_olympus_devices()
    if not devices:
        print("No potential Olympus devices found")
        return
    
    # Try to connect
    print("Attempting to connect...")
    if not comm.connect_via_pyvisa():
        if devices and not comm.connect_raw_usb(devices[0]):
            print("Failed to connect to device")
            return
    
    # Initialize testing
    tester = DeviceTesting(comm)
    
    try:
        # Always start with basic connectivity test
        print_separator("Basic Connectivity Test", "-")
        print("Testing basic commands...")
        
        basic_success = 0
        basic_commands = ["VER?", "ID?", "UNITS?", "RANGE?"]
        
        for cmd in basic_commands:
            if tester.test_single_command(cmd):
                basic_success += 1
        
        print(f"\nBasic connectivity: {basic_success}/{len(basic_commands)} commands working")
        
        if basic_success == 0:
            print("No basic commands working. Device may not be responding correctly.")
            return
        
        # Show current device state
        print_separator("Current Device State", "-")
        tester.analyze_current_state()
        
        # Interactive menu for different testing modes
        while True:
            choice = show_menu()
            
            if choice == "1":
                print_separator("Quick Test", "-")
                # Test only essential commands
                essential_commands = [
                    "VER?", "ID?", "UNITS?", "RANGE?", "VELOCITY?", 
                    "ZERO?", "MEMORY?", "MODE?", "STATUS?", "MEAS?"
                ]
                for cmd in essential_commands:
                    tester.test_single_command(cmd)
                    
            elif choice == "2":
                print_separator("Full Command Probe", "-")
                working_commands = tester.probe_all_commands()
                print(f"Found {len(working_commands)} working commands")
                
            elif choice == "3":
                print_separator("Measurement Commands", "-")
                measurement_commands = tester.probe_measurement_commands()
                print(f"Found {len(measurement_commands)} working measurement commands")
                
            elif choice == "4":
                print_separator("File System Probe", "-")
                file_results = tester.probe_file_system()
                print(f"Found {len(file_results)} working file system commands")
                
            elif choice == "5":
                print_separator("Live Monitoring", "-")
                live_reading = tester.get_live_reading()
                
                if live_reading:
                    duration = input("Monitor duration in seconds (default 30): ").strip()
                    try:
                        duration = int(duration) if duration else 30
                    except ValueError:
                        duration = 30
                    tester.monitor_readings(duration)
                else:
                    print("No live reading commands found")
                    
            elif choice == "6":
                print_separator("Custom Command Test", "-")
                while True:
                    cmd = input("Enter command to test (or 'back' to return): ").strip()
                    if cmd.lower() == 'back':
                        break
                    if cmd:
                        tester.test_single_command(cmd)
                        
            elif choice == "7":
                break
            
            elif choice == "8":
                print_separator("Recall Stored Data by Index", "-")
                mem_response = comm.send_command("MEMORY?")
                file_count = 0

                if mem_response and "ER:" not in mem_response and "TIMEOUT" not in mem_response:
                    try:
                        # Expected format: "TOTAL_MEM USED_MEM FILE_COUNT ...". Take the 3rd value.
                        file_count = int(mem_response.split()[2])
                        print(f"Device reports {file_count} stored records. Attempting recall...")
                    except (ValueError, IndexError):
                        print(f"Could not parse file count from MEMORY? response: '{mem_response}'")
                else:
                    print(f"Could not get file count from MEMORY? command. Response: '{mem_response}'")

                if file_count == 0:
                    try:
                        # Manual fallback
                        count_input = input("Enter number of files to test manually (e.g., 24): ").strip()
                        file_count = int(count_input) if count_input else 0
                    except ValueError:
                        print("Invalid number. Aborting recall test.")
                        continue
                
                if file_count > 0:
                    # Expanded list of commands to try for fetching data
                    # These will be tried in both one-step and two-step recalls.
                    fetch_commands = [
                        "DATA?", "MEAS?", "DUMP?", "TABLE?", "MEASUREMENTS?", 
                        "THICKNESS?", "SEND?", "FETCH?", "GET?"
                    ]
                    
                    # Commands to select a file index (for two-step recall)
                    select_formats = ["ID:{i:03d}", "RECALL:{i:03d}", "{i:03d}", "FILE:{i:03d}"]

                    for i in range(1, file_count + 1):
                        print(f"\n--- Testing Index {i} ---")
                        found_data = False

                        # --- STRATEGY 1: Two-Step Recall (Select, then Fetch) ---
                        for sel_fmt in select_formats:
                            select_cmd = sel_fmt.format(i=i)
                            # Send the selection command (don't expect a useful response)
                            comm.send_command_with_timeout(select_cmd, timeout_ms=1000)
                            
                            # Now, try to fetch the data
                            for fetch_cmd in fetch_commands:
                                response = comm.send_command_with_timeout(fetch_cmd, timeout_ms=3000)
                                if response and response not in ["ER:UNKNOWN COMMAND", "TIMEOUT", "OK"]:
                                    print(f"*** SUCCESS (2-Step): Sent '{select_cmd}', then '{fetch_cmd}' -> {response} ***")
                                    found_data = True
                                    break 
                            if found_data:
                                break
                        
                        if found_data:
                            continue # Move to the next index

                        # --- STRATEGY 2: One-Step Recall (Direct Query) ---
                        for fetch_cmd_base in [cmd.replace('?', '') for cmd in fetch_commands]:
                            # e.g., create "DATA:001?"
                            query_cmd = f"{fetch_cmd_base}:{i:03d}?"
                            response = comm.send_command_with_timeout(query_cmd, timeout_ms=3000)
                            if response and response not in ["ER:UNKNOWN COMMAND", "TIMEOUT", "OK"]:
                                print(f"*** SUCCESS (1-Step): Sent '{query_cmd}' -> {response} ***")
                                found_data = True
                                break
                else:
                    print("No file count specified. Aborting recall test.")
            else:
                print("Invalid choice, please try again")
        
        # Save results and show summary
        print_separator("Saving Results", "-")
        tester.save_results()
        
        # Clean summary without duplicates
        unique_working_commands = list(set(tester.working_commands))
        
        print_separator("FINAL SUMMARY")
        print(f"Total unique working commands: {len(unique_working_commands)}")
        
        if unique_working_commands:
            print("\nWorking Commands:")
            print("-" * 40)
            for cmd, resp in sorted(unique_working_commands):
                print(f"{cmd:12} -> {resp}")
            
            # Highlight key findings
            print("\nKey Findings:")
            print("-" * 20)
            
            # Check for measurement capabilities
            measurement_indicators = [cmd for cmd, resp in unique_working_commands 
                                    if any(keyword in cmd.upper() for keyword in 
                                          ['MEAS', 'THICK', 'RANGE', 'READ', 'DATA'])]
            if measurement_indicators:
                print(f"• Measurement commands found: {', '.join(measurement_indicators)}")
            
            # Check RANGE? value (likely current thickness)
            range_value = next((resp for cmd, resp in unique_working_commands if cmd == "RANGE?"), None)
            if range_value:
                try:
                    float(range_value)
                    print(f"• Current thickness reading: {range_value} (from RANGE?)")
                except ValueError:
                    pass
            
            # Show device info
            version = next((resp for cmd, resp in unique_working_commands if cmd == "VER?"), None)
            device_id = next((resp for cmd, resp in unique_working_commands if cmd == "ID?"), None)
            units = next((resp for cmd, resp in unique_working_commands if cmd == "UNITS?"), None)
            
            if version:
                print(f"• Device version: {version}")
            if device_id:
                print(f"• Device ID: {device_id}")
            if units:
                print(f"• Measurement units: {units}")
        
        print(f"\nResults saved to: olympus_test_results.txt")
        
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        comm.disconnect()


if __name__ == "__main__":
    main()