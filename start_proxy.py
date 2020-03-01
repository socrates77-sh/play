import os


def main():
    # mitm_cmd = 'mitmdump -s'
    mitm_cmd = 'mitmweb -s'
    addon_file = r'e:\py\play\DriverPass.py'
    os.system('%s %s' % (mitm_cmd, addon_file))


if __name__ == '__main__':
    main()
