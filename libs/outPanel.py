import wx
import fsm


class OutPanel(wx.Panel):
	def __init__(self, *a, **k):
		self.cSound = k.pop('cSound', None)
		super(OutPanel, self).__init__(*a, **k)#super the subclass
		mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		controlSizer = wx.GridBagSizer(vgap=5, hgap=5)
		siz=wx.Size(70,-1)
		#gain for direct signal
		gainTI = wx.StaticText(self, -1, "Gain\nDirect", style= wx.ALIGN_LEFT)
		self.gainI = fsm.FsmTs(parent=self, id=-1,
										digits=3,
										min_val = 0.0,
										max_val = 10.0,
										increment=0.001,
										value = 1.0,
										size = siz,
										cSound = self.cSound,
										ftable = 99,
										indxn = 2)#channel = "outdirectV"
		#gain for freeze signal
		gainTD = wx.StaticText(self, -1, "Gain\nFreeze", style= wx.ALIGN_LEFT)
		self.gainD = fsm.FsmTs(parent=self, id=-1,
										digits=3,
										min_val = 0.0,
										max_val = 10.0,
										increment=0.001,
										value = 1.0,
										size = siz,
										cSound = self.cSound,
										ftable = 99,
										indxn = 3)
		#Limiter activation
		limitT = wx.StaticText(self, -1, "Limiter", style= wx.ALIGN_LEFT)
		self.limit = wx.CheckBox(self, -1, style=wx.CHK_2STATE)
		self.Bind(wx.EVT_CHECKBOX, self.limitSet, self.limit)
		#VUMETER OUTPUT
		vuLT = wx.StaticText(self, -1, "dB L", style= wx.ALIGN_CENTER | wx.TE_RICH)
		self.vumeter_inL = wx.TextCtrl(self, -1, size=(60,20))
		vuRT = wx.StaticText(self, -1, "dB R", style= wx.ALIGN_CENTER | wx.TE_RICH)
		self.vumeter_inR = wx.TextCtrl(self, -1, size=(60,20))
		#Timer Update MUST BE STOPPED IN MAIN FRAME
		self.timerRefresh = wx.Timer(self, wx.ID_ANY)
		self.timerRefresh.Start(200)
		self.Bind(wx.EVT_TIMER, self.timerUpdate, self.timerRefresh)
		#sizer
		controlSizer.Add(gainTI, pos=(0,0))
		controlSizer.Add(self.gainI, pos=(0,1))
		controlSizer.Add(gainTD, pos=(1,0))
		controlSizer.Add(self.gainD, pos=(1,1))
		controlSizer.Add(limitT, pos=(2,0))
		controlSizer.Add(self.limit, pos=(2,1))
		controlSizer.Add(vuLT, pos=(3,0))
		controlSizer.Add(self.vumeter_inL, pos=(3,1))
		controlSizer.Add(vuRT, pos=(4,0))
		controlSizer.Add(self.vumeter_inR, pos=(4,1))
		#
		mainSizer.AddSpacer(5, flag=wx.EXPAND)
		mainSizer.Add(controlSizer, 0, wx.EXPAND)
		mainSizer.AddSpacer(5, flag=wx.EXPAND)
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)		
		#initialize values
		self.cSound.TableSet(99, 2, 1.0)
		self.cSound.TableSet(99, 3, 1.0)
		self.cSound.TableSet(99, 4, 0.0)


	def OnClose(self, event):
		'''to destroy self and stop the timer'''
		self.timerRefresh.Stop() 
		self.Destroy()

	
	def limitSet(self, evt):
		"""activate the limiter"""
		state = self.limit.IsChecked()
		if state:
			self.cSound.TableSet(99, 4, 1.0)
		else:
			self.cSound.TableSet(99, 4, 0.0)


	def timerUpdate(self, evt):
		"""update the vumeters"""
		self.dbL = self.cSound.GetChannel("totalvul")
		self.dbR = self.cSound.GetChannel("totalvur")
		if self.dbL < -1.0:
			self.vumeter_inL.SetForegroundColour((100,250, 100))
		elif -1.0<= self.dbL < 0.0:
			self.vumeter_inL.SetForegroundColour((250, 200, 0))
		else:
			self.vumeter_inL.SetForegroundColour((250, 10, 10))
		if self.dbR < -1.0:
			self.vumeter_inR.SetForegroundColour((100,250, 100))
		elif -1.0<= self.dbR < 0.0:
			self.vumeter_inR.SetForegroundColour((250, 200, 0))
		else:
			self.vumeter_inR.SetForegroundColour((250, 10, 10))
		self.vumeter_inL.SetValue(str(self.dbL))
		self.vumeter_inR.SetValue(str(self.dbR))