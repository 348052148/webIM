import conn
class userInfo(object):
    def __init__(self,name,uid,gid,stat,friends,conn):
        self.name=name
        self.uid=uid
        self.gid=gid
        self.stat=stat
        self.conn=conn
        self.friend=friends
    def say(self):
        pass
class utils(object):
    def __init__(self):
        pass

class User(object):
    def __init__(self):
        self.conn=conn.conn('test.db')
    def find(self,name):
        cursor=self.conn.query('select * from user where name="'+name+'" and stat!=1')
        if cursor is False:
            return False
        for row in cursor:
            self.uid=row[0]
            self.name=row[1]
            self.pw=row[2]
            self.fid=row[3]
            self.eid=row[4]
            self.stat=row[5]
            self.avater=row[6]
            print(self.pw)
            return True
        return False
    def updateUserStat(self,stat):
        cursor=self.conn.query('update user set stat='+str(stat)+' where uid='+str(self.uid))
        if cursor is False:
            return False
        return True
    def getFriends(self):
        friends=list()
        cursor=self.conn.query('select fname,uid,avater from friend where fid='+str(self.fid))
        print('select fname,uid from friend where fid'+str(self.fid))
        if cursor is False:
            return False
        for row in cursor:
            doc={'name':row[0],'uid':row[1],'avater':row[2]}
            friends.append(doc)
        return friends
    def register(self):
        pass
    def searchFriend(self,name):
        friends=list()
        cursor=self.conn.query('select name,uid,avater from user where name="'+name+'"')
        if cursor is False:
            return False
        for row in cursor:
            doc={'name':row[0],'uid':row[1],'avater':row[2]}
            friends.append(doc)
        return friends
    def addFriend(self,uid,name):
        print('insert into friend (fid,fname,uid) values('+str(self.fid)+',"'+name+'",'+uid+')')
        if int(uid) == int(self.uid):
            return {'stat':'3'}
        cor=self.conn.query('select count(*) from friend where fname="'+name+'" and uid='+uid+" and fid="+str(self.fid))
        print('添加好友'+'select count(*) from friend where fname="'+name+'" and uid='+uid+" and fid="+str(self.fid))
        for row in cor:
            count=row[0]
        print(count)
        if count > 0:
            return {'stat':'1'}
        cor=self.conn.query('select avater from user where uid='+uid)
        for row in cor:
            cursor=self.conn.query('insert into friend (fid,fname,uid,avater) values('+str(self.fid)+',"'+name+'",'+uid+',"'+row[0]+'")')
            avater=row[0]
        if cursor is False:
            return {'stat':'2'}
        return {'stat':'0','uid':uid,'name':name,'avater':avater}


