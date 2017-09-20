#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: Wine

short_description: A module to manage Wine

version_added: ""

description:
    - "Use Ansible to run and manage Windows programs on UNIX-like systems using Wine"

options:
    expected_return_code:
        description:
            - A list of expected return codes. By default, both 0 (success) and 3010 (requires reboot) will be marked as successful return codes.
        required: false
    path:
        description:
            - The full path to the Windows executable to run.
        required: true
    wine_binary:
        description:
            - Specify a custom path to a different Wine binary.
        required: false

author:
    - Luke Short (ekutlails)
'''

EXAMPLES = '''
- name: Install a Windows program from a mounted ISO disc
  wine:
    wine_binary: /usr/bin/wine-2.0.2
    path: /run/media/iso/Setup.exe
    expected_return_code: [0, 800, 3010]
'''

RETURN = '''
rc:
    description: The return code from the command.
    type: int
stdout:
    description: The standard output from the command.
    type: str
stderr:
    description: The standard error from the command.
    type: str
'''

from ansible.module_utils.basic import AnsibleModule

wine_binary = None

def run_module():

    module = AnsibleModule(
        argument_spec=dict(
            path=dict(type='str', required=True),
            wine_binary=dict(type='str', required=False),
            # 0 = success, 3010 = requires reboot
            expected_return_code=dict(type='list', required=False, default=[0, 3010])
        ),
        # Running any program will result in unpredicatble results.
        supports_check_mode=False
    )

    global wine_binary

    # Find and set the Wine binary path if it was not provided by the "wine_binary" argument.
    if not wine_binary:
        wine_binary = module.get_bin_path('wine', required=True)
        module.params['wine_binary'] = wine_binary

    result = dict(
        changed=True
    )

    # Put together the full command that will be run on the managed sytem.
    cmd = [wine_binary, module.params['path']]
    # Run the command.
    rc, stdout, stderr = module.run_command(cmd)

    # Save the module results.
    result['rc'] = rc
    result['stdout'] = stdout
    result['stderr'] = stderr

    if rc in module.params['expected_return_code']:
        module.exit_json(**result)
    else:
        module.fail_json(msg="Unexpected return code %s" % str(rc), **results)

def main():
    run_module()

if __name__ == '__main__':
    main()
