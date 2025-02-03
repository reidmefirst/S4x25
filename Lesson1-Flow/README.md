# Lesson 1: 'flow' keyword for fewer false positives

## Background
Using the 'flow' keyword is a good idea, especially for rules which match on TCP ports greater than 1024.

In the industrial security space, this includes protocols such as Ethernet/IP (TCP/44818), DNP3 (TCP/20000), IEC-104 (TCP/2404), and many other protocols.

These ports may be used by network clients, since the operating system will assign them as 'source' TCP ports to network clients.

The PCAP included has a contrived example of such behaviour: a web client, which happens to be assigned TCP source port 44818. It issues a request, and the server responds with data that may be misinterpreted as an Ethernet/IP response, and thus might match on some signatures. Since the server response has a destination port of TCP/44818, poorly-written Snort and Suricata rules may mistakenly believe that one of the response packets is actually suspicious or malicious in nature.

Included is a rule which poorly matches on the Ethernet/IP protocol, and the same rule with a 'flow' keyword which will not result in the false positive.

The 'flow' keyword has a downside of course: if your sensor does not see the initial TCP handshake, then your rules which match based on flow will fail to fire. This tradeoff is generally worth it, especially if your sensor does not store PCAPs to review the offending packet.

## Running this example

It is best to modify your suricata or snort3 configuration files to have no
rules, so that you can focus on troubleshooting and testing just these rules.
### Suricata
`suricata -r <pcap> -s <rules file> -k none`
### Snort
`snort -r <pcap> -R <rules file> -k none`
