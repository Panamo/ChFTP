# In The Name Of God
# ========================================
# [] File Name : main.py
#
# [] Creation Date : 26-05-2015
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
# =======================================
__author__ = 'Parham Alvani'

import cmd
import sys
import logging

from presence import PresenceService
from peer import PeerList


class ChFTP(cmd.Cmd):
    def __init__(self):
        super(ChFTP, self).__init__()
        self.files = []
        self.username = ""
        self.presenceService = None

    def do_login(self, args: str):
        self.username = args
        print("Welcome %s" % self.username)

    def do_add(self, args: str):
        self.files += args.split(" ")

    def do_run(self, args: str):
        self.presenceService = PresenceService(self.files, self.username)
        self.presenceService.start()
        print("Presence service started....")

    def do_list(self, args: str):
        for peer in PeerList():
            print(peer)

    def do_get(self, args: str):
        args = args.split(" ")
        if len(args) != 2:
            print("*** invalid number of arguments")
            return
        username = args[0]
        file = args[1]
        for peer in PeerList():
            if peer.username == username and peer.files.count(file) > 0:
                ip = peer
                break
        else:
            print("*** invalid username, file pair")

    def do_quit(self, args: str):
        self.presenceService.shutdown()
        sys.exit(0)


logging.basicConfig(filename='ChFTP.log', level=logging.INFO)
cli = ChFTP()
cli.prompt = "ChFTP> "
cli.cmdloop()