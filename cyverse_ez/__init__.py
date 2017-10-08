import click
from git import Repo
from os import listdir
from os.path import isfile, join
import os
import sys
from datetime import datetime
import subprocess

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
EZ_ROOT_DIR='/opt/cyverse/tmp/'
EZ_MODULES_DIR=EZ_ROOT_DIR + 'python-cyverse-ez-modules'
EZ_MODULES_REPO="https://github.com/edwins/python-cyverse-ez-modules.git"
DEBUG=False

# Writing log to /tmp since it doesn't require root privs
LOG_NAME='/tmp/cyverse-ez.log'
LOG_HANDLE = None

#@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--debug', is_flag=True, default=False, help='enables python debugging')
@click.pass_context
def ez(ctx, debug):
   global DEBUG

   init_log()
   
   if debug:
      echo_msg ("Debugging enabled")
      DEBUG = True

   debug_msg('start ez.ez()')

   if ctx.invoked_subcommand is None:
      click.echo(ctx.get_help())

   debug_msg('end ez.ez()')
      

if __name__ == '__main__':
   ez()

@ez.command('update',short_help='update the ez commands')
def update():

   debug_msg('start ez.update()')

   echo_msg ("Updating ez")

   if not os.path.exists(EZ_ROOT_DIR):
      debug_msg("update: creating root directory " + EZ_ROOT_DIR)
      subprocess.call ('/usr/bin/sudo /bin/mkdir -p -m 0777 ' + EZ_ROOT_DIR, shell=True)

   if not os.path.exists(EZ_MODULES_DIR):
      debug_msg("update: cloning repo " + EZ_MODULES_REPO + " into "+ EZ_MODULES_DIR)
      Repo.clone_from (EZ_MODULES_REPO, EZ_MODULES_DIR)
      #os.makedirs (EZ_MODULES_DIR)
      os.chmod (EZ_MODULES_DIR, 0777)
   else:
      debug_msg("update: git pulling modules repo " + EZ_MODULES_REPO)
      repo = Repo.init(EZ_MODULES_DIR)
      repo.remotes.origin.pull()
      
   echo_msg ("Finished updating. You can call ez again")
   debug_msg('end ez.update()')

def init_log():
   global LOG_HANDLE

   # touch the file and set the perms
   if LOG_HANDLE is None:
      if not os.path.exists (LOG_NAME):
         os.mknod (LOG_NAME)
         os.chmod (LOG_NAME, 0777)
      LOG_HANDLE = click.open_file(LOG_NAME, 'a')

# This function will write to stdout and to the log file
def echo_msg (msg):
   
   time_stamp = datetime.now().strftime('%b %d %H:%M:%S')
   click.echo (msg)
   LOG_HANDLE.write (time_stamp + ' ' + msg + '\n')

def debug_msg (msg):
   global DEBUG
   global LOG_HANDLE
   
   if DEBUG:
      echo_msg ("DEBUG " + msg)

# stub for the main function
ez_command_collection = click.CommandCollection (sources=[ez])
if __name__ == '__main__':
   ez_command_collection()

