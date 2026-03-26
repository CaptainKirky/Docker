import smbus2
import time

# I2C bus (1 for modern Raspberry Pi)
bus = smbus2.SMBus(1)

ADS1115_ADDRESS = 0x48

# Register pointers
CONVERSION_REG = 0x00
CONFIG_REG = 0x01

def read_channel(channel):
    if channel < 0 or channel > 3:
        raise ValueError("Channel must be 0-3")

    # Config setup
    config = 0x8000  # Start single conversion

    # Select channel (AIN0–AIN3)
    config |= (0x4000 + (channel * 0x1000))

    # ±4.096V range
    config |= 0x0200

    # Single-shot mode
    config |= 0x0100

    # 128 SPS
    config |= 0x0080

    # Disable comparator
    config |= 0x0003

    # Write config register (split into two bytes)
    bus.write_i2c_block_data(
        ADS1115_ADDRESS,
        CONFIG_REG,
        [(config >> 8) & 0xFF, config & 0xFF]
    )

    # Wait for conversion
    time.sleep(0.01)

    # Read conversion result
    data = bus.read_i2c_block_data(ADS1115_ADDRESS, CONVERSION_REG, 2)

    result = (data[0] << 8) | data[1]

    # Convert to signed integer
    if result > 0x7FFF:
        result -= 0x10000

    return result

# Read soil sensor on A0
while True:
    value = read_channel(0)
    print("Soil Moisture Raw:", value)
    print(max(0, min(100, (18900 - value) * 100 / (18900 - 7800))))
    time.sleep(1)
