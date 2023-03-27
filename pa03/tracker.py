'''
todo2 is an app that maintains a todo list
just as with the todo code in this folder.

but it also uses an Object Relational Mapping (ORM)
to abstract out the database operations from the
UI/UX code.

The ORM, TodoList, will map SQL rows with the schema
    (rowid,title,desc,completed)
to Python Dictionaries as follows:

(5,'commute','drive to work',false) <-->

{rowid:5,
 title:'commute',
 desc:'drive to work',
 completed:false)
 }

In place of SQL queries, we will have method calls.

This app will store the data in a SQLite database ~/todo.db

Recall that sys.argv is a list of strings capturing the
command line invocation of this program
sys.argv[0] is the name of the script invoked from the shell
sys.argv[1:] is the rest of the arguments (after arg expansion!)

Note the actual implementation of the ORM is hidden and so it 
could be replaced with PostgreSQL or Pandas or straight python lists

'''

from transaction import Transaction
import sys


# here are some helper functions ...

def print_usage():
    ''' print an explanation of how to use this command '''
    print('''usage:
            tracker quit
            tracker show
            tracker add amount category date description
            tracker delete item_id
            tracker summarizeDate month day year
            tracker summarizeMonth month year
            tracker summarizeYear year
            tracker summarizeCategory category
            '''
            )

def print_transactions(transactions):
    ''' print the todo items '''
    if len(transactions)==0:
        print('no transactions to print')
        return
    print('\n')
    print("%-10s %-10s %-10s %-10s %-10s %-10s %-10s"%('item #','amount','category','month', 'day', 'year', 'desc'))
    print('-'*70)
    for item in transactions:
        values = tuple(item.values()) #(rowid,amount,category,month,day,year,desc)
        print("%-10s %-10s %-10s %-10s %-10s %-10s %-10s"%values)

def process_args(arglist):
    ''' examine args and make appropriate calls to TodoList'''
    transactions = Transaction()
    if arglist==[]:
        print_usage()
    elif arglist[0]=="show":
        print_transactions(transactions.showTransactions())
    elif arglist[0]=='add':
        if len(arglist)!=7:
            print(arglist)
            print_usage()
        else:
            transaction = {'amount':arglist[1],'category':arglist[2],'month':arglist[3],'day':arglist[4],'year':arglist[5],'description':arglist[6]}
            transactions.addTransaction(transaction)
    elif arglist[0]=='delete':
        if len(arglist)!= 2:
            print_usage()
        else:
            transactions.deleteTransaction(arglist[1])
    elif arglist[0]=='summarizeDate':
        print_transactions(transactions.summarizeDate(arglist[1],arglist[2],arglist[3]))
    elif arglist[0]=='summarizeMonth':
        print_transactions(transactions.summarizeMonth(arglist[1],arglist[2]))
    elif arglist[0]=='summarizeYear':
        print_transactions(transactions.summarizeYear(arglist[1]))
    elif arglist[0]=='summarizeCategory':
        print_transactions(transactions.summarizeCategory(arglist[1]))
    else:
        print(arglist,"is not implemented")
        print_usage()


def toplevel():
    ''' read the command args and process them'''
    if len(sys.argv)==1:
        # they didn't pass any arguments, 
        # so prompt for them in a loop
        print_usage()
        args = []
        while args!=['']:
            args = input("command> ").split(' ')
            if args[0]=='quit':
                break
            #if args[0]=='add':
                # join everyting after the name as a string
                #args = ['add',args[1]," ".join(args[2:])]
            process_args(args)
            print('-'*70+'\n'*3)
    else:
        # read the args and process them
        args = sys.argv[1:]
        process_args(args)
        print('-'*70+'\n'*3)

    
toplevel()

