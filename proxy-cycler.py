import re
import time
from datetime import datetime, timedelta


class ProxyCycler():

	def __init__(self):
		
		self.proxies = [];
		
		self.hitCount = 0;
		self.hitLimit = float("inf");
		
		self.rotateNum = 0;
		self.lastRotateTime = datetime.now();
		self.rotateInterval = timedelta.max;
	
	
	def setRotateInterval(self, timeDelta):
		self.rotateInterval = timeDelta;
		
	def setHitLimit(self, limit):
		self.hitLimit = limit;
	
	def setRotateRate(self):
		return;
	
	
	def addProxy(self, config):
		
		if isinstance(config, str):
		
			patt = "(https?|socks)://(.+?):(\d+)";
			result = re.search(patt, config);
			if (result):
				config = {
					"protocol": result.group(1), 
					"host": result.group(2),
					"port": result.group(3)
				};
			else:
				pattWithAuth = "(https?|socks)://(.+?):(.+?)@(.+?):(\d+)";
				result = re.search(pattWithAuth, config)
				if (result):
					config = {
						"protocol": result.group(1), 
						"user": result.group(2),
						"password": result.group(3),
						"host": result.group(4),
						"port": result.group(5)
					};
				else:
					#Bad proxy
					return;
		
		if not isinstance(config, list):
			config = [config];
		
		for proxy in config:
			if not isinstance(proxy, dict):
				raise Exception('proxy config must be in the form of a dictionary')
			
			self.proxies.append(proxy);
		
		return;
	
	def getNumProxies(self):
		return len(self.proxies);
	
	
	def getProxy(self):
	
		if len(self.proxies) == 0:
			raise Exception('You must first add proxies to the list');
		
		if (self.hitCount < self.hitLimit):
			self.hitCount += 1;
		else:
			self.hitCount = 1;
			self.rotateNum += 1;
			self.lastRotateTime = datetime.now();
		
		if (datetime.now() - self.lastRotateTime > self.rotateInterval):
			self.rotateNum += 1;
			self.lastRotateTime = datetime.now();
			
		return self.proxies[self.rotateNum % len(self.proxies)];
	
	def getNextProxy(self):
		
		self.hitCount = 0;
		self.rotateNum += 1;
		self.lastRotateTime = datetime.now();
		
		return self.getProxy();
	
	
	def getIP(self):
	
		if len(self.proxies) == 0:
			raise Exception('You must first add proxies to the list');
		
		if (self.hitCount < self.hitLimit):
			self.hitCount += 1;
		else:
			self.hitCount = 1;
			self.rotateNum += 1;
			self.lastRotateTime = datetime.now();
		
		if (datetime.now() - self.lastRotateTime > self.rotateInterval):
			self.rotateNum += 1;
			self.lastRotateTime = datetime.now();
		
		proxy = self.proxies[self.rotateNum % len(self.proxies)];
		
		auth = "";
		if "user" in proxy and "password" in proxy:
			auth = "{}:{}@".format(proxy["user"], proxy["password"]);
		
		ip = "{}://{}{}:{}".format(proxy["protocol"], auth, proxy["host"], proxy["port"]);
		
		return ip;
	
	def getNextIP(self):
		
		self.hitCount = 0;
		self.rotateNum += 1;
		self.lastRotateTime = datetime.now();
		
		return self.getIP();
	

def main():
	
	proxyList = [
		{"host": "239.208.1.167", "protocol": "http", "port": 8080},
		{"host": "230.34.28.109", "protocol": "http", "port": 8080},
		{"host": "120.77.68.24", "protocol": "https", "port": 8443, "user": "dan", "password": "123456"},
		{"host": "245.89.141.55", "protocol": "https", "port": 8443, "user": "dan2", "password": "234567"},
		{"host": "181.113.177.87", "protocol": "socks", "port": 8090},
	];
	
	switch = ProxyCycler();
	
	switch.addProxy(proxyList);
	# switch.addProxy("https://120.77.68.24:8443");
	# switch.addProxy("https://dan:123456@120.77.68.24:8443");
	
	switch.setRotateInterval(timedelta(milliseconds=100));
	
	for i in range(5):
		ip = switch.getIP();
		time.sleep(0.1);
		print("{}) {}".format(i + 1, ip));
	
	return;
	
	for i in range(7):
		ip = switch.getNextProxy();
		print("{}) {}".format(i + 1, ip));
	
	return;


if __name__ == "__main__":
	main();
	
	
	