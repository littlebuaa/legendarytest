#python v3.4; coding:UTF-8
from framework.common.testing import Test
from framework.tools.device import CommandResult, DUT
from framework.tools.config import configget
from framework.tools.utils import compare_value
import time


class CheckWiFiPER(Test):
    def __init__(self, dut):
        super().__init__(dut, "Check WiFi PER")
    def test(self):
        ''' This function is WiFi test of packet error rate. A golden sample is needed'''
        numpkt = 100
        server_ip = configget("RADIO_TEST","server_ip")
        client_ip = configget("RADIO_TEST","client_ip")
        ssid = configget("RADIO_TEST","ssid")
        ref_com =  configget("COM","REF")
        ref = DUT("ref",ref_com)
        if not ref.open():
            self.logger.info("Golden board UART Problem, COM port open failed!!")
            return False
        mac_ref = ref.get_mac()

        ## reset and wifi init
        self.dut.send_command('reset')
        ref.send_command('reset')
        time.sleep(1)
        ref.execute_command('wifi init')
        self.dut.execute_command('wifi init')

        ## creat (server, client) pair   
        pairs = ((ref, self.dut),(self.dut,ref))
        for pair in pairs:
            server = pair[0]
            client = pair[1]
            if server.get_name() == "ref":
                mode = 'DUT_RX'
                self.logger.info("++++++++++++Golden Sample As the server, to send Packet to DUT++++++++++++++")
            else:
                mode = 'DUT_TX'
                self.logger.info("++++++++++++DUT As the sever, to send Packet to Golden Sample++++++++++++++")
            for channel in (1,13):
                server.execute_command('wifi ap_start %s %d' % (ssid,channel))
                time.sleep(0.2)
                server.execute_command('wifi set_ip %s 255.255.255.0 %s %s' % ((server_ip,)*3))
                time.sleep(0.2)
                client.execute_command('wifi join %s'%(ssid))
                time.sleep(0.2)
                client.execute_command('wifi set_ip %s 255.255.255.0 %s %s' % (client_ip,server_ip,server_ip))
                time.sleep(0.2)
                res = self.measure_per(server, client, numpkt)
                client.execute_command('wifi disconnect')
                server.execute_command('wifi clr_ip')
                server.execute_command('wifi ap_stop')


                ## every channel has N et B mode:
                count = 0
                for j in (0,1):
                    rssi_prefix = "channel_%d_%s_%s_rssi"%(channel,res[j][0],mode)
                    pkt_prefix = "channel_%d_%s_%s_pkt"%(channel,res[j][0],mode)
                    count = compare_value(pkt_prefix, res[j][1],configget("RADIO_TEST","nb_packet_min"),configget("RADIO_TEST","nb_packet_max"))
                    count +=compare_value(rssi_prefix, res[j][2],configget("RADIO_TEST","rssi_min"),configget("RADIO_TEST","rssi_max"))
                if count <0 :
                    return False
                time.sleep(2)

        self.logger.info(" wifi per test fini")
        return True

    def measure_per(self,server, client, numpkt):
        client_ip = configget("RADIO_TEST","client_ip")
        server_ip = configget("RADIO_TEST","server_ip")

        per_results = list()
        client.execute_command('wifi pkt rx')
        rates = [   ('wifi rate -m 7', 'N'),## 65mbps
                    ('wifi rate -b 11', 'B')] ## 11mbps
        for rate in rates:
            server.execute_command(rate[0])
            # server.execute_command('wifi pkt tx %s 100 10 10' % (client_ip)) # close loop
            time.sleep(0.1) # wait all packets are transmitted
            client.execute_command('wifi pkt rst_cnt')
            server.execute_command('wifi pkt tx %s 1000 %d 10' % (client_ip, numpkt), timeout_ms=30*1000)
            time.sleep(1) # wait all packets are transmitted
            rt, text = client.execute_command('wifi pkt cnt')
            res = CommandResult.parse(text)
            pkt_cnt = int(res.data['pkt_cnt'])

            rt, text = client.execute_command('wifi get_rssi')
            res = CommandResult.parse(text)
            rssi = int(res.data['rssi'])

            client_mac = client.get_mac()
            per_results.append((rate[1], pkt_cnt,rssi))
        client.execute_command('wifi pkt stop')
        return per_results