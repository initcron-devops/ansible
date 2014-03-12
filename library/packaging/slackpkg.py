!/usr/bin/python

import re
import shlex
import syslog

path = '/root/Downloads'

# Function used for executing commands.
def execute_command(cmd, module):
    if debug:
        syslog.syslog("execute_command(): cmd = %s" % cmd)
    # Break command line into arguments.
    # This makes run_command() use shell=False which we need to not cause shell
    # expansion of special characters like '*'.
    cmd_args = shlex.split(cmd)
    return module.run_command(cmd_args)



# Function used to make sure a package is present.
def package_present(name, installed_state, pkg_spec, module):

        # Install the package
        (rc, stdout, stderr) = execute_command("%s %s" % (install_cmd, name), module)

         rc = 1

    return (rc, stdout, stderr, changed)



# Main control flow

def main():
    module = AnsibleModule(
        argument_spec = dict(
            name = dict(required=True),
            state = dict(required=True, choices=['present']),
        ),
        supports_check_mode = True
    )

    name = module.params['name']
    state = module.params['state']

    rc = 0
    stdout = ''
    stderr = ''
    result = {}
    result['name'] = name
    result['state'] = state



    # Parse package name and put results in the pkg_spec dictionary.
    pkg_spec = {}
    parse_package_name(name, pkg_spec, module)



    # Perform requested action.
    if state in ['present']:
        (rc, stdout, stderr, changed) = package_present(name, installed_state, pkg_spec, module)
    

   
    module.exit_json(**result)

# import module snippets
from ansible.module_utils.basic import *
main()

