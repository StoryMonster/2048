#-*- coding:utf-8 -*-
import os
import pyHook
import random
import pythoncom
import win32api


class Game2048:
	def __init__(self):
		self.hm = pyHook.HookManager()
		self.hm.KeyDown = self.OnKeyboardEvent
		self.hm.HookKeyboard()
		self.Map = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
		self.BiggestNum = 1
		self.randomNumSeq = [1]
		self.GameOver = False
		self.GameResult = 'You Fail!'

	def MoveLeft(self):
		Moved = False
		for i in range(0, 4):
			oldLine = []
			for k in range(0, 4): oldLine.append(self.Map[i][k]) 
			line = self.GetNoneZeroSeq(self.Map[i])
			tempLine = self.Combine(line,"FRONT")
			tempLine = self.GetNoneZeroSeq(tempLine)
			newLine = [0,0,0,0]
			for k in range(0,4):
				self.Map[i][k] = 0
			for k in range(0,len(tempLine)):
				self.Map[i][k] = tempLine[k]
				newLine[k] = tempLine[k]
			if newLine != oldLine: Moved = True
			print(oldLine)
			print(newLine)
		return Moved

	def MoveRight(self):
		Moved = False
		for i in range(0,4):
			oldLine = []
			for k in range(0,4): oldLine.append(self.Map[i][k]) 
			line = self.GetNoneZeroSeq(self.Map[i])
			tempLine = self.Combine(line,"BACK")
			tempLine = self.GetNoneZeroSeq(tempLine)
			newLine = [0,0,0,0]
			for k in range(0,4):
				self.Map[i][k] = 0
			for k in range(0,len(tempLine)):
				self.Map[i][-1-k] = tempLine[k]
				newLine[-1-k] = tempLine[k]
			if oldLine != newLine: Moved = True
		return Moved

	def MoveUp(self):
		Moved = False
		for i in range(0,4):
			col = []
			for k in range(0,4):
				col.append(self.Map[k][i])
			oldCol = col
			tempCol = self.GetNoneZeroSeq(col)
			tempCol = self.Combine(tempCol,"FRONT")
			tempCol = self.GetNoneZeroSeq(tempCol)
			newCol = [0,0,0,0]
			for k in range(0,4):
				self.Map[k][i] = 0
			for k in range(0,len(tempCol)):
				self.Map[k][i] = tempCol[k]
				newCol[k] = tempCol[k]
			if oldCol != newCol: Moved = True	
		return Moved

	def MoveDown(self):
		Moved = False
		for i in range(0,4):
			col = []
			for k in range(0,4):
				col.append(self.Map[k][i])
			oldCol = col
			tempCol = self.GetNoneZeroSeq(col)
			tempCol = self.Combine(tempCol,"BACK")
			tempCol = self.GetNoneZeroSeq(tempCol)
			newCol = [0,0,0,0]
			for k in range(0,4):
				self.Map[k][i] = 0
			for k in range(0,len(tempCol)):
				self.Map[-1-k][i] = tempCol[k]
				newCol[-1-k] = tempCol[k]
			if oldCol != newCol: Moved = True	
		return Moved

	def GetNoneZeroSeq(self,seq):
		newSeq = []
		for i in seq:
			if i != 0:
				newSeq.append(i)
		return newSeq

	def Combine(self,seq,dir):
		if dir == 'BACK':
			seq.reverse()
		for i in range(0,len(seq)-1):
			if seq[i] == seq[i+1]:
				seq[i] *= 2
				seq[i+1]= 0
				if seq[i] > self.BiggestNum:
					self.BiggestNum = seq[i]
					if self.BiggestNum >= 8:
						self.randomNumSeq.append(self.BiggestNum/4)	
		return seq
		
	def IsGameOver(self):
		if self.BiggestNum == 2048:
			self.GameResult = 'You Win!'
			return True
		for i in range(0,4):
			for j in range(0,4):
				if self.Map[i][j] == 0: return False
				if j != 3:
					if self.Map[i][j] == self.Map[i][j+1]: return False
				if i != 3:
					if self.Map[i][j] == self.Map[i+1][j]: return False
		self.GameResult = 'You Fail!'
		return True

	def GameOverSurface(self,info):
		print(' ' * 20, info)
		win32api.PostQuitMessage()
		
	def PlayingSurface(self):
		os.system('cls')
		print('\n')
		print(' '*19,'2048')
		for i in range(0,4):
			print(' '*8,'-'*25)
			print(' '*8,'|%5d|%5d|%5d|%5d|' % (self.Map[i][0],self.Map[i][1],self.Map[i][2],self.Map[i][3]))
		print(' '*8,'-'*25)
		
	def run(self):
		self.CreateNewDigit()
		self.PlayingSurface()
		pythoncom.PumpMessages()
			
	def CreateNewDigit(self):
		newDigit = random.choice(self.randomNumSeq)
		pos = random.randrange(1,17,1)
		count = 0
		for i in range(0,4):
			for j in range(0,4):
				if self.Map[i][j] == 0:
					count += 1
					if count == pos:
						self.Map[i][j] = newDigit
						return 

	def OnKeyboardEvent(self,event):
		Moved = False
		if event.Key == 'Right':
			Moved = self.MoveRight()
		elif event.Key == 'Left':
			Moved = self.MoveLeft()
		elif event.Key == 'Down':
			Moved = self.MoveDown()
		elif event.Key == 'Up':
			Moved = self.MoveUp()
		elif event.Key == 'Escape':
			win32api.PostQuitMessage()
		else : return True
		if  Moved == True:
			self.CreateNewDigit()
			self.PlayingSurface()
			if self.IsGameOver():
				self.GameOverSurface(self.GameResult)
		return True

if __name__ == '__main__':
	game = Game2048()
	game.run()
