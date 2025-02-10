# Pipelining and Pitfalls

## Background

Request Pipelining is a super old evasion technique and it presents an interesting challenge for some modern IDS engines.

The idea is simple: multiple protocol requests can be shoved into one TCP packet. This works against nearly every TCP-based protocol in the industrial space.

The background on this is kind of interesting. 

There are actually two ways to explain the behaviour. The first school of thought: Pipelining was originally a feature to help speed up requests on serial networks. Consider a 300 baud network, where you want to issue a series of 4 commands back-to-back. If you issue the command, and wait for a response, the round-trip might be a full second or even longer. You can more than double the speed of the requests if you simply don't wait for a response.

The other school of thought is that the widespread support for protocol pipelining was a mistakex.: TCP is a streaming transport layer, but ICS protocols are really datagrams. For whatever reason, the industry has settled on shoving datagram packets into a stream transport, and so the internal parsing code gives you pipelining 'for free' as devices implement a receive queue. The receive queue might get fragmented packets, so it simply deals with such fragmentation by checking that it has received enough data to process. If there is leftover data on a buffer, it is assumed that this data is the start of another request, so it remains on the buffer to be processed when the current packet is finished.

## Testing

I've included two interesting PCAPs here. The simple PCAP has a pipelined request: the 'attacker' issues a request to read a register, and to write a register, in a single TCP request. If you look at the write request, you'll see it is for register 40000 (note: this is written as 39999 'on the wire'; wireshark didn't get the memo about Modbus' weird definition of starting the register at address 1). It is pretty obvious why the suricata rule will match on this: the request is to write register 40000, and the request is to write register 40000. So, the preprocessor wins and it detects the 'attack'.

![double evasion](./images/yo-dawg.jpg "Double Evasion")

The second PCAP is in my opinion far more interesting: it represents an evasion inside of an evasion. And Suricata handles it beautifully. In this case, we write multiple registers beginning at register 39999, which includes our target register of 40000. Again, Suricata detects this!

## Challenge

Suricata detecting this 'evasion inside of an evasion' works great.

Snort3, no the other hand, has a pretty limited Modbus preprocessor: it only gives us function code, unit identifier, and 'data'. It is therefore quite easy to detect the first pcap using Modbus. However, the second PCAP is a real challenge: you'll have to use some fancy math: extract the register address, add the number of registers, and figure out if the target register (40000) lies between the endpoints. This is not easy. It demonstrates how a good preprocessor can be worth its weight in gold.
