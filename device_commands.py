#!/usr/bin/env python3
"""
Command definitions and command testing for NDT devices
"""

# Standard SCPI commands
SCPI_COMMANDS = [
    "*IDN?",           # Standard identification
    "*RST",            # Reset
    "*TST?",           # Self test
    "*CLS",            # Clear status
    "*ESR?",           # Event status register
    "*STB?",           # Status byte
    "*OPC?",           # Operation complete
]

# Basic help and info commands
BASIC_COMMANDS = [
    "?",               # Simple help
    "HELP",            # Help command
    "COMMANDS",        # List commands
    "CMD",             # Command list
    "LIST",            # List
    "VER?",            # Version
    "VERSION?",        # Full version query
    "ID?",             # Device ID query
    "INFO?",           # Information query
]

# File discovery and enumeration commands
NDT_DISCOVERY_COMMANDS = [
    # Directory and file listing
    "DIR",             # Directory (no ?)
    "DIR?",            # Directory listing
    "LS",              # Linux-style list
    "LS?",             # Linux-style list
    "FILES",           # List files (no ?)
    "FILES?",          # List files
    "LIST",            # List (no ?)
    "LIST?",           # List
    "CATALOG",         # Catalog (no ?)
    "CATALOG?",        # File catalog
    "INDEX",           # Index (no ?)
    "INDEX?",          # File index
    "NAMES",           # File names (no ?)
    "NAMES?",          # File names
    
    # Memory enumeration
    "ENUM",            # Enumerate (no ?)
    "ENUM?",           # Enumerate
    "COUNT",           # Count (no ?)
    "COUNT?",          # Count files/measurements
    "SIZE",            # Size (no ?)
    "SIZE?",           # Memory size
    "USED",            # Used memory (no ?)
    "USED?",           # Used memory
    "FREE",            # Free memory (no ?)
    "FREE?",           # Free memory
    
    # Get by index/position
    "FIRST",           # First file (no ?)
    "FIRST?",          # First file
    "LAST",            # Last file (no ?)
    "LAST?",           # Last file
    "NEXT",            # Next file (no ?)
    "NEXT?",           # Next file
    "PREV",            # Previous file (no ?)
    "PREV?",           # Previous file
    "ALL",             # All files (no ?)
    "ALL?",            # All files
    
    # Numbered access (0-based, 1-based indexing)
    "0",               # Index 0
    "0?",              # Index 0
    "1",               # Index 1
    "1?",              # Index 1
    "2",               # Index 2
    "2?",              # Index 2
    "3",               # Index 3
    "3?",              # Index 3
    "4",               # Index 4
    "4?",              # Index 4
    "5",               # Index 5
    "5?",              # Index 5
]

# File and data retrieval commands
NDT_FILE_COMMANDS = [
    # Generic file operations
    "FILE",            # Current file (no ?)
    "FILE?",           # Current file
    "FILENAME",        # Filename (no ?)
    "FILENAME?",       # Filename
    "CURRENT",         # Current data (no ?)
    "CURRENT?",        # Current data
    "ACTIVE",          # Active file (no ?)
    "ACTIVE?",         # Active file
    "OPEN",            # Open file (no ?)
    "OPEN?",           # Open file
    
    # Data transfer formats
    "F1",              # F1 format (no ?)
    "F1?",             # F1 format (from manual)
    "F2",              # F2 format (no ?)
    "F2?",             # F2 format
    "F3",              # F3 format (no ?)
    "F3?",             # F3 format
    "FORMAT",          # Current format (no ?)
    "FORMAT?",         # Current format
    "EXPORT",          # Export data (no ?)
    "EXPORT?",         # Export data
    "DUMP",            # Dump data (no ?)
    "DUMP?",           # Dump data
    "TRANSFER",        # Transfer data (no ?)
    "TRANSFER?",       # Transfer data
    "SEND",            # Send data (no ?)
    "SEND?",           # Send data
    
    # Table and measurement data
    "TABLE",           # Thickness table (no ?)
    "TABLE?",          # Thickness table
    "DATA",            # All data (no ?)
    "DATA?",           # All data
    "MEASUREMENTS",    # All measurements (no ?)
    "MEASUREMENTS?",   # All measurements
    "THICKNESS",       # Thickness data (no ?)
    "THICKNESS?",      # Thickness data
    "VELOCITY",        # Velocity data (no ?)
    "VELOCITY?",       # Velocity data
    "TOF",             # Time of Flight data (no ?)
    "TOF?",            # Time of Flight data
    "TRANSDUCER",      # Custom transducer setups (no ?)
    "TRANSDUCER?",     # Custom transducer setups
]

# Memory and storage commands
NDT_MEMORY_COMMANDS = [
    "MEM",             # Memory (no ?)
    "MEM?",            # Memory
    "MEMORY",          # Full memory (no ?)
    "MEMORY?",         # Full memory
    "STORE",           # Store (no ?)
    "STORE?",          # Store
    "RECALL",          # Recall (no ?)
    "RECALL?",         # Recall
    "SAVE",            # Save (no ?)
    "SAVE?",           # Save
    "LOAD",            # Load (no ?)
    "LOAD?",           # Load
    "CLEAR",           # Clear (no ?)
    "CLEAR?",          # Clear
    
    # Specific memory locations/IDs from manual
    "001",             # ID 001 (no ?)
    "001?",            # ID 001
    "002",             # ID 002 (no ?)
    "002?",            # ID 002
    "003",             # ID 003 (no ?)
    "003?",            # ID 003
    "004",             # ID 004 (no ?)
    "004?",            # ID 004
    "005",             # ID 005 (no ?)
    "005?",            # ID 005
    
    # Memory operations
    "BANK",            # Memory bank (no ?)
    "BANK?",           # Memory bank
    "SLOT",            # Memory slot (no ?)
    "SLOT?",           # Memory slot
    "LOCATION",        # Memory location (no ?)
    "LOCATION?",       # Memory location
]

# Configuration and status commands
NDT_CONFIG_COMMANDS = [
    "STATUS?",         # Status
    "STATE?",          # State
    "MODE?",           # Mode
    "UNITS?",          # Units
    "RANGE?",          # Range setting
    "GAIN?",           # Gain
    "VEL?",            # Velocity setting
    "FREQ?",           # Frequency
    "ZERO?",           # Zero point
    "CAL?",            # Calibration
    "SETUP?",          # Setup
    "CONFIG?",         # Configuration
    
    # From manual - setup parameters
    "DIFF?",           # Differential setting
    "LO_ALM?",         # Low alarm  
    "HI_ALM?",         # High alarm
    "BASE?",           # Base measurement setup
    "SU?",             # Setup number
    "FLAGS?",          # Flags setting
]

# Communication and protocol commands
NDT_PROTOCOL_COMMANDS = [
    # Protocol commands that might trigger data transfer
    "START",           # Start transfer (no ?)
    "START?",          # Start transfer
    "BEGIN",           # Begin operation (no ?)
    "BEGIN?",          # Begin operation
    "FETCH",           # Fetch data (no ?)
    "FETCH?",          # Fetch data
    "GET",             # Get data (no ?)
    "GET?",            # Get data
    "PULL",            # Pull data (no ?)
    "PULL?",           # Pull data
    "RETRIEVE",        # Retrieve data (no ?)
    "RETRIEVE?",       # Retrieve data
    "DOWNLOAD",        # Download (no ?)
    "DOWNLOAD?",       # Download
    "UPLOAD",          # Upload (no ?)
    "UPLOAD?",         # Upload
    
    # Buffer and stream commands
    "BUFFER",          # Buffer contents (no ?)
    "BUFFER?",         # Buffer contents
    "STREAM",          # Stream data (no ?)
    "STREAM?",         # Stream data
    "OUTPUT",          # Output data (no ?)
    "OUTPUT?",         # Output data
    "PRINT",           # Print data (no ?)
    "PRINT?",          # Print data
    "SHOW",            # Show data (no ?)
    "SHOW?",           # Show data
    "DISPLAY",         # Display data (no ?)
    "DISPLAY?",        # Display data
]

# Single character commands
SINGLE_CHAR_COMMANDS = [
    f"{c}" for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
] + [
    f"{c}?" for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
] + [
    f"{i}" for i in range(10)
] + [
    f"{i}?" for i in range(10)
]

# Olympus 45MG specific data retrieval commands
OLYMPUS_45MG_DATA_COMMANDS = [
    # Direct measurement recall (Olympus format)
    "MEAS?",           # Current measurement
    "THICK?",          # Thickness reading
    "READ?",           # Read current value
    "VALUE?",          # Current value
    "LAST?",           # Last measurement
    
    # Memory recall with ID format (common in Olympus)
    "RECALL 001",      # Recall memory 001
    "RECALL 002",      # Recall memory 002  
    "RECALL 003",      # Recall memory 003
    "RECALL 004",      # Recall memory 004
    "RECALL 005",      # Recall memory 005
    "RCL 001",         # Short recall format
    "RCL 002",         # Short recall format
    "RCL 003",         # Short recall format
    "RCL 004",         # Short recall format
    "RCL 005",         # Short recall format
    
    # Memory with colon format
    "MEM:001",         # Memory location 001
    "MEM:002",         # Memory location 002
    "MEM:003",         # Memory location 003
    "MEM:004",         # Memory location 004
    "MEM:005",         # Memory location 005
    "MEM:001?",        # Query memory 001
    "MEM:002?",        # Query memory 002
    "MEM:003?",        # Query memory 003
    "MEM:004?",        # Query memory 004
    "MEM:005?",        # Query memory 005
    
    # Extended memory range
    "MEM:006", "MEM:007", "MEM:008", "MEM:009", "MEM:010",
    "MEM:006?", "MEM:007?", "MEM:008?", "MEM:009?", "MEM:010?",
    "RECALL 006", "RECALL 007", "RECALL 008", "RECALL 009", "RECALL 010",
    
    # Block data retrieval
    "BLOCK?",          # Data block
    "SEGMENT?",        # Data segment
    "RECORD?",         # Data record
    "ENTRY?",          # Data entry
    "LOG?",            # Data log
    "HISTORY?",        # Measurement history
]

# Olympus 45MG Datalogger Commands (focused on actual datalogger functionality)
OLYMPUS_45MG_DATALOGGER_COMMANDS = [
    # Grid/Sequence specific commands
    "GRID:DATA?",      # Grid data export
    "GRID:EXPORT?",    # Export grid data
    "GRID:LIST?",      # List grid measurements
    "GRID:ALL?",       # All grid data
    "GRID:COUNT?",     # Count grid points
    "GRID:DUMP?",      # Dump all grid data
    
    # Sequence data commands
    "SEQ:DATA?",       # Sequence data
    "SEQ:LIST?",       # List sequence data
    "SEQ:EXPORT?",     # Export sequence
    "SEQ:ALL?",        # All sequence data
    "SEQ:COUNT?",      # Count sequence items
    
    # Datalogger memory commands
    "DLOG:DATA?",      # Datalogger data
    "DLOG:LIST?",      # List datalogger entries
    "DLOG:EXPORT?",    # Export datalogger data
    "DLOG:ALL?",       # All datalogger data
    "DLOG:COUNT?",     # Count datalogger entries
    "DLOG:DUMP?",      # Dump datalogger data
    
    # File system navigation
    "FILES:LIST?",     # List all files
    "FILES:COUNT?",    # Count files
    "FILES:EXPORT?",   # Export files
    "FILES:DUMP?",     # Dump all files
    
    # Memory bank access
    "BANK:0?", "BANK:1?", "BANK:2?", "BANK:3?", "BANK:4?",
    "BANK:5?", "BANK:6?", "BANK:7?", "BANK:8?", "BANK:9?",
    
    # Setup/calibration data
    "SETUP:DATA?",     # Setup data
    "CAL:DATA?",       # Calibration data
    "CONFIG:DATA?",    # Configuration data
    
    # Report formats
    "REPORT:CSV?",     # CSV report
    "REPORT:TXT?",     # Text report
    "REPORT:TAB?",     # Tab-delimited report
    "REPORT:FULL?",    # Full report
]

# Advanced data access patterns
ADVANCED_DATA_COMMANDS = [
    # Range-based access
    "RANGE:1-10",      # Get range of measurements
    "RANGE:ALL",       # Get all measurements in range
    "FROM:1",          # Starting from position 1
    "TO:10",           # Up to position 10
    
    # Format-specific exports
    "CSV?",            # CSV format export
    "TAB?",            # Tab-delimited export
    "TXT?",            # Text format export
    "RAW?",            # Raw data format
    
    # Batch operations
    "BATCH?",          # Batch data
    "BULK?",           # Bulk data retrieval
    "MASS?",           # Mass data export
    "COMPLETE?",       # Complete dataset
    
    # Time-based queries
    "TODAY?",          # Today's measurements
    "RECENT?",         # Recent measurements
    "LATEST?",         # Latest measurements
    "OLDEST?",         # Oldest measurements
]

# User interface simulation commands  
UI_SIMULATION_COMMANDS = [
    # Simulate pressing buttons/keys
    "ENTER",           # Enter key
    "MENU",            # Menu key
    "UP",              # Up arrow
    "DOWN",            # Down arrow
    "LEFT",            # Left arrow
    "RIGHT",           # Right arrow
    "SELECT",          # Select button
    "BACK",            # Back button
    "HOME",            # Home button
    "ESC",             # Escape key
    
    # Menu navigation
    "MENU:DATA",       # Navigate to data menu
    "MENU:MEMORY",     # Navigate to memory menu
    "MENU:RECALL",     # Navigate to recall menu
    "MENU:EXPORT",     # Navigate to export menu
]

# Protocol variations for data retrieval
DATA_PROTOCOL_VARIANTS = [
    # Generic data access patterns
    "GET ALL",         # Get all data
    "GET:ALL",         # Get all data (colon format)
    "GET=ALL",         # Get all data (equals format)
    "EXPORT ALL",      # Export all data
    "EXPORT:ALL",      # Export all data (colon format)
    "DATA ALL",        # All data
    "DATA:ALL",        # All data (colon format)
    
    # Different formats
    "FORMAT:F1",       # Set F1 format
    "FORMAT:F2",       # Set F2 format
    "FORMAT:F3",       # Set F3 format
    "FORMAT:CSV",      # Set CSV format
    "FORMAT:TAB",      # Set tab format
    
    # Binary/hex access attempts
    "BIN:ALL",         # Binary format
    "HEX:ALL",         # Hex format
    "ASCII:ALL",       # ASCII format
]

# Beep-triggering and interactive commands (based on "0" command discovery)
OLYMPUS_INTERACTIVE_COMMANDS = [
    # Numeric commands that might trigger device functions
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "00", "01", "02", "03", "04", "05", "06", "07", "08", "09",
    "000", "001", "002", "003", "004", "005", "006", "007", "008", "009",
    
    # Zero-related commands (since "0" causes beep)
    "ZERO", "ZERO?", "Z", "Z?", "ZER", "ZER?",
    "CAL", "CAL?", "CALIBRATE", "CALIBRATE?",
    "NULL", "NULL?", "NULLIFY", "NULLIFY?",
    "BASELINE", "BASELINE?", "BASE", "BASE?",
    
    # Menu navigation (might cause beeps)
    "MENU", "M", "ESC", "ENTER", "ENT", "OK",
    "UP", "DOWN", "LEFT", "RIGHT", "U", "D", "L", "R",
    "SELECT", "SEL", "BACK", "HOME", "H",
    
    # Function keys that might beep
    "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8",
    "FUNC", "FUNCTION", "MODE", "SETUP", "CONFIG",
    
    # Memory access that might beep
    "STORE", "RECALL", "SAVE", "LOAD", "MEM",
    "ST", "RC", "SV", "LD", "M",
    
    # Measurement commands that might beep
    "MEAS", "MEASURE", "READ", "TAKE", "SAMPLE",
    "START", "STOP", "PAUSE", "RESET", "CLEAR",
]

# All command categories combined
ALL_COMMAND_CATEGORIES = {
    "SCPI": SCPI_COMMANDS,
    "Basic": BASIC_COMMANDS,
    "Discovery": NDT_DISCOVERY_COMMANDS,
    "File Operations": NDT_FILE_COMMANDS,
    "Memory": NDT_MEMORY_COMMANDS,
    "Configuration": NDT_CONFIG_COMMANDS,
    "Protocol": NDT_PROTOCOL_COMMANDS,
    "Single Character": SINGLE_CHAR_COMMANDS,
    "Olympus 45MG Data": OLYMPUS_45MG_DATA_COMMANDS,
    "Olympus Datalogger": OLYMPUS_DATALOGGER_COMMANDS,
    "Olympus 45MG Datalogger": OLYMPUS_45MG_DATALOGGER_COMMANDS,
    "Advanced Data": ADVANCED_DATA_COMMANDS,
    "UI Simulation": UI_SIMULATION_COMMANDS,
    "Protocol Variants": DATA_PROTOCOL_VARIANTS,
    "Olympus Interactive": OLYMPUS_INTERACTIVE_COMMANDS,
}

def get_all_commands():
    """Get all commands as a flat list"""
    all_commands = []
    for category_commands in ALL_COMMAND_CATEGORIES.values():
        all_commands.extend(category_commands)
    return all_commands

def get_commands_by_category(category):
    """Get commands for a specific category"""
    return ALL_COMMAND_CATEGORIES.get(category, [])

# Update the 6I file variants function to be more generic
def get_datalogger_variants():
    """Get all possible command variations for accessing datalogger data"""
    base_commands = ["RECALL", "GET", "LOAD", "READ", "DATA", "EXPORT", "FETCH", "PULL", "DUMP"]
    separators = [":", " ", ",", "="]
    targets = ["ALL", "DATA", "LOG", "GRID", "SEQ", "MEASUREMENTS", "TABLE"]
    
    variants = []
    
    # Add direct access
    variants.extend(["ALL?", "DATA?", "LOG?", "GRID?", "TABLE?", "MEASUREMENTS?"])
    
    # Add command + separator + target combinations
    for cmd in base_commands:
        for sep in separators:
            for target in targets:
                variants.append(f"{cmd}{sep}{target}")
                variants.append(f"{cmd}{sep}{target}?")
    
    return variants

def get_memory_range_commands(start=1, end=20):
    """Generate memory access commands for a range of IDs"""
    commands = []
    
    for i in range(start, end + 1):
        # Zero-padded format
        id_str = f"{i:03d}"
        commands.extend([
            f"MEM:{id_str}",
            f"MEM:{id_str}?",
            f"RECALL {id_str}",
            f"RECALL:{id_str}",
            f"GET:{id_str}",
            f"ID:{id_str}",
            f"ID:{id_str}?",
        ])
        
        # Non-padded format
        commands.extend([
            f"MEM:{i}",
            f"MEM:{i}?",
            f"RECALL {i}",
            f"GET:{i}",
            f"ID:{i}",
        ])
    
    return commands