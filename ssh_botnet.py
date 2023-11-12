import os
import nmap
from termcolor import colored
from botnet import Botnet
import optparse


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-u", "--username", dest="user", help="Specify common username")
    parser.add_option("-p", "--password", dest="password", help="Specify common password")
    parser.add_option("-i", "--interface", dest="interface", help="Network interface")

    (options, arguments) = parser.parse_args()
    if not options.user:
        _extracted_from_get_arguments_9(
            "[-] Specify common username accross ssh servers\n", parser
        )
    if not options.password:
        _extracted_from_get_arguments_9(
            "[-] Specify common password accross ssh servers\n", parser
        )
    if not options.interface:
        _extracted_from_get_arguments_9("[-] Specify network interface\n", parser)
    return options


# TODO Rename this here and in `get_arguments`
def _extracted_from_get_arguments_9(arg0, parser):
    print
    arg0
    print
    parser.print_help()
    exit()


def getSshServers(myip):
    nm = nmap.PortScanner()

    print
    "\n[*] Scanning network for ssh servers ..."
    nm.scan(f'{myip}/24')
    print
    "[+] Scan complete\n"

    hosts = nm.all_hosts()
    hosts.remove(myip)

    if len(hosts) == 0:
        print
        "[-] No live hosts other than you found on this network"
        exit()

    ssh_servers = {}
    for i in hosts:
        openPorts = list(nm[i]['tcp'].keys())
        for j in openPorts:
            if nm[i]['tcp'][j]['name'] == 'ssh':
                por = j
                ssh_servers[i] = j
                break
            por = -1

    return ssh_servers


def listSshServers(ssh_servers):
    print("Running ssh servers : ")
    with open('session.txt', 'w') as f2:
        for i, j in ssh_servers.items():
            print
            f"Host : {i}" + "\t\t" + "port : " + str(j)
            f2.write(f"{i}:{str(j)}" + '\n')
        print
        '\n'


def main():
    options = get_arguments()
    print("""
Author : Goutham R
GitHub : https://github.com/G0uth4m
	
	- This is a simple tool handy for linux administrators 
	in schools, colleges, etc where all the systems used by students
	in the lab or elsewhere have same usernames and passwords.

	- Future releases will be having a choice to input different usernames
	and passwords via a file.

	- This code was tested on a bunch metasploitable 2 servers.

	- Using this tool for illegal stuff is highly not recommended.

	- 'sudo' is unsupported. You can use root as username for superuser access.

	 _         _           _              _   
 ___ ___| |__     | |__   ___ | |_ _ __   ___| |_ 
/ __/ __| '_ \    | '_ \ / _ \| __| '_ \ / _ \ __|
\__ \__ \ | | |   | |_) | (_) | |_| | | |  __/ |_ 
|___/___/_| |_|___|_.__/ \___/ \__|_| |_|\___|\__|
             |_____|                              
""")

    interface = options.interface
    user = options.user
    password = options.password

    myip = (
        os.popen(
            f"ifconfig {interface}" + " | grep \"inet \" | awk \'{print $2}\'"
        )
        .read()
        .replace("\n", "")
    )
    ssh_servers = getSshServers(myip)
    listSshServers(ssh_servers)

    choice = raw_input("Continue adding bots to the botnet?[Y/n] ")
    print("\n")
    if (choice in ["n", "N", "no"]):
        exit()

    botnet = Botnet()
    for i, j in ssh_servers.items():
        botnet.addBot(i, user, password, j)

    while True:
        strr = colored('ssh@botnet:~$ ', 'red', None, ['bold'])
        a = raw_input(strr)

        if a in ["exit()", "exit"]:
            botnet.f.close()
            print("\n[*] History of commands stored in logs.txt")
            break;
        else:
            botnet.sendCommandsToBots(a)


if __name__ == "__main__":
    main()
