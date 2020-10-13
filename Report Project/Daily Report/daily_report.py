import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd
import numpy as np
from datetime import datetime 
import pandas_datareader as web
from datetime import timedelta
from info_data import info_dict

today = datetime.today().date()
start = today-timedelta(days=5)

print('test1')

index = ['^GSPC','^DJI','^IXIC','^RUT']

current,pts,per = [],[],[]

for i in range(len(index)):
    data = web.DataReader(index[i],'yahoo',start,today)['Close']
    data[-1]
    pts_change = round(data[-1] - data[-2],2)
    per_change = str(round(pts_change/data[-2]*100,2))+'%'
    
    current.append(str(round(data[-1],2)))
    pts.append(str(pts_change))
    per.append(per_change)

def color(number):
    if number < 0:
        return 'red'
    elif number >= 0:
        return 'green'

def price_alert(info_dictionary):
    ticker = list(info_dictionary.keys())
    for i in range(len(info_dictionary)):
        
        data = web.DataReader(ticker[i], 'yahoo', start, today)
        price_data = data['Adj Close']
        curr_price = round(price_data[-1],2)
        of_target = curr_price/(info_dictionary[ticker[i]]['Target'])
        
        info_dictionary[ticker[i]]['Open']= round(data['Open'][-1],2)
        info_dictionary[ticker[i]]['Close']= curr_price
        info_dictionary[ticker[i]]['Move Today'] = round(((price_data[-1]-price_data[-2])/price_data[-2])*100,2)
        info_dictionary[ticker[i]]['% of Target']= round(of_target*100,2)
        info_dictionary[ticker[i]]['% Below Basis'] = round((info_dictionary[ticker[i]]['Close']-info_dictionary[ticker[i]]['Basis'])/(info_dictionary[ticker[i]]['Basis'])*100,2)        
    return info_dictionary

print('test2')

info = price_alert(info_dict)
df = pd.DataFrame(info).transpose()

price_alert = df[['Target','Open','Close','% of Target']]
price_alert = price_alert[price_alert['% of Target']>97]
for i in range(len(price_alert)):
    price_alert.replace(price_alert['% of Target'][i],str(price_alert['% of Target'][i])+'%',inplace = True)
    price_alert.replace(price_alert['Open'][i],'$'+str(price_alert['Open'][i]),inplace = True)
    price_alert.replace(price_alert['Target'][i],'$'+str(price_alert['Target'][i]),inplace = True)
    price_alert.replace(price_alert['Close'][i],'$'+str(price_alert['Close'][i]),inplace = True)
price_alert = price_alert.to_html()[:34] + ' style="text-align: center'+ price_alert.to_html()[34:]

poor_alert = df[['Basis','Close','Move Today','% Below Basis']]
poor_alert = poor_alert[poor_alert['% Below Basis'] < -10]
for i in range(len(poor_alert)):
    poor_alert.replace(poor_alert['% Below Basis'][i],str(poor_alert['% Below Basis'][i])+'%',inplace = True)
#    poor_alert.replace(poor_alert['Open'][i],'$'+str(poor_alert['Open'][i]),inplace = True)
    poor_alert.replace(poor_alert['Move Today'][i],str(poor_alert['Move Today'][i])+'%',inplace = True)
    poor_alert.replace(poor_alert['Basis'][i],'$'+str(poor_alert['Basis'][i]),inplace = True)
    poor_alert.replace(poor_alert['Close'][i],'$'+str(poor_alert['Close'][i]),inplace = True)
poor_alert = poor_alert.to_html()[:34] + ' style="text-align: center'+ poor_alert.to_html()[34:]

move_today = df[['Target','Open','Close','Move Today']]
move_today = move_today[abs(move_today['Move Today'])>=5]
for i in range(len(move_today)):
    move_today.replace(move_today['Move Today'][i],str(move_today['Move Today'][i])+'%',inplace = True)
    move_today.replace(move_today['Open'][i],'$'+str(move_today['Open'][i]),inplace = True)
    move_today.replace(move_today['Target'][i],'$'+str(move_today['Target'][i]),inplace = True)
    move_today.replace(move_today['Close'][i],'$'+str(move_today['Close'][i]),inplace = True)
move_today = move_today.to_html()[:34] + ' style="text-align: center'+ move_today.to_html()[34:]
print('test3')
html = """<html>

<head>
	<title> Daily Report </title>
	<style>
		.main_head {
			text-align: center;
			font-size: 25px;
			margin: 15px auto 0px auto;
		}

		.col {
			float: left;
			width: 25%;
			text-align: center;
			font-size: 15px;
			font-weight: bold;
		}

		.index {
			margin-bottom: 0px;
		}

		.spy,
		.djia,
		.nasdaq,
		.r2000 {
			margin: 0px;
		}

		.spy {
			color:""" + color(float(pts[0])) + """;
		}

		.djia {
			color:"""+color(float(pts[1])) +""";
		}

		.nasdaq {
			color: """+color(float(pts[2]))+""";
		}

		.r2000 {
			color: """ + color(float(pts[3])) +""";
		}

		.index_info {
			font-size: 10px;
		}

		table {
			width: 80%;
			margin-left: auto;
			margin-right: auto;
		}

		.price_alert {
			margin-top: 10%;
		}
		
		footer p{
			text-align: center;
		}
	</style>
</head>

<body>
	<p class='main_head'>Daily Report ("""+str(today.month)+"""/"""+str(today.day)+"""/"""+str(today.year)+""")</p>
	<div class="row">
		<div class="col">
			<p class="index"> S&amp;P 500</p>
			<p class="spy">"""+current[0]+"""</p>
			<p class='spy index_info'>"""+pts[0]+"""("""+per[0]+""")</p>
		</div>
		<div class="col">
			<p class="index">Dow 30</p>
			<p class="djia">"""+current[1]+"""</p>
			<p class="djia index_info">"""+pts[1]+"""("""+per[1]+""")</p>
		</div>
		<div class="col">
			<p class="index">Nasdaq</p>
			<p class="nasdaq">"""+current[2]+"""</p>
			<p class="nasdaq index_info">"""+pts[2]+"""("""+per[2]+""")</p>
		</div>
		<div class="col">
			<p class="index">Russell 2000</p>
			<p class="r2000">"""+current[3]+"""</p>
			<p class="r2000 index_info">"""+pts[3]+"""("""+per[3]+""")</p>
		</div>
	</div>
	<div class="price_alert">
		<p class="main_head">Daily Report Alert<sup>*</sup></p>
        """ +price_alert+ """
	</div>
	<div class='poor_perf'>
		<p class="main_head">Poor Stock Performer Alert<sup>&dagger;</sup></p>
""" +poor_alert+ """
	</div>
	<div class="swing">
		<p class="main_head">Daily Biggest Movement<sup>&loz;</sup></p>
"""+move_today+"""
	</div>
	<footer>
		<p>
		*: A company is featured in this list if its current price within 3% or over the IMA target Price<br>
		&dagger;: A company is featured in this list if its current price is down >=10% buying price<br>
		&loz;: A company is featuerd in this list if its price jumped >=5% today
			
			
		</p>
		
	</footer>
</body>

</html>

"""

sender = ##sender email
receiver = ##receiver email
password = ##password of the sender email
date_today = today

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] =  str(date_today.month)+ '/' + str(date_today.day) + '/' +str(date_today.year)+" || Daily Report"
msg['From'] = sender
msg['To'] = ", ".join(receiver)

def email_send():
    if len(price_alert) or len(poor_alert) or len(move_today)>= 0:
        p2 = MIMEText(html, 'html')

        msg.attach(p2)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender,password)

        server.sendmail(sender, receiver, msg.as_string())
        server.quit()

##Only sends email on the weekdays
day = date_today.isoweekday()
if day != 7 and day != 6:
    email_send()
