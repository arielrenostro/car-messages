import time

from RPi import GPIO

from mq import send_error_message, send_info_message
from settings import CAR


def init():
    print("Setup GPIO")
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(CAR['PIN']['FIRST_STAGE_KEY'], GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(CAR['PIN']['SECOND_STAGE_KEY'], GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(CAR['PIN']['HAND_BREAK'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(CAR['PIN']['TURNED_ON'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def stop():
    if is_turned_on():
        turn_off()

    GPIO.cleanup()


def is_turned_on():
    return GPIO.input(CAR['PIN']['TURNED_ON']) == GPIO.HIGH


def is_hand_break_pulled():
    return GPIO.input(CAR['PIN']['HAND_BREAK']) == GPIO.HIGH


def turn_on():
    try:
        if not is_hand_break_pulled() or is_turned_on():
            send_error_message(f'Invalid state to turn on. Hand break [{is_hand_break_pulled()}], Turned ON [{is_turned_on()}]')
            return

        print(f'Turning to the first stage...')
        set_first_stage_key(True)
        time.sleep(5)

        timeout = 1.2
        for i in range(3):
            print(f'Trying to start with {timeout} seconds...')

            set_second_stage_key(True)
            time.sleep(timeout)
            set_second_stage_key(False)

            time.sleep(3)
            if not is_turned_on():
                timeout += 0.3
            else:
                send_info_message(f"Car's turned on!")
                break

        if not is_turned_on():
            send_error_message(f'Fail to car start after 3 retries')
            set_first_stage_key(False)

    except Exception as e:
        send_error_message(f'Error on turn_car_on. {e}')
        set_first_stage_key(False)


def turn_off():
    if not is_turned_on():
        send_error_message(f"Car's already turned off")
        return

    set_first_stage_key(False)
    set_second_stage_key(False)
    time.sleep(3)

    if is_turned_on():
        send_error_message(f"Failed to turn off the car")
        return

    send_info_message(f"Car's turned off")


def set_first_stage_key(bool_value):
    gpio_level = _get_gpio_level(bool_value)
    GPIO.output(CAR['PIN']['FIRST_STAGE_KEY'], gpio_level)


def set_second_stage_key(bool_value):
    gpio_level = _get_gpio_level(bool_value)
    GPIO.output(CAR['PIN']['SECOND_STAGE_KEY'], gpio_level)


def _get_gpio_level(bool_value):
    return GPIO.LOW if bool_value else GPIO.HIGH
