from threading import Thread
import telepot
from telepot.loop import MessageLoop
import time
import configparser
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize
###############################
from sdpcam import waktu
###############################
import datetime
import cv2
from urllib.request import urlopen, URLError
import subprocess as sp
import os


class telebot():
	def __init__(self):
		self.mn = True
		self.mnn1 = 0
		self.konfigjam = ""
		self.konfigmenit = ""
		self.konfigdurasi = ""
		self.hasil = ""
		self.status = 0
		self.config = configparser.SafeConfigParser()
		self.stopped = False
		self.sdpcam = waktu()
		try:
			self.config.read(open('SMADHARMAPUTRA.ini'))
			print('memuat konfigurasi....')
		except:
			try:
				self.config.add_section('alarmcam1')
				self.config.add_section('alarmcam2')
				self.config.add_section('alarmcam3')
				self.config.add_section('alarmcam4')
				self.config.add_section('alarmrelay1')
				self.config.add_section('alarmrelay2')
				self.config.add_section('alarmrelay3')
				self.config.add_section('alarmrelay4')
				self.config.add_section('status')
				self.config.set('status','status','0')
				self.config.set('alarmcam1','hour','00:00:00')
				self.config.set('alarmcam2','hour','00:00:00')
				self.config.set('alarmcam3','hour','00:00:00')
				self.config.set('alarmcam4','hour','00:00:00')
				self.config.set('alarmrelay1','time_on','00:00:00')
				self.config.set('alarmrelay2','time_on','00:00:00')
				self.config.set('alarmrelay3','time_on','00:00:00')
				self.config.set('alarmrelay4','time_on','00:00:00')
				self.config.set('alarmcam1','durasi','00:00:00')
				self.config.set('alarmcam2','durasi','00:00:00')
				self.config.set('alarmcam3','durasi','00:00:00')
				self.config.set('alarmcam4','durasi','00:00:00')
				self.config.set('alarmrelay1','time_off','00:00:00')
				self.config.set('alarmrelay2','time_off','00:00:00')
				self.config.set('alarmrelay3','time_off','00:00:00')
				self.config.set('alarmrelay4','time_off','00:00:00')
				with open('SMADHARMAPUTRA.ini','w') as configfile:
					self.config.write(configfile)
				print('Membuat Konfigurasi....')
			except:
				print('cannot Create File')
			self.status = self.config.get('status','status')
		
		#self.start()
	def startBot(self):
		self.bot = telepot.Bot('333574709:AAH6JLNwXwYgExVxfFQ0rSGfBd-Ofq4eI4U')
		MessageLoop(self.bot, {'chat': self.handle}).run_as_thread()
		while 1:
			time.sleep(20)
	def handle(self, msg):
	
		content_type, chat_type, chat_id = telepot.glance(msg)
		command = msg['text']
		
		print ('Got command: %s' % command)
		print (chat_id)
		
		def papanmenu():
			keyboardLayout = [['AMBIL GAMBAR','AMBIL VIDEO'],
				['WaktuBell01','WaktuBell02','WaktuBell03','WaktuBell04',],
				['WaktuKamera01','WaktuKamera02','WaktuKamera03','WaktuKamera04']
				['Panduan']]			
			replyKeyboardMakeup = {'keyboard': keyboardLayout, 'resize_keyboard': False, 'one_time_keyboard': True}
			self.bot.sendMessage(chat_id, text = '[Panduan] untuk informasi lebih lanjut',reply_markup = replyKeyboardMakeup)
			#self.bot.sendMessage(chat_id, text = 'AMBIL GAMBAR - Mengambil gambar pada CCTV \nAMBIL VIDEO - Merekam video selama 5 detik \nALARM1-ALARM4 - Mengoperasikan kamera pada waktu dan durasi yang telah ditentukan \n\nSMA Dharma Putra', reply_markup = replyKeyboardMakeup)
		
		def papankonfigurasi(jam, alarm):
			a0 = ['BATAL']
			a1 =['00','01','02','03']
			a2 =['04','05','06','07']
			a3 =['08','09','10','11']
			a4 =['12','13','14','15']
			a5 =['16','17','18','19']
			a6 =['20','21','22','23']
			keyboardLayout = [a0,a1,a2,a3,a4,a5,a6]
			replyKeyboardMakeup = {'keyboard': keyboardLayout, 'resize_keyboard': False, 'one_time_keyboard': True}
			
			b1 = ['00','05','10','15']
			b2 = ['20','25','30','35']
			b3 = ['40','45','50','55']
			keyboardLayout1 = [a0,b1,b2,b3]
			replyKeyboardMakeup1 = {'keyboard': keyboardLayout1, 'resize_keyboard': False, 'one_time_keyboard': True}
			
			c1 = ['05','10','15','20']
			c2 = ['25','30','35','40']
			c3 = ['45','50','55','60']
			keyboardLayout2 = [a0,c1,c2,c3]
			replyKeyboardMakeup2 = {'keyboard': keyboardLayout2, 'resize_keyboard': False, 'one_time_keyboard': True}
			if jam == 'BATAL':
				papanmenu()
				self.status = 4
				self.mn = True
				self.mnn1 = 0
				menuutama(command)
			if self.status == 0:
				self.bot.sendMessage(chat_id, text = 'Pada Jam Berapa?', reply_markup = replyKeyboardMakeup)
				self.status = self.status + 1
			elif self.status == 1:
				self.konfigjam = jam
				self.bot.sendMessage(chat_id, text = 'Pada Menit Berapa ??', reply_markup = replyKeyboardMakeup1)
				self.status = self.status + 1
			elif self.status == 2:
				self.konfigmenit = jam
				self.bot.sendMessage(chat_id, text = 'Berapa Lama', reply_markup = replyKeyboardMakeup2)
				self.status = self.status + 1
			elif self.status == 3:
				self.konfigdurasi = jam
				self.hasil = self.konfigjam+':'+self.konfigmenit
				self.config.read('SMADHARMAPUTRA.ini')
				self.config.set(alarm,'hour',self.hasil+':00')
				self.config.set(alarm,'durasi','00:'+self.konfigdurasi+':00')
				with open('SMADHARMAPUTRA.ini','w+') as configfile:
					self.config.write(configfile)
				testjam = self.config.get(alarm,'hour')
				testdurasi = self.config.get(alarm,'durasi')
				self.bot.sendMessage(chat_id, text = alarm+' telah disetel setiap pukul '+testjam+' selama '+testdurasi+' Menit')
				self.mn = True
				self.status = self.status + 1
				self.mnn1 = 0
				papanmenu()
				menuutama(command)
			elif self.status == 4:
				print('[INFO]-Done.')
		def menuutama(commands):
			if commands == 'AMBIL GAMBAR':
				filenameimg = datetime.datetime.now().strftime('%Y%m%d-%H%M%S.jpg')
				self.sdpcam.startCaptureCam(filenameimg)
				#grab = cam()
				#grab.capImage(filenameimg)
				#grab.stop()
				self.bot.sendPhoto(chat_id, photo = open(filenameimg,'rb'),caption= filenameimg)
			elif commands == 'AMBIL VIDEO':
				filenamevid = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'+'.mp4')
				self.sdpcam.startRecordCam(filenamevid)
				self.bot.sendChatAction(chat_id, 'upload_video')
				self.bot.sendVideo(chat_id, video = open(filenamevid, 'rb'),caption = filenamevid)
			elif commands == 'Panduan':
				self.bot.sendMessage(chat_id, text = 'AMBIL GAMBAR - Mengambil gambar pada CCTV \nAMBIL VIDEO - Merekam video selama 10 detik \nWaktuKamera01-04 - Mengoperasikan kamera pada waktu dan durasi yang telah ditentukan \nWaktuBell01-04 - Mengoperasikan Bell pada waktu yang telah ditentukan\n\nSMA Dharma Putra', reply_markup = replyKeyboardMakeup)
			elif commands == 'WaktuKamera01':
				self.mn == False
				self.mnn1 = 1
				self.status = 0
			elif commands == 'WaktuKamera02':
				self.mn == False
				self.mnn1 = 2
				self.status = 0
			elif commands == 'WaktuKamera03':
				self.mn == False
				self.mnn1 = 3
				self.status = 0
			elif commands == 'WaktuKamera04':
				self.mn == False
				self.mnn1 = 4
				self.status = 0
			
		if command == '/test':
			self.mn == True
			self.bot.sendMessage(chat_id, 'Test Mode')
		if command == '/start':
			papanmenu()
		if command == '/run':
			self.config.read('SMADHARMAPUTRA.ini')
			self.config.set('status','status','1')
			with open('SMADHARMAPUTRA.ini','w+') as configfile:
				self.config.write(configfile)
			self.waktux.loadConfig()
			self.waktux.LoadGPIO()
			self.waktux.start()
		if command == '/stop':
			self.config.read('SMADHARMAPUTRA.ini')
			self.config.set('status','status','0')
			with open('SMADHARMAPUTRA.ini','w+') as configfile:
				self.config.write(configfile)
			self.waktux.loadConfig()
			self.waktux.ClearGPIO()
		if self.mn == True:
			menuutama(command)
		if self.mnn1 == 0:
			self.mn == True
		if self.mnn1 == 1:
			papankonfigurasi(command,'alarmcam1')
		if self.mnn1 == 2:
			papankonfigurasi(command,'alarmcam2')
		if self.mnn1 == 3:
			papankonfigurasi(command,'alarmcam3')
		if self.mnn1 == 4:
			papankonfigurasi(command,'alarmcam4')

def check_connectivity(reference):
    try:
        urlopen(reference, timeout=1)
        return True
    except URLError:
        return False


def wait_for_internet():
    while not check_connectivity("https://api.telegram.org"):
        print("Waiting for internet")
        time.sleep(1)
	
def main():
	wait_for_internet()
	try:
		a = myClassA()
		a.startBot()
	except:
		print("[INFO] no internet connection")
		return
if __name__ == "__main__":
	main()