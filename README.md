# S4x25Talk

PCAPs and IDS rules that highlight some of the IDS 'gotchas' and tricks for dealing with common ICS protocol features.

I break this down into a number of example cases:

Lesson 1: Flow. This covers how to use the 'flow' keyword and why you may experience false positives from network clients that just so happen to get assigned a port similar to an ICS protocol.

Lesson 2: Pipelining. This shows what protocol pipelining looks like using a PCAP of a real live PLC. It shows how bad detections are often done against ICS protocols, and how to use preprocessors and generic pipelining detection rules to augment your rulset.

Lesson 3: We don't talk about Lesson 3, because there isn't enough time this year.

Lesson 4: Datasets. This covers how to use Suricata datasets as a form of asset management. We can identify devices with an insecure-by-design feature, add that device to a dataset. Later, we can look for malicious activity which only applies to devices previously identified as insecure-by-design. We use a contrived protocol in this example, but it can be extended to things such as Modbus, ENIP, or other protocols.

# Acknowledgements

This repo goes along with [my talk](https://www.youtube.com/watch?v=LYDk-tkM3eM).

Thanks to a bunch of people for helping me along the way:
OISF Discord: [https://discord.gg/t3rV2x7MrG](https://discord.gg/t3rV2x7MrG). Everybody there is incredibly cool and helpful, Shivani Bhardwaj and Jason Ish are cool humans who answer my dumb questions a lot.
Tony Robinson's Suricata Operator's Handbook [https://leanpub.com/suri_operator](https://leanpub.com/suri_operator). The book isn't even done and it's already helped me a lot.
Suricata documentation [https://docs.suricata.io](https://docs.suricata.io). Be sure to click on the version you're working with. 'Latest' currently shows documents for the development version.
Snort3 documentation: [https://docs.snort.org](https://docs.snort.org). I really recommend reading through this if you are using Suricata too, some rule syntax is described better here.
Coworkers at Dragos in no particular order who have helped me write better rules: Matthew Pahl, Oscar Delgado, Austin Scott, Michael Lagoyda, and of course my boss Kate Johnson (nee Vajda) who gives me room to learn weird stuff.
The crew at Cisco TALOS. Jared Rittle and Patrick DeSantis have inspired me to make quite a few mindbending CTF challenges over the years.
