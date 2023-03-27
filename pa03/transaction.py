'''

'''
import sqlite3
import os

def toDict(t):
    ''' t is a tuple (rowid,amount, category, date, description)'''
    print('t='+str(t))
    todo = {'rowid':t[0], 'amount':t[1], 'category':t[2], 'date':t[3], 'description':t[4]}
    return todo

class Transaction():
    def __init__(self):
        self.runQuery('''CREATE TABLE IF NOT EXISTS tracker
                    (amount int, category text, date text, description text)''',())
    
    def quit(self):
        return None
    
    def showTransactions(self):
        ''' returns all transactions '''
        return self.runQuery("SELECT rowid,* from tracker",())
        
    def addTransaction(self,item):
        '''adds category'''
        return self.runQuery("INSERT INTO tracker VALUES(?,?,?,?)", (item['amount'], item['category'], item['date'], item['description']))
    
    def deleteTransaction(self,rowid):
        ''' delete a transaction '''
        return self.runQuery("DELETE FROM tracker WHERE rowid=(?)",(rowid,))
        
    def summarizeDate(self, month, day, year):
        return self.runQuery("SELECT rowid,* from tracker WHERE date=(?)",(month +'/'+day+'/'+year))
    
    def summarizeMonth(self, month, year):
        return self.runQuery("SELECT rowid,* from tracker WHERE date LIKE '(?)%(?)'",(month,year))
    
    def summarizeYear(self, year):
        return self.runQuery("SELECT rowid,* from tracker WHERE date LIKE '%(?)'",(year))
    
    def summarizeCategory(self, category):
        return self.runQuery("SELECT rowrid,* from tracker WHERE category=(?)",(category))

    def runQuery(self,query,tuple):
        ''' return all of the uncompleted tasks as a list of dicts.'''
        con= sqlite3.connect(os.getenv('HOME')+'/todo.db')
        cur = con.cursor() 
        cur.execute(query,tuple)
        tuples = cur.fetchall()
        con.commit()
        con.close()
        return [toDict(t) for t in tuples]
    
    # def selectActive(self):
    #     ''' return all of the uncompleted tasks as a list of dicts.'''
    #     return self.runQuery("SELECT rowid,* from todo where completed=0",())

    # def selectAll(self):
    #     ''' return all of the tasks as a list of dicts.'''
    #     return self.runQuery("SELECT rowid,* from todo",())

    # def selectCompleted(self):
    #     ''' return all of the completed tasks as a list of dicts.'''
    #     return self.runQuery("SELECT rowid,* from todo where completed=1",())

    # def add(self,item):
    #     ''' create a todo item and add it to the todo table '''
    #     return self.runQuery("INSERT INTO todo VALUES(?,?,?)",(item['title'],item['desc'],item['completed']))

    # def delete(self,rowid):
    #     ''' delete a todo item '''
    #     return self.runQuery("DELETE FROM todo WHERE rowid=(?)",(rowid,))

    # def setComplete(self,rowid):
    #     ''' mark a todo item as completed '''
    #     return self.runQuery("UPDATE todo SET completed=1 WHERE rowid=(?)",(rowid,))

