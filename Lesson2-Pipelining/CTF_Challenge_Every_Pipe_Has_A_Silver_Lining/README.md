# S4x19/SANS 2021 ICS CTF challenge source

## Background

This was a CTF challenge from the S4x19 conference CTF, which was re-used for
the SANS ICS CTF in 2021.

You can run this example to show how ICS protocol request pipelining can evade IDS signatures, as well as application-layer firewalls.

## Preparation

You will need the following python packages installed:
- circuits (3.2.3 works fine)
- hexdump (or, simply comment out all of the lines that dump hex format data on the server)
- twisted

## Components

The challenge consists of two components:
- circuitproxy.py
- simulator_server.py

`simulator_server.py` is a simulated safety controller. It binds a listening port to localhost:44819
`circuitproxy_2025.py` is a firewall service. It binds to all network interfaces, on 0.0.0.0:44818. It will accept a limited set ENIP requests, and will decide whether to answer those requests itself, or if it should forward those requests on to the target PLC.
## Goal

Your goal is to read out the simulator_server's serial number, proving that you bypassed the firewall.

## Theory of operation

The proxy server is configured (via its source code) to listen ton 0.0.0.0:44818 and to open a connection to localhost:44819. It acts as a reverse proxy service to a PLC. It will answer List Identity requests itself. It will forward other request types on to the PLC, but if and only if you are allowed to make those requests.

## Solving recommendations

Try the obvious thing first:
`nmap -p 44818 --script enip-info localhost`

You should see the proxy server response, saying that it detected unauthorized access. This response will show a serial number of all 00s, which is not the correct solution.

Since this is a challenge involving pipelining, you should edit the enip-info script and add 24 null bytes to the beginning of the List Identity request (search for the string '6300' in the script, then add 48 '0' characters before it). Re-run the script for a new hint.

I recommend using a packet capture utility and looking at the traffic. What are the 24 null bytes doing? If the firewall suggests that this is somehow a 'TALOS evasion', maybe the firewall authors didn't understand what the bytes really meant...perhaps you can change some of the NOP request bytes such that it will still be a valid packet, but will not look exactly like the evasion that TALOS showed in their vulnerability writeup?

If you can solve this challenge, you will understand IDS detection evasions quite a bit better than the 'best of the best' teams who participated in 2019 and at least as well as the best teams in 2021. Pat yourself on the back and then help out the rest of the community by writing better detection rules (and, publish those rules if you are able).

## License

This is released for educational purposes only. The proxy 'security server' is purposefully broken, so is not fit for protecting any actual industrial control system. The software may also fail unexpectedly if exposed to the open Internet...during the SANS CTF challenge we encountered a bunch of fun bugs related to remote ends disconnecting unexpectedly, the PLC disconnecting unexpectedly, etc.
