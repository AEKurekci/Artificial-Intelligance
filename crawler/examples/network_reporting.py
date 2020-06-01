import time
import sys
import os
import datetime

TODAY = str(datetime.datetime.now().date())


def hello():
    print("hello world")


def install_libs():
    os.system("sudo apt-get install -y auditd")
    os.system("sudo apt-get install dstat")


def add_etc_audit(audit_type):
    os.system("sudo auditctl -w /etc/" + audit_type + " -p wa -k " +
              audit_type + "_changes")


def add_rules():
    add_etc_audit("passwd")
    add_etc_audit("group")
    add_etc_audit("sudoers")
    add_etc_audit("shadow")


def check_faileds():
    os.system("sudo ausearch -m USER_LOGIN -sv no >> " + path + "/reporting" + "/failed_login_" + TODAY + ".log")
    os.system("sudo aureport --failed -ts yesterday -te now >> " + path + "/reporting/failed_summary_" + TODAY + ".log")


def create_reporting(path):
    os.system("mkdir " + path + "/reporting")


def report():
    check_faileds()
    os.system("sudo aureport -ts yesterday -te now >> " + path + "/reporting/" + "summary_report_" + TODAY + ".log")
    os.system("printf '\n\n=======Memory Report=====\n\n' >> " + path +
              "/reporting/memory_report_" + TODAY + ".log")
    os.system("df -h --total >> " + path + "/reporting/memory_report_" +
              TODAY + ".log")


def report_with_dstat():
    os.system("dstat --output >> " + path + "/reporting/current_report_" +
              TODAY + ".csv")


def current_status():
    os.system("sudo service --status-all > " + path + "/reporting/current_status_" + TODAY + ".log")


def encrypt():
    os.system("gpg -c " + path + "/reporting/current_status_" + TODAY + ".log")


path = ""
if len(sys.argv) > 1:
    if os.path.isdir(sys.argv[1]):
        path = sys.argv[1]
    else:
        print("Path couldn't find, default path is ~/Desktop")
        path = "~/Desktop"
else:
    path = "~/Desktop"

is_install_lib = raw_input("Do you want to install related libraries?(y/n)(auditd, dstat)(advised for first running)")
print(is_install_lib)

if is_install_lib == "y":
    install_libs()

is_add_rules = raw_input("Do you want to add initial rules for auditd?(y/n)(advised for first running)")
if is_add_rules == "y":
    add_rules()

create_reporting(path)
# report_with_dstat()
try:
    while True:
        report()
        current_status()
        print("Reporting now..until you press Ctrl+C")
        time.sleep(3)
except KeyboardInterrupt:
    encrypt()
    pass
