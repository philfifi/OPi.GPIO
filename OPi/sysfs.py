# -*- coding: utf-8 -*-
# Copyright (c) 2017 Richard Hull
# See LICENSE.md for details.

import time
import os
from contextlib import contextmanager
from OPi.constants import HIGH, LOW, IN, OUT, \
    NONE, RISING, FALLING, BOTH

# Allow to wait up to 1 second for the file have the correct permissions
WAIT_PERMISSION_TIMEOUT = 1.

@contextmanager
def value_descriptor(pin, mode="r"):
    path = "/sys/class/gpio/gpio{0}/value".format(pin)
    start_time = time.time()
    while not os.access(path, os.W_OK) and time.time() - start_time < WAIT_PERMISSION_TIMEOUT:
        time.sleep(0.1)
    with open(path, mode) as fp:
        yield fp


def export(pin):
    path = "/sys/class/gpio/export"
    start_time = time.time()
    while not os.access(path, os.W_OK) and time.time() - start_time < WAIT_PERMISSION_TIMEOUT:
        time.sleep(0.1)
    with open(path, "w") as fp:
        fp.write(str(pin))


def unexport(pin):
    path = "/sys/class/gpio/unexport"
    start_time = time.time()
    while not os.access(path, os.W_OK) and time.time() - start_time < WAIT_PERMISSION_TIMEOUT:
        time.sleep(0.1)
    with open(path, "w") as fp:
        fp.write(str(pin))


def direction(pin, dir):
    assert dir in [IN, OUT]
    path = "/sys/class/gpio/gpio{0}/direction".format(pin)
    start_time = time.time()
    while not os.access(path, os.W_OK) and time.time() - start_time < WAIT_PERMISSION_TIMEOUT:
        time.sleep(0.1)
    with open(path, "w") as fp:
        if dir == IN:
            fp.write("in")
        else:
            fp.write("out")


def input(pin):
    with value_descriptor(pin) as fp:
        value = fp.read()
        if value.strip() == str(LOW):
            return LOW
        else:
            return HIGH


def output(pin, value):
    str_value = "1" if value else "0"
    with value_descriptor(pin, "w") as fp:
        fp.write(str_value)


def edge(pin, trigger):
    assert trigger in [NONE, RISING, FALLING, BOTH]
    path = "/sys/class/gpio/gpio{0}/edge".format(pin)
    start_time = time.time()
    while not os.access(path, os.W_OK) and time.time() - start_time < WAIT_PERMISSION_TIMEOUT:
        time.sleep(0.1)
    opts = {
        NONE: "none",
        RISING: "rising",
        FALLING: "falling",
        BOTH: "both"
    }
    with open(path, "w") as fp:
        fp.write(opts[trigger])
