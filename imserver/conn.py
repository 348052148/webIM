import sqlite3
class conn(object):
    def __init__(self,url):
        self.con=sqlite3.connect(url)
    def query(self,sql):
        try:
            cursor=self.con.execute(sql)
            self.con.commit()
        except:
            print('db excpt')
            return False
        print('cumm')
        return cursor
