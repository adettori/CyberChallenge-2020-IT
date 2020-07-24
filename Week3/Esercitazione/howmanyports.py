
import pyshark

def concatenate_list_str(packet_list):
    
    result = ""

    for packet in packet_list:
        if(result == ""):
            result += str(packet.number)
        else:
            result += "->" + str(packet.number)

    return result

cap = pyshark.FileCapture('./howmanyports.pcap', display_filter='tcp.flags.syn == 1 and tcp.flags.ack == 0')

#Parameters
max_port_dist = 100000
max_frame_num_dist = 10000
min_len = 2

src_dst_ip_dict = {}
cond_already_verified = False

for packet in cap:

    if(not hasattr(packet, "ip")):
        continue

    dict_key = str(packet['ip'].src) + ":" + str(packet['ip'].dst)

    if(dict_key in src_dst_ip_dict):
        prec_pack = src_dst_ip_dict[dict_key][-1]
    else:
        src_dst_ip_dict[dict_key] = [packet]
        continue
    
    if(hasattr(prec_pack, "icmp")):
        prec_src_port = prec_pack["icmp"].udp_port
        prec_dst_port = prec_pack["icmp"].udp_dstport
    else:
        prec_src_port = prec_pack[prec_pack.transport_layer].port
        prec_dst_port = prec_pack[prec_pack.transport_layer].dstport

    if(hasattr(packet, "icmp")):
        cur_src_port = packet["icmp"].udp_port
        cur_dst_port = packet["icmp"].udp_dstport
    else:
        cur_src_port = packet[packet.transport_layer].port
        cur_dst_port = packet[packet.transport_layer].dstport

    diff1 = abs(int(cur_src_port) - int(prec_src_port))
    diff2 = abs(int(cur_dst_port) - int(prec_dst_port))
    diff3 = abs(int(prec_pack.number) - int(packet.number))
    expr1 = (diff1 <= max_port_dist) and (diff1 > 0)
    expr2 = (diff2 <= max_port_dist) and (diff2 > 0)
    expr3 = (diff3 <= max_frame_num_dist)
    cond = (expr1 or expr2) and expr3
    
    if(cond):
        src_dst_ip_dict[dict_key].append(packet)
        cond_already_verified = True
    elif(cond_already_verified):
        if(len(src_dst_ip_dict[dict_key]) >= min_len):
            print(concatenate_list_str(src_dst_ip_dict[dict_key]))
        src_dst_ip_dict.pop(dict_key, None)
        cond_already_verified = False

for array in src_dst_ip_dict.values():
    print(concatenate_list_str(array))
