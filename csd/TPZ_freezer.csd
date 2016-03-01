<CsoundSynthesizer> 
<CsOptions> 
</CsOptions> 
<CsInstruments> 
sr = $SRATE
ksmps = $KRATE
nchnls = 2
0dbfs = 1
zakinit 4, 1

#define TRIGGER(NUM)#
kind$NUM init $NUM
kcoActvd$NUM init 0;count activated instaces

kmode_prev$NUM init 0
kmode$NUM tab kind$NUM, 15
kthrs$NUM tab kind$NUM, 16

;activation
kactive_prev$NUM init 0
kactive$NUM tab kind$NUM, 14
if kmode$NUM == 0 then;manual activation
	if kactive_prev$NUM != kactive$NUM then
		if kactive$NUM > 0 then
			kcoActvd$NUM wrap kcoActvd$NUM + 1, 1, 10
			event "i", 10 + 0.01 * $NUM + 0.001 * kcoActvd$NUM, 0, -1, $NUM
			;tabw 1, kind$NUM, 14;not necessary, written by gui
		else
			event "i", -10 - 0.01 * $NUM - 0.001 * kcoActvd$NUM, 0, -1
			;tabw 0, kind$NUM, 14;not necessary, written by gui
		endif
		kactive_prev$NUM = kactive$NUM
	endif
	
elseif kmode$NUM == 1 then
	kthrs$NUM tab kind$NUM, 16
	ktrig trigger k_t_rms_db, kthrs$NUM, 0
	if kactive$NUM == 0 && ktrig == 1 then
		kcoActvd$NUM wrap kcoActvd$NUM + 1, 1, 10
		event "i", 10 + 0.01 * $NUM + 0.001 * kcoActvd$NUM, 0, -1, $NUM
		tabw 1, kind$NUM, 14
	elseif kactive$NUM > 0 && ktrig == 1 then
		event "i", -10 - 0.01 * $NUM - 0.001 * kcoActvd$NUM, 0, 0.01
		tabw 0, kind$NUM, 14
		kcoActvd$NUM wrap kcoActvd$NUM + 1, 1, 10
		event "i", 10 + 0.01 * $NUM  + 0.001 * kcoActvd$NUM, 0, -1, $NUM
		tabw 1, kind$NUM, 14
		;printk2 kcoActvd$NUM
	endif

elseif kmode$NUM == 2 then
	kthrs$NUM tab kind$NUM, 16
	ktrig trigger k_t_rms_db, kthrs$NUM, 1
	if kactive$NUM == 0 && ktrig == 1 then
		kcoActvd$NUM wrap kcoActvd$NUM + 1, 1, 10
		event "i", 10 + 0.01 * $NUM + 0.001 * kcoActvd$NUM, 0, -1, $NUM
		tabw 1, kind$NUM, 14
	elseif kactive$NUM > 0 && ktrig == 1 then
		event "i", -10 - 0.01 * $NUM - 0.001 * kcoActvd$NUM, 0, 0.01
		tabw 0, kind$NUM, 14
		kcoActvd$NUM wrap kcoActvd$NUM + 1, 1, 10
		event "i", 10 + 0.01 * $NUM  + 0.001 * kcoActvd$NUM, 0, -1, $NUM
		tabw 1, kind$NUM, 14
		;printk2 kcoActvd$NUM
	endif
endif

if kmode$NUM != kmode_prev$NUM then
	event "i", -10 - 0.01 * $NUM - 0.001 * kcoActvd$NUM, 0, 0.01
	kcoActvd$NUM wrap kcoActvd$NUM + 1, 1, 10
	kactive_prev$NUM = kactive$NUM
	kmode_prev$NUM = kmode$NUM
	tabw 0, kind$NUM, 14
endif
#



;bus channels
chn_k "test_sound", 1;in Channel

chn_k "directvul", 2;direct vumeter LH
chn_k "directvur", 2;direct vumeter RH
chn_k "totalvul", 2;output vumeter LH
chn_k "totalvur", 2;output vumeter RH



opcode AtanLimit, a, a
ain xin
aout = 2 * taninv(ain) / 3.1415927
xout aout
endop


giWav ftgen  1, 0, 16384, 10, 1

giAtt ftgen  10, 0, 16, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
giRel ftgen  11, 0, 16, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
giPan ftgen  12, 0, 16, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
giSfh ftgen  13, 0, 16, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
;Autotrigger
giActives ftgen  14, 0, 16, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
giMode ftgen  15, 0, 16, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
giThr ftgen  16, 0, 16, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
;Otherpars
giVol ftgen  17, 0, 16, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

;0 - mono stereo
;1 - in gain
;2 - out direct gain
;3 - out freeze gain
;4 - limiter
giOpts ftgen  99, 0, 16, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
;midi activation
giMidiCh ftgen  200, 0, 16, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
giMidiComm ftgen  201, 0, 16, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
giMidiVal1 ftgen  202, 0, 16, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
giMidiVal2 ftgen  203, 0, 16, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0


instr 1;globals
ktest chnget "test_sound"
if ktest == 1 then
	ktrig metro 1
	String  = "i 2 0 1.0"
	scoreline String, ktrig
endif

;midiactivation
kstatus, kchan, kdata1, kdata2 midiin
kincr init 1
kmax init 8
kind = 0
if kstatus != 0 then
	loop:
		kch tab kind, giMidiCh
		kco tab kind, giMidiCh
		kv1 tab kind, giMidiCh
		kv2 tab kind, giMidiCh
		if kchan == kch && kco == kstatus && kv1 == kdata1 then
			kstat tab kind, 14
			if kstat == 0 then
				tabw 1, kind, 14
			else
				tabw 0, kind, 14
			endif
		endif
	loop_lt  kind, kincr, kmax, loop
endif
endin


instr 2;test
ipitch unirand 48
ivol unirand 0.2
ipos unirand 1.0
kenve linseg 0, 0.07, 0.7, p3 - 0.15, 0.4, 0.1, 0
ao oscil 0.1 + ivol, cpsmidinn(36 + ipitch), giWav
alh, arh pan2 ao * kenve, ipos

;kinGainDly chnget "inGainDly"
kind = 1
kinGain tab kind, giOpts

zawm alh * kinGain, 0
zawm arh * kinGain, 1
endin



instr 3;input
ainl, ainr ins
;mono/stereo input operation
kind = 0
kstereoin tab kind, giOpts

;input gain
kind = 1
kinGain tab kind, giOpts
kinGainP port kinGain, 0.05
kinGainP init 1

if kstereoin == 0 then
	;only left chennel
	aoutl = ainl
	aoutr = ainl
else
	;both
	aoutl = ainl
	aoutr = ainr
endif


atestl zar 0
atestr zar 1

zawm aoutl * kinGainP, 0
zawm aoutr * kinGainP, 1


;global fsig for
;pitch shifting
;lowest f = sr / ifftsize
ifftsize  = 1024
ioverlap  = ifftsize / 2
iwinsize  = ifftsize
iwintype = 1
gfsig  pvsanal ((aoutl + aoutr) * kinGainP + atestl + atestr) * kinGainP, ifftsize, ioverlap, iwinsize, iwintype

;triggers
;calculate current rms in db
k_t_rms max_k (aoutl + aoutr) * .5 * kinGainP, 1, 1
;k_t_rms_db = dbfsamp(k_t_rms)
k_t_rms_db = dbamp(k_t_rms)
;printk2 k_t_rms_db
$TRIGGER(1)
$TRIGGER(2)
$TRIGGER(3)
$TRIGGER(4)
$TRIGGER(5)
$TRIGGER(6)
$TRIGGER(7)
$TRIGGER(8)
endin


instr 10;freezer
iatt tab_i p4, giAtt
irel tab_i p4, giRel
kindx init p4
kpan tab kindx, giPan
kpanP port kpan, 0.05
kshift tab kindx, giSfh
kshiftP port kshift, 0.05
kvol tab kindx, giVol
kvolP port kvol, 0.05

/*
;PVS FREEZE
idel = 0.02
kfreeztrig line 0, idel, 1
kenv linsegr 0, idel * 2, 0, iatt, 1, irel, 0

ffreeze pvsfreeze gfsig, kfreeztrig, kfreeztrig
fshift pvscale ffreeze, semitone(kshiftP), 1, 1, 100

aout pvsynth	fshift;fftblur
aouthp buthp aout, 30
aouthp buthp aouthp, 30
aout buthp aouthp, 30
*/

;PVS BUFFER
idelbuf = 0.03
kenv linsegr 0, idelbuf * 2, 0, iatt, 1, irel, 0

ktime line 0, idelbuf, 1.00 
if (ktime < 1) then 
	ibuf1,kt1   pvsbuffer   gfsig, idelbuf 
endif 
khan init ibuf1 
if (ktime > 1) then 
	kpt phasor 1 / idelbuf
	kspl jspline 0.1, 0.2, 1
	kpointer wrap (kpt + kpt * kspl), 0, 1
	fsb1  pvsbufread  kpointer * idelbuf, khan, 31, sr/3, 1
	fshift pvscale fsb1, semitone(kshiftP), 0, 1, 70
	aout  pvsynth fshift
endif 
aout buthp aout, 31

alh, arh pan2 aout * 1.5 * kvolP * kenv, kpanP

zawm alh, 2
zawm arh, 3
endin




instr 50; output mixer and VUmeter
kdecl linsegr 0, 0.1, 1, 0.1, 0
;volume compensation

;Mixer

kind = 2
kdirect tab kind, giOpts
kdirectP port kdirect, 0.05
kind = 3
kfreez tab kind, giOpts
kfreezP port kfreez, 0.05
kind = 4
klimit tab kind, giOpts

kinst init 10
kacti10 active kinst
kacti10 = (kacti10 < 1 ? 1 : kacti10)
kacti10p port kacti10, .15


adirectl zar 0
adirectr zar 1
afreezl zar 2
afreezr zar 3
atl = kdecl * (adirectl * kdirectP + kfreezP * afreezl / sqrt(kacti10p))
atr = kdecl * (adirectr * kdirectP + kfreezP * afreezr / sqrt(kacti10p))

if klimit == 1 then
	atl AtanLimit atl
	atr AtanLimit atr
endif

;VU meters
ktrigamp metro 5;must be synched with gui
;direct signal
kdirectl_rms max_k adirectl, ktrigamp, 1
kdirectr_rms max_k adirectr, ktrigamp, 1
kdirectl_rms_db = dbfsamp(kdirectl_rms)
kdirectr_rms_db = dbfsamp(kdirectr_rms)
;total signal
ktl_rms max_k atl, ktrigamp, 1
ktr_rms max_k atr, ktrigamp, 1
ktl_rms_db = dbfsamp(ktl_rms)
ktr_rms_db = dbfsamp(ktr_rms)

;transmits VUmeters to GUI
if ktrigamp == 1 then
	chnset kdirectl_rms_db, "directvul"
	chnset kdirectr_rms_db, "directvur"
	chnset ktl_rms_db, "totalvul"
	chnset ktr_rms_db, "totalvur"
endif

outs atl, atr
zacl 0, 3
endin




</CsInstruments> 
<CsScore> 
;Run
i 1 0 36000
i 3 0 36000
i 50 0 36000

</CsScore> 
</CsoundSynthesizer> 
