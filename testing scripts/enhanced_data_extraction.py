#!/usr/bin/env python3
"""
Enhanced data extraction specifically for Olympus 45MG measurements
"""

def test_olympus_specific_commands(comm):
    """Test commands specific to Olympus 45MG based on manual patterns"""
    
    # Commands that often work on Olympus devices for data retrieval
    olympus_data_commands = [
        # Format-specific data dumps (F1, F2, F3 are common in Olympus manuals)
        "F1?", "F2?", "F3?", "F4?", "F5?",
        
        # Table formats (thickness tables are common)
        "TABLE?", "THTABLE?", "THICK_TABLE?",
        
        # Batch data retrieval
        "ALLDATA?", "ALL_DATA?", "BATCH?", "EXPORT_ALL?",
        
        # Memory dump with different syntax
        "MEMDUMP?", "MEM_DUMP?", "DUMP_MEM?",
        
        # Sequential data access
        "FIRST_DATA?", "NEXT_DATA?", "DATA_NEXT?",
        
        # CSV-style exports (some Olympus devices support this)
        "CSV?", "CSVDATA?", "CSV_EXPORT?",
        
        # Database-style queries
        "SELECT_ALL?", "QUERY_ALL?", "LIST_DATA?"
    ]
    
    successful_commands = []
    
    for cmd in olympus_data_commands:
        print(f"Testing: {cmd}")
        response = comm.send_command_with_timeout(cmd, timeout_ms=5000)  # Longer timeout for data
        
        if response and response not in ["ER:UNKNOWN COMMAND", "TIMEOUT", "OK"]:
            print(f"SUCCESS: {cmd} -> {response[:100]}...")
            successful_commands.append((cmd, response))
    
    return successful_commands

def test_indexed_recall_patterns(comm, file_count):
    """Test different indexing patterns for the 24 stored measurements"""
    
    # Multiple indexing patterns to try
    index_patterns = [
        # Direct numeric access
        "{i:03d}?", "{i:02d}?", "{i}?",
        
        # With prefixes
        "ID:{i:03d}?", "MEM:{i:03d}?", "FILE:{i:03d}?", 
        "DATA:{i:03d}?", "MEAS:{i:03d}?", "REC:{i:03d}?",
        
        # Table-style access
        "TABLE:{i}?", "ROW:{i}?", "ENTRY:{i}?",
        
        # Get/Recall patterns
        "GET:{i}?", "RECALL:{i}?", "FETCH:{i}?", "READ:{i}?",
    ]
    
    successful_retrievals = []
    
    for i in range(1, min(file_count + 1, 6)):  # Test first 5 records
        print(f"\n--- Testing Record {i} ---")
        
        for pattern in index_patterns:
            cmd = pattern.format(i=i)
            response = comm.send_command_with_timeout(cmd, timeout_ms=3000)
            
            if response and response not in ["ER:UNKNOWN COMMAND", "TIMEOUT", "OK"]:
                print(f"*** FOUND DATA: {cmd} -> {response} ***")
                successful_retrievals.append((i, cmd, response))
                break  # Found working pattern for this index
    
    return successful_retrievals