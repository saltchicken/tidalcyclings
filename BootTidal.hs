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
let r1 = s "rust" # midichan 0
    r2 = s "rust" # midichan 1
    r3 = s "rust" # midichan 2
    r10 = s "rust" # midichan 9

    bd pat = midinote (pat + 35) # r10
    sn pat = midinote (pat + 37) # r10
    ch pat = midinote (pat + 41) # r10
    oh pat = midinote (pat + 45) # r10
    cp pat = midinote (pat + 38) # r10
    lt pat = midinote (pat + 40) # r10
    mt pat = midinote (pat + 44) # r10
    ht pat = midinote (pat + 47) # r10

    drumMap = [ ("bd", 36)
              , ("sn", 38)
              , ("ch", 42)
              , ("oh", 46)
              , ("cp", 39)
              , ("lt", 41)
              , ("mt", 45)
              , ("ht", 48)
              ]
              
    drumNote pat = unwrap $ (\name -> maybe 0 id (lookup name drumMap)) <$> pat

    metro = p "metronome" $ midinote "42" # r10

:}

