# In The Name Of God
# ========================================
# [] File Name : ChFTP_cli.py
#
# [] Creation Date : 26-05-2015
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
# =======================================

import cmd
import logging
import sys

from ftp.file_transfer import FileTransferServer
from ftp.file_transfer import recv_file
from ftp.storage import FileStorage
from presence.peer import PeerList
from presence.presence import PresenceService

try:
    import termcolor
except ImportError:
    termcolor = None


class ChFTP(cmd.Cmd):
    def __init__(self):
        super(ChFTP, self).__init__()

        if termcolor:
            self.prompt = termcolor.colored("ChFTP> ", color='red')
        else:
            self.prompt = "ChFTP> "
        self.intro = "Welcome to ChFTP shell from chapna company.\n"

        self.folders = []
        self.username = ""
        self.presenceService = None
        self.fileTransferServer = None

    def do_login(self, args: str):
        self.username = args
        print("Welcome %s" % self.username)

    def help_login(self):
        command = "login {username}"
        if termcolor:
            command = termcolor.colored(command, color='green', attrs=['bold'])
        print(command)
        print("Save your username in application")

    def do_add(self, args: str):
        self.folders += args.split(" ")

    def help_add(self):
        if termcolor:
            print(termcolor.colored("add {folders}", color='green', attrs=['bold']))
        else:
            print("add {folders}")
        print("Add these folder into remote storage")

    def do_run(self, args: str):
        self.presenceService = PresenceService(FileStorage(self.folders).get_files_name(), self.username)
        self.presenceService.start()
        print("Presence service started....")
        self.fileTransferServer = FileTransferServer()
        self.fileTransferServer.start()
        print("File transfer server started....")

    def help_run(self):
        command = "run"
        if termcolor:
            command = termcolor.colored(command, color='green', attrs=['bold'])
        print(command)
        print("Run presence and file transfer services,")
        print("please note that after this you cannot change your username or add new folders")

    def do_list(self, args: str):
        for peer in PeerList():
            print(peer)

    def help_list(self):
        command = "list"
        if termcolor:
            command = termcolor.colored(command, color='green', attrs=['bold'])
        print(command)
        print("List known peer with their ip, username and files")

    def do_get(self, args: str):
        args = args.split(" ")
        if len(args) != 3:
            print("*** invalid number of arguments")
            return
        username = args[0]
        rfile = args[1]
        lfile = args[2]
        for peer in PeerList():
            if peer.username == username and peer.files.count(rfile) > 0:
                ip = peer.ip
                break
        else:
            print("*** invalid username, file pair")
            return
        recv_file(ip, rfile, lfile)

    def help_get(self):
        command = "get {username} {remote filename} {local filename}"
        if termcolor:
            command = termcolor.colored(command, color='green', attrs=['bold'])
        print(command)
        print("Get file with remote filename from username and,")
        print("store it in current directory with local filename")

    def do_quit(self, args: str):
        if self.presenceService:
            self.presenceService.shutdown()
        sys.exit(0)

    def help_quit(self):
        command = "quit"
        if termcolor:
            command = termcolor.colored(command, color='green', attrs=['bold'])
        print(command)
        print("Exit from ChFTP")


logging.basicConfig(filename='ChFTP.log', level=logging.INFO)
cli = ChFTP()
try:
    cli.cmdloop()
except KeyboardInterrupt:
    cli.do_quit("")
