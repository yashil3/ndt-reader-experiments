#!/usr/bin/env python3
"""
USB communication module for Olympus/Panametrics devices
Handles both PyVISA and raw USB communication
"""

import usb.core
import usb.util
import time

# Try to import pyvisa for USBTMC support
try:
    import pyvisa
    PYVISA_AVAILABLE = True
except ImportError:
    PYVISA_AVAILABLE = False
    print("PyVISA not available, using direct USB access")


class DeviceCommunication:
    def __init__(self):
        self.device = None
        self.visa_resource = None
        self.rm = None
        
    def find_usbtmc_devices(self):
        """Find all USBTMC devices connected"""
        devices = []
        
        print("=== Scanning for USB devices ===")
        
        # Find all USB devices
        usb_devices = usb.core.find(find_all=True)
        
        for dev in usb_devices:
            try:
                # Check if device has USBTMC interface (class 0xFE, subclass 0x03)
                for cfg in dev:
                    for intf in cfg:
                        if (intf.bInterfaceClass == 0xFE and 
                            intf.bInterfaceSubClass == 0x03):
                            
                            device_info = {
                                'device': dev,
                                'vid': dev.idVendor,
                                'pid': dev.idProduct,
                                'manufacturer': usb.util.get_string(dev, dev.iManufacturer) if dev.iManufacturer else "Unknown",
                                'product': usb.util.get_string(dev, dev.iProduct) if dev.iProduct else "Unknown",
                                'serial': usb.util.get_string(dev, dev.iSerialNumber) if dev.iSerialNumber else "Unknown"
                            }
                            devices.append(device_info)
                            print(f"Found USBTMC device: VID:0x{dev.idVendor:04x} PID:0x{dev.idProduct:04x}")
                            print(f"  Manufacturer: {device_info['manufacturer']}")
                            print(f"  Product: {device_info['product']}")
                            print(f"  Serial: {device_info['serial']}")
                            break
                            
            except (usb.core.USBError, UnicodeDecodeError, ValueError) as e:
                # Skip devices we can't access or read strings from
                # Added ValueError to handle permission issues gracefully
                continue
                
        return devices
    
    def find_olympus_devices(self):
        """Look for potential Olympus/Panametrics devices by VID/PID"""
        print("\n=== Looking for Olympus/Panametrics devices ===")
        
        # Known Olympus/Panametrics vendor and product IDs
        # Add your device's VID/PID here for more reliable detection.
        known_devices = {
            0x1245: [0x0086],  # Olympus NDT (e.g., 45MG)
            0x07CF: [],        # Olympus (other models)
        }
        
        potential_devices = []
        
        # First, try to find devices by specific VID/PID pairs
        for vid, pids in known_devices.items():
            for pid in pids:
                device = usb.core.find(idVendor=vid, idProduct=pid)
                if device:
                    potential_devices.append(device)
        
        # If no specific devices found, scan all devices and check against known VIDs
        if not potential_devices:
            all_devices = usb.core.find(find_all=True)
            for dev in all_devices:
                if dev.idVendor in known_devices:
                    potential_devices.append(dev)

        found_devices_info = []
        # Use a set to avoid processing the same device multiple times
        for dev in set(potential_devices):
            try:
                device_info = {
                    'device': dev,
                    'vid': dev.idVendor,
                    'pid': dev.idProduct,
                    'manufacturer': usb.util.get_string(dev, dev.iManufacturer) if dev.iManufacturer else "Unknown",
                    'product': usb.util.get_string(dev, dev.iProduct) if dev.iProduct else "Unknown",
                }
                found_devices_info.append(device_info)
                print(f"Potential device: VID:0x{dev.idVendor:04x} PID:0x{dev.idProduct:04x}")
                print(f"  Manufacturer: {device_info['manufacturer']}")
                print(f"  Product: {device_info['product']}")
                    
            except (usb.core.USBError, UnicodeDecodeError, ValueError) as e:
                print(f"Could not read info for VID:0x{dev.idVendor:04x} PID:0x{dev.idProduct:04x} (Error: {e})")
                # This can happen due to permission errors.
                continue
                
        return found_devices_info
    
    def connect_via_pyvisa(self):
        """Connect using PyVISA for USBTMC communication"""
        if not PYVISA_AVAILABLE:
            return False
            
        try:
            self.rm = pyvisa.ResourceManager()
            resources = self.rm.list_resources()
            
            print(f"Available VISA resources: {resources}")
            
            # Look for USB resources
            usb_resources = [r for r in resources if r.startswith('USB')]
            
            if not usb_resources:
                print("No USB VISA resources found")
                return False
                
            # Try to connect to each USB resource
            for resource in usb_resources:
                try:
                    print(f"Attempting to connect to: {resource}")
                    self.visa_resource = self.rm.open_resource(resource)
                    self.visa_resource.timeout = 5000  # 5 second timeout
                    
                    # Test basic communication
                    idn = self.visa_resource.query("*IDN?")
                    print(f"Successfully connected! Device ID: {idn.strip()}")
                    return True
                    
                except Exception as e:
                    print(f"Failed to connect to {resource}: {e}")
                    if self.visa_resource:
                        self.visa_resource.close()
                        self.visa_resource = None
                    continue
                    
        except Exception as e:
            print(f"PyVISA connection error: {e}")
            
        return False
    
    def connect_raw_usb(self, device_info):
        """Connect using raw USB communication"""
        try:
            dev = device_info['device']
            
            # Try to claim the device
            interface_num = 0
            if dev.is_kernel_driver_active(interface_num):
                try:
                    dev.detach_kernel_driver(interface_num)
                    print(f"Detached kernel driver from interface {interface_num}")
                except usb.core.USBError:
                    print("Could not detach kernel driver")
                    
            dev.set_configuration()
            usb.util.claim_interface(dev, interface_num)
            
            self.device = dev
            print(f"Successfully claimed USB device VID:0x{dev.idVendor:04x} PID:0x{dev.idProduct:04x}")
            return True
            
        except usb.core.USBError as e:
            print(f"USB connection error: {e}")
            return False
    
    def send_command_with_timeout(self, command, timeout_ms):
        """Send a command with a specific timeout."""
        if self.visa_resource:
            return self._send_usbtmc_command(command, timeout_ms)
        elif self.device:
            return self._send_raw_usb_command(command, timeout_ms)
        else:
            print("Cannot send command: No active connection.")
            return None

    def send_command(self, command):
        """Send command using appropriate method with a default timeout."""
        # This now calls the more specific function with a default timeout.
        return self.send_command_with_timeout(command, timeout_ms=2000)
    
    def _send_usbtmc_command(self, command, timeout_ms=2000):
        """Send USBTMC command using PyVISA"""
        original_timeout = None
        try:
            # Set the timeout for this specific operation
            original_timeout = self.visa_resource.timeout
            self.visa_resource.timeout = timeout_ms

            if command.endswith('?'):
                response = self.visa_resource.query(command)
                return response.strip()
            else:
                self.visa_resource.write(command)
                return "OK"
                
        except Exception as e:
            # Do not print error for timeouts during probing, as it's expected
            if "Timeout" not in str(e):
                print(f"Command error: {e}")
            return "TIMEOUT" if "Timeout" in str(e) else None
        finally:
            # Always restore the original timeout
            if self.visa_resource and original_timeout is not None:
                self.visa_resource.timeout = original_timeout
    
    def _send_raw_usb_command(self, command, timeout_ms=2000):
        """Send command via raw USB"""
        try:
            cfg = self.device.get_active_configuration()
            intf = cfg[(0, 0)]
            
            bulk_out = None
            bulk_in = None
            
            # Find bulk endpoints
            for ep in intf:
                ep_dir = usb.util.endpoint_direction(ep.bEndpointAddress)
                ep_type = usb.util.endpoint_type(ep.bmAttributes)
                
                if ep_type == usb.util.ENDPOINT_TYPE_BULK:
                    if ep_dir == usb.util.ENDPOINT_OUT:
                        bulk_out = ep
                    elif ep_dir == usb.util.ENDPOINT_IN:
                        bulk_in = ep
            
            if not bulk_out:
                return None
            
            # Send command
            cmd_bytes = command.encode() + b'\r\n'
            self.device.write(bulk_out.bEndpointAddress, cmd_bytes, timeout=timeout_ms)
            
            # Try to read response if input endpoint exists
            if bulk_in:
                try:
                    response = self.device.read(bulk_in.bEndpointAddress, 1024, timeout=timeout_ms)
                    response_str = bytes(response).decode('utf-8', errors='ignore').strip()
                    return response_str if response_str else None
                except usb.core.USBTimeoutError:
                    # This is an expected timeout, not an error
                    return "TIMEOUT"
            else:
                return "SENT"

        except usb.core.USBTimeoutError:
            # This is an expected timeout, not an error
            return "TIMEOUT"
        except Exception as e:
            print(f"Raw USB command error: {e}")
            return None
    
    def disconnect(self):
        """Close connections and release resources."""
        if self.visa_resource:
            self.visa_resource.close()
            self.visa_resource = None
        if self.device:
            try:
                # Release the interface
                usb.util.release_interface(self.device, 0)
                # Re-attach the kernel driver if it was detached
                self.device.attach_kernel_driver(0)
                print("Re-attached kernel driver.")
            except Exception as e:
                # This can fail if no driver was attached, which is fine.
                pass
            self.device = None
        if self.rm:
            # This is part of PyVISA, no need to close separately if resource is closed
            self.rm = None
        print("Disconnected")