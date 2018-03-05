import json
from os.path import isfile as file_exists


def get_assets(filename):

    assert file_exists(filename), \
            "Filename '{}' doesn't exist!".format(filename)
    with open(filename, 'r') as f:
        compiled_interfaces = json.loads(f.read())['contracts']
    
    # compiled assets JSON object should be structured like:
    # 'contracts' : {
    #   'Contract1' : {
    #           'abi' : ..., 
    #           'bytecode' : ..., 
    #           'bytecode_runtime' : ... 
    #   },
    #   'Contract2' : ...
    # }
    required_members = ['abi', 'bytecode', 'bytecode_runtime']

    for name, interface in compiled_interfaces.items():
        # Filter out stuff we don't need
        filtered_interface = dict()
        for member in interface.keys():
            if member == 'abi':
                filtered_interface['abi'] = interface[member]
            # Standardize names to Web3.py expected interfaces
            if member == 'bin':
                filtered_interface['bytecode'] = interface[member]
            if member == 'bin-runtime':
                filtered_interface['bytecode_runtime'] = interface[member]

        # Check for required interfaces
        for member in required_members:
            assert member in filtered_interface.keys(), \
                    "Contract '{}' doesn't have '{}'!".format(name, member)

        # Result is now exactly what we were looking for
        compiled_interfaces[name] = filtered_interface
    
    return compiled_interfaces
