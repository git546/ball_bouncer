
<CsoundSynthesizer>
<CsInstruments>
sr = 44100
ksmps = 32
nchnls = 1
0dbfs = 1

instr 1
    aenv linsegr 0, 0.1, p4, p3 - 0.2, p4, 0.1, 0
    asig poscil aenv, p5, 1
    outs asig, asig
endin

instr 2
    aenv linsegr 0, 0.1, p4, p3 - 0.2, p4, 0.1, 0
    asig pluck aenv, p5, p6, 0, 1
    outs asig, asig
endin

instr 3
    aenv linsegr 0, 0.1, p4, p3 - 0.2, p4, 0.1, 0
    asig poscil aenv, p5, 1
    asig2 poscil aenv * 0.5, p5 * 2, 1
    outs asig + asig2, asig + asig2
endin

</CsInstruments>
<CsScore>
i2 0 2.5 0.5 311.1269837220809 0.5
i3 0 2.5 0.5 329.6275569128699 0.5
i3 0 2.5 0.5 466.1637615180899 0.5
i2 0 2.5 0.5 466.1637615180899 0.5
</CsScore>
</CsoundSynthesizer>