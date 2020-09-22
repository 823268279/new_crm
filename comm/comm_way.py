# -*- coding: utf-8 -*-
__author__ = "wowo"


import datetime
import random
import os
import sys
import time
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
import pymysql

class Way():
    # mysql config
    def __init__(self):
        self.localhost = 'localhost'
        self.username = 'root'
        self.password = 'root'
        self.database = 'crm'
    # sql insert 
    def sql_insert(self,table,data):
        # mysql connect
        conn = pymysql.connect(self.localhost,self.username,self.password,self.database)
        cur = conn.cursor()
        try:
            # create table
            sql="create table %s(%s varchar(40) primary key)" % (table,'insert_date')
            cur.execute(sql)
            # for add col
            for i in data:
                sql="alter table %s add %s varchar(120)" % (table,i)  
                cur.execute(sql) 
        except:
            pass
        finally:
            now=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            for i,n in data.items():
                # date desc select first col data whether equal now_date
                sql="select insert_date from %s order by insert_date DESC limit 0,1" % (table)
                cur.execute(sql)
                x=cur.fetchall()
                # exist update data
                if x and str(x[0][0])==str(now):
                    sql="update %s set %s='%s' where insert_date='%s'" % (table,i,n,now)
                    cur.execute(sql)
                # inexistence insert data
                else:
                    sql="insert into %s(insert_date,%s) values('%s','%s')" % (table,i,now,n)
                    cur.execute(sql)
        cur.close()
        conn.commit()
        conn.close()

    # sql select 
    def sql_select(self,table):
        # mysql connect
        conn = pymysql.connect(self.localhost,self.username,self.password,self.database)
        cur = conn.cursor()
        data={}
        # date desc select first row
        sql="select * from %s order by insert_date DESC limit 0,1" % table
        cur.execute(sql)
        select_data=cur.fetchone()
        # pymysql select col_naame
        sql="select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s'" % table
        cur.execute(sql)
        row_name=cur.fetchall()
        for i in range(len(row_name)):
            # pymysql
            data['%s' % row_name[i][0]]=select_data[i]
        cur.close()
        conn.close()
        return data
        
    def sql_select_commodity_data(self,table):
        # mysql connect
        conn = pymysql.connect(self.localhost,self.username,self.password,self.database)
        cur = conn.cursor()
        data={}
        # select row sum
        sql="select count(*) from commodity_data"
        cur.execute(sql)
        select_sum_row=cur.fetchone()
        # random select one row
        sql="select * from %s limit %s,1" % (table,sum(random.sample(range(select_sum_row[0]),1)))
        cur.execute(sql)
        select_data=cur.fetchone()
        # pymysql select col_naame
        sql="select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s'" % table
        cur.execute(sql)
        row_name=cur.fetchall()
        for i in range(len(row_name)):
            # pymysql
            data['%s' % row_name[i][0]]=select_data[i]
        cur.close()
        conn.close()
        return data
    
    # response dispose to capitalize
    def response_dispose(self,dict_info):
        new_dict = {}
        for i, n in dict_info.items():
                new_dict[i.capitalize()] = n
        return new_dict



# localhost get html report 
class Report():  
    sys.path.append('./report')
    def get_new_report(self,file_path):
        dir_list = os.listdir(file_path)
        if not dir_list:
            return
        else:
            for i in dir_list:
                html_path ='./report/' + i 
                html_crate_time = time.localtime(os.stat(html_path).st_mtime)
                html_crate_time=time.strftime("%Y-%m-%d %H:%M", html_crate_time)
                nowtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                if html_crate_time == nowtime:
                    return html_path    
                else:
                    pass


# send html
class Smtp():
    def format_addr(self,x):
        name, addr = parseaddr(x)
        return formataddr((Header(name, 'utf-8').encode(), addr))
    def send_mail(self,local_file):
        user='503645047@qq.com'
        password='hufvhexcdiifbidg'
        user_to='823268279@qq.com'
        msg = MIMEMultipart()
        msg.attach(MIMEText('send with file...', 'plain', 'utf-8'))
        msg['From'] = Smtp().format_addr('徐铃纹 <%s>' % user)
        msg['To'] = Smtp().format_addr('管理员 <%s>' % user_to)
        msg['Subject'] = Header('来自测试部————徐……', 'utf-8').encode()
        att1 = MIMEText(open('%s' % local_file, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename= %s' %  local_file
        msg.attach(att1)
        stmp_server='smtp.qq.com'
        server=smtplib.SMTP(stmp_server,25)
        server.set_debuglevel(1)
        server.login(user,password)
        server.sendmail(user,[user_to],msg.as_string())
        server.quit()

