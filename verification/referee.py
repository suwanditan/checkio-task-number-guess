from checkio.signals import ON_CONNECT
from checkio import api
from checkio.referees.multicall import CheckiORefereeMulti

from tests import TESTS

MAX_ATTEMPT = 8

def initial_referee(data):
    data["attempt_count"] = 0
    data["guess"] = 0
    return data

def process_referee( referee_data, user_result ):
    referee_data['attempt_count'] += 1
    
    if referee_data['attempt_count'] > MAX_ATTEMPT:
        referee_data.update({"result": False, "result_addon": "Too many moves."})
        return referee_data
        
    if not isinstance( user_result, ( list, tuple ) ) or len( user_result ) != 2:
        referee_data.update({"result": False, "result_addon": "The function should return a list with two values."})
        return referee_data
        
    goal = referee_data['number']
    prev_steps = referee_data['input']
    divisor, guess = user_result
    referee_data['guess'] = guess
    
    if not isinstance( divisor, int ) or not isinstance( guess, int ):
        referee_data.update({"result": False, "result_addon": "Result list format is [int, int]"})
        return referee_data
        
    if divisor <= 1 or divisor > 10:
        referee_data.update({"result": False, "result_addon": "You gave wrong divisor range."})
        return referee_data

    if guess < 1 or guess > 100:
        referee_data.update({"result": False, "result_addon": "You gave wrong guess number range."})
        return referee_data

    remainder = goal % divisor
    prev_steps.append( ( remainder , divisor ) )
    
    referee_data.update({"result": True, "result_addon": "Next Step"})
    return referee_data

def is_win_referee(referee_data):
    goal = referee_data['number']
    guess = referee_data['guess']
    
    return goal == guess

api.add_listener(
    ON_CONNECT,
    CheckiORefereeMulti(
        tests=TESTS,
        initial_referee=initial_referee,
        process_referee=process_referee,
        is_win_referee=is_win_referee,
        ).on_ready)
