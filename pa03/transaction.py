'''

'''
import sqlite3
import os

def toDict(t):
    ''' t is a tuple (rowid,title, desc,completed)'''
    print('t='+str(t))
    todo = {'rowid':t[0], 'title':t[1], 'desc':t[2], 'completed':t[3]}
    return todo

class TodoList():
    def __init__(self):
        self.runQuery('''CREATE TABLE IF NOT EXISTS tracker
                    (amount int, category text, date text, description text)''',())
    
    
    def quit(self):
        return null
    
    def showTransactions():
        ''' returns all transactions '''
        return self.runQuery("SELECT rowid,* from todo")
        
    def addTransaction(self,item):
        '''adds category'''
        return self.runQuery("INSERT INTO tracker VALUES(?,?,?,?)", (item['amount'], item['category'], item['date'], item['description']))
    
    def deleteTransaction(self,rowid):
        ''' delete a transaction '''
        return self.runQuery("DELETE FROM transaction WHERE rowid=(?)",(rowid,))
        
    def summarizeDate(self):
        return null
    
    def summarizeMonth(self):
        return null
    
    def summarizeYear(self):
        return null
    
    def summarizeCategory(self):
        return null

    
    
    def selectActive(self):
        ''' return all of the uncompleted tasks as a list of dicts.'''
        return self.runQuery("SELECT rowid,* from todo where completed=0",())

    def selectAll(self):
        ''' return all of the tasks as a list of dicts.'''
        return self.runQuery("SELECT rowid,* from todo",())

    def selectCompleted(self):
        ''' return all of the completed tasks as a list of dicts.'''
        return self.runQuery("SELECT rowid,* from todo where completed=1",())

    def add(self,item):
        ''' create a todo item and add it to the todo table '''
        return self.runQuery("INSERT INTO todo VALUES(?,?,?)",(item['title'],item['desc'],item['completed']))

    def delete(self,rowid):
        ''' delete a todo item '''
        return self.runQuery("DELETE FROM todo WHERE rowid=(?)",(rowid,))

    def setComplete(self,rowid):
        ''' mark a todo item as completed '''
        return self.runQuery("UPDATE todo SET completed=1 WHERE rowid=(?)",(rowid,))

    def runQuery(self,query,tuple):
        ''' return all of the uncompleted tasks as a list of dicts.'''
        con= sqlite3.connect(os.getenv('HOME')+'/todo.db')
        cur = con.cursor() 
        cur.execute(query,tuple)
        tuples = cur.fetchall()
        con.commit()
        con.close()
        return [toDict(t) for t in tuples]