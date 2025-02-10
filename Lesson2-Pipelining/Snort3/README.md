# snort rules for playing with modbus preprocessor

## Background

Snort3's modbus preprocessor isn't that great in my experience. Maybe someone can issue a pull request to this to make it into a better example. I won't claim to be an expert with snort3 (or suricata for that matter).

In this example we show detecting pipelined write requests.

I have included a PCAP that will make the rule fire. Unfortunately 'double evasion' detection doesn't work: it's not really possible to detect a modbus write to a specific register (if that's the sort of thing you want to do), due to limitations in the rule language. See the comments in the .rules file for an explanation.

## Testing

To test the rule, make sure your Snort3 configuration has enabled the modbus inspector.

Then run

`snort -q -c /path/to/your/snort.lua -R modbus-preprocessor-snort.rules -r modbus-requests-with-pipelined-write.pcapng -A cmg`

This should emit a fire on the write detection.

