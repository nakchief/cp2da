import os,requests,subprocess

class Whm():

    def __init__(self,ip,port,username,passwd):
        self.username = username
        self.passwd = passwd
        self.ip = ip
        self.port = port
    
    # Do all fuctions of WHM API
    def query(self,cmd,paras=None):
        url = "https://%s:%s/json-api/%s?api.version=1" %(self.ip,self.port,cmd)
        if ( paras != None ):
            paras = paras.replace(",","%2C")
            url = url + paras
        r = requests.get(url, auth=(self.username,self.passwd),data=paras,verify=False)
        return r.json()

    # List accounts and their attributes
    def listAcct(self,paras=None):
        data = {}
        res = self.query("listaccts",paras)
        if 'data' in res :
            data = res["data"]["acct"]
        return data        
    # List all account name
    def listAll(self):
        data = self.query("list_users")["data"]["users"]
        return data

    # Check user
    def checkAcct(self,acct):
        if acct in self.listAll():
            return True
        else:
            return False                            
    
    def suspend(self,acct,reason=''):
        reason = "&user=%s&reason=%s" %(acct,reason)
        self.query("suspendacct",reason)
        return
    
    def unsuspend(self,acct):
        acct = "&user=%s" %acct
        self.query("unsuspendacct",acct)        
        return            
    # List all packages            
    def listPkg(self):
        data =  self.query("listpkgs")["data"]["pkg"]
        return data

    # List user databases
    def listUserDB(self,user):
        paras = "&user=" + user
        data = self.query("list_mysql_databases_and_users",paras)["data"]["mysql_databases"]
        return data
        



    # Get encrypted password in file /etc/shadow
    def getPass(user):    
        with open("/etc/shadow") as f:
            mylist = f.read().splitlines()    
            for j in mylist:
               secret = j.split(":")
               if user == secret[0]:
                   password = secret[1]
                   break    
        return password                

    def listDB(self):
        dbs = []
        data =  self.query("list_databases")["data"]["payload"]
        for db in data:
            dbs.append(db['name'])
        return dbs                

    # List all users in WHM.
    def listUsers():
        listuser = os.listdir("/var/cpanel/users")
        listuser.sort()
        return listuser

    def suspend_email(self,user):
        paras = "&user=" + user
        self.query("suspend_outgoing_email",paras)
        return

    def unsuspend_email(self,user):
        paras = "&user=" + user
        self.query("unsuspend_outgoing_email",paras)
        return
                
            

