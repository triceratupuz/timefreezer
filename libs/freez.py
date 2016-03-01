import wx
import fsm
import midiconf

class FreezPanel(wx.Panel):
	'''Panel containing all the freezers GUI elements'''
	def __init__(self, *a, **k):
		self.cSound = k.pop('cSound', None)
		self.freezers = k.pop('freezers', None)
		super(FreezPanel, self).__init__(*a, **k)#super the subclass
		mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.gridSizer = wx.GridBagSizer(vgap=2, hgap=5)
		ath = wx.StaticText(self, -1, "Auto Th", style= wx.ALIGN_RIGHT | wx.TE_RICH)
		self.gridSizer.Add(ath, pos=(2,0))
		att = wx.StaticText(self, -1, "Attack", style= wx.ALIGN_RIGHT | wx.TE_RICH)
		self.gridSizer.Add(att, pos=(3,0))
		rel = wx.StaticText(self, -1, "Release", style= wx.ALIGN_RIGHT | wx.TE_RICH)
		self.gridSizer.Add(rel, pos=(4,0))
		psh = wx.StaticText(self, -1, "Pan", style= wx.ALIGN_RIGHT | wx.TE_RICH)
		self.gridSizer.Add(psh, pos=(5,0))
		pan = wx.StaticText(self, -1, "Shift", style= wx.ALIGN_RIGHT | wx.TE_RICH)
		self.gridSizer.Add(pan, pos=(6,0))
		volu = wx.StaticText(self, -1, "Vol", style= wx.ALIGN_RIGHT | wx.TE_RICH)
		self.gridSizer.Add(volu, pos=(7,0))
		self.freezlist = []
		for val in range(0, self.freezers):
			self.freezlist.append(Freezer(parent = self, cSound = self.cSound, istance = val + 1))
			for item in range(0, len(self.freezlist[val].items)):
				self.gridSizer.Add(self.freezlist[val].items[item], pos=(item,1 + val))
		
		#Set sizer
		mainSizer.AddSpacer(5, flag=wx.EXPAND)
		mainSizer.Add(self.gridSizer, 0, wx.EXPAND)
		mainSizer.AddSpacer(5, flag=wx.EXPAND)
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)
		self.mcFr =[]
		#timer for update
		self.timerRefresh = wx.Timer(self, wx.ID_ANY)
		self.timerRefresh.Start(100)
		self.Bind(wx.EVT_TIMER, self.timerUpdate, self.timerRefresh)

	def OnClose(self, event):
		'''to destroy configuration frames, if open
		stop the timer'''
		for mcFrame in self.mcFr:
			mcFrame.Destroy()
		self.timerRefresh.Stop() 
		self.Destroy()
	
	def timerUpdate(self, evt):
		'''read csound and update buttons accordingly'''
		for item in range(0, len(self.freezlist)):
			frrrr = self.freezlist[item]
			frrrr_ist = frrrr.istance
			csStatus = self.cSound.TableGet(14, frrrr_ist)
			if frrrr.startstopBval <> csStatus:
				frrrr.startstopBval = csStatus
				frrrr.doFreezeB(evt)
				if frrrr.items[0].GetSelection() <> 0:
					if csStatus == 1:
						frrrr.items[1].SetBackgroundColour('red')
					else:
						frrrr.items[1].SetBackgroundColour('blue')

class Freezer():
	'''Single freezer GUI elements'''
	def __init__(self, parent, cSound, istance):
		self.parent = parent
		self.cSound = cSound
		self.istance = istance
		self.items=[]
		siz=wx.Size(70,-1)#size of widgets
		#Trigger Mode
		self.actModes = ["Manual", "Auto Above", "Auto Below"] 
		self.trigmode = wx.ComboBox(self.parent, -1, choices=self.actModes, size=siz)
		self.trigmode.SetValue(self.actModes[0])
		self.trigmode.SetSelection(0)
		self.trigmode.Bind(wx.EVT_COMBOBOX, self.setTrigModeB)
		self.items.append(self.trigmode)
		#manual Activation
		self.startstopB = wx.Button(self.parent, -1, label='Off', size = siz)
		self.startstopB.SetBackgroundColour('green')
		self.startstopBval = 0
		self.startstopB.Bind(wx.EVT_BUTTON, self.doFreezeB)
		self.startstopB.Bind(wx.EVT_RIGHT_DOWN, self.openMidiConf)#midi configuration panel
		self.cSound.TableSet(14, self.istance, 0)
		self.items.append(self.startstopB)
		#Auto threshold
		self.thres = fsm.FsmTs(parent=self.parent, id=-1,
											digits=2,
											min_val = -60.0,
											max_val = 0.0,
											increment=0.01,
											value = 0.0,
											size = siz,
											cSound = self.cSound,
											indxn = self.istance,
											ftable = 16)
		self.items.append(self.thres)
		self.cSound.TableSet(16, self.istance, 0)
		#attack
		self.att = fsm.FsmTs(parent=self.parent, id=-1,
											digits=3,
											min_val = 0.0,
											max_val = 1.0,
											increment=0.01,
											value = 0.1,
											size = siz,
											cSound = self.cSound,
											indxn = self.istance,
											ftable = 10)
		self.items.append(self.att)
		self.cSound.TableSet(10, self.istance, 0.1)
		#release
		self.rel = fsm.FsmTs(parent=self.parent, id=-1,
											digits=3,
											min_val = 0.0,
											max_val = 1.0,
											increment=0.01,
											value = 0.1,
											size = siz,
											cSound = self.cSound,
											indxn = self.istance,
											ftable = 11)
		self.items.append(self.rel)
		self.cSound.TableSet(11, self.istance, 0.1)
		#pan
		self.pan = fsm.FsmTs(parent=self.parent, id=-1,
											digits=3,
											min_val = 0.0,
											max_val = 1.0,
											increment=0.01,
											value = 0.5,
											size = siz,
											mousev = 0,
											cSound = self.cSound,
											indxn = self.istance,
											ftable = 12)
		self.items.append(self.pan)
		self.cSound.TableSet(12, self.istance, 0.5)
		#pitchshift
		self.shf = fsm.FsmTs(parent=self.parent, id=-1,
											digits=2,
											min_val = -12.0,
											max_val = 12.0,
											increment=0.01,
											value = 0.0,
											size = siz,
											cSound = self.cSound,
											indxn = self.istance,
											ftable = 13)
		self.items.append(self.shf)
		self.cSound.TableSet(13, self.istance, 0)
		#Volume
		self.vol = fsm.FsmTs(parent=self.parent, id=-1,
											digits=2,
											min_val = 0.0,
											max_val = 3.0,
											increment=0.01,
											value = 1.0,
											size = siz,
											cSound = self.cSound,
											indxn = self.istance,
											ftable = 17)
		self.items.append(self.vol)
		self.cSound.TableSet(17, self.istance, 1.0)
		
		
	def doFreezeB(self, evt):
		"""to launch or stop a freezer instrument"""
		if self.trigmode.GetSelection() == 0:
			obj = evt.GetEventObject()
			if self.startstopBval == 0:
				obj.SetLabel('Freezed')
				obj.SetBackgroundColour('red')
				self.cSound.TableSet(14, self.istance, 1)
				self.startstopBval = 1
			else:
				obj.SetLabel('Off')
				self.cSound.TableSet(14, self.istance, 0)
				obj.SetBackgroundColour('green')
				self.startstopBval = 0
	
	def setTrigModeB(self, evt):
		'''set the triggering mode'''
		mode = self.trigmode.GetSelection()
		self.cSound.TableSet(15, self.istance, mode)
		if mode <> 0:
			self.startstopB.SetLabel('Disabled')
			self.startstopB.SetBackgroundColour('blue')
			self.startstopBval = 0
			self.cSound.TableSet(14, self.istance, 0)
		else:
			self.startstopB.SetLabel('Off')
			self.startstopB.SetBackgroundColour('green')
			self.startstopBval = 0
			self.cSound.TableSet(14, self.istance, 0)
			
			
	def openMidiConf(self, evt):
		'''open a midi Configuration frame'''
		print "open Midi Conf"
		newframe = midiconf.MidiConfFr(self.parent, -1, title="Time Freezer Midi Configuration", cSound = self.cSound)
		self.parent.mcFr.append(newframe)
		newframe.Show()
		