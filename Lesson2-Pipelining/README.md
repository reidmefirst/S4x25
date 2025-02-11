# Lesson 2: request pipelining evasion and detection

## Background: An Old Man is Talking
Request pipelining is an ancient technique that is not often talked about (or thought about) in the industrial space.

Suppose you have a 300 baud serial loop (RS485 or RS422 network) and you are talking to a PLC. You want to issue commands to the PLC to open 3 relays, which will in turn cause some process 'stuff' to happen. Suppose also that your communications protocol uses 16 byte commands.

It takes about half of a second to send the first command. You then have to wait roughly half of a second to receive a response to that command. You can then send the next command, receive the next response, and so on. To open the three relays will take a bit over 3 seconds at this rate. That is pretty slow, especially if the relays were doing some electric rather than mechanical.

You could speed up the process by not bothering to wait for responses. Just send the three commands, and then receive all three responses. You take a 3 seconds job down to 1.5 seconds. That's pretty good.

This concept has carried over and is generally implemented in every industrial doodad that speaks a TCP protocol. For example, Modbus/TCP, Ethernet/IP, DNP3, 61850/MMS, 60870-5-104: these protocols all generally allow pipelined requests. To give it a try, simply shove two request into a single TCP packet. If you are bad at programming and you forget to set the socket option TCP_NODELAY on your socket, you'll probably get pipelining for free if you send two commands without waiting for a response.

## About the PCAPs

### modbus-requests-with-pipelined-write.pcapng
I've included a PCAP of a Modbus/TCP session that uses request pipelining.

I highly encourage you to look at the PCAP in Wireshark.

In this example, the client issues a Read Register request to read out register 40000 from a PLC (Note: if you look at the PCAP in wireshark it'll say register 39999...that's because Modbus registers start at '1' (engineering speak) for '0' (on the wire). Thus, register 40000 (according to an engineer, and according to suricata) is encoded as 39999 (on the wire)). 
### modbus-requests-with-pipelined-write-using-write-multiple-registers.pcapng
Again, I highly recommend checking out this PCAP in wireshark.

In this case, we write multiple registers beginning with register 39999 and including register 40000. (again, as above, note that Wireshark has an off-by-one in the display: integer 39998 == register number 39999, and integer 39999 == register number 40000).

In this case, the suricata preprocessor handles the pcap and will correctly flag it as a write to register 40000. Writing a snort rule to detect this becomes tricky, though, we realize: since Snort3 only has the `modbus_data` keyword, it is up to us to write some logic that can 1) extract the starting register, 2) add the register count, and finally 3) determine if the target register resides in between the starting register and the ending register. So far, this does seem possible with any of the Snort3 logic verbs, but I would love it someone would correct me...
### Ethernet/IP 'Shallow Packet Inspection'
I've also included the S4x19 and 2021 SANS ICS CTF 'PipeDream' (sorry for the name, I used it for the challenge before we used it to denote a piece of malware) challenge.

This challenge contains two components:
- An Ethernet/IP PLC simulator
- A shallow packet inspection firewall

Start the simulator first. The simulator will listen on localhost:44819.
Start the shallow packet inspection firewall second. The firewall is really a proxy server. It listens on 0.0.0.0:44818. When a client connects, it will determine if their request is allowed. If the request is allowed, it will pass the request on to the PLC simulator, and will forward the response from the simulator back to the remote client.

The shallow packet inspection firewall can also be used to 'protect' a real Ethernet/IP PLC, although I wouldn't use it because it is purposefully made to function incorrectly.

The challenge is to obtain the device serial number from the PLC. The shallow packet inspection firewall blocks remote attempts to read the device information via the common Ethernet/IP 'List Identity' command (used by the nmap `enip-info.nse` script).

I provide information on how to defeat this challenge in my S4x25 talk, but the gist of it is to read this Cisco TALOS advisory here:

The advisory notes that you can place 24 null bytes in front of their malicious request. You can do this by simply editing nmap's `enip-info.nse` script and placing 48 0 characters in front of the list identity hex command.

I strongly encourage you to look at a PCAP of this modified nmap script. You should see two requests: a NOP (no-operation) command, followed by a List Identity command if you modified the script correctly.

You can then see a new response from the firewall: it will indicate that it detect an attack.

Think about how the ethernet/ip NOP command works, now ethernet/ip length fields work, and look at the firewall code. How does the firewall actually check for the TALOS evasion? (Hint: it's not very smart). Think how you might modify a NOP command to evade the 'TALOS evasion' detection. Et voilla, you'll bypass the firewall.

## Running examples in your favorite IDS

I included a set of IDS rules to demonstrate a few techniques:
suricata-preprocessor.rules contains modbus preprocessor rules to detect the modbus-pipeline 'write' request.

snort-preprocessor.rules contains modbus preprocessor rules to detect the attack. Note that the snort preprocessor has some serious limitations. For example, if you write register 39999, quantity 2, you can overwrite register 40000 and not get caught, even with the preprocessor. This is because the rule will need some fancy math to check if the register number is less than our 'problem' register, while register number + count is greater than or equal to our 'problem' register.

