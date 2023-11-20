import types
from method_result import MethodResult as Result
import json

class DictState:
    def __init__(self) -> None:
        self.unprocessed_value = None
        self.hanging_key = None
        self.data: dict = {}

def get_input(dict_state: DictState) -> Result:
    if dict_state.hanging_key:
        val = input('Enter val: ') 
        if val == 'exit()':
            return Result.failure('exit')
        dict_state.unprocessed_value = val
    else:
        val = input('Enter key: ')        
        if val == 'exit()':
            return Result.failure('exit()')
        if not valid_key(val):
            is_valid = False
            while not is_valid:
                val = input('You must enter a string for the value: ')                    
                if val == 'exit()':
                    return Result.failure('exit()')
                elif isinstance(val, str):
                    is_valid = True
        else:
            dict_state.unprocessed_value = val
    return Result.success(dict_state)

def process_input(dict_state: DictState) -> Result:
    raw_val = dict_state.unprocessed_value
    val = None
    val_type = get_val_type(dict_state.unprocessed_value)
    if val_type == 'list':
        val = raw_val.split(',')
    elif val_type == 'dict':
        val = raw_val.split(':')
        if len(val) % 2 != 0:
            return Result.failure('odd number of colons for dict input only')
        else:
            creating_dict = True
            item_index = 0
            dict_pair_index = 0
            dict_pairs = [[]]
            whole_dict = {}
            while creating_dict:
                if len(dict_pairs[dict_pair_index]) == 2:
                    dict_pair_index += 1
                dict_pairs[dict_pair_index].append(val[item_index])
                item_index += 1
                if item_index == len(val):
                    creating_dict = False
            for pair in dict_pairs:
                whole_dict[pair[0]] = pair[1]
            val = whole_dict
    elif val_type == 'int':
        val = int(val)
    elif val_type == 'float':
        val = float(val)
    elif val_type == 'bool':
        val = True if val == 'True' else False
    elif val_type == 'str':
        val = val
    else:
        return Result.failure('Invalid data type')

#########################################################
    if dict_state.hanging_key:
        d1 = dict_state.data
        d2 = { dict_state.hanging_key : val }
        dict_state.hanging_key = None
        dict_state.unprocessed_value = None
        val = { **d1, **d2 }
    else:
        if val_type in invalid_key_types:
            return Result.failure('Invalid datatype for key')
        else:
            dict_state.hanging_key = val
    dict_state.unprocessed_value = None
    return Result.success(dict_state)

def get_typed_val(val: any) -> Result:
    result_data = None
    result = None
    if len(val.split(',')) > 0 and len(val.split(',')) != 1:
        result_data = val.split(',')
    else:
        parse_dictish(val):
        result_data = json.loads(val)
    else:
        try:
            if isinstance(val, int):
                result = 'int'
        except ValueError:
            try:
                if isinstance(val, float):
                    result = 'float'
            except ValueError:
                if val == 'True' or val == 'False':
                    result = 'bool' 
                else:
                    result = 'str'
    return Result.success(result) if result else Result.failure('failed to find type of val')

def parse_dictish(val: str) -> Result:
    coms = val.split(',')
    cols = [com.split(':') for com in coms]
    # print('is bad') if False in [False for col in cols if len(col) != 2] else None
    cols_valid = True
    for col in cols:
        if len(col) != 2:
            return Result.failure('not a dict')
    dict_str = ''
    dict_str += '{'
    for col in cols:
        dict_str += 'f{col[0]}:{col[1]},'
    dict_str = dict_str[:-1]
    dict_str += '}'
    
def valid_key(val: any) -> bool:
    if isinstance(val, dict) or \
        isinstance(val, list) or \
        isinstance(val, tuple) or \
        isinstance(val, int) or \
        isinstance(val, bool) or \
        isinstance(val, float):
            return False
    return True


def main():

    dict_state = DictState()

    print('welcome')
    print('enter exit() to quit at any time.')
    print('Begin!')
    is_active = True        
    while is_active:
        input_result = get_input(dict_state)
        if not input_result.success:
            print(f'error on input result: {input_result.error_message}')
            is_active = False
        else:
            dict_state = input_result.data
            processed_input_result = process_input(dict_state)
            if processed_input_result.success:
                dict_state = processed_input_result.data
                print(json.dumps(dict_state.data, indent=4))
            else:
                print(f'error on process_input: {processed_input_result.error_message}')
                is_active = False

if __name__ == '__main__':
    main()