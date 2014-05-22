import signal
import sys
import urllib
import urllib2
import random
import lxml.html

frm_token = random.random();
url = 'http://karresults.nic.in/resSSLC2014.asp'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
values = {'frm_tokens':frm_token, 
	  'regno': 20140100001,
          'B1':'Go' 
	 }
headers = { 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	    'Accept-Encoding':'gzip,deflate,sdch',
	    'Accept-Language':'en-US,en;q=0.8',
	    'Cache-Control':'max-age=0',
	    'Connection':'keep-alive',
	    'Content-Type':'application/x-www-form-urlencoded',
	    'DNT':'1',
	    'Host':'karresults.nic.in',
	    'Origin':'http://karresults.nic.in',
	    'Referer':'http://karresults.nic.in/indexsslc2014.asp',
	    'User-Agent' : user_agent 
					} 
subjects = [{},{},{},{},{},{},{}] 
students = 0;

def signal_handler(signal, frame):
	# In case of any error(Cntrl-C by user or network disconnected or PC going to sleep mode ) Print the dictionary data and exit
	# handle this in a better way. if network discoonnects wait till network is back instead of exiting
	print subjects, students;
	sys.exit(0)

def get_result(n):
	values['frm_tokens'] = random.random();
	values['regno']=n;
	data = urllib.urlencode(values)
	req = urllib2.Request(url, data, headers)
	response = urllib2.urlopen(req)
	the_page = response.read()
	the_page = the_page.replace('\r\n', '')

	root = lxml.html.fromstring(the_page)
	table_main = root.xpath('//table');
	row1= root.xpath('//table')[0].xpath('.//tr/td//text()');
	if row1[7] == "Back":
		print 'Invavid roll number ',n
		return [0,[]];
	row1 = root.xpath('//table')[1].xpath('.//tr/td//text()')
	print row1;
	return [1,[int(row1[7]), int(row1[9]), int(row1[11]), int(row1[13]), int(row1[15]), int(row1[17])] ];

def get_all_marks():
	global students
	signal.signal(signal.SIGINT, signal_handler)
	try:
		for major_num in range(88):
			for minnor_num in range(99999):
				roll = 20140000000 + (major_num+1) * 100000 + (minnor_num+1) ;
				[result, marks]=get_result(str(roll));
				if result == 0:
					continue;
				else:
					for i in range(len(marks)):
						if marks[i] in	subjects[i]:
							subjects[i][marks[i]] +=1 ;
						else:
							subjects[i][marks[i]] = 1;
				students += 1;
		print subjects, students;
	except :
		print subjects, students;

if __name__ == '__main__':
	get_all_marks()
