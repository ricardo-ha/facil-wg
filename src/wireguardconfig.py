from uuid import uuid4
import json
import subprocess, platform
from config import *


def gen_preshared_key():
    result = subprocess.run(['wg', "genpsk"], capture_output=True, text=True)
    return result.stdout.strip()

def gen_key(): # Private and Public
    genkey_process = subprocess.Popen(['wg', 'genkey'], stdout=subprocess.PIPE, text=True)
    private_key, _ = genkey_process.communicate()

    pubkey_process = subprocess.Popen(['wg', 'pubkey'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    public_key, _ = pubkey_process.communicate(input=private_key)

    return private_key.strip(), public_key.strip()


class WireguardConfigJson:
    def __init__(self, json_data:dict|None):
        if isinstance(json_data, dict):
            server, peers = json_data.values()
            # Server values
            self.server:dict[str:str] = server
            #Peers values
            self.peers:list[dict[str:str]] = peers
        else:
            private_key, public_key = gen_key()
            self.server = {
                "privateKey": private_key,
                "publicKey": public_key,
                "address": SERVER_IP
            }
            self.peers = []

        return
    
    def _new_ip(self):
        if not self.peers:
            return SERVER_IP[:-1] + "2"
        address:list[str]  = [d["address"] for d in self.peers]        
        indexs = [int(ip.split(".")[-1]) for ip in address]
        indexs.sort()
        i = 2
        while i in indexs:
            i += 1
        if i >= 255: # With CIDR = /24
            return Exception("Maximun devices number.")
        base = address[0].split(".")
        return f"{base[0]}.{base[1]}.{base[2]}.{i}"
        
    
    def devices(self):
        return [{key: value for key, value in d.items() if key in ["name", "id", "address", "enabled"]} for d in self.peers]

    def add_device(self, name, enabled=False):
        private_key, public_key = gen_key()
        preshared_key = gen_preshared_key()

        id = str(uuid4())
        address = self._new_ip()
        self.peers.append(
            {
            "id" : id,
            "name": name,
            "address" : address,
            "privateKey" : private_key,
            "publicKey" : public_key,
            "presharedKey" : preshared_key,
            "enabled": enabled
        })
        return  {"id":id, "name":name, "address":address, "enabled":enabled}

    def remove_device(self, id:str):
        self.peers = [peer for peer in self.peers if peer["id"] != id]

    def enable_device(self, id:str, enabled:bool):
        for peer in self.peers:
            if peer["id"] == id:
                if bool(int(enabled)):
                    peer["enabled"] = True
                else:
                    peer["enabled"] = False
                  

    def to_WireguarConfig(self) -> str:
        config = f"""
# Server
[Interface]
PrivateKey = {self.server["privateKey"]}
Address = {self.server["address"]}/24
ListenPort = {WG_PORT}
PreUp = {WG_PRE_UP}
PostUp = {WG_POST_UP}
PreDown = {WG_PRE_DOWN}
PostDown = {WG_POST_DOWN}
"""
        peer_config = """
# Device: {name} ({id})
[Peer]
PublicKey = {publicKey}
PresharedKey = {presharedKey}
AllowedIPs = {address}/32
"""
        for peer in self.peers:
            if peer["enabled"] == True:
                config += peer_config.format(
                    name=peer["name"],
                    id = peer["id"],
                    publicKey = peer["publicKey"],
                    presharedKey = peer["presharedKey"],
                    address = peer["address"]
                    )
        return config

    def to_device(self, id)-> str:
        for peer in self.peers:
            if peer["id"] == id:
                return f'''
[Interface]
PrivateKey = {peer["privateKey"]}
Address = {peer["address"]}/24
DNS = {DNS}

[Peer]
PublicKey = {self.server["publicKey"]}
PresharedKey = {peer["presharedKey"]}
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 0
Endpoint = {WG_HOST}:{WG_PORT}
        '''
    
    def __str__(self):
        return self.to_WireguarConfig()
    
    def __repr__(self):
        return json.dumps(dict(server=self.server, peers=self.peers))

# Usage example
if __name__ == "__main__":
    from pprint import pprint
    config_data = {
        "server": {
            "privateKey": "KH/uVLjqnsJhURTVwDkgLkcuCuKVGp60w5PdYj1Vo0A=",
            "publicKey": "N9QHWlcwrDrG7FQrqBtrF/oymeG3NbltcM6xLSX3zFE=",
            "address": "10.8.0.1"
        },
        "peers": [
        {
            "id": "1d6ca9e1-b4af-4946-8142-40bfb7677f0f",
            "name": "Móvil",
            "address": "10.8.0.2",
            "privateKey": "+E/SCJhB9OHhZjIO+bDVHoXRESUjCfqwj2Veln8lWFs=",
            "publicKey": "Jr2WmDgpBJsQyp1MYhx9/NH5rSkmtd7H/QFzFpVKSmc=",
            "presharedKey": "tG5R7JaYP34Z9EMDbsBhsCiDS8/Kv1mrhK3okxI8pX4=",
            "enabled": True
        }
        ]
    }

    config = WireguardConfigJson(config_data)
    id2 = config.add_device("Dispositivo molón")
    config.remove_device("1d6ca9e1-b4af-4946-8142-40bfb7677f0f")
    config.add_device("Dispositivo molón", True)
    id = config.add_device("", True)
    config.enable_device(id[0], enabled=False)
    config.enable_device(id2[0], enabled=True)
    print(config)
    pprint(repr(config))




