
import lgpio
import time
import sys

GPIO_LED_PIN = int(sys.argv[1])
GPIO_LED_ON_TIME = int(sys.argv[2])/1000
GPIO_LED_DELAY = int(sys.argv[3])/1000


# Open GPIO chip (0 is usually correct for Raspberry Pi)
chip = lgpio.gpiochip_open(0)

#LED_PIN = 17  # BCM pin number (change if needed)

# Claim the pin as output
lgpio.gpio_claim_output(chip, GPIO_LED_PIN)

try:
    while True:
        lgpio.gpio_write(chip, GPIO_LED_PIN, 1)  # LED ON
        time.sleep(GPIO_LED_ON_TIME)

        lgpio.gpio_write(chip, GPIO_LED_PIN, 0)  # LED OFF
        time.sleep(GPIO_LED_DELAY)

except KeyboardInterrupt:
    pass

# Cleanup
lgpio.gpiochip_close(chip)


