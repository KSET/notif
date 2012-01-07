#!/usr/bin/env python

import sys, time, imaplib, pynotify, os
from getpass import getpass
from gtk import gdk

def run(timeout, username, password):
  number = 0
  
  #icon load
  logoFile = open("./kset.png").read()
  pixbufLoader = gdk.PixbufLoader("png")
  pixbufLoader.write(logoFile, len(logoFile))
  pixbuf = pixbufLoader.get_pixbuf()
  pixbufLoader.close()
  
  #inicijalizira notifajera iz pynotify
  if pynotify.init("Naughty-fy"):
    notif = pynotify.Notification("You have mail!", "Number of new messages: error, didn't check yet?")
    notif.set_urgency(pynotify.URGENCY_CRITICAL)
    notif.set_icon_from_pixbuf(pixbuf)
  else:
    print "there was a problem initializing the pynotify module"
    sys.exit(0)
  
  #konstantni loop za provjeru mejla
  while('True'):
    #spajanje i dohvatanje broja mejlova
    obj = imaplib.IMAP4_SSL('mail.kset.org','993')
    obj.login(username + '@kset.org', password) # ( 'user@kset.org', 'password' )
    obj.select()
    typ, msgnum = obj.search(None,'UnSeen') #Uread msgs
    obj.logout()

    #ispisuje ako treba se broj povecao
    if number < len(msgnum[0].split()):
      #print "\nType:", typ, "\nNumber of new:", len(msgnum[0].split())
      notif = pynotify.Notification("You have mail!", "Number of unread messages:" + str(len(msgnum[0].split())))
      notif.set_urgency(pynotify.URGENCY_CRITICAL)
      notif.set_icon_from_pixbuf(pixbuf)
      notif.show()
        
    #pamti koliko je trenutno neprocitanih
    number = len(msgnum[0].split())
    
    time.sleep(timeout) #sleep 120 sec
      
def UpdateCreds(username, password):
  homePath = os.getenv("HOME")
  userSave = ''
  passSave = ''
  if os.path.exists( homePath+ '/.credentials' ):
    creds = open(homePath+ '/.credentials', 'r').read().split('\n')
    userSave = creds[0].strip()
    passSave = creds[1].strip()
  f = open(homePath+ '/.credentials', 'w')
  if username == '':
    f.write(userSave+'\n')
  else:
    f.write(username+'\n')
  if password == '':
    f.write(passSave)
  else:
    f.write(password)
      
if __name__ == "__main__":
  user = ""
  password = ""
  if len(sys.argv) == 2:
    if 'configure' == sys.argv[1] or '--conf' == sys.argv[1]:
      sys.stdout.write('User: ')
      user = raw_input().split('@')[0].strip()
      password = getpass()
      UpdateCreds(user, password)
    elif 'user' == sys.argv[1] or '--user' == sys.argv[1] or '-u' == sys.argv[1]:
      sys.stdout.write('User: ')
      user = raw_input().split('@')[0].strip()
      UpdateCreds(user, '')
    elif 'pass' == sys.argv[1] or '--pass' == sys.argv[1] or '-p' == sys.argv[1]:
      password = getpass()
      UpdateCreds('', password)
    elif '--help' == sys.argv[1]:
        print """Usage: ./notif.py [OPTION [ARGUMENT]] ...
        
                Checks unread messages from mail.kset.org and displays how many there are.
                To operate correctly, it needs to be given an username and password.
                They will be encrypted.
        
                Options:
                -u      If only option, prompts for username input.
                    Alternatively, it can be followed by username immediately.

                -p      If only option, ptompts for password input and also hides it.
                    Alternatively, it can be followed by password immediately,
                    but in that case it will be visible during it's input, obviously.

                --user  Same as '-u' option.

                --pass  Same as '-p' option.

                --help  Displays this help. 

                --conf  Can only be used if it's the only option.
                    Asks for username and than asks for password.
                    This option hides the pasword too.
              """
    else:
      print 'Unknown command!'
      sys.exit(0)
  elif len(sys.argv) > 2:
    if '-x' == sys.argv[1]:
      run(float(sys.argv[4]), sys.argv[2], sys.argv[3])
      exit(0);
    for arg_num in range(1,len(sys.argv), 2):
      if arg_num >= len(sys.argv)-1:
        print 'Mising argument...'
        sys.exit(0)
      if sys.argv[arg_num] == '-u' or sys.argv[arg_num] == '--user':
        user = sys.argv[arg_num+1].split('@')[0].strip()
        UpdateCreds(user, '')
      if sys.argv[arg_num] == '-p' or sys.argv[arg_num] == '--pass':
        password = sys.argv[arg_num+1]
        UpdateCreds('', password)
    #run(120, user, password)
  else:
    homePath = os.getenv("HOME")
    if os.path.exists( homePath+ '/.credentials' ):
      creds = open(homePath+ '/.credentials', 'r').read().split('\n')
      user = creds[0].strip()
      password = creds[1].strip()
      run(5, user, password) # timeout in secondsu
    else:
      print 'Could not load credentials!'
