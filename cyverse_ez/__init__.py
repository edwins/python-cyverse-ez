import click
from git import Repo
import os
import sys

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
EZ_CLICK_MODULES='/opt/cyverse/tmp/ez_modules'
DEBUG=False
UPDATE_DONE=False

@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--debug', is_flag=True, default=False, help='enables python debugging')
@click.pass_context
def ez(ctx, debug):
   global DEBUG
   
   if debug:
      click.echo ("Debugging enabled")
      DEBUG = True

   debug_msg('in ez.ez()')

   # force an update if the modules don't exist
   if not os.path.exists(EZ_CLICK_MODULES):
      ctx.invoke(update)

if __name__ == '__main__':
   ez()

@ez.command('update',short_help='update the ez commands')
def update():
   global UPDATE_DONE

   # check if update done, if so ignore
   if UPDATE_DONE:
      return
   
   debug_msg('in ez.update()')

   click.echo ("ez: " + EZ_CLICK_MODULES + " not found or 'update' called. Updating...")
   if not os.path.exists(EZ_CLICK_MODULES):
      os.makedirs (EZ_CLICK_MODULES)
      
   # TODO: do a git pull

   click.echo ("ez: finished updating. You can call ez again")

   # set the fact that an update was already finished
   UPDATE_DONE = True
   

def debug_msg (msg):
   global DEBUG
   if DEBUG:
      click.echo ("DEBUG " + msg)
