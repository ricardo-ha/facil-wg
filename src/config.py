import os
from password import set_password


# YOU MUST INTRODUCE THIS VARIBALES
PASSWORD = set_password(os.getenv("PASSWORD"))
WG_HOST = os.getenv("HOST") 


## DEFAULT VARIBALES
SERVER_IP = "10.8.0.1" # It is recommended to use the default parameter to avoid IP conflicts.

WG_PORT = 51820
DNS = "1.1.1.1"
WG_PRE_UP = ""
WG_POST_UP = f"iptables -t nat -A POSTROUTING -s {SERVER_IP}/24 -o eth0 -j MASQUERADE; iptables -A INPUT -p udp -m udp --dport 51820 -j ACCEPT; iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT;"
WG_PRE_DOWN = ""
WG_POST_DOWN = f"iptables -t nat -A POSTROUTING -s {SERVER_IP}/24 -o eth0 -j MASQUERADE; iptables -A INPUT -p udp -m udp --dport 51820 -j ACCEPT; iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT;"

# IF YOU INTRODUCE SOME DIFERENT IN THE DOCKER CONFIG
WG_PORT = int(os.getenv("PORT", WG_PORT))
DNS = os.getenv("DNS", DNS)
WG_PRE_UP = os.getenv("WG_PRE_UP", WG_PRE_UP)
WG_POST_UP = os.getenv("WG_POST_UP", WG_POST_UP)
WG_PRE_DOWN = os.getenv("WG_PRE_DOWN", WG_PRE_DOWN)
WG_POST_DOWN = os.getenv("WG_POST_DOWN", WG_POST_DOWN)
SERVER_IP = os.getenv("SERVER_IP", SERVER_IP)