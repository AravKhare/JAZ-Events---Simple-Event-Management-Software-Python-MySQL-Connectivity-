import mysql.connector as msc

# Global Database Configuration
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWD = "" # Password is no longer hardcoded
DB_NAME = "JAZ" 

#-----------------------|CREATING THE DATABASE & TABLES|---------------------------------
# We consolidate the setup into a single connection block inside a function 
# so we can validate the user's password before proceeding.

def initialize_database():
    global DB_PASSWD
    try:
        # Connect to MySQL Server (without specifying DB yet)
        db = msc.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD)
        cur = db.cursor()
        
        # Safely create database if it doesn't already exist
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        
        # Switch to the target database
        cur.execute(f"USE {DB_NAME}")
        
        # Create the EMPLOYEE table
        cur.execute("""CREATE TABLE IF NOT EXISTS EMPLOYEE (
                       ID INT(3) PRIMARY KEY,
                       NAME VARCHAR(25) NOT NULL,
                       GENDER CHAR(1),
                       EMAIL VARCHAR(50),
                       MOB VARCHAR(10),
                       DOB date)""")

        # Create the EVENTS table
        cur.execute("""CREATE TABLE IF NOT EXISTS EVENTS (
                       ID INT(5) PRIMARY KEY,
                       EVENTNAME VARCHAR(25) NOT NULL,
                       CLIENTID INT(5),
                       BUDGET INT,
                       TOTALCOST INT,
                       VENUE VARCHAR(25),
                       DATE date,
                       CITY VARCHAR(25),
                       STATE VARCHAR(25),
                       EMPLOYEEID INT(3))""")

        # Create the CLIENTS table
        cur.execute("""CREATE TABLE IF NOT EXISTS CLIENTS (
                       ID INT(5) PRIMARY KEY,
                       NAME VARCHAR(25) NOT NULL,
                       GENDER CHAR(1),
                       EMAIL VARCHAR(50),
                       MOB VARCHAR(10),
                       DOB date,
                       PAYMENTSTATUS INT(1))""")
        
        # Commit changes
        db.commit()
        return True

    except msc.Error as err:
        print(f"Error during database/table setup or incorrect password: {err}")
        return False
    finally:
        # Safely close connection after setup
        if 'db' in locals() and db.is_connected():
            cur.close()
            db.close()

#----------------------------|EMPLOYEE FUNCTIONS|---------------------------------

def Employee_Insert():
    try:
        # Establish connection for this operation
        mydb = msc.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)
        mycur = mydb.cursor()
    except Exception as e:
        print("Error connecting to database: ", e)
        return

    try:
        # Validate Employee ID
        while True:
            try:
                Id = int(input("Enter Employee ID (1-999): "))
                if 0 < Id < 1000:
                    mycur.execute("SELECT ID FROM EMPLOYEE WHERE ID = %s", (Id,))
                    if mycur.fetchone():
                        print(f"Error: Employee ID {Id} already exists.")
                    else:
                        break
                else:
                    print("Please Enter a valid ID! (1-999)")
            except ValueError:
                print("Please enter a numeric ID.")

        Name = input("Enter Employee Name: ").strip().upper()

        # Validate Gender
        while True:
            Gender = input("Enter Gender (M/F): ").strip().upper()
            if Gender in ["M", "F"]:
                break
            else:
                print("Please input valid value (M/F)")

        Email = input("Enter Employee Email: ").strip().lower()

        # Validate Mobile Number
        while True:
            Mob = input("Enter Employee Mob (10 digits): ")
            if len(Mob) == 10 and Mob.isdigit():
                break
            else:
                print("Invalid mobile number! Must be numerical and exactly 10 digits.")

        # Validate Date of Birth
        while True:
            DOB = input("Enter Employee DOB ('YYYY-MM-DD'): ").strip()
            if len(DOB) == 10 and DOB[4] in ["-", "/"] and DOB[7] in ["-", "/"]:
                year, month, day = DOB[:4], DOB[5:7], DOB[8:]
                if (year.isdigit() and month.isdigit() and day.isdigit() and
                    1 <= int(month) <= 12 and
                    1 <= int(day) <= 31 and
                    1964 < int(year) < 2011):
                    DOB = DOB.replace('/', '-') # Standardize for MySQL
                    break
                else:
                    print("Invalid DOB, please try again.")
            else:
                print("Incorrect format of Date, please follow 'YYYY-MM-DD'.")

        # Execute Insert Query
        Data = (Id, Name, Gender, Email, Mob, DOB)
        Query = "INSERT INTO EMPLOYEE (ID, NAME, GENDER, EMAIL, MOB, DOB) VALUES (%s, %s, %s, %s, %s, %s)"
        
        mycur.execute(Query, Data)
        mydb.commit()
        print("\nRecord inserted successfully!")

    except Exception as e:
        print("Unexpected error:", e)

    finally:
        # Safely clean up resources
        if 'mycur' in locals(): mycur.close()
        if 'mydb' in locals() and mydb.is_connected(): mydb.close()

def Employee_Search():
    try:
        mydb = msc.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)
        mycur = mydb.cursor()
    except Exception as e:
        print("Error connecting to database: ", e)
        return

    try:
        print("\n-- Employee Search Menu --")
        print("  1: Search by Name")
        print("  2: Search by ID")
        print("  3: Return")
        
        ch = input("  Enter Choice: ").strip()

        if ch == '1':
            Name = input("Enter Employee Name to search: ").strip()
            Query = "SELECT * FROM EMPLOYEE WHERE NAME = %s"
            mycur.execute(Query, (Name,))
            results = mycur.fetchall()

            if not results:
                print("No record found with Name:", Name)
            else:
                print(f"Found {len(results)} record(s):\n")
                for result in results:
                    print("-------------| Employee Record |-------------- ")
                    print(f"Employee ID      : {result[0]}")
                    print(f"Employee Name    : {result[1]}")
                    print(f"Gender           : {result[2]}")
                    print(f"Email            : {result[3]}")
                    print(f"Mobile Number    : {result[4]}")
                    print(f"Date of Birth    : {result[5]}")
                    print("------------------------------------------------ \n")

        elif ch == '2':
            try:
                Id = int(input("Enter Employee ID to search: "))
                Query = "SELECT * FROM EMPLOYEE WHERE ID = %s"
                mycur.execute(Query, (Id,))
                result = mycur.fetchone()

                if result:
                    print("\nEmployee Record Found!")
                    print("-------------| Employee Record |-------------- ")
                    print(f"Employee ID      : {result[0]}")
                    print(f"Employee Name    : {result[1]}")
                    print(f"Gender           : {result[2]}")
                    print(f"Email            : {result[3]}")
                    print(f"Mobile Number    : {result[4]}")
                    print(f"Date of Birth    : {result[5]}")
                    print("------------------------------------------------ ")
                else:
                    print(f"No record found with Employee ID: {Id}")
            except ValueError:
                print("Please enter a valid numeric Employee ID.")
        
        elif ch == '3':
            return
        else:
            print("Invalid choice.")

    except Exception as e:
        print("Unexpected error: ", e)

    finally:
        if 'mycur' in locals(): mycur.close()
        if 'mydb' in locals() and mydb.is_connected(): mydb.close()

def Employee_Update():
    try:
        mydb = msc.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)
        mycur = mydb.cursor()
    except Exception as e:
        print("Error connecting to database: ", e)
        return

    try:
        try:
            Id = int(input("Enter Employee ID to update: "))
        except ValueError:
            print("Please enter a valid numeric Employee ID.")
            return

        # Fetch existing record to display current values
        Query_Search = "SELECT * FROM EMPLOYEE WHERE ID = %s"
        mycur.execute(Query_Search, (Id,))
        result = mycur.fetchone()

        if not result:
            print(f"No record found with Employee ID: {Id}")
            return

        print("\n----------| Current Employee Record |----------")
        print(f"Employee ID      : {result[0]}")
        print(f"Employee Name    : {result[1]}")
        print(f"Gender           : {result[2]}")
        print(f"Email            : {result[3]}")
        print(f"Mobile Number    : {result[4]}")
        print(f"Date of Birth    : {result[5]}")
        print("---------------------------------------------")
        print("Enter new details (leave blank to keep old value):")

        # Collect new inputs, defaulting to old values if left blank
        New_Name = input("Enter New Name: ").strip()
        if New_Name == "": New_Name = result[1]

        while True:
            New_Gender = input("Enter New Gender (M/F): ").strip().upper()
            if New_Gender == "":
                New_Gender = result[2]
                break
            elif New_Gender in ["M", "F"]:
                break
            else:
                print("Please input valid value (M/F)")

        New_Email = input("Enter New Email: ").strip().lower()
        if New_Email == "": New_Email = result[3]

        while True:
            New_Mob = input("Enter New Mobile (10 digits): ").strip()
            if New_Mob == "":
                New_Mob = result[4]
                break
            elif len(New_Mob) == 10 and New_Mob.isdigit():
                break
            else:
                print("Invalid mobile number! Must be exactly 10 digits.")

        while True:
            New_DOB = input("Enter New DOB ('YYYY-MM-DD'): ").strip()
            if New_DOB == "":
                New_DOB = result[5]
                break
            elif len(New_DOB) == 10 and New_DOB[4] in ["-", "/"] and New_DOB[7] in ["-", "/"]:
                year, month, day = New_DOB[:4], New_DOB[5:7], New_DOB[8:]
                if (year.isdigit() and month.isdigit() and day.isdigit() and
                    1 <= int(month) <= 12 and 1 <= int(day) <= 31 and
                    1964 < int(year) < 2011):
                    New_DOB = New_DOB.replace('/', '-')
                    break
                else:
                    print("Invalid DOB, please try again.")
            else:
                print("Incorrect format of Date, please follow 'YYYY-MM-DD'.")
                
        # Perform Update
        Query_Update = """UPDATE EMPLOYEE SET 
                          NAME=%s, GENDER=%s, EMAIL=%s, MOB=%s, DOB=%s 
                          WHERE ID=%s"""
        Data = (New_Name, New_Gender, New_Email, New_Mob, New_DOB, Id)

        mycur.execute(Query_Update, Data)
        mydb.commit()
        print("\nRecord updated successfully!")

    except Exception as e:
        print("Unexpected error: ", e)

    finally:
        if 'mycur' in locals(): mycur.close()
        if 'mydb' in locals() and mydb.is_connected(): mydb.close()

def Employee_Delete():
    try:
        mydb = msc.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)
        mycur = mydb.cursor()
    except Exception as e:
        print("Error connecting to database: ", e)
        return

    try:
        try:
            Id = int(input("Enter Employee ID to delete: "))
        except ValueError:
            print("Please enter a valid numeric Employee ID.")
            return
            
        # Prevent deletion if the employee is assigned to an event
        mycur.execute("SELECT ID FROM EVENTS WHERE EMPLOYEEID = %s", (Id,))
        if mycur.fetchone():
            print(f"\nError: Cannot delete Employee ID {Id}. They are managing one or more events.")
            print("Please re-assign events before deleting this employee.")
            return

        Query_Search = "SELECT * FROM EMPLOYEE WHERE ID = %s"
        mycur.execute(Query_Search, (Id,))
        result = mycur.fetchone()

        if not result:
            print(f"No record found with Employee ID: {Id}")
            return

        print("\n----------| Employee Record to Delete |---------- ")
        print(f"Employee ID      : {result[0]}")
        print(f"Employee Name    : {result[1]}")
        print(f"Gender           : {result[2]}")
        print(f"Email            : {result[3]}")
        print(f"Mobile Number    : {result[4]}")
        print(f"Date of Birth    : {result[5]}")
        print("---------------------------------------------")

        confirm = input("Are you sure you want to delete this record? (Y/N): ").strip().upper()
        if confirm == "Y":
            Query_Delete = "DELETE FROM EMPLOYEE WHERE ID = %s"
            mycur.execute(Query_Delete, (Id,))
            mydb.commit()
            print("Record deleted successfully!")
        else:
            print("Deletion cancelled.")

    except Exception as e:
        print("Unexpected error:", e)

    finally:
        if 'mycur' in locals(): mycur.close()
        if 'mydb' in locals() and mydb.is_connected(): mydb.close()

#----------------------------|EVENT FUNCTIONS|---------------------------------

def Event_Insert():
    try:
        mydb = msc.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)
        mycur = mydb.cursor()
    except Exception as e:
        print("Error connecting to database: ", e)
        return
        
    try:
        while True:
            try:
                Id = int(input("Enter Event ID (1-99999): "))
                if 0 < Id < 100000:
                    mycur.execute("SELECT ID FROM EVENTS WHERE ID = %s", (Id,))
                    if mycur.fetchone():
                        print(f"Error: Event ID {Id} already exists.")
                    else:
                        break
                else:
                    print("Please enter a valid 1-5 digit positive ID.")
            except ValueError:
                print("Please enter a numeric Event ID.")

        EventName = input("Enter Event Name: ").strip()
        
        # Validating Client ID with a fallback choice menu
        client_validated = False
        while not client_validated:
            try:
                ClientID = int(input("Enter Client ID (1-99999): "))
                if 0 < ClientID < 100000:
                    mycur.execute("SELECT ID FROM CLIENTS WHERE ID = %s", (ClientID,))
                    if mycur.fetchone():
                        client_validated = True
                    else:
                        print(f"\nError: Client ID {ClientID} not found.")
                        print("1: Try entering Client ID again")
                        print("2: Cancel & Return to Menu (Go define a new client first)")
                        opt = input("Enter choice (1/2): ").strip()
                        if opt == '2':
                            print("Returning to Event Menu...")
                            return # Exits the Event_Insert function safely
                else:
                    print("Please enter a valid 1-5 digit positive ID.")
            except ValueError:
                print("Please enter a numeric Client ID.")

        while True:
            try:
                Budget = int(input("Enter Budget (Revenue): "))
                if Budget >= 0: break
                else: print("Budget cannot be negative.")
            except ValueError:
                print("Please enter a numeric value for Budget.")

        while True:
            try:
                TotalCost = int(input("Enter Total Cost (Expense): "))
                if TotalCost >= 0: break
                else: print("Cost cannot be negative.")
            except ValueError:
                print("Please enter a numeric value for Cost.")

        Venue = input("Enter Venue: ").strip()

        while True:
            Date = input("Enter Event Date ('YYYY-MM-DD'): ").strip()
            if len(Date) == 10 and Date[4] in ["-", "/"] and Date[7] in ["-", "/"]:
                year, month, day = Date[:4], Date[5:7], Date[8:]
                if (year.isdigit() and month.isdigit() and day.isdigit() and
                    1 <= int(month) <= 12 and 1 <= int(day) <= 31):
                    Date = Date.replace('/', '-')
                    break
                else:
                    print("Invalid date! Please check year, month, day values.")
            else:
                print("Incorrect format! Use 'YYYY-MM-DD'.")

        City = input("Enter City: ").strip()
        State = input("Enter State: ").strip()

        # Validating Employee ID with a fallback choice menu
        employee_validated = False
        while not employee_validated:
            try:
                EmployeeID = int(input("Enter assigned Employee ID (1-999): "))
                if 0 < EmployeeID < 1000:
                    mycur.execute("SELECT ID FROM EMPLOYEE WHERE ID = %s", (EmployeeID,))
                    if mycur.fetchone():
                        employee_validated = True
                    else:
                        print(f"\nError: Employee ID {EmployeeID} not found.")
                        print("1: Try entering Employee ID again")
                        print("2: Cancel & Return to Menu (Go define a new employee first)")
                        opt = input("Enter choice (1/2): ").strip()
                        if opt == '2':
                            print("Returning to Event Menu...")
                            return # Exits the Event_Insert function safely
                else:
                    print("Please enter a valid 1-3 digit positive ID.")
            except ValueError:
                print("Please enter a numeric Employee ID.")
        
        Data = (Id, EventName, ClientID, Budget, TotalCost, Venue, Date, City, State, EmployeeID)
        Query = "INSERT INTO EVENTS (ID, EVENTNAME, CLIENTID, BUDGET, TOTALCOST, VENUE, DATE, CITY, STATE, EMPLOYEEID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        mycur.execute(Query, Data)
        mydb.commit()
        print("\nEvent record inserted successfully!")

    except Exception as e:
        print("Unexpected error:", e)
    finally:
        if 'mycur' in locals(): mycur.close()
        if 'mydb' in locals() and mydb.is_connected(): mydb.close()

def Event_Search():
    try:
        mydb = msc.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)
        mycur = mydb.cursor()
    except Exception as e:
        print("Error connecting to database: ", e)
        return

    try:
        print("\n-- Event Search Menu --")
        print("  1: Search by Event Name")
        print("  2: Search by Event ID")
        print("  3: Search by Manager (Employee ID)")
        print("  4: Return")
        
        ch = input("  Enter Choice: ").strip()

        if ch == '1':
            Name = input("Enter Event Name to search: ").strip()
            # Fetch with SQL JOIN to get Client details
            Query = """SELECT E.ID, E.EVENTNAME, E.CLIENTID, C.NAME, C.MOB, C.EMAIL, 
                          E.BUDGET, E.TOTALCOST, E.VENUE, E.DATE, E.CITY, E.STATE, E.EMPLOYEEID 
                       FROM EVENTS E 
                       JOIN CLIENTS C ON E.CLIENTID = C.ID 
                       WHERE E.EVENTNAME = %s"""
            mycur.execute(Query, (Name,))
            results = mycur.fetchall()
            
            if not results:
                print(f"No record found with Event Name: {Name}")
            else:
                print(f"Found {len(results)} record(s):\n")
                for result in results:
                    print("-----------| Event Record |----------- ")
                    print(f"Event ID       : {result[0]}")
                    print(f"Event Name     : {result[1]}")
                    print(f"Client ID      : {result[2]}")
                    print(f"Client Name    : {result[3]}")
                    print(f"Client Mobile  : {result[4]}")
                    print(f"Client Email   : {result[5]}")
                    print(f"Budget         : {result[6]}")
                    print(f"Total Cost     : {result[7]}")
                    print(f"Venue          : {result[8]}")
                    print(f"Event Date     : {result[9]}")
                    print(f"City           : {result[10]}")
                    print(f"State          : {result[11]}")
                    print(f"Manager ID     : {result[12]}")
                    print("--------------------------------------\n")
        
        elif ch == '2':
            try:
                Id = int(input("Enter Event ID to search: "))
                Query = """SELECT E.ID, E.EVENTNAME, E.CLIENTID, C.NAME, C.MOB, C.EMAIL,
                              E.BUDGET, E.TOTALCOST, E.VENUE, E.DATE, E.CITY, E.STATE, E.EMPLOYEEID 
                           FROM EVENTS E 
                           JOIN CLIENTS C ON E.CLIENTID = C.ID 
                           WHERE E.ID = %s"""
                mycur.execute(Query, (Id,))
                result = mycur.fetchone()
                
                if result:
                    print("\nEvent Record Found!")
                    print("-----------| Event Record |----------- ")
                    print(f"Event ID       : {result[0]}")
                    print(f"Event Name     : {result[1]}")
                    print(f"Client ID      : {result[2]}")
                    print(f"Client Name    : {result[3]}")
                    print(f"Client Mobile  : {result[4]}")
                    print(f"Client Email   : {result[5]}")
                    print(f"Budget         : {result[6]}")
                    print(f"Total Cost     : {result[7]}")
                    print(f"Venue          : {result[8]}")
                    print(f"Event Date     : {result[9]}")
                    print(f"City           : {result[10]}")
                    print(f"State          : {result[11]}")
                    print(f"Manager ID     : {result[12]}")
                    print("--------------------------------------")
                else:
                    print(f"No record found with Event ID: {Id}")
            except ValueError:
                print("Please enter a valid numeric Event ID.")

        elif ch == '3':
            try:
                Id = int(input("Enter Employee ID to search: "))
                Query = """SELECT E.ID, E.EVENTNAME, E.CLIENTID, C.NAME, E.DATE, E.VENUE
                           FROM EVENTS E 
                           JOIN CLIENTS C ON E.CLIENTID = C.ID 
                           WHERE E.EMPLOYEEID = %s"""
                mycur.execute(Query, (Id,))
                results = mycur.fetchall()
                
                if not results:
                    print(f"No events found for Employee ID: {Id}")
                else:
                    print(f"Found {len(results)} event(s) for Manager ID {Id}:\n")
                    for result in results:
                        print("-----------| Event Record |----------- ")
                        print(f"Event ID       : {result[0]}")
                        print(f"Event Name     : {result[1]}")
                        print(f"Client ID      : {result[2]}")
                        print(f"Client Name    : {result[3]}")
                        print(f"Event Date     : {result[4]}")
                        print(f"Venue          : {result[5]}")
                        print("--------------------------------------\n")
            except ValueError:
                print("Please enter a valid numeric Employee ID.")

        elif ch == '4':
            return
        else:
            print("Invalid choice.")

    except Exception as e:
        print("Unexpected error:", e)

    finally:
        if 'mycur' in locals(): mycur.close()
        if 'mydb' in locals() and mydb.is_connected(): mydb.close()

def Event_Update():
    try:
        mydb = msc.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)
        mycur = mydb.cursor()
    except Exception as e:
        print("Error connecting to database: ", e)
        return

    try:
        try:
            Id = int(input("Enter Event ID to update: "))
        except ValueError:
            print("Please enter a valid numeric Event ID.")
            return

        Query_Search = """SELECT E.ID, E.EVENTNAME, E.CLIENTID, C.NAME, C.MOB, C.EMAIL,
                              E.BUDGET, E.TOTALCOST, E.VENUE, E.DATE, E.CITY, E.STATE, E.EMPLOYEEID 
                           FROM EVENTS E 
                           JOIN CLIENTS C ON E.CLIENTID = C.ID 
                           WHERE E.ID = %s"""
        mycur.execute(Query_Search, (Id,))
        result = mycur.fetchone()

        if not result:
            print(f"No record found with Event ID: {Id}")
            return

        print("\n-----------| Current Event Record |----------- ")
        print(f"Event ID       : {result[0]}")
        print(f"Event Name     : {result[1]}")
        print(f"Client ID      : {result[2]}")
        print(f"Client Name    : {result[3]}")
        print(f"Client Mobile  : {result[4]}")
        print(f"Client Email   : {result[5]}")
        print(f"Budget         : {result[6]}")
        print(f"Total Cost     : {result[7]}")
        print(f"Venue          : {result[8]}")
        print(f"Event Date     : {result[9]}")
        print(f"City           : {result[10]}")
        print(f"State          : {result[11]}")
        print(f"Manager ID     : {result[12]}")
        print("------------------------------------------")
        print("Enter new details (leave blank to keep old value):")

        EventName = input("Enter New Event Name: ").strip()
        if EventName == "": EventName = result[1]

        while True:
            New_ClientID = input("Enter New Client ID (1-99999): ").strip()
            if New_ClientID == "":
                ClientID = result[2] 
                break
            else:
                try:
                    ClientID = int(New_ClientID)
                    if 0 < ClientID < 100000:
                        mycur.execute("SELECT ID FROM CLIENTS WHERE ID = %s", (ClientID,))
                        if mycur.fetchone():
                            break
                        else:
                            print(f"\nError: Client ID {ClientID} not found.")
                            print("1: Try entering Client ID again")
                            print("2: Cancel Event Update & Return to Menu")
                            opt = input("Enter choice (1/2): ").strip()
                            if opt == '2':
                                print("Update cancelled. Returning to Event Menu...")
                                return
                    else:
                        print("Please enter a valid 1-5 digit positive ID.")
                except ValueError:
                    print("Please enter a numeric Client ID.")

        while True:
            Budget_Input = input("Enter New Budget: ").strip()
            if Budget_Input == "":
                Budget = result[6]
                break
            else:
                try:
                    Budget = int(Budget_Input)
                    if Budget >= 0: break
                    else: print("Budget cannot be negative.")
                except ValueError:
                    print("Please enter a numeric value.")
        
        while True:
            TotalCost_Input = input("Enter New Cost: ").strip()
            if TotalCost_Input == "":
                TotalCost = result[7]
                break
            else:
                try:
                    TotalCost = int(TotalCost_Input)
                    if TotalCost >= 0: break
                    else: print("Cost cannot be negative.")
                except ValueError:
                    print("Please enter a numeric value.")

        Venue = input("Enter New Venue: ").strip()
        if Venue == "": Venue = result[8]

        while True:
            Date = input("Enter New Event Date ('YYYY-MM-DD'): ").strip()
            if Date == "":
                Date = result[9]
                break
            elif len(Date) == 10 and Date[4] in ["-", "/"] and Date[7] in ["-", "/"]:
                year, month, day = Date[:4], Date[5:7], Date[8:]
                if (year.isdigit() and month.isdigit() and day.isdigit() and
                    1 <= int(month) <= 12 and 1 <= int(day) <= 31):
                    Date = Date.replace('/', '-')
                    break
                else:
                    print("Invalid date, please try again.")
            else:
                print("Incorrect format! Use 'YYYY-MM-DD'.")

        City = input("Enter New City: ").strip()
        if City == "": City = result[10]

        State = input("Enter New State: ").strip()
        if State == "": State = result[11]

        while True:
            EmployeeID_Input = input("Enter New Manager ID: ").strip()
            if EmployeeID_Input == "":
                EmployeeID = result[12]
                break
            else:
                try:
                    EmployeeID = int(EmployeeID_Input)
                    if 0 < EmployeeID < 1000:
                        mycur.execute("SELECT ID FROM EMPLOYEE WHERE ID = %s", (EmployeeID,))
                        if mycur.fetchone():
                            break
                        else:
                            print(f"\nError: Employee ID {EmployeeID} not found.")
                            print("1: Try entering Employee ID again")
                            print("2: Cancel Event Update & Return to Menu")
                            opt = input("Enter choice (1/2): ").strip()
                            if opt == '2':
                                print("Update cancelled. Returning to Event Menu...")
                                return
                    else: print("Please enter a valid 1-3 digit ID.")
                except ValueError:
                    print("Please enter a numeric value.")

        Query_Update = """UPDATE EVENTS SET
                          EVENTNAME=%s, CLIENTID=%s,
                          BUDGET=%s, TOTALCOST=%s, VENUE=%s, DATE=%s, CITY=%s, STATE=%s, EMPLOYEEID=%s
                          WHERE ID=%s"""
        Data = (EventName, ClientID, Budget, TotalCost, Venue, Date, City, State, EmployeeID, Id)

        mycur.execute(Query_Update, Data)
        mydb.commit()
        print("\nEvent record updated successfully!")

    except Exception as e:
        print("Unexpected error:", e)

    finally:
        if 'mycur' in locals(): mycur.close()
        if 'mydb' in locals() and mydb.is_connected(): mydb.close()

def Event_Delete():
    try:
        mydb = msc.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)
        mycur = mydb.cursor()
    except Exception as e:
        print("Error connecting to database: ", e)
        return

    try:
        try:
            Id = int(input("Enter Event ID to delete: "))
        except ValueError:
            print("Please enter a valid numeric Event ID.")
            return
            
        Query_Search = """SELECT E.ID, E.EVENTNAME, C.NAME 
                           FROM EVENTS E 
                           JOIN CLIENTS C ON E.CLIENTID = C.ID 
                           WHERE E.ID = %s"""
        mycur.execute(Query_Search, (Id,))
        result = mycur.fetchone()

        if not result:
            print(f"No record found with Event ID: {Id}")
            return
        
        print("\n----------| Event Record to Delete |---------- ")
        print(f"Event ID       : {result[0]}")
        print(f"Event Name     : {result[1]}")
        print(f"Client Name    : {result[2]}")
        print("------------------------------------------")

        confirm = input("Are you sure you want to delete this event? (Y/N): ").strip().upper()
        if confirm == "Y":
            Query_Delete = "DELETE FROM EVENTS WHERE ID = %s"
            mycur.execute(Query_Delete, (Id,))
            mydb.commit()
            print("Event record deleted successfully!")
        else:
            print("Deletion cancelled.")

    except Exception as e:
        print("Unexpected error:", e)

    finally:
        if 'mycur' in locals(): mycur.close()
        if 'mydb' in locals() and mydb.is_connected(): mydb.close()

#----------------------------|CLIENT FUNCTIONS|---------------------------------

def Client_Insert():
    try:
        mydb = msc.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)
        mycur = mydb.cursor()
    except Exception as e:
        print("Error connecting to database: ", e)
        return

    try:
        while True:
            try:
                Id = int(input("Enter Client ID (1-99999): "))
                if 0 < Id < 100000:
                    mycur.execute("SELECT ID FROM CLIENTS WHERE ID = %s", (Id,))
                    if mycur.fetchone():
                        print(f"Error: Client ID {Id} already exists.")
                    else:
                        break
                else:
                    print("Please enter a valid 1-5 digit positive ID.")
            except ValueError:
                print("Please enter a numeric Client ID.")
                
        Name = input("Enter Client Name: ").strip()
        
        while True:
            Gender = input("Enter Gender (M/F): ").strip().upper()
            if Gender in ["M", "F"]:
                break
            else:
                print("Please input valid value (M/F)")
                
        Email = input("Enter Client Email: ").strip().lower()
        
        while True:
            Mob = input("Enter Client Mob (10 digits): ")
            if len(Mob) == 10 and Mob.isdigit():
                break
            else:
                print("Invalid mobile number! Must be exactly 10 digits.")
                
        while True:
            DOB = input("Enter Client DOB ('YYYY-MM-DD'): ").strip()
            if len(DOB) == 10 and DOB[4] in ["-", "/"] and DOB[7] in ["-", "/"]:
                year, month, day = DOB[:4], DOB[5:7], DOB[8:]
                if (year.isdigit() and month.isdigit() and day.isdigit() and
                    1 <= int(month) <= 12 and 1 <= int(day) <= 31 and
                    int(year) > 1920):
                    DOB = DOB.replace('/', '-')
                    break
                else:
                    print("Invalid DOB, please try again.")
            else:
                print("Incorrect format of Date, please follow 'YYYY-MM-DD'.")

        while True:
            Status = input("Enter Payment Status (1 for Paid, 0 for Unpaid): ").strip()
            if Status in ["0", "1"]:
                PaymentStatus = int(Status)
                break
            else:
                print("Please enter 0 or 1.")

        Data = (Id, Name, Gender, Email, Mob, DOB, PaymentStatus)
        Query = "INSERT INTO CLIENTS (ID, NAME, GENDER, EMAIL, MOB, DOB, PAYMENTSTATUS) VALUES (%s, %s, %s, %s, %s, %s, %s)"

        mycur.execute(Query, Data)
        mydb.commit()
        print("\nRecord inserted successfully!")

    except Exception as e:
        print("Unexpected error: ", e)

    finally:
        if 'mycur' in locals(): mycur.close()
        if 'mydb' in locals() and mydb.is_connected(): mydb.close()

def Client_Search():
    try:
        mydb = msc.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)
        mycur = mydb.cursor()
    except Exception as e:
        print("Error connecting to database: ", e)
        return

    try:
        print("\n-- Client Search Menu --")
        print("  1: Search by Name")
        print("  2: Search by ID")
        print("  3: Search by Payment Status")
        print("  4: Return")
        
        ch = input("  Enter Choice: ").strip()

        if ch == '1':
            Name = input("Enter Client Name to search: ").strip()
            Query = "SELECT * FROM CLIENTS WHERE NAME = %s"
            mycur.execute(Query, (Name,))
            results = mycur.fetchall()

            if not results:
                print(f"No record found with Name: {Name}")
            else:
                print(f"Found {len(results)} record(s):\n")
                for result in results:
                    print("-------------| Client Record |-------------- ")
                    print(f"Client ID        : {result[0]}")
                    print(f"Client Name      : {result[1]}")
                    print(f"Gender           : {result[2]}")
                    print(f"Email            : {result[3]}")
                    print(f"Mobile Number    : {result[4]}")
                    print(f"Date of Birth    : {result[5]}")
                    print(f"Payment Status   : {'Paid' if result[6] == 1 else 'Unpaid'}")
                    print("---------------------------------------------- \n")

        elif ch == '2':
            try:
                Id = int(input("Enter Client ID to search: "))
                Query = "SELECT * FROM CLIENTS WHERE ID = %s"
                mycur.execute(Query, (Id,))
                result = mycur.fetchone()

                if result:
                    print("\nClient Record Found!")
                    print("-------------| Client Record |-------------- ")
                    print(f"Client ID        : {result[0]}")
                    print(f"Client Name      : {result[1]}")
                    print(f"Gender           : {result[2]}")
                    print(f"Email            : {result[3]}")
                    print(f"Mobile Number    : {result[4]}")
                    print(f"Date of Birth    : {result[5]}")
                    print(f"Payment Status   : {'Paid' if result[6] == 1 else 'Unpaid'}")
                    print("---------------------------------------------- ")
                else:
                    print(f"No record found with Client ID: {Id}")
            except ValueError:
                print("Please enter a valid numeric Client ID.")
        
        elif ch == '3':
            try:
                Status = int(input("Enter Payment Status (1 for Paid, 0 for Unpaid): "))
                if Status not in [0, 1]:
                    print("Invalid status. Please enter 0 or 1.")
                else:
                    Query = "SELECT * FROM CLIENTS WHERE PAYMENTSTATUS = %s"
                    mycur.execute(Query, (Status,))
                    results = mycur.fetchall()
                    if not results:
                        print(f"No records found with status: {'Paid' if Status == 1 else 'Unpaid'}")
                    else:
                        print(f"Found {len(results)} record(s):\n")
                        for result in results:
                            print("-------------| Client Record |-------------- ")
                            print(f"Client ID        : {result[0]}")
                            print(f"Client Name      : {result[1]}")
                            print(f"Payment Status   : {'Paid' if result[6] == 1 else 'Unpaid'}")
                            print("---------------------------------------------- \n")
            except ValueError:
                print("Please enter 0 or 1.")

        elif ch == '4':
            return
        else:
            print("Invalid choice.")

    except Exception as e:
        print("Unexpected error:", e)

    finally:
        if 'mycur' in locals(): mycur.close()
        if 'mydb' in locals() and mydb.is_connected(): mydb.close()

def Client_Update():
    try:
        mydb = msc.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)
        mycur = mydb.cursor()
    except Exception as e:
        print("Error connecting to database: ", e)
        return

    try:
        try:
            Id = int(input("Enter Client ID to update: "))
        except ValueError:
            print("Please enter a valid numeric Client ID.")
            return
            
        Query_Search = "SELECT * FROM CLIENTS WHERE ID = %s"
        mycur.execute(Query_Search, (Id,))
        result = mycur.fetchone()
        
        if not result:
            print(f"No record found with Client ID: {Id}")
            return
            
        print("\n----------| Current Client Record |----------")
        print(f"Client ID        : {result[0]}")
        print(f"Client Name      : {result[1]}")
        print(f"Gender           : {result[2]}")
        print(f"Email            : {result[3]}")
        print(f"Mobile Number    : {result[4]}")
        print(f"Date of Birth    : {result[5]}")
        print(f"Payment Status   : {'Paid' if result[6] == 1 else 'Unpaid'}")
        print("-------------------------------------------")
        print("Enter new details (leave blank to keep old value):")

        New_Name = input("Enter New Name: ").strip()
        if New_Name == "": New_Name = result[1]

        while True:
            New_Gender = input("Enter New Gender (M/F): ").strip().upper()
            if New_Gender == "":
                New_Gender = result[2]
                break
            elif New_Gender in ["M", "F"]:
                break
            else:
                print("Please input valid value (M/F)")
        
        New_Email = input("Enter New Email: ").strip().lower()
        if New_Email == "": New_Email = result[3]

        while True:
            New_Mob = input("Enter New Mobile (10 digits): ").strip()
            if New_Mob == "":
                New_Mob = result[4]
                break
            elif len(New_Mob) == 10 and New_Mob.isdigit():
                break
            else:
                print("Invalid mobile number! Must be exactly 10 digits.")

        while True:
            New_DOB = input("Enter New DOB ('YYYY-MM-DD'): ").strip()
            if New_DOB == "":
                New_DOB = result[5]
                break
            elif len(New_DOB) == 10 and New_DOB[4] in ["-", "/"] and New_DOB[7] in ["-", "/"]:
                year, month, day = New_DOB[:4], New_DOB[5:7], New_DOB[8:]
                if (year.isdigit() and month.isdigit() and day.isdigit() and
                    1 <= int(month) <= 12 and 1 <= int(day) <= 31 and
                    int(year) > 1920):
                    New_DOB = New_DOB.replace('/', '-')
                    break
                else:
                    print("Invalid DOB, please try again.")
            else:
                print("Incorrect format of Date, please follow 'YYYY-MM-DD'.")
        
        while True:
            New_Status = input("Enter New Payment Status (1 for Paid, 0 for Unpaid): ").strip()
            if New_Status == "":
                New_PaymentStatus = result[6]
                break
            elif New_Status in ["0", "1"]:
                New_PaymentStatus = int(New_Status)
                break
            else:
                print("Please enter 0 or 1.")

        Query_Update = """UPDATE CLIENTS SET
                          NAME=%s, GENDER=%s, EMAIL=%s, MOB=%s, DOB=%s, PAYMENTSTATUS=%s
                          WHERE ID=%s"""
        Data = (New_Name, New_Gender, New_Email, New_Mob, New_DOB, New_PaymentStatus, Id)

        mycur.execute(Query_Update, Data)
        mydb.commit()
        print("\nRecord updated successfully!")

    except Exception as e:
        print("Unexpected error:", e)

    finally:
        if 'mycur' in locals(): mycur.close()
        if 'mydb' in locals() and mydb.is_connected(): mydb.close()

def Client_Delete():
    try:
        mydb = msc.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)
        mycur = mydb.cursor()
    except Exception as e:
        print("Error connecting to database: ", e)
        return
        
    try:
        try:
            Id = int(input("Enter Client ID to delete: "))
        except ValueError:
            print("Please enter a valid numeric Client ID.")
            return
            
        # Prevent deletion if client is connected to an event
        mycur.execute("SELECT ID FROM EVENTS WHERE CLIENTID = %s", (Id,))
        if mycur.fetchone():
            print(f"\nError: Cannot delete Client ID {Id}. They are linked to one or more events.")
            print("Please delete or re-assign events before deleting this client.")
            return
            
        Query_Search = "SELECT * FROM CLIENTS WHERE ID = %s"
        mycur.execute(Query_Search, (Id,))
        result = mycur.fetchone()

        if not result:
            print(f"No record found with Client ID: {Id}")
            return

        print("\n----------| Client Record to Delete |---------- ")
        print(f"Client ID        : {result[0]}")
        print(f"Client Name      : {result[1]}")
        print(f"Payment Status   : {'Paid' if result[6] == 1 else 'Unpaid'}")
        print("---------------------------------------------")

        confirm = input("Are you sure you want to delete this record? (Y/N): ").strip().upper()
        if confirm == "Y":
            Query_Delete = "DELETE FROM CLIENTS WHERE ID = %s"
            mycur.execute(Query_Delete, (Id,))
            mydb.commit()
            print("Record deleted successfully!")
        else:
            print("Deletion cancelled.")

    except Exception as e:
        print("Unexpected error:", e)

    finally:
        if 'mycur' in locals(): mycur.close()
        if 'mydb' in locals() and mydb.is_connected(): mydb.close()

#----------------------------|REPORT FUNCTIONS|---------------------------------

def Report_Financials():
    try:
        mydb = msc.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)
        mycur = mydb.cursor()
    except Exception as e:
        print("Error connecting to database: ", e)
        return
    
    try:
        print("\n-- Financial Statement Menu --")
        print("  1: Last Month")
        print("  2: Last Year")
        print("  3: Lifetime")
        print("  4: Return")
        
        ch = input("  Enter Choice: ").strip()
        Query = ""

        if ch == '1':
            print("\n-- Financials: Last Month --")
            Query = "SELECT SUM(BUDGET), SUM(TOTALCOST), SUM(BUDGET - TOTALCOST) FROM EVENTS WHERE DATE BETWEEN DATE_SUB(NOW(), INTERVAL 1 MONTH) AND NOW()"
        elif ch == '2':
            print("\n-- Financials: Last Year --")
            Query = "SELECT SUM(BUDGET), SUM(TOTALCOST), SUM(BUDGET - TOTALCOST) FROM EVENTS WHERE DATE BETWEEN DATE_SUB(NOW(), INTERVAL 1 YEAR) AND NOW()"
        elif ch == '3':
            print("\n-- Financials: Lifetime --")
            Query = "SELECT SUM(BUDGET), SUM(TOTALCOST), SUM(BUDGET - TOTALCOST) FROM EVENTS"
        elif ch == '4':
            return
        else:
            print("Invalid choice.")
            return

        mycur.execute(Query)
        result = mycur.fetchone()

        # If data exists and isn't populated entirely with 'None's
        if result and result[0] is not None:
            revenue = result[0]
            expense = result[1] if result[1] is not None else 0
            profit = result[2] if result[2] is not None else 0
            
            print(f"Total Revenue (Budget): {revenue}")
            print(f"Total Expenses (Cost) : {expense}")
            if profit > 0:
                print(f"Total Profit          : {profit}")
            elif profit < 0:
                print(f"Total Loss            : {profit}")
            else:
                print("Total P/L             : 0 (Breakeven)")
        else:
            print("No financial data found for this period.")

    except Exception as e:
        print("Unexpected error:", e)

    finally:
        if 'mycur' in locals(): mycur.close()
        if 'mydb' in locals() and mydb.is_connected(): mydb.close()

def Report_PL_Statement():
    try:
        mydb = msc.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)
        mycur = mydb.cursor()
    except Exception as e:
        print("Error connecting to database: ", e)
        return
        
    try:
        print("\n-- P&L Statement Search Menu --")
        print("  1: Search by Event Name")
        print("  2: Search by Event ID")
        print("  3: Search by Client Name")
        print("  4: Search by Client ID")
        print("  5: Search by City (Aggregate)")
        print("  6: Search by State (Aggregate)")
        print("  7: Return")
        
        ch = input("  Enter Choice: ").strip()

        if ch == '1':
            Name = input("Enter Event Name to search: ").strip()
            Query = "SELECT EVENTNAME, BUDGET, TOTALCOST, (BUDGET - TOTALCOST) FROM EVENTS WHERE EVENTNAME = %s"
            mycur.execute(Query, (Name,))
            results = mycur.fetchall()
            if not results: print("No events found.")
            for res in results:
                print(f"Event: {res[0]:<15} | Revenue: {res[1]:<8} | Expense: {res[2]:<8} | P&L: {res[3]}")

        elif ch == '2':
            try:
                Id = int(input("Enter Event ID to search: "))
                Query = "SELECT EVENTNAME, BUDGET, TOTALCOST, (BUDGET - TOTALCOST) FROM EVENTS WHERE ID = %s"
                mycur.execute(Query, (Id,))
                res = mycur.fetchone()
                if not res: print("No event found.")
                else: print(f"Event: {res[0]:<15} | Revenue: {res[1]:<8} | Expense: {res[2]:<8} | P&L: {res[3]}")
            except ValueError:
                print("Invalid ID.")
        
        elif ch == '3':
            Name = input("Enter Client Name to search: ").strip()
            Query = """SELECT E.EVENTNAME, C.NAME, E.BUDGET, E.TOTALCOST, (E.BUDGET - E.TOTALCOST) 
                       FROM EVENTS E 
                       JOIN CLIENTS C ON E.CLIENTID = C.ID 
                       WHERE C.NAME = %s"""
            mycur.execute(Query, (Name,))
            results = mycur.fetchall()
            if not results: print("No events found.")
            for res in results:
                print(f"Event: {res[0]:<15} | Client: {res[1]:<15} | P&L: {res[4]}")

        elif ch == '4':
            try:
                Id = int(input("Enter Client ID to search: "))
                Query = """SELECT E.EVENTNAME, C.NAME, E.BUDGET, E.TOTALCOST, (E.BUDGET - E.TOTALCOST) 
                           FROM EVENTS E 
                           JOIN CLIENTS C ON E.CLIENTID = C.ID 
                           WHERE C.ID = %s"""
                mycur.execute(Query, (Id,))
                results = mycur.fetchall()
                if not results: print("No events found.")
                for res in results:
                    print(f"Event: {res[0]:<15} | Client: {res[1]:<15} | P&L: {res[4]}")
            except ValueError:
                print("Invalid ID.")

        elif ch == '5':
            City = input("Enter City Name to search: ").strip()
            Query = "SELECT SUM(BUDGET), SUM(TOTALCOST), SUM(BUDGET - TOTALCOST) FROM EVENTS WHERE CITY = %s"
            mycur.execute(Query, (City,))
            res = mycur.fetchone()
            if not res or res[0] is None: print("No events found.")
            else: print(f"City: {City:<10} | Total Revenue: {res[0]:<8} | Total Expense: {res[1]:<8} | Total P&L: {res[2]}")

        elif ch == '6':
            State = input("Enter State Name to search: ").strip()
            Query = "SELECT SUM(BUDGET), SUM(TOTALCOST), SUM(BUDGET - TOTALCOST) FROM EVENTS WHERE STATE = %s"
            mycur.execute(Query, (State,))
            res = mycur.fetchone()
            if not res or res[0] is None: print("No events found.")
            else: print(f"State: {State:<10} | Total Revenue: {res[0]:<8} | Total Expense: {res[1]:<8} | Total P&L: {res[2]}")
        
        elif ch == '7':
            return
        else:
            print("Invalid choice.")

    except Exception as e:
        print("Unexpected error:", e)

    finally:
        if 'mycur' in locals(): mycur.close()
        if 'mydb' in locals() and mydb.is_connected(): mydb.close()

def Report_Top_Clients():
    try:
        mydb = msc.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)
        mycur = mydb.cursor()
    except Exception as e:
        print("Error connecting to database: ", e)
        return
        
    try:
        print("\n-- Top 5 Clients (by Total Revenue) --")
        Query = """SELECT C.NAME, SUM(E.BUDGET) AS TotalRevenue
                   FROM EVENTS E
                   JOIN CLIENTS C ON E.CLIENTID = C.ID
                   GROUP BY C.ID, C.NAME
                   ORDER BY TotalRevenue DESC
                   LIMIT 5"""
        
        mycur.execute(Query)
        results = mycur.fetchall()

        if not results:
            print("No client data found.")
        else:
            print("Rank | Client Name        | Total Revenue")
            print("------------------------------------------")
            for rank, res in enumerate(results, start=1):
                # We use f-strings to align the columns seamlessly regardless of string length
                print(f"{rank:<4} | {res[0]:<18} | {res[1]}")

    except Exception as e:
        print("Unexpected error:", e)

    finally:
        if 'mycur' in locals(): mycur.close()
        if 'mydb' in locals() and mydb.is_connected(): mydb.close()

def Report_Top_Events():
    try:
        mydb = msc.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)
        mycur = mydb.cursor()
    except Exception as e:
        print("Error connecting to database: ", e)
        return
    
    try:
        print("\n-- Top 5 Events (by Profit) --")
        Query = """SELECT EVENTNAME, (BUDGET - TOTALCOST) AS Profit
                   FROM EVENTS
                   ORDER BY Profit DESC
                   LIMIT 5"""
        
        mycur.execute(Query)
        results = mycur.fetchall()

        if not results:
            print("No event data found.")
        else:
            print("Rank | Event Name         | Profit")
            print("--------------------------------------")
            for rank, res in enumerate(results, start=1):
                # Replacing brittle string multiplication formatting with formatted f-strings
                print(f"{rank:<4} | {res[0]:<18} | {res[1]}")

    except Exception as e:
        print("Unexpected error:", e)

    finally:
        if 'mycur' in locals(): mycur.close()
        if 'mydb' in locals() and mydb.is_connected(): mydb.close()


#----------------------------|MENU FUNCTIONS|---------------------------------

def show_employee_menu():
    while True:
        print("\n-------------| EMPLOYEE MENU |------------")
        print("1: Insert New Employee Data ")
        print("2: Search for Employee")
        print("3: Update Employee Record")
        print("4: Delete Employee Record")
        print("5: Return to Main Menu")
        print("----------------------------------\n")
        try:
            ch = input("Enter Choice: ").strip()
            if ch == '1':
                Employee_Insert()
            elif ch == '2':
                Employee_Search()
            elif ch == '3':
                Employee_Update()
            elif ch == '4':
                Employee_Delete()
            elif ch == '5':
                print("Returning to Main Menu...")
                break 
            else:
                print("Invalid choice, please try again (1-5).")
        except Exception as e:
            print("An error occurred in employee menu:", e)

def show_event_menu():
    while True:
        print("\n-------------| EVENTS MENU |------------")
        print("1: Insert New Event Data ")
        print("2: Search for Event")
        print("3: Update Event Record")
        print("4: Delete Event Record")
        print("5: Return to Main Menu")
        print("----------------------------------\n")
        try:
            ch = input("Enter Choice: ").strip()
            if ch == '1':
                Event_Insert()
            elif ch == '2':
                Event_Search()
            elif ch == '3':
                Event_Update()
            elif ch == '4':
                Event_Delete()
            elif ch == '5':
                print("Returning to Main Menu...")
                break
            else:
                print("Invalid choice, please try again (1-5).")
        except Exception as e:
            print("An error occurred in event menu:", e)

def show_client_menu():
    while True:
        print("\n-------------| CLIENTS MENU |------------")
        print("1: Insert New Client Data ")
        print("2: Search for Client")
        print("3: Update Client Record")
        print("4: Delete Client Record")
        print("5: Return to Main Menu")
        print("----------------------------------\n")
        try:
            ch = input("Enter Choice: ").strip()
            if ch == '1':
                Client_Insert()
            elif ch == '2':
                Client_Search()
            elif ch == '3':
                Client_Update()
            elif ch == '4':
                Client_Delete()
            elif ch == '5':
                print("Returning to Main Menu...")
                break
            else:
                print("Invalid choice, please try again (1-5).")
        except Exception as e:
            print("An error occurred in client menu:", e)

def show_report_menu():
    while True:
        print("\n-------------| REPORT MENU |------------")
        print("1: Show Financial Statement")
        print("2: Search for P&L Statement")
        print("3: Top Client Ranks")
        print("4: Top Event Ranks")
        print("5: Return to Main Menu")
        print("----------------------------------\n")
        try:
            ch = input("Enter Choice: ").strip()
            if ch == '1':
                Report_Financials()
            elif ch == '2':
                Report_PL_Statement()
            elif ch == '3':
                Report_Top_Clients()
            elif ch == '4':
                Report_Top_Events()
            elif ch == '5':
                print("Returning to Main Menu...")
                break
            else:
                print("Invalid choice, please try again (1-5).")
        except Exception as e:
            print("An error occurred in report menu:", e)


#--------------------------------|MAIN MENU|-----------------------------------

def main():
    global DB_PASSWD
    print("\n========| JAZ EVENT MANAGEMENT LOGIN |========")
    # Simple login system checking Database password
    while True:
        DB_PASSWD = input(f"Enter MySQL Password for '{DB_USER}@{DB_HOST}' (or type 'exit' to quit): ").strip()
        if DB_PASSWD.lower() == 'exit':
            print("Exiting Program.. Thank you!")
            return
            
        if initialize_database():
            print("Login and Database Initialization Successful!")
            break
        else:
            print("\nPlease check your credentials and try again.")
            
    while True:
        print("\n========| JAZ EVENT MANAGEMENT |========")
        print("-------------| MAIN MENU |------------")
        print("1: Employees")
        print("2: Events")
        print("3: Clients")
        print("4: Report")
        print("5: Exit Program")
        print("----------------------------------\n")
        try:
            ch = input("Enter Choice: ").strip()
            
            if ch == '1':
                show_employee_menu()
            elif ch == '2':
                show_event_menu()
            elif ch == '3':
                show_client_menu()
            elif ch == '4':
                show_report_menu()
            elif ch == '5':
                print("Exiting Program.. Thank you!")
                break
            else:
                print("Invalid Input, Please try again (1, 2, 3, 4, or 5)!")
        
        except Exception as e:
            print("An unexpected error occurred in the main menu:", e)
        except KeyboardInterrupt:
            # Handles unexpected Ctrl+C program interrupt properly
            print("\n\nProgram interrupted by user. Exiting...")
            break

# Run the main program
if __name__ == "__main__":
    main()