import asyncio  
import websockets
import websockets.legacy
import websockets.legacy.server  
from LM_gpt_server import sync_vivogpt
from LM_img_require import askVivo_for_img
import json

APP_ID = '3031259083'
APP_KEY = 'ZCaBAbjMRsAtNcls'

def chat_Deal(source_data):
    get_from_vivo=sync_vivogpt(source_data['prompt'],APP_ID,APP_KEY)
    return get_from_vivo
def wst_img_Deal(source_data):
    img_url=askVivo_for_img(source_data['message'],APP_ID,APP_KEY)
    return img_url

#这个函数能接受任意大小的bytes数据并返回
async def My_receiver(websocket : websockets.legacy.server.WebSocketServerProtocol):
    #客户端每次收到READY后发送数据，直到发送 'message_have_sent_done'结束一次传送
    data=''
    total=''
    while True:
        await websocket.send('READY__')
        data = await websocket.recv()
        if(data == 'message_have_sent_done'):
            #print(total)
            return total
        else:
            total+=data
            


client_list = set()

async def echo(websocket : websockets.legacy.server.WebSocketServerProtocol, path): 
    print('websocket connect:')
    print(websocket.origin) 
    client_list.add(websocket)
    async for message in websocket:  
        #客户端每次请求要先以字符串发送command，服务器返回对应的ack
        if(message == 'chat'):
            await websocket.send('chat_OK')
            print("chat OK")
            chat_info=json.loads(await My_receiver(websocket))
            #这里没有使用分片发送，数据量会受到限制
            await websocket.send("CHAT_RETURN"+chat_Deal(chat_info))
        elif(message == 'wst_img'):
            await websocket.send('wst_img_OK')
            img_info=json.loads(await My_receiver(websocket))
            #这里没有使用分片发送，数据量会受到限制
            await websocket.send("WST_IMG_RETURN"+json.dumps(wst_img_Deal(img_info)))


if __name__ == "__main__":
    start_server = websockets.serve(echo, "127.0.0.1", 8765)  

    loop=asyncio.get_event_loop()
    loop.run_until_complete(start_server)  
    loop.run_forever()