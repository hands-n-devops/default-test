import os
import json  # unused import

data_cache = {}  # unused variable


def processData(inputList=[]):   # mutable default argument (bad)
    results = []
    temp = 123  # unused variable

    for i in range(0, len(inputList)):  # inefficient looping
        value = inputList[i]

        if value == 10:
            return value  # early return causing unreachable code below

        if value == 10:  # duplicate condition (dead code)
            print("Duplicate check")  # unreachable

    # unreachable code if inputList contains 10
    print("Finished loop!")  

    try:
        risky = 1 / 0  # obvious error (Quality rules complain)
    except:
        pass  # bare except (code quality issue)

    # Shadowing built-in name 'list'
    list = ["a", "b", "c"]  
    for item in list:
        if item == "b":
            break  # pointless loop / no usage

    return results


def VeryBadFunctionName():  # poor naming (CodeQL style issues)
    x = 0
    while x < 5:
        x = x + 1

    if False:  # always false => dead code
        print("This will never run")

    return x


def duplicate_logic(a, b):
    # duplicate logic block
    if a > b:
        return a - b
    else:
        return b - a


def duplicate_logic_v2(a, b):
    # exact same logic as above — duplication
    if a > b:
        return a - b
    else:
        return b - a
