#!/usr/bin/env python2

import time,imaplib,os,argparse
from sys import exit
import pynotify as pyn


def notif_gen(n):
	return pyn.Notification("You have mail.","New messages:"+str(n))


def checkmail(wher,un,pw):
	try:
		m = imaplib.IMAP4_SSL(wher,'993')
	except:
		print "Name or service unknown"
		exit()
	try:
		m.login(un,pw)
	except:
		print "Authentication failed."
		exit()
	m.select()
	t , mnum = m.search(None,"UnSeen" )
	m.logout()
	return len(mnum[0].split())

def credinals():
	pars = argparse.ArgumentParser(description="py-notify mail checker" )
	pars.add_argument("-u",action="store",dest="usr",help="username@host")
	pars.add_argument("-p",action="store",dest="pas",help="email password")
	pars.add_argument("-s",action="store",dest="ser",help="email server")
	pars.add_argument("-t",action="store",dest="tmt",type=int,default=120,help="check timeout")
	c= pars.parse_args()
	if c.pas and c.usr and c.ser:
		return (c.ser,c.usr,c.pas,c.tmt)
	else:
		pars.print_help()
		exit(0)

if __name__ == "__main__" :
	pyn.init("mail checker")
	c = credinals()
	tmp = checkmail(c[0],c[1],c[2])
	notif_gen(tmp).show()
	while True:
		a = checkmail(c[0],c[1],c[2])
		if a > tmp:
			tmp=a
			notif_gen(tmp).show()
		else:
			time.sleep(c[3])



