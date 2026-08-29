:set -fno-warn-orphans -Wno-type-defaults -XMultiParamTypeClasses -XOverloadedStrings
:set prompt ""

-- Import all the boot functions and aliases.
import Sound.Tidal.Boot

default (Rational, Integer, Double, Pattern String)

-- Create a Tidal Stream with the default settings.
-- To customize these settings, use 'mkTidalWith' instead
tidalInst <- mkTidal

-- tidalInst <- mkTidalWith [(superdirtTarget { oLatency = 0.01 }, [superdirtShape])] (defaultConfig {cFrameTimespan = 1/50, cProcessAhead = 1/20})

-- This orphan instance makes the boot aliases work!
-- It has to go after you define 'tidalInst'.
instance Tidally where tidal = tidalInst

-- `enableLink` and `disableLink` can be used to toggle synchronisation using the Link protocol.
-- Uncomment the next line to enable Link on startup.
-- enableLink

-- You can also add your own aliases in this file. For example:
-- fastsquizzed pat = fast 2 $ pat # squiz 1.5

:set prompt "tidal> "
:set prompt-cont ""


:{
let lead = s "rust" # midichan 0
    bass = s "rust" # midichan 1
    pluck = s "rust" # midichan 2
    drums = s "rust" # midichan 9

    bd pat = midinote (pat + 35) # drums
    sn pat = midinote (pat + 37) # drums
    ch pat = midinote (pat + 41) # drums
    oh pat = midinote (pat + 45) # drums
    cp pat = midinote (pat + 38) # drums
    lt pat = midinote (pat + 40) # drums
    mt pat = midinote (pat + 44) # drums
    ht pat = midinote (pat + 47) # drums

    metro = p "metronome" $ midinote "42" # r10
:}
