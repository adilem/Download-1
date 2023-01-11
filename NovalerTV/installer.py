# -*- coding: utf-8 -*-
# code: BY MOHAMED_OS


from json import loads
from os import chdir, popen, remove, system
from os.path import isfile
from sys import version_info
from time import sleep

if version_info[0] == 3:
    from urllib.error import HTTPError, URLError
    from urllib.request import Request, urlopen, urlretrieve
else:
    from urllib import urlretrieve

    from urllib2 import HTTPError, Request, URLError, urlopen


# colors
C = "\033[0m"     # clear (end)
R = "\033[0;31m"  # red (error)
G = "\033[0;32m"  # green (process)
B = "\033[0;36m"  # blue (choice)
Y = "\033[0;33m"  # yellow (info)

URL = 'https://raw.githubusercontent.com/MOHAMED19OS/Download/main/NovalerTV/'

package = 'enigma2-plugin-extensions-novalertv'


def Image():
    global status, update, install, uninstall
    if isfile('/etc/opkg/opkg.conf'):
        status = '/var/lib/opkg/status'
        update = 'opkg update >/dev/null 2>&1'
        install = 'opkg install'
        uninstall = 'opkg remove --force-depends'
    return isfile('/etc/opkg/opkg.conf')


def info(item):
    try:
        req = Request('{}version.json'.format(URL))
        req.add_header(
            'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0')
        response = urlopen(req)
        link = loads(response.read()).get(item)
        if item == 'depends':
            if version_info[0] == 3:
                return list(map(lambda x: x.replace('python', 'python3').replace('python3-imaging', 'python3-pillow'), link))
        return link
    except HTTPError as e:
        print('HTTP Error code: ', e.code)
    except URLError as e:
        print('URL Error: ', e.reason)


def check():
    package_list = info('depends')
    with open(status) as f:
        for c in f.readlines():
            if c.startswith('Package:'):
                pkg = c[c.index(' '):].strip()
                while (package_list.count(pkg)):
                    package_list.remove(pkg)
    return package_list


def version():
    return popen("opkg info {} | grep Version | awk '{{print $2}}'".format(package)).read().strip()


def main():
    if not Image():
        print('\n{}(!){}sorry image not supported!!\n'.format(R, C).capitalize())
        sleep(0.8)
        print("   Written by {}MOHAMED_OS{} (͡๏̯͡๏)\n".format(R, C))
        exit(0)

    if check():
        system(update)
        for name in check():
            system('clear')
            print("   >>>>   {}Please Wait{} while we Install {}{}{} ...".format(
                G, C, Y, name, C))
            system(" ".join([install, name]))
            sleep(1)

    if version_info[0] == 3:
        file = "".join([package, "_py3_{}_all.ipk".format(info('version'))])
    else:
        file = "".join([package, "_py2_{}_all.ipk".format(info('version'))])

    chdir('/tmp')

    if isfile(file):
        remove(file)
        sleep(0.8)

    if version() == info('version'):
        system('clear')
        print('you are use the latest version: {}{}{}\n'.format(
            Y, info('version'), C).capitalize())
        sleep(0.8)
        print("   Written by {}MOHAMED_OS{} (͡๏̯͡๏)\n".format(R, C))
        exit()
    else:
        system("".join([uninstall, package]))

    system('clear')
    print("{}Please Wait{} while we Download And Install {}Novaler TV{} ...".format(
        G, C, Y, C))

    urlretrieve("".join([URL, file]), filename=file)
    sleep(0.8)

    system(" ".join([install, file]))
    sleep(1)

    system('killall -9 enigma2')


if __name__ == '__main__':
    Image()
    main()
    print("\n   Written by {}MOHAMED_OS{} (͡๏̯͡๏)\n".format(R, C))
