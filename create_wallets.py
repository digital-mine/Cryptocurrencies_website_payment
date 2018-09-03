##PLEASE CREATE A DATABASE FILE IN THE SAME FOLDER OF THIS SCRIPT, and name it "addresses.db"
##With this program you will be able to create 100 unique deposit addresses for your website USERS, and store them into a database
##It will generate 100 addresses, once you will have used all of them it will create 100 more.
##Please read the README FILE.

from subprocess import call
from subprocess import check_output
import subprocess
import re
import csv

def create_addresses():
	y=1
	while y<=100: #change the number if you want to generate more or less addresses
		out = check_output(['./clamd','getnewaddress',''])#./bitcoin-cli for Bitcoin
		print (out)
		y+=1
	outt = check_output(['./clamd','getaddressesbyaccount',''])#./bitcoin-cli for Bitcoin
	addr=re.findall('"(.+?)"',str(outt))
	L=[]
	with open('addresses.db') as csvfile:
		reader=csv.DictReader(csvfile)
		for row in reader:
			cont=row['ID']	
			L.append(cont)
	print ('datbase:',len(L),'entries')
	print ('wallet:',len(addr),'entries')
	if len(L)>0:
		x=int(L[-1])+1
	else:
		x=1
	print ("I'm writing new addresses to database")
	old=[]
	with open('addresses.db') as csvfile:
		reader=csv.DictReader(csvfile)
		for row in reader:
			old_=row['ADDRESS']	
			old.append(old_)
	new=[]
	for i in addr:
		if i not in old:
			print ('new', i)
			new.append(i)
	with open('addresses.db','a') as csvfile:
		fieldnames = ['ID','EMAIL','ADDRESS']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		for i in new:
			writer.writerow({'ID':x,'EMAIL':'','ADDRESS':i})
			x+=1
	return len(new)
def check_addresses():
	out = check_output(['./clamd','getaddressesbyaccount',''])#./bitcoin-cli for Bitcoin
	addr=re.findall('"(.+?)"',str(out))
	return len(addr)

def check_double():
	current=[]
	with open('addresses.db') as csvfile:
		reader=csv.DictReader(csvfile)
		for row in reader:
			old_=row['ADDRESS']	
			#print (old_)
			current.append(old_)
	print ('TOTAL CURRENT DATABASE:',len(current))
	
	double=[]
	check=[]
	for i in current:
		if i not in check:
			check.append(i)
		else:
			double.append(i)
			print ('DUPLICATE WALLET:',i)
	print ('LEN DUPLICATE WALLET:',len(double))
		
	
##################################################################
tot=check_addresses()
print ('TOTAL CURRENT ADDRS:',tot)
if tot <=1:
	print("I'm creating 100 new addresses")
	new_addrs=create_addresses()
	print ('Number of new wallet:',new_addrs)
check_double()
###################################################################
