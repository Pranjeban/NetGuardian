import time
import asyncio
from netgaurdian import *
from datetime import datetime
from quart import Quart, websocket, request, render_template

app = Quart(__name__)
search = netgaurd()

@app.route('/', methods=['GET'])
async def index():
    global search
    return await render_template(
        'homepage.html',
        config=[search.INTERFACE, search.MY_IP, search.MY_MAC],
        flags=search.FILTERED_ACTIVITIES
    )

async def WS_receiver():
    global search
    while search.WEBSOCKET is not None:
        data = await search.WEBSOCKET.receive()
        if data == 'CMD::START':
            if search.flag:
                await search.WEBSOCKET.send('LOG::Already Running')
            else:
                await search.WEBSOCKET.send(f'LOG::Started Sniffer @ {str(datetime.now()).split(".")[0]}')
                search.start()
        elif data == 'CMD::STOP':
            if search.flag:
                await search.WEBSOCKET.send(f'LOG::Stopped Sniffer @ {str(datetime.now()).split(".")[0]}')
                search.stop()
            else:
                await search.WEBSOCKET.send('LOG::Already Stopped')
        elif data == 'CMD::FATTACKERS':
            if any([search.FILTERED_ACTIVITIES[category]['flag'] for category in search.FILTERED_ACTIVITIES]):
                await search.WEBSOCKET.send(f"FA0::{search.find_attackers('TCP-SYN')}{search.find_attackers('TCP-SYNACK')}{search.find_attackers('ICMP-POD')}{search.find_attackers('ICMP-SMURF')}")
            else:
                await search.WEBSOCKET.send('FA0::No DDOS attack detected yet. Try again later.')
        else:
            await search.WEBSOCKET.send('LOG::Invalid CMD')

async def WS_sender():
    global search
    while search.WEBSOCKET is not None:
        if search.RECENT_ACTIVITIES:
            data = []
            for pkt in search.RECENT_ACTIVITIES[::-1]:
                msg = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(pkt[0]))} <{'|'.join(pkt[1])}> {pkt[2]}:{pkt[6]} ({pkt[4]}) => {pkt[3]}:{pkt[7]} ({pkt[5]})"
                if pkt[8]:
                    msg += f" [{pkt[8]} bytes]"
                if pkt[9]:
                    msg += f" <{pkt[9]}>"
                data.append(msg)
            await search.WEBSOCKET.send("PKT::"+"\n".join(data))
        await search.WEBSOCKET.send(f"FLAG:{search.FILTERED_ACTIVITIES['TCP-SYN']['flag']},{search.FILTERED_ACTIVITIES['TCP-SYNACK']['flag']},{search.FILTERED_ACTIVITIES['ICMP-POD']['flag']},{search.FILTERED_ACTIVITIES['ICMP-SMURF']['flag']}")

@app.websocket('/ws')
async def ws():
    global search
    try:
        if not search.WEBSOCKET:
            search.WEBSOCKET = websocket
            await websocket.accept()
        else:
            return "Already connect to WS", 400
        producer = asyncio.create_task(WS_sender())
        consumer = asyncio.create_task(WS_receiver())
        await asyncio.gather(producer, consumer)
    except asyncio.CancelledError:
        search.WEBSOCKET = None
        search.stop()
        raise

if not is_admin():
    sys.exit("[-] Please execute the script with root or administrator priviledges.\n[-] Exiting.")
else:
    try:
        app.run()
    except KeyboardInterrupt:
        sys.exit("[-] Ctrl + C triggered.\n[-] Shutting Down")
