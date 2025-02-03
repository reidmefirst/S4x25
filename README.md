# S4x25Talk

PCAPs and IDS rules that highlight some of the IDS 'gotchas' and tricks for dealing with common ICS protocol features.

I break this down into a number of example cases:

Lesson 1: Flow. This covers how to use the 'flow' keyword and why you may experience false positives from network clients that just so happen to get assigned a port similar to an ICS protocol.

Lesson 2: Pipelining. This shows what protocol pipelining looks like using a PCAP of a real live PLC. It shows how bad detections are often done against ICS protocols, and how to use preprocessors and generic pipelining detection rules to augment your rulset.

Lesson 3: We don't talk about Lesson 3, because there isn't enough time this year.

Lesson 4: Datasets. This covers how to use Suricata datasets as a form of asset management. We can identify devices with an insecure-by-design feature, add that device to a dataset. Later, we can look for malicious activity which only applies to devices previously identified as insecure-by-design. We use a contrived protocol in this example, but it can be extended to things such as Modbus, ENIP, or other protocols.
