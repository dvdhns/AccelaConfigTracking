# ------------------------------------------------------------------------------
# AccelaConfigTracking
# ------------------------------------------------------------------------------
# start of user defined parms

#location of SQL and CSV files
path = "C:\\AccelaGit\\" #must end with \\

#the location of your git executable (git.exe)
gitExe = r"C:\prg\git.exe"

#the ODBC connection string, example is in SQL Server format with a database user
#example 'Driver={SQL Server};Server=mySqlServer;Database=myAccelaDatabase;Uid=myuser;Pwd=mypassword;'
connectString = 'Driver={SQL Server};Server=mySqlServer;Database=myAccelaDatabase;Uid=myuser;Pwd=mypassword;'

# end of user defined parms
# ------------------------------------------------------------------------------

import sys, os, fnmatch
import subprocess
import pypyodbc #https://code.google.com/p/pypyodbc/


def main():
    #get the list of table names and SQL Queries
    tableList = getTableList();

    #read through the table list and create the CSV and commit it to the Git Repo
    for table in tableList:
        #export the CSV file
        exportTable(table[0],table[1])

        #use git to commit changes
        doGit( table[0])

# ------------------------------------------------------------------------------

def exportTable(tableName,tableSql):
    print tableName
    #print tableSql + "\n"
    try:
        # create the csv file
        f = open(path + tableName + '.csv','w')

        # get a connection to MSSQL ODBC DSN via pypyodbc, and assign it to conn
        conn = pypyodbc.connect( connectString )

        # Give me a cursor so I can operate the database with the cursor
        cur = conn.cursor()
        # run the SQL
        cur.execute(tableSql + ';') #just add a ; at the end just in case
        # get just the field names
        header = ''
        skipColumnList = []
        for d in cur.description:
            if cur.description.index(d) not in skipColumnList:
                header = header + '"' + d[0] + '",' #add quotes around each field and add comma after name
        header = header[:-1] #get rid of last comma
        header = header + "\n" #new line
        #write the field names to the CSV
        f.write(header)

        #go through each row of the SQL result and  write to file
        for row in cur.fetchall():
            line = ''
            for field in row:
                line = line+ '"' + str(field) + '",' #add quotes around each field and add comma after name
            line = line[:-1] #get rid of last comma
            line = line + '\n' #new line
            #write the row to the CSV
            f.write(line)
        f.close() #close the CSV
        # Close the cursor and connection
        cur.close()
        conn.close()
    except Exception,e:
        print "ERROR: " + tableName
        print str(e)
        print '\n'


def doGit( myCsv ):
    #make the command to add the csv file to the repo
    cmd = [gitExe, "add", myCsv  + ".csv" ]
    #run the command
    p = subprocess.call(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    #make the command to commit the csv file to the repo
    cmd = [gitExe, "commit", "-m", "Changes to " + myCsv ]
    #run the command
    p = subprocess.call(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

def getTableList():
    # returns the table list in the format of:
    # [ [ NameOfCsvFileToCreate1 , SqlQuery1 ] , [ NameOfCsvFileToCreate2 , SqlQuery2 ] , etc... ]
    tableList = [] #define the list
    sqlFileList = fileList("*.sql", path)
    for sqlFile in sqlFileList:
        #read the file
        f = open(sqlFile, 'r')
        sqlText = f.read()
        #get the name of the file with no extension
        baseFile= os.path.basename(sqlFile)
        fileName = os.path.splitext(baseFile)[0]
        #append to the table list
        tableList.append( [fileName, sqlText ])
    return tableList

def fileList(pattern, root):
    '''Locate all files matching supplied filename pattern in and below
    supplied root directory.'''
    ps = []
    i = 0;
    for path, dirs, files in os.walk(os.path.abspath(root)):
        i += 1
        for filename in fnmatch.filter(files, pattern):
            #yield os.path.join(path, filename)
            ps.append(os.path.join(path, filename))
    return ps


if __name__ == '__main__':
    main()
