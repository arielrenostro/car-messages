import time

import RPi.GPIO as gpio

from settings import CAR


def turn_car_on():
    try:
        gpio.setmode(gpio.BOARD)

        gpio.setup(CAR['PIN']['FIRST_STAGE_KEY'], gpio.OUT)
        gpio.setup(CAR['PIN']['SECOND_STAGE_KEY'], gpio.OUT)
        gpio.setup(CAR['PIN']['HAND_BREAK'], gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(CAR['PIN']['TURNED_ON'], gpio.IN, pull_up_down=gpio.PUD_UP)

        hand_break_state = gpio.input(CAR['PIN']['HAND_BREAK'])
        turned_on_state = gpio.input(CAR['PIN']['TURNED_ON'])
        if hand_break_state == gpio.HIGH \
                and turned_on_state == gpio.LOW:
            gpio.output(CAR['PIN']['FIRST_STAGE_KEY'], gpio.HIGH)
            time.sleep(5)

            timeout = 1
            for i in range(3):
                gpio.output(CAR['PIN']['SECOND_STAGE_KEY'], gpio.HIGH)
                time.sleep(timeout)
                gpio.output(CAR['PIN']['SECOND_STAGE_KEY'], gpio.LOW)

                time.sleep(3)
                turned_on_state = gpio.input(CAR['PIN']['TURNED_ON'])
                if turned_on_state != gpio.HIGH:
                    timeout += 1
                else:
                    break

            if turned_on_state == gpio.LOW:
                print(f'Fail to car start after 3 retries')
        else:
            print(f'Invalid state to turn on. Hand break [{hand_break_state}], Turned ON [{turned_on_state}]')
    except Exception as e:
        print(f'Error on turn_car_on. {e}')
    finally:
        gpio.cleanup()
