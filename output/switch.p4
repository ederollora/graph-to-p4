/* -*- P4_16 -*- */

#include <core.p4>
#include <v1model.p4>




const bit<16> TYPE_IPV4 = 0x800;

const bit<16> ETHERTYPE_IPV4 = 0x0800;
const bit<16> ETHERTYPE_IPV6 = 0x86DD;
const bit<16> ETHERTYPE_ARP = 0x0806;
const bit<8> NEXTHEADER_ICMP = 0x01;
const bit<8> NEXTHEADER_UDP = 0x11;
const bit<8> NEXTHEADER_TCP = 0x06;
const bit<8> PROTOCOL_TCP = 0x06;
const bit<8> PROTOCOL_UDP = 0x11;
const bit<8> PROTOCOL_ICMP = 0x01;

typedef bit<32> ip4Addr_t;
typedef bit<48> macAddr_t;


header ethernet_t{
    bit<48>    dstAddr;
    bit<48>    srcAddr;
    bit<16>    etherType;
}

header vlan_t{
    bit<3>     pcp;
    bit<1>     cfi;
    bit<12>    vid;
    bit<16>    etherType;
}

header ipv4_t{
    bit<4>     version;
    bit<4>     ihl;
    bit<6>     dscp;
    bit<2>     ecn;
    bit<16>    totalLength;
    bit<16>    identification;
    bit<3>     flags;
    bit<13>    fragOffset;
    bit<8>     ttl;
    bit<8>     protocol;
    bit<16>    hdrChecksum;
    bit<32>    srcAddr;
    bit<32>    dstAddr;
}

header ipv6_t{
    bit<4>      version;
    bit<8>      trafficClass;
    bit<20>     flowLabel;
    bit<16>     len;
    bit<8>      nextHeader;
    bit<8>      hopLimit;
    bit<128>    srcAddr;
    bit<128>    dstAddr;
}

header arp_t{
    bit<16>    hardwareType;
    bit<16>    protocolType;
    bit<8>     hlen;
    bit<8>     plen;
    bit<16>    operation;
    bit<48>    sha;
    bit<32>    spa;
    bit<48>    tha;
    bit<32>    tpa;
}

header icmp_t{
    bit<8>     tp;
    bit<8>     code;
    bit<16>    checksum;
    bit<16>    id;
    bit<16>    seqNo;
}

header tcp_t{
    bit<16>    srcPort;
    bit<16>    dstPort;
    bit<32>    seqNo;
    bit<32>    ackNo;
    bit<4>     dataOffset;
    bit<3>     res;
    bit<3>     ecn;
    bit<6>     crtl;
    bit<16>    window;
    bit<16>    checksum;
    bit<16>    urgentPtr;
}

header udp_t{
    bit<16>    srcPort;
    bit<16>    dstPort;
    bit<16>    len;
    bit<16>    checksum;
}

struct metadata {
 /* empty */ 
}


struct headers_t{
    ethernet_t  ethernet;
    vlan_t      vlan;
    ipv4_t      ipv4;
    ipv6_t      ipv6;
    arp_t       arp;
    icmp_t      icmp;
    tcp_t       tcp;
    udp_t       udp;
}

parser ParserImpl(packet_in packet,
                  out headers_t hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata){

    state start {
        transition parse_ethernet;
    }

    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition parse_vlan;
    }

    state parse_vlan {
        packet.extract(hdr.vlan);
        transition select(hdr.vlan.etherType) {
            ETHERTYPE_IPV4: parse_ipv4;
            ETHERTYPE_IPV6: parse_ipv6;
            ETHERTYPE_ARP: parse_arp;
            default: accept;
        }
    }

    state parse_ipv6 {
        packet.extract(hdr.ipv6);
        transition select(hdr.ipv6.nextHeader) {
            NEXTHEADER_ICMP: parse_icmp;
            NEXTHEADER_UDP: parse_udp;
            NEXTHEADER_TCP: parse_tcp;
            default: accept;
        }
    }

    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition select(hdr.ipv4.protocol) {
            PROTOCOL_TCP: parse_tcp;
            PROTOCOL_UDP: parse_udp;
            PROTOCOL_ICMP: parse_icmp;
            default: accept;
        }
    }

    state parse_arp {
        packet.extract(hdr.arp);
        transition accept;
    }

    state parse_tcp {
        packet.extract(hdr.tcp);
        transition accept;
    }

    state parse_icmp {
        packet.extract(hdr.icmp);
        transition accept;
    }

    state parse_udp {
        packet.extract(hdr.udp);
        transition accept;
    }

}

control VerifyChecksumImpl(inout headers_t hdr,
                           inout metadata meta){

    apply{ }

}

control IngressImpl(inout headers_t hdr,
                    inout metadata meta,
                    inout standard_metadata_t standard_metadata){

    apply{ }

}

control EgressImpl(inout headers_t hdr,
                   inout metadata meta,
                   inout standard_metadata_t standard_metadata){

    apply{ }

}

control ComputeChecksumImpl(inout headers_t hdr,
                            inout metadata meta){

    apply{ }

}

control DeparserImpl(packet_out packet,
                     in headers_t hdr){

    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.vlan);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.ipv6);
        packet.emit(hdr.arp);
        packet.emit(hdr.icmp);
        packet.emit(hdr.tcp);
        packet.emit(hdr.udp);
    }
}

V1Switch(
    ParserImpl(),
    VerifyChecksumImpl(),
    IngressImpl(),
    EgressImpl(),
    ComputeChecksumImpl(),
    DeparserImpl()
) main;