#!/usr/bin/python

import re
import shlex
import syslog

path = '/root/Downloads/'


# Function used for executing commands.
def execute_command(cmd, module):
   # if debug:
        syslog.syslog("execute_command(): cmd = %s" % cmd)
    # Break command line into arguments.
    # This makes run_command() use shell=False which we need to not cause shell
    # expansion of special characters like '*'.
        cmd_args = shlex.split(cmd)
        return module.run_command(cmd_args)



# Function used to install package.
def package_present(name, module):

        install_cmd = 'upgradepkg'

        # Install the package
        (rc, stdout, stderr) = execute_command("%s %s %s" % (install_cmd, path, name), module)

        # rc=1

        return (rc, stderr)


#        rc, stdout, stderr = execute_command(command, module)

        if (stderr):
              module.fail_json(msg="failed in get_package_state(): " + stderr)

        if rc == 0:
              return True
        else:
              return False


# Main control flow

def main():
    module = AnsibleModule(
        argument_spec = dict(
            name = dict(required=True),
            state = dict(required=True, choices=['present']),
        ),
#        supports_check_mode = True
    )

    name = module.params['name']
    state = module.params['state']

    rc = 0
    stdout = ''
    stderr = ''
    dpath = ''
    result = {}
    result['name'] = name
    result['state'] = state



    # Parse package name and put results in the pkg_spec dictionary.
#    pkg_spec = {}
#    parse_package_name(name, pkg_spec, module)


    # Get package state.
#    installed_state = get_package_state(name, pkg_spec, module)


    # Perform requested action.
    if state in ['present']:
         (rc, changed)=package_present(name, module)

    if rc != 0:
        if stderr:
            module.fail_json(msg=stderr)
        else:
            module.fail_json(msg=stdout)

    result['changed'] = changed

    module.exit_json(**result)

# import module snippets
from ansible.module_utils.basic import *
main()




