#!/usr/bin/python
#-*- coding:utf-8 -*-
__author__ = 'LanChorY'
import sys
import json
import time
import urllib
import httplib
import subprocess
 
reqUrl1 = '/Record.Modify'
params1 = dict(
    login_email="mail@yanxiaoyi.com", # replace with your email
    login_password="password", # replace with your password
    format="json",
    domain_id=000000, # replace with your domain_od, can get it by API Domain.List
    record_id=1111111, # replace with your record_id, can get it by API Record.List
    sub_domain="server1", # replace with your sub_domain
    record_type="A",
    record_line="默认",
)
 
reqUrl2 = '/Record.List'
params2 = dict(
    login_email="", # replace with your email
    login_password="", # replace with your password
    format="json",
    domain_id=, # replace with your domain_od, can get it by API Domain.List
    record_line="默认",
)
 
def getRecord(params, requrl, servername):
    #if not ip.strip():
    #    params.update(dict(value=ip))
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}
    conn = httplib.HTTPSConnection('dnsapi.cn')
    conn.request("POST", requrl, urllib.urlencode(params), headers)
    response = conn.getresponse()
    data = response.read()
    s = json.loads(data)
    list = s["records"]
    for i in list:
        if i[u'name'] == servername:
            remote_ip = i['value']
            print '''[remoteip]:  %s''' %(remote_ip)
    conn.close()
    return remote_ip
 
def modifyRecord(ip='', params='', requrl=''):
    if ip.strip():
        params.update(dict(value=ip))
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}
    conn = httplib.HTTPSConnection('dnsapi.cn')
    conn.request("POST", requrl, urllib.urlencode(params), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
 
def getLocalIp(iframe):
    ipaddr = ''' ifconfig %s |grep "inet\\b" |awk  -F'[ :]+' '{print $4}' ''' % (iframe)   #很笨的获取本机IP的方法，我觉得socket更好...
    p = subprocess.Popen(ipaddr, shell=True, stdout=subprocess.PIPE)
    local_ip = p.stdout.read().strip()
    print '''[localip]:   %s''' %(local_ip)
    return local_ip
 
def checkIp():
    remote_ip=getRecord(params2, reqUrl2, "server1")
    if local_ip == remote_ip:
        print "everything is ok"
        sys.exit(0)
    if remote_ip != local_ip:
        modifyRecord(local_ip, params1, reqUrl1)
        getRecord(params2, reqUrl2, "server1")
 
if __name__ == '__main__':
    times = 0
    while times <= 2:
        local_ip=getLocalIp("eth0")
        checkIp()
        time.sleep(2)
        times += 1
