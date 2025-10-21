#!/usr/bin/env python3
"""
Data extraction and CSV export for Olympus measurements
"""

import csv
import re
from datetime import datetime
from typing import List, Dict, Tuple, Optional

class OlympusDataExtractor:
    def __init__(self, comm):
        self.comm = comm
        self.measurement_data = []
        
    def extract_all_measurements(self) -> List[Dict]:
        """Extract all stored measurements using discovered working commands"""
        
        # First, determine how many measurements are stored
        mem_response = self.comm.send_command("MEMORY?")
        file_count = 0
        
        if mem_response:
            try:
                file_count = int(mem_response.split()[2])
                print(f"Found {file_count} stored measurements")
            except (ValueError, IndexError):
                print("Could not determine file count, trying manual discovery")
                file_count = 50  # Try up to 50
        
        measurements = []
        
        # Try the most promising data retrieval methods
        retrieval_methods = [
            self._try_bulk_export,
            self._try_table_format,
            self._try_indexed_recall,
            self._try_sequential_access
        ]
        
        for method in retrieval_methods:
            try:
                results = method(file_count)
                if results:
                    measurements.extend(results)
                    print(f"Retrieved {len(results)} measurements using {method.__name__}")
                    break
            except Exception as e:
                print(f"Method {method.__name__} failed: {e}")
                continue
        
        return measurements
    
    def _try_bulk_export(self, file_count: int) -> List[Dict]:
        """Try bulk data export commands"""
        bulk_commands = ["F1?", "F2?", "F3?", "TABLE?", "ALLDATA?", "CSV?"]
        
        for cmd in bulk_commands:
            response = self.comm.send_command_with_timeout(cmd, timeout_ms=10000)
            if response and len(response) > 50:  # Substantial response
                return self._parse_bulk_response(response, cmd)
        
        return []
    
    def _try_indexed_recall(self, file_count: int) -> List[Dict]:
        """Try individual record recall by index"""
        measurements = []
        
        # Try the patterns most likely to work based on your tests
        working_patterns = ["ID:{i:03d}?", "MEM:{i:03d}?", "{i:03d}?"]
        
        for i in range(1, file_count + 1):
            for pattern in working_patterns:
                cmd = pattern.format(i=i)
                response = self.comm.send_command_with_timeout(cmd, timeout_ms=2000)
                
                if response and response not in ["ER:UNKNOWN COMMAND", "TIMEOUT", "OK"]:
                    measurement = self._parse_single_measurement(response, i)
                    if measurement:
                        measurements.append(measurement)
                    break
        
        return measurements
    
    def _parse_bulk_response(self, response: str, command: str) -> List[Dict]:
        """Parse bulk data response into individual measurements"""
        measurements = []
        
        # Common patterns in Olympus data:
        # - Multiple lines with measurement data
        # - Comma or space-separated values
        # - Fixed-width format
        
        lines = response.strip().split('\n')
        
        for i, line in enumerate(lines):
            if line.strip():
                measurement = self._parse_measurement_line(line, i + 1)
                if measurement:
                    measurements.append(measurement)
        
        return measurements
    
    def _parse_single_measurement(self, response: str, index: int) -> Optional[Dict]:
        """Parse a single measurement response"""
        return self._parse_measurement_line(response, index)
    
    def _parse_measurement_line(self, line: str, index: int) -> Optional[Dict]:
        """Parse a line containing measurement data"""
        # Clean the line
        line = line.strip()
        
        # Try to extract numeric values (thickness measurements)
        numbers = re.findall(r'\d+\.?\d*', line)
        
        if numbers:
            # Assume first number is thickness, others might be velocity, etc.
            thickness = float(numbers[0])
            
            measurement = {
                'index': index,
                'thickness': thickness,
                'raw_data': line,
                'timestamp': datetime.now().isoformat(),
                'units': self._get_units()
            }
            
            # Try to extract additional parameters
            if len(numbers) > 1:
                measurement['velocity'] = float(numbers[1])
            if len(numbers) > 2:
                measurement['zero_offset'] = float(numbers[2])
                
            return measurement
        
        return None
    
    def _get_units(self) -> str:
        """Get current measurement units"""
        units_response = self.comm.send_command("UNITS?")
        return units_response.strip() if units_response else "unknown"
    
    def export_to_csv(self, measurements: List[Dict], filename: str = None) -> str:
        """Export measurements to CSV file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"olympus_measurements_{timestamp}.csv"
        
        if not measurements:
            print("No measurements to export")
            return filename
        
        # Determine all available fields
        all_fields = set()
        for measurement in measurements:
            all_fields.update(measurement.keys())
        
        # Order fields logically
        ordered_fields = ['index', 'timestamp', 'thickness', 'units', 'velocity', 'zero_offset', 'raw_data']
        remaining_fields = sorted(all_fields - set(ordered_fields))
        final_fields = [f for f in ordered_fields if f in all_fields] + remaining_fields
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=final_fields)
            writer.writeheader()
            writer.writerows(measurements)
        
        print(f"Exported {len(measurements)} measurements to {filename}")
        return filename