import wx
import csnd6
import fsm

class FreezMidi():
	def __init__(self, parent, cSound, istance, command, commande):
		self.parent = parent
		self.cSound = cSound
		self.istance = istance
		self.items =[]
		siz=wx.Size(70,-1)#size of widgets
		ath = wx.StaticText(self.parent, -1, "Freez "+str(self.istance), style= wx.ALIGN_RIGHT | wx.TE_RICH)
		self.items.append(ath)
		########
		self.command = command
		self.commande = commande
		self.comm = wx.ComboBox(self.parent, -1, choices=self.command, size=siz)
		self.comm.SetValue(self.command[0])
		self.comm.SetSelection(0)
		self.comm.Bind(wx.EVT_COMBOBOX, self.setComm)
		self.items.append(self.comm)
		########
		#Channel
		self.cha = fsm.FsmTs(parent=self.parent, id=-1,
																		digits=0,
																		min_val = 1.0,
																		max_val = 16.0,
																		increment=1.0,
																		value = 1.0,
																		size = siz,
																		cSound = self.cSound,
																		indxn = self.istance,
																		ftable = 200)
		self.items.append(self.cha)
		#self.cSound.TableSet(16, self.istance, 0)
		#value
		self.vall = fsm.FsmTs(parent=self.parent, id=-1,
																		digits=0,
																		min_val = 1.0,
																		max_val = 127.0,
																		increment=1.0,
																		value = 1.0,
																		size = siz,
																		cSound = self.cSound,
																		indxn = self.istance,
																		ftable = 202)
		self.items.append(self.vall)
		#self.cSound.TableSet(16, self.istance, 0)
		
		
	def setComm(self, evt):
		ind = self.comm.GetSelection()
		val = self.commande[ind]
		self.cSound.TableSet(201, self.istance, val)



class MidiConfFr(wx.Frame):
	"""Main frame"""
	def __init__(self, *a, **k):
		self.cSound = k.pop('cSound', None)
		super(MidiConfFr, self).__init__(*a, **k)#super the subclass
		self.Bind(wx.EVT_CLOSE, self.on_close)

		panel = wx.Panel(self)
		panel.SetBackgroundColour((250, 0, 0))
		box = wx.GridBagSizer(vgap=2, hgap=5)
		
		self.command = ["NO", "NoteON", "NoteOFF", "PC"] 
		self.commande = [0, 144, 128, 192]
		'''
		#kstatus, kchan, kdata1, kdata2 midiin
		128 (note off)
		144 (note on)
		160 (polyphonic aftertouch)
		176 (control change)
		192 (program change)
		208 (channel aftertouch)
		224 (pitch bend
		0 if no MIDI message are pending in the MIDI IN buffer
		'''
		co = wx.StaticText(panel, -1, "Command", style= wx.ALIGN_RIGHT | wx.TE_RICH)
		box.Add(co, pos=(1,0))
		ch = wx.StaticText(panel, -1, "Channel", style= wx.ALIGN_RIGHT | wx.TE_RICH)
		box.Add(ch, pos=(2,0))
		va = wx.StaticText(panel, -1, "Value", style= wx.ALIGN_RIGHT | wx.TE_RICH)
		box.Add(va, pos=(3,0))
		self.midicomms = []
		for cou in range(1, 9):
			midicomm = FreezMidi(parent = panel, cSound = self.cSound, istance=cou, command = self.command, commande = self.commande)
			self.midicomms.append(midicomm)
			for item in range(0, len(midicomm.items)):
				box.Add(midicomm.items[item], pos=(item, cou))
		
		self.loadVals()
		panel.SetSizer(box)
		panel.Layout()
		box.Fit(self)
		
		
	def loadVals(self):
		f = open('midiconf.txt', 'r')
		for l in f:
			spll = l.strip()
			spl = spll.split('_')
			item = int(float(spl[1]))
			if spl[0] == "C":
				self.midicomms[item -1].cha.SetValue(int(spl[2]))
			elif spl[0] == "P":
				self.midicomms[item -1].comm.SetSelection(self.commande.index(int(spl[2])))
			elif spl[0] == "V":
				self.midicomms[item -1].vall.SetValue(float(spl[2]))
		f.close()

	def saveVals(self):
		f = open('midiconf.txt', 'w')
		for cou in range(0, len(self.midicomms)):
			for index in range(1, len(self.midicomms[cou].items)):
				if index == 1:
					let = "P"
					se = self.midicomms[cou].items[index].GetSelection()
					val = self.commande[se]
				elif index == 2:
					let = "C"
					val = int(self.midicomms[cou].items[index].GetValue())
				elif index == 3:
					let = "V"
					val = int(self.midicomms[cou].items[index].GetValue())
				f.write(let+'_'+str(cou+1)+'_'+str(val)+'\n')
		f.close()
		
		
		
	def on_close(self, evt):
		'''remove itself from the parent list of open istances
		then destroy itself'''
		for item in self.GetParent().mcFr:
			if item == self:
				self.GetParent().mcFr.remove(item)
		self.saveVals()
		self.Destroy()