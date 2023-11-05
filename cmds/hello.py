info = {
    'name':'hello',
    'usage':'hello <ask>',
    'version':'1.0.0',
}



async def run(api,msg,id,thread):
    print('hi',msg)
    
    return  await api.sendMessage(msg, thread_id=id, thread_type=thread)
    
    
if __name__=='__main__':
    print('[ warning ] you cannot run this command directly')