# Better Living through Datasets

## Background

Sometimes, you have an insecure-by-design device and you want to detect a very particular action being performed against it.

Unfortunately, this insecure-by-design device speaks a common protocol, and there are a ton of other devices that don't fall over for the particular action that the really bad one supports.

In this example, we have two field devices which speak a simple plaintext protocol. One is made by ACME Widgets, while the other is made by TYRELL replicants. The thing is, ACME Widget will respond to an EVIL command and will blow up, while TYRELL replicants...won't. So we only really care if someone sends an EVIL command to an ACME.

Think about this scenario with common industrial protocols like Modbus. For devices with a very specific purpose (say, digital protective relays, or HVAC controllers), they will have a register map that is pre-defined. If you write to a specific register on these devices, the device will perform a very specific, pre-defined action. Possibly this action will be very bad, like shutting off heat, or opening a circuit breaker. And yet, there are millions of PLCs that have open Modbus maps -- writing to any given register on these is behaviour that is undetermined (usually), and we really can't say whether the action is bad.

We can use datasets to define groups of devices where the EVIL command (or a particular modbus register write) is really harmful, and we should let our SOC know that an attack was attempted. And, we can ignore the EVIL command (or the same modbus register write) if it targets a device that isn't vulnerable.
## Running the samples

You only need one rules file: the 'dataset-acme.rules'. This file has a signature to detect ACME devices and place them in the dataset, and to detect attacks against devices which were previously identified as ACME.

I recommend you run the pcaps through suricata in this order:

Phase 1: PCAPs that identify the device
1 or 2) the tyrell 'ver' PCAP
1 or 2) the acme 'ver' PCAP

Phase 2: PCAPs that show attempts to hack
1) the tyrell 'evil' PCAP
(now look at the alert log and see that no alert fired)
2) the acme 'evil' PCAP
(now look at the alert log and see that an alert fired!)

## Some follow-on notes

One fun thing you can do is try and use suricata's socket access to datasets. See the documentation here:
How to access Suricata via Unix Sockets using the 'suricatasc' command: https://docs.suricata.io/en/suricata-7.0.7/unix-socket.html 
How to access datasets using the sockets:
https://docs.suricata.io/en/suricata-7.0.7/rules/datasets.html#unix-socket

You can both add and delete ipv4 addresses from your datasets. Play around with it! Comment out the asset identification rule and delete the .list file, then run the widget simulators on your own to see if you can manually add the asset and get it recognized.
