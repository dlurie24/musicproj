# Author ~ Danielle Lurie 
# c. November 2020 ~ Year of the Roni

import os
import argparse

DIRECTORIES = [] # list of strings of current directories at level Snugtrees/

# flags
withVideo = False # adds folder video, video/assets
withLogic = True # adds folders audio, audio/logic, audio/logic/bounces, audio/master
newRootFolder = False # adds folder at level Snugtrees/<dir>
listFolders = False # lists folders in Snugtrees/

# strings
snugtrees = "/Volumes/Danielle Lurie External HD/Music/Snugtrees"

audio = "audio"
logic = "audio/logic"
bounces = "audio/logic/bounces"
master = "audio/master"

vid = "video"
assets = "video/assets"

final = "final"

def run():
  get_directories() # sets DIRECTORIES
  parser = make_parser()
  cmds = parse_args(parser)
  run_commands(cmds)

def make_parser():
  parser = argparse.ArgumentParser(description="Make a new music project")
  parser.add_argument('name', type=str, nargs="?", help="a name for the project")
  parser.add_argument('dir', type=str, nargs="?", help="directory to store project within")
  parser.add_argument('-lst', '--list', action='store_true', help="list existing directories")
  parser.add_argument('-n', '--new', action="store_true", help="create a new directory Snugtrees/<dir>")
  parser.add_argument('-l', '--logic', action='store_true', 
                      default=not withLogic, help="don't create folders for Logic files (on by default)")
  parser.add_argument('-v', '--video', dest='video', action='store_true', 
                      default=withVideo, help="add folders for video editing")
  return parser

def parse_args(parser):
  obj = parser.parse_args()
  args = []

  name = obj.name
  dirname = obj.dir

  args.append(name)
  args.append(dirname)

  log = withLogic
  if (obj.logic):
    log = not withLogic
  args.append(log)

  vid = withVideo
  if (obj.video):
    vid = not withVideo
  args.append(vid)

  newRoot = newRootFolder
  if (obj.new):
    newRoot = not newRootFolder
  args.append(newRoot)

  folders = listFolders
  if (obj.list):
    folders = not listFolders
  args.append(folders)
  
  return args

def run_commands(cmds):
  name = cmds[0]
  dirname = cmds[1]
  makeLogicFolders = cmds[2]
  makeVideoFolders = cmds[3]
  newRoot = cmds[4]
  listFolders = cmds[5]

  if listFolders:
    list_directories()
    return

  if name is None:
    raise ValueError("Error: expected name after mproj")
  if dirname is None:
    raise ValueError("Error: expected directory within Snugtrees/ after name")
  if not newRoot and dirname not in DIRECTORIES:
    raise ValueError("Error: directory does not exist (use -n to create a new one)")
  if newRoot and dirname in DIRECTORIES:
    raise ValueError("Error: directory already exists (don't use -n)")
  
  prefix = dirname + '/' + name

  dirs = []
  if newRoot:
    dirs.append(dirname)
  dirs.append(prefix)
  dirs.append(prefix + '/' + final)
  if makeLogicFolders:
    dirs.append(prefix + '/' + audio)
    dirs.append(prefix + '/' + logic)
    dirs.append(prefix + '/' + bounces)
    dirs.append(prefix + '/' + master)
  if makeVideoFolders:
    dirs.append(prefix + '/' + vid)
    dirs.append(prefix + '/' + assets)
  for d in dirs:
    make_directory(d)

def make_directory(dirname):
  s = snugtrees + '/' + dirname + '/'
  os.mkdir(s)
  return s

# Returns a string containing the directories in my music folder
def get_directories():
  dirs = os.listdir(snugtrees)
  dirs = [d for d in dirs if os.path.isdir(snugtrees + "/" + d)]
  s = ''

  for d in dirs:
    DIRECTORIES.append(d)
    s = s + '~ ' + d + '\n'
  return s

def list_directories():
  dirs = get_directories()
  print("Existing Folders :")
  print(dirs)
  print('note: using -lst cancels all other commands')
  

if __name__ == "__main__":
  run()