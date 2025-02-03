# S4x25Talk

PCAPs and IDS rules that highlight some of the IDS 'gotchas' and tricks for dealing with common ICS protocol features.

I break this down into a number of example cases:

Example1: Modbus protocol which uses protocol pipelining. This is an example of how /not/ to do things: We write a bad IDS signature. It will detect one attack, but not the other (because the second attack pcap uses protocol pipelining to hide itself)

Example2: Modbus pipelining using the preprocessor. In this case, we run the same PCAPs as Example 1, but we alert on both of them. This demonstrates how useful protocol preprocessors can be!

Example3: Enip Pipelining. Just like our Modbus example, this is a Bad Signature that can be evaded, along with the accompanying PCAPs. Note that I show a few ways of pipelining requests in the PCAP, just to drive home the point of how difficult it is to write a signature using simple content matches (or even PCRE).

Example 4: Enip Pipelining using the preprocessor. Note that the CIP preprocessors for Suricata and Snort3 differ quite a bit, this highlights some of the differences.

Example 5: Modbus pipelining detection -- pipeline detection only. This shows how to detect that pipelining is being used (but, it can't do deep packet inspection of the pipelined request). There are several requests here, some with up to 25 pipelined requests in a single TCP packet, to highlight how difficult it is to detect the actual attack using simple content and PCRE matching.

Example 6: Modbus datasets. We show how to assign a device to a dataset, and to later detect an attack against the device because it belongs to the dataset of 'insecure by design' devices.

If you have questions about the 
