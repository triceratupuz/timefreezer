import wx
import fsm

class InputPanel(wx.Panel):
	def __init__(self, *a, **k):
		self.cSound = k.pop('cSound', None)
		super(InputPanel, self).__init__(*a, **k)#super the subclass
		siz=wx.Size(70,-1)#size of gui elements
		mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		#Mono Stereo Input Selector
		self.monoStereo = wx.CheckBox(self, -1, label='StereoIn', style=wx.CHK_2STATE)
		self.Bind(wx.EVT_CHECKBOX, self.monoStereoSelect, self.monoStereo)
		#VUMETER
		self.vuSizer  = wx.GridBagSizer(vgap=10, hgap=10)
		vuLT = wx.StaticText(self, -1, "dB L", style= wx.ALIGN_CENTER | wx.TE_RICH)
		self.vumeter_inL = wx.TextCtrl(self, -1, size=(60,20))
		vuRT = wx.StaticText(self, -1, "dB R", style= wx.ALIGN_CENTER | wx.TE_RICH)
		self.vumeter_inR = wx.TextCtrl(self, -1, size=(60,20))
		#Gain
		gainT = wx.StaticText(self, -1, "Gain", style= wx.ALIGN_LEFT)
		self.gain = fsm.FsmTs(parent=self, id=-1,
										digits=3,
										min_val = 0.0,
										max_val = 1.1,
										increment=0.001,
										value = 1.0,
										size = siz,
										cSound = self.cSound,
										ftable = 99,
										indxn = 1)
		#Test Sound
		self.testSound = wx.CheckBox(self, -1, label='test Sound', style=wx.CHK_2STATE)
		self.Bind(wx.EVT_CHECKBOX, self.testSoundSelect, self.testSound)
		#Timer Update MUST BE STOPPED IN MAIN FRAME
		self.timerRefresh = wx.Timer(self, wx.ID_ANY)
		self.timerRefresh.Start(200)
		self.Bind(wx.EVT_TIMER, self.timerUpdate, self.timerRefresh)
		#initialize values
		self.cSound.TableSet(99, 0, 0.0)
		self.cSound.TableSet(99, 1, 1.0)
		#Sizer
		self.vuSizer.Add(self.monoStereo, pos=(0,1))
		self.vuSizer.Add(vuLT, pos=(2,0))
		self.vuSizer.Add(self.vumeter_inL, pos=(2,1))
		self.vuSizer.Add(vuRT, pos=(3,0))
		self.vuSizer.Add(self.vumeter_inR, pos=(3,1))
		self.vuSizer.Add(gainT, pos=(1,0))
		self.vuSizer.Add(self.gain, pos=(1,1))
		self.vuSizer.Add(self.testSound, pos=(4,1))
		#
		mainSizer.AddSpacer(5, flag=wx.EXPAND)
		mainSizer.Add(self.vuSizer, 0, wx.EXPAND)
		mainSizer.AddSpacer(5, flag=wx.EXPAND)
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)

	def OnClose(self, event):
		'''to destroy self and stop the timer'''
		self.timerRefresh.Stop() 
		self.Destroy()


	def monoStereoSelect(self, evt):
		'''set the mono or stereo input'''
		state = self.monoStereo.IsChecked()
		if state:
			self.cSound.TableSet(99, 0, 1.0)
		else:
			self.cSound.TableSet(99, 0, 0.0)
		
		

	def testSoundSelect(self, evt):
		'''activate/deactivate test sound'''
		state = self.testSound.IsChecked()
		if state:
			self.cSound.SetChannel("test_sound", 1)
		else:
			self.cSound.SetChannel("test_sound", 0)
		
		
	def timerUpdate(self, evt):
		"""update the vumeters values and colours"""
		self.dbL = self.cSound.GetChannel("directvul")
		self.dbR = self.cSound.GetChannel("directvur")
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
		
