'''

'''
import sqlite3
import os

def toDict(t):
    ''' t is a tuple (rowid,amount, category, month, day, year, description)'''
    print('t='+str(t))
    todo = {'rowid':t[0], 'amount':t[1], 'category':t[2], 'month':t[3], 'day':t[4], 'year':t[5], 'description':t[6]}
    return todo

class Transaction():
    def __init__(self):
        self.runQuery('''CREATE TABLE IF NOT EXISTS tracker
                    (amount int, category text, month int, day int, year, int description text)''',())
        #self.runQuery('''DROP TABLE IF EXISTS tracker''',())
    
    def showTransactions(self):
        ''' returns all transactions '''
        return self.runQuery("SELECT rowid,* from tracker",())
        
    def addTransaction(self,item):
        '''adds category'''
        return self.runQuery("INSERT INTO tracker VALUES(?,?,?,?,?,?)", (item['amount'], item['category'], item['month'], item['day'], item['year'], item['description']))
    
    def deleteTransaction(self,rowid):
        ''' delete a transaction '''
        return self.runQuery("DELETE FROM tracker WHERE rowid=(?)",(rowid,))
        
    def summarizeDate(self, month, day, year):
        return self.runQuery("SELECT rowid,* from tracker WHERE month=(?) AND day=(?) AND year=(?)",(month, day, year,))
    
    def summarizeMonth(self, month, year):
        return self.runQuery("SELECT rowid,* from tracker WHERE month=(?) AND year=(?)",(month,year,))
    
    def summarizeYear(self, year):
        return self.runQuery("SELECT rowid,* from tracker WHERE year=(?)",(year,))
    
    def summarizeCategory(self, category):
        return self.runQuery("SELECT rowid,* from tracker WHERE category=(?)",(category,))

    def runQuery(self,query,tuple):
        ''' return all of the uncompleted tasks as a list of dicts.'''
        con= sqlite3.connect(os.getenv('HOME')+'/todo.db')
        cur = con.cursor() 
        cur.execute(query,tuple)
        tuples = cur.fetchall()
        con.commit()
        con.close()
        return [toDict(t) for t in tuples]
    
