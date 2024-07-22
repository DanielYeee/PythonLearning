from Quartz.CoreGraphics import CGEventCreateKeyboardEvent, kCGEventKeyDown, kCGEventKeyUp, CGEventPost, kCGEventFlagMaskShift, kCGEventFlagMaskControl, kCGEventFlagMaskAlternate, kCGEventFlagMaskCommand, kCGAnnotatedSessionEventTap
import time

# Define the key codes for the keys we need
key_code_period = 0x2F

# Create and post the key down event
def create_key_event(key_code, is_key_down):
    event = CGEventCreateKeyboardEvent(None, key_code, is_key_down)
    CGEventPost(kCGAnnotatedSessionEventTap, event)

# Press the key combination
def press_sysdiagnose_keys():
    # Define the flags for the modifier keys
    flags = kCGEventFlagMaskShift | kCGEventFlagMaskControl | kCGEventFlagMaskAlternate | kCGEventFlagMaskCommand
    
    # Create the key down event with modifiers
    event = CGEventCreateKeyboardEvent(None, key_code_period, True)
    event.setFlags(flags)
    CGEventPost(kCGAnnotatedSessionEventTap, event)
    
    # Create the key up event
    event = CGEventCreateKeyboardEvent(None, key_code_period, False)
    event.setFlags(flags)
    CGEventPost(kCGAnnotatedSessionEventTap, event)

# Give some time before executing the key press
time.sleep(3)

# Execute the key press
press_sysdiagnose_keys()
