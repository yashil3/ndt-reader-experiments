#!/usr/bin/env python3
"""
Device testing and probing functionality
"""

import time
from device_commands import get_all_commands, ALL_COMMAND_CATEGORIES


class DeviceTesting:
    def __init__(self, communication):
        self.comm = communication
        self.response_buffer = []
        self.working_commands = []
        self.timeout_commands = []
        
    def log_response(self, command, response):
        """Log command and response"""
        self.response_buffer.append((command, response))
        if response and response not in ["ER:UNKNOWN COMMAND", "OK", "SENT"]:
            self.working_commands.append((command, response))
    
    def test_single_command(self, command, timeout_sensitive=False):
        """Test a single command and log the response"""
        print(f"Testing: {command}")
        
        # For potentially timeout-sensitive commands, try shorter timeout first
        if timeout_sensitive:
            response = self.comm.send_command_with_timeout(command, timeout=500)  # 500ms
        else:
            response = self.comm.send_command(command)
        
        if response == "TIMEOUT":
            print(f"TIMEOUT: {command} (might be data transfer command)")
            self.timeout_commands.append(command)
            return False
        elif response:
            self.log_response(command, response)
            if response not in ["ER:UNKNOWN COMMAND", "OK", "SENT"]:
                print(f"*** SUCCESS: {command} -> {response} ***")
                return True
            elif response == "ER:UNKNOWN COMMAND":
                print(f"Unknown: {command}")
            else:
                print(f"Response: {response}")
        
        return False
    
    def test_discovery_commands(self):
        """Test commands for discovering files/measurements on device"""
        print("\n=== Testing File Discovery Commands ===")
        
        # Commands that might list files or show what's stored
        discovery_commands = [
            "DIR", "DIR?", "LS", "LS?", "FILES", "FILES?", "LIST", "LIST?", 
            "CATALOG", "CATALOG?", "INDEX", "INDEX?", "NAMES", "NAMES?",
            "ENUM", "ENUM?", "COUNT", "COUNT?", "SIZE", "SIZE?", 
            "USED", "USED?", "FREE", "FREE?", "ALL", "ALL?"
        ]
        
        successful = []
        
        print("Testing directory and enumeration commands...")
        for cmd in discovery_commands:
            if self.test_single_command(cmd):
                successful.append((cmd, self.response_buffer[-1][1]))
                # If we get a substantial response, this might be the file list!
                if len(self.response_buffer[-1][1]) > 20:
                    print(f"*** SUBSTANTIAL RESPONSE from {cmd} - might be file listing! ***")
        
        return successful
    
    def test_indexed_access(self):
        """Test accessing files by index rather than name"""
        print("\n=== Testing Indexed File Access ===")
        
        successful = []
        
        # Try numbered access patterns
        index_patterns = [
            # Simple numbers
            "{i}", "{i}?",
            # With prefixes
            "FILE:{i}", "FILE:{i}?", "MEM:{i}", "MEM:{i}?",
            "ID:{i}", "ID:{i}?", "RECALL:{i}", "RECALL:{i}?",
            "GET:{i}", "GET:{i}?", "LOAD:{i}", "LOAD:{i}?",
            # With formatting
            "{i:03d}", "{i:03d}?", "ID:{i:03d}", "ID:{i:03d}?",
        ]
        
        print("Testing indexed access (0-9)...")
        for i in range(10):
            for pattern in index_patterns:
                cmd = pattern.format(i=i)
                if self.test_single_command(cmd):
                    successful.append((cmd, self.response_buffer[-1][1]))
                    print(f"*** Found indexed access: {cmd} ***")
        
        return successful
    
    def test_bulk_data_commands(self):
        """Test commands that might return all data at once"""
        print("\n=== Testing Bulk Data Commands ===")
        
        bulk_commands = [
            # Commands that might return everything
            "ALL", "ALL?", "DUMP", "DUMP?", "EXPORT", "EXPORT?",
            "TABLE", "TABLE?", "DATA", "DATA?", "MEASUREMENTS", "MEASUREMENTS?",
            
            # Format-specific dumps
            "F1", "F1?", "F2", "F2?", "F3", "F3?",
            
            # Memory dumps
            "BUFFER", "BUFFER?",
        ]
        
        successful = []
        
        for cmd in bulk_commands:
            print(f"Testing bulk command: {cmd}")
            response = self.comm.send_command(cmd)
            
            if response and response not in ["ER:UNKNOWN COMMAND", "TIMEOUT"]:
                if len(response) > 50:  # Substantial response
                    print(f"*** BULK DATA from {cmd}: {response[:100]}{'...' if len(response) > 100 else ''} ***")
                    successful.append((cmd, response))
                    self.log_response(cmd, response)
                elif response not in ["OK", "SENT"]:
                    print(f"Response: {response}")
                    successful.append((cmd, response))
                    self.log_response(cmd, response)
        
        return successful
    
    def probe_file_system(self):
        """Comprehensive file system probing"""
        print("\n=== Comprehensive File System Probe ===")
        
        all_results = []
        
        # Test discovery commands first
        discovery_results = self.test_discovery_commands()
        all_results.extend(discovery_results)
        
        # Test indexed access
        indexed_results = self.test_indexed_access()
        all_results.extend(indexed_results)
        
        # Test bulk data commands
        bulk_results = self.test_bulk_data_commands()
        all_results.extend(bulk_results)
        
        # Test your specific file in various ways
        print("\nTesting your '6I' file with discovered patterns...")
        file_variants = [
            "6I", "6I?", "FILE:6I", "FILE:6I?", "MEM:6I", "MEM:6I?",
            "ID:6I", "ID:6I?", "RECALL:6I", "RECALL:6I?",
            "GET:6I", "GET:6I?", "LOAD:6I", "LOAD:6I?"
        ]
        
        for cmd in file_variants:
            if self.test_single_command(cmd):
                all_results.append((cmd, self.response_buffer[-1][1]))
        
        print(f"\nFile system probe found {len(all_results)} working commands")
        return all_results
    
    def test_file_operations(self):
        """Specifically test file and data retrieval operations"""
        print("\n=== Testing File and Data Operations ===")
        
        # Test basic file listing commands first (less likely to timeout)
        basic_file_commands = [
            "DIR?", "FILES?", "LIST?", "CATALOG?", "INDEX?",
            "FILE?", "FILENAME?", "CURRENT?", "ACTIVE?"
        ]
        
        print("Testing basic file commands...")
        successful = []
        
        for cmd in basic_file_commands:
            if self.test_single_command(cmd):
                successful.append((cmd, self.response_buffer[-1][1]))
        
        # Test your specific file with different formats
        print("\nTesting your specific file '6I' with different formats...")
        file_6i_variants = [
            "6I?", "6I", "RECALL:6I", "RECALL 6I", "GET 6I", "LOAD 6I", 
            "FILE 6I", "MEM:6I?", "ID:6I?"
        ]
        
        for cmd in file_6i_variants:
            if self.test_single_command(cmd):
                successful.append((cmd, self.response_buffer[-1][1]))
        
        return successful
    
    def test_measurement_recall_commands(self):
        """Test commands for recalling stored measurements"""
        print("\n=== Testing Measurement Recall Commands ===")
        
        # Based on the manual, try ID-based recall
        id_commands = []
        
        # Try IDs from manual (001-005) and some additional ones
        for i in range(1, 21):  # Try IDs 1-20
            id_commands.extend([
                f"{i:03d}?", f"ID:{i:03d}?", f"RECALL:{i:03d}", f"GET:{i:03d}", f"MEM:{i:03d}?"
            ])
        
        # Also try your file name variants
        file_variants = [
            "6I", "6I?", "RECALL:6I", "GET:6I", "ID:6I", "MEM:6I", "FILE:6I", "LOAD:6I", "READ:6I"
        ]
        
        all_test_commands = id_commands + file_variants
        successful = []
        
        print(f"Testing {len(all_test_commands)} ID and file recall commands...")
        
        for cmd in all_test_commands:
            if self.test_single_command(cmd):
                successful.append((cmd, self.response_buffer[-1][1]))
                if ":" in cmd and len(self.response_buffer[-1][1]) > 10:
                    print(f"Found working format with {cmd}, trying similar commands...")
        
        return successful
    
    def test_data_transfer_commands(self):
        """Test commands that might initiate data transfer"""
        print("\n=== Testing Data Transfer Commands (Short Timeout) ===")
        
        transfer_commands = [
            "START?", "BEGIN?", "FETCH?", "GET?", "PULL?", "RETRIEVE?",
            "DOWNLOAD?", "UPLOAD?", "BUFFER?", "STREAM?", "OUTPUT?",
            "PRINT?", "SHOW?", "DISPLAY?", "TRANSFER?", "SEND?",
            
            # Try without question marks (might be write commands)
            "START", "BEGIN", "FETCH", "GET", "PULL", "RETRIEVE",
            "DOWNLOAD", "UPLOAD", "BUFFER", "STREAM", "OUTPUT",
            "PRINT", "SHOW", "DISPLAY", "TRANSFER", "SEND"
        ]
        
        successful = []
        
        for cmd in transfer_commands:
            if self.test_single_command(cmd, timeout_sensitive=True):
                successful.append((cmd, self.response_buffer[-1][1]))
        
        return successful
    
    def probe_all_commands(self):
        """Test all predefined commands"""
        print("\n=== Testing All Predefined Commands ===")
        
        total_commands = 0
        successful_commands = 0
        
        for category, commands in ALL_COMMAND_CATEGORIES.items():
            print(f"\n--- Testing {category} Commands ---")
            category_success = 0
            
            # Determine if this category might have timeout-sensitive commands
            timeout_sensitive = category in ["File Operations", "Protocol"]
            
            for cmd in commands:
                total_commands += 1
                if self.test_single_command(cmd, timeout_sensitive):
                    successful_commands += 1
                    category_success += 1
            
            print(f"{category} category: {category_success}/{len(commands)} successful")
        
        if self.timeout_commands:
            print(f"\nCommands that timed out (might be data transfer): {len(self.timeout_commands)}")
            for cmd in self.timeout_commands[:10]:  # Show first 10
                print(f"  {cmd}")
            if len(self.timeout_commands) > 10:
                print(f"  ... and {len(self.timeout_commands) - 10} more")
        
        print(f"\nOverall: {successful_commands}/{total_commands} commands successful")
        return self.working_commands
    
    def probe_measurement_commands(self):
        """Focus on measurement-related commands"""
        print("\n=== Testing Measurement Commands ===")
        
        # Start with file operations and measurement recall
        file_results = self.test_file_operations()
        recall_results = self.test_measurement_recall_commands()
        transfer_results = self.test_data_transfer_commands()
        
        all_results = file_results + recall_results + transfer_results
        
        print(f"Found {len(all_results)} working measurement-related commands")
        return all_results
    
    def get_live_reading(self):
        """Try to get stored data or file contents"""
        print("\n=== Attempting to Retrieve Stored Data ===")
        
        # Try commands most likely to return stored measurement data
        data_commands = [
            # Your specific file with various formats
            "6I", "6I?", "RECALL:6I", "GET:6I", "ID:6I", "FILE:6I",
            
            # Standard data commands
            "F1?", "DIR?", "FILES?", "LIST?", "CATALOG?",
            
            # Memory locations from manual
            "001?", "002?", "003?", "004?", "005?",
            "RECALL:001", "RECALL:002", "RECALL:003",
            
            # Table format
            "TABLE?", "DATA?", "MEASUREMENTS?"
        ]
        
        for cmd in data_commands:
            print(f"Trying {cmd}...")
            response = self.comm.send_command(cmd)
            
            if response and response != "ER:UNKNOWN COMMAND" and response != "TIMEOUT":
                if len(response) > 10:  # Substantial response
                    print(f"*** DATA FOUND: {cmd} -> {response[:100]}{'...' if len(response) > 100 else ''} ***")
                    return response
                else:
                    print(f"Short response: {response}")
        
        print("No substantial data retrieval found")
        return None
    
    def monitor_readings(self, duration=30, command=None):
        """Monitor a command for changes (if any)"""
        if not command:
            # Find a working command that might change
            test_commands = ["RANGE?", "MEMORY?", "STATUS?", "6I?"]
            
            for cmd in test_commands:
                response = self.comm.send_command(cmd)
                if response and response != "ER:UNKNOWN COMMAND":
                    command = cmd
                    break
        
        if not command:
            print("No suitable command found for monitoring")
            return
        
        print(f"\n=== Monitoring {command} for {duration} seconds ===")
        print("Press Ctrl+C to stop early")
        
        start_time = time.time()
        reading_count = 0
        last_response = None
        
        try:
            while time.time() - start_time < duration:
                response = self.comm.send_command(command)
                
                if response and response != "ER:UNKNOWN COMMAND":
                    reading_count += 1
                    elapsed = time.time() - start_time
                    
                    if response != last_response:
                        print(f"[{elapsed:.1f}s] CHANGE #{reading_count}: {response}")
                        last_response = response
                    else:
                        print(f"[{elapsed:.1f}s] Same #{reading_count}: {response}")
                
                time.sleep(2)  # Wait 2 seconds between readings
                
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")
        
        print(f"Monitored {reading_count} times in {time.time() - start_time:.1f} seconds")
    
    def analyze_current_state(self):
        """Get current device state using known working commands"""
        print("\n=== Current Device State ===")
        
        # Test key status commands
        status_commands = {
            "Version": "VER?",
            "ID": "ID?", 
            "Units": "UNITS?",
            "Range": "RANGE?",
            "Velocity": "VELOCITY?",
            "Zero": "ZERO?",
            "Mode": "MODE?",
            "Status": "STATUS?",
            "Memory": "MEMORY?",
        }
        
        for name, cmd in status_commands.items():
            response = self.comm.send_command(cmd)
            if response:
                print(f"{name:12}: {response}")
                self.log_response(cmd, response)
    
    def save_results(self, filename="olympus_test_results.txt"):
        """Save all test results to file with working commands at the end"""
        with open(filename, 'w') as f:
            f.write("=== Olympus NDT-35DL Communication Test Results ===\n")
            f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Write all command/response pairs
            f.write("=== All Commands Tested ===\n")
            for cmd, resp in self.response_buffer:
                f.write(f"Command: {cmd}\n")
                f.write(f"Response: {resp}\n")
                f.write("-" * 50 + "\n")
            
            # Write timeout commands
            if self.timeout_commands:
                f.write(f"\n=== Commands That Timed Out (Possible Data Transfer) ===\n")
                for cmd in self.timeout_commands:
                    f.write(f"{cmd}\n")
                f.write("-" * 50 + "\n")
            
            # Write summary of working commands at the end
            f.write("\n" + "=" * 60 + "\n")
            f.write("=== WORKING COMMANDS SUMMARY ===\n")
            f.write("=" * 60 + "\n\n")
            
            if self.working_commands:
                # Remove duplicates
                unique_commands = list(set(self.working_commands))
                f.write(f"Found {len(unique_commands)} working commands:\n\n")
                
                for cmd, resp in sorted(unique_commands):
                    f.write(f"'{cmd}' -> '{resp}'\n")
                
                f.write(f"\n=== Working Commands by Category ===\n")
                
                # Categorize working commands
                for category, commands in ALL_COMMAND_CATEGORIES.items():
                    working_in_category = [(cmd, resp) for cmd, resp in unique_commands if cmd in commands]
                    if working_in_category:
                        f.write(f"\n{category}:\n")
                        for cmd, resp in working_in_category:
                            f.write(f"  {cmd} -> {resp}\n")
            else:
                f.write("No working commands found.\n")
        
        print(f"Results saved to {filename}")
        print(f"Found {len(list(set(self.working_commands)))} unique working commands")
        if self.timeout_commands:
            print(f"Found {len(self.timeout_commands)} commands that timed out (possible data transfer commands)")