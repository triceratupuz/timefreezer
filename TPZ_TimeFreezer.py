#!/usr/bin/python

import os
import wx
import csnd6
import libs.inputPanel as inputPanel
import libs.freez as freez
import libs.outPanel as outPanel


#CSND CODE###########################################################
###################################################################
###################################################################
c = csnd6.Csound()    # create an instance of Csound

file = "csd/TPZ_freezer.csd"

c.Compile(file)     # Compile Orchestra from String

perfThread = csnd6.CsoundPerformanceThread(c)
#performance thread RUN
perfThread.Play()




#GUI CODE###########################################################
###################################################################
###################################################################
#Frame
class TopFrame(wx.Frame):
	"""Main frame"""
	def __init__(self, parent, title):
		#wx.Frame.__init__(self, *a, **k)
		#self.csound = k.pop('csound', None)
		#super(TopFrame, self).__init__(*a, **k)#super the subclass
		super(TopFrame, self).__init__(parent= parent, title = title, style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER |wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX))#super the subclass
		#panel
		self.hboxsizer = wx.BoxSizer(wx.HORIZONTAL)
		self.inP = inputPanel.InputPanel(self, -1, cSound=c)
		#self.inP.SetBackgroundColour((200, 250, 200))
		self.hboxsizer.Add(self.inP, 0,wx.EXPAND)
		self.freezers = freez.FreezPanel(self, -1, cSound=c, freezers=8)
		self.hboxsizer.Add(self.freezers, 0,wx.EXPAND)
		self.outP = outPanel.OutPanel(self, -1, cSound=c)
		self.hboxsizer.Add(self.outP, 0,wx.EXPAND)
		#Midi Conf Frame
		self.loadMidiSet()
		#set sizer to panel
		self.SetSizer(self.hboxsizer)
		self.hboxsizer.Fit(self)
		self.Show()

	def loadMidiSet(self):
		f = open('midiconf.txt', 'r')
		for l in f:
			spll = l.strip()
			spl = spll.split('_')
			item = int(float(spl[1]))
			if spl[0] == "C":
				c.TableSet(200, item, int(spl[2]))
				#self.midicomms[item -1].cha.SetValue(int(spl[2]))
			elif spl[0] == "P":
				c.TableSet(201, item, int(spl[2]))
				#self.midicomms[item -1].comm.SetSelection(self.commande.index(int(spl[2])))
			elif spl[0] == "V":
				c.TableSet(202, item, int(spl[2]))
				#self.midicomms[item -1].vall.SetValue(float(spl[2]))
		f.close()


class AppWithTerm(wx.App):
	"""wx.App subclassed to include csound Thread termination"""
	def OnExit(self):
		print "Closing csnd Thread"
		perfThread.Stop()
		print "Stopped csnd Thread"
		perfThread.Join()
		print "Closed csnd Thread"
		return


app = AppWithTerm(False)#True to redirect stdin/sterr
frame = TopFrame(None, title='Time Freezer')
#frame.Show()
app.MainLoop()
