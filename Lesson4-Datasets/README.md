# Better Living through Datasets

Datasets are a Suricata-only mechanism that have some interesting rules possibilities.

## Background

Say we have an ICS network. We connected an IDS a few years ago. In that time, we've had to replace a few PLCs and some other miscellaneous equipment.

Also in that time, a few interesting vulnerabilities have been uncovered by those pesky vulnerability researchers. These vulnerabilities may be simple problems with insecure-by-design protocols. In this example, we have a device which speaks a simple protocol. If you type the command 'EVIL', the device catches fire and burns your plant down.

The protocol is widely supported, but only ACME brand devices actually blow up from the EVIL command. Tyrell Corp devices don't blow up, they simply accept the code and do nothing with it.

As engineers, we want to sound the alarms whenever we see the EVIL command, but only when it is run on an ACME brand controller. After all, who cares if someone tries it on the Tyrell, it just ignores the command and all is well.

This contrived scenario is similar to most insecure-by-design protocols where perhaps a special purpose controller has some register which is dangerous to write to, but other controllers which speak the same protocol must have that register written daily.

We don't want to alarm every time we see one of these commands, since most of the time is benign. However, if we know that a product will misbehave, we want to trigger an alert for only those products.

Enter Datasets.

We have a rule which detects the device via a device-specific signature. This rule doesn't create an alert itself, but rather adds the device IP address to a dataset. The dataset is used to identify vulnerable devices to this particular problem, and only devices we know are vulnerable will be in the dataset.

A second rule will look for the 'attack' packet. This second rule will only trigger an alert if the target of the attack was in the dataset defined by the first rule.

Why not just use network variables in Suricata's configuration? I mean, sure, you could do that. But these variables cannot be changed while Suricata is running. If you identify a new vulnerable host, you have to edit Suricata's config file and then restart the sensor. And I hope you didn't make a typo in the config file, otherwise you will be blind to what is happening on your network until you correct it.

Datasets let us add to these IP address groups on-the-fly. We can also modify them via Suricata's Unix Sockets api. See https://docs.suricata.io/en/suricata-7.0.7/rules/datasets.html#unix-socket for information (as of Suricata 7).


