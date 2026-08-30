// s.options.numInputBusChannels = 0;
s.options.numOutputBusChannels = 2;

// s.options.device = "hw:Dummy";
s.options.device = "default";

s.options.numWireBufs = 1024;
s.boot;

(
s.waitForBoot {
    // 1. Start SuperDirt and explicitly assign it to ~dirt
    ~dirt = SuperDirt(2, s);
	~dirt.loadSoundFiles;
    ~dirt.start(57120, 0 ! 2);

    // 2. Wait for the audio server and SuperDirt to finish loading
    s.sync;

    // 3. Initialize MIDI and connect it to ~dirt
    MIDIClient.init;

    // Change this string if your virtual MIDI port has a different name!
    ~midiOut = MIDIOut.newByName("Midi Through", "Midi Through Port-0");
    ~midiOut.latency = 0;

    ~dirt.soundLibrary.addMIDI(\rust, ~midiOut);

    "\n✅ SUCCESS: SuperDirt and MIDI are ready for TidalCycles!\n".postln;
};
)


