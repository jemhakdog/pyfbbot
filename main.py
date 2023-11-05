from fbchat import log, Client
import os
import importlib
import  asyncio
import  json
import builtins
import sys

with open("config.json","r") as file:
    config=json.load(file)
    builtins.config=config



try:
    with open(config["appsate"],"r") as file:
        appstate=json.load(file)
except Exception as e:
    print('error:',e)
    sys.exit()

session={}    
for i in appstate:
    session.__setitem__(i['key'],i['value'])
       

from cmds import *

command_names=[]
command_file_name=[]

def get_command():
  print('<<===[ loading commands ]===>>')
  
  for roots,dirs,files in os.walk(config['command_folder']):
    files1=files
    break
  for i in files1:
    if i!='__init__.py' and i.endswith('.py'):
      name=i[:-3]
      cmd=importlib.import_module('cmds')
      info=eval(f'cmd.{name}.info')
      if 'name' in info and 'usage' in info and 'version' in info:
          print(f'[ command ] {info["name"]} ({i}) >> loaded')
          command_names.append(info["name"])
          command_file_name.append(name)
      return cmd
                         
sc=get_command()              
async def handle_commands(self,message,id,thread):
    use=False
    msg=message.split(" ",1)
    if config['use_prefix'] and msg[0].startswith(config['prefix']):
        use=True
        msg[0]=msg[0].replace(config['prefix'],'')
    elif config['use_prefix'] == False:
        use=True
    if msg[0] in command_names and use:
        try:
            return await eval(f'sc.{msg[0]}.run(self,msg[1],id,thread)')
        except:
            msg[1]=''
            return await eval(f'sc.{msg[0]}.run(self,msg[1],id,thread)')
        
        

          
print('<<===[ logging in ]===>>')
logged_in=False
class Bot(Client):
    #print('<<===[ logged in ]===>>')
    
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)

        log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))


        try:
            msg = str(message_object).split(",")[15][14:-1]
        
            if "//video.xx.fbcdn" in msg:
                msg = msg
            else:
                msg = str(message_object).split(",")[19][20:-1]
        except:
            try:
                msg = message_object.text.lower()
            except:
                msg = "Unable to extract message content."
            
        
        
        if author_id != self.uid:
            
            asyncio.run(handle_commands(self,msg,thread_id,thread_type))  
    def onFriendRequest(self,from_id,msg):
          print(f'friend request from {from_id}')
          friend_id=from_id
          try:
              self.friendConnect(friend_id)        
          except:
              pass   
          
                      
client = Bot("<email>", "<password>",session_cookies=session)

if client.isLoggedIn() and not logged_in:
        user = client.fetchUserInfo(client.uid)[client.uid]
        if config['use_prefix']:
            print(f'logged in as:{user.name}')
            print(f"prefix:{config['prefix']}")
        else:
            print(f'logged in as:{user.name}')
log=''
client.listen()
