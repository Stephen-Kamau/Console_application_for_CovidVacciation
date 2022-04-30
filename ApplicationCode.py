#!/usr/bin/env python
# coding: utf-8

# start of the application
from tabulate import tabulate
from beautifultable import BeautifulTable
# table = BeautifulTable()
from datetime import datetime , timedelta
import os


# check if  file exists and create new one if it doesn,t
if not os.path.isfile("patients.txt"):
    open("patients.txt" , 'w')
    print("Patient Records File created")
if not os.path.isfile("vaccination.txt"):
    open("vaccination.txt" , "w")
    print("Vaccination Records File created")


def displayVaccine(codes , vaccine_details):
    """
    Prints out Vaccines with their Respective codes.
    params:
        - codes -> A list of vaccination Codes
        - vaccine_details -> a dictionary with dictionary for vaccine details
    returns:None
    """
    print("Vaccine Code	Dosage Interval  Min_Age   Max_Age\n")
    #get all vaccine codes with their details
    for code in codes:
        detail = vaccine_details[code]
        print(f"{code}                {detail['dosage']}     {detail['interval']}          {detail['min_age']}       {detail['max_age']}")
    print("")



def SelectCenter():
    """
    It prints a MENU for Vaccination Center Selection
    returns : None
    """
    print("Please select a vaccination center for you to be attended in...")
    print("""
    Select 1 for VC1 , 2 for VC2 or 3 to quit;

    1.  Vaccination Center 1 -> VC1
    2.  Vaccination Center 2 -> VC2
    3.  Exit..
    """)

    
    
def isValidCode(code , limit):
    """
    returns false if code is not END or code<0 or code>limit
    params:
        - code  which is the product code to be selected
        - limit -Maximum reach of the value to be entered
    returns : Bool whether the code meets some criteria
    """
    #use try-catch block in order to avoid program breaking because of int conversion
    try:
        #change to integer
        code = int(code)
    except ValueError:
        return False
    else:
        #check the criteria
        if int(code)>=0 and int(code) <= limit:
            return True
        else:
            return False
            
def GetVC():
    """
    Used to get Vaccination center Formated as VC{Number}
    returns : Vaccination center from user Input
    """
    #display the menu for vaccination center
    SelectCenter()
    vc = input("Your Choice:  ")
    #check for valid inputs
    while not isValidCode(vc , 3):
        print("Please select The correct option Must be between 1 and 3")
        SelectCenter()
        vc = input("Your Choice:  ")
    
    #only convert vc1 and vc2 but do not convert for 3       
    return  "3" if  vc == "3" else  f"VC{vc}"


def getAge():
    """
    Get the User's age
    returns : An Int which represents the age of an intividual
    """
    age = input('Please Enter your Age')
    
    #assumption is that no age is greated than 150
    while not isValidCode(age , 150):
        age = input("Please Enter a valid age from 0 - 150")
    return int(age)


def RegisterUser():
    """
    It adds a new user to the file system.
    The user must provided his or her details in order to be added.
    returns : None
    """
    #get vaccinations
    vaccine_details = {
    "AF":{"dosage":2 ,"interval":2 , "min_age":12 , "max_age":200},
    "BV":{"dosage":2 ,"interval":3 , "min_age":18 , "max_age":200},
    "CZ":{"dosage":2 ,"interval":3 , "min_age":12 , "max_age":45},
    "DM":{"dosage":2 ,"interval":4 , "min_age":12 , "max_age":200},
    "EC":{"dosage":1 ,"interval":0 , "min_age":18 , "max_age":200},
    }

    #get vaccination center
    vc = GetVC()
    #continue if it is either vc1 or vc2
    if vc != "3":
        #get age
        age = getAge()
        #people less than 12 years has no vaccine code.
        if age<12:
            print("Not eligible for Vaccination")
            print("exiting....")
            return
        else:
            #display vaccination code and details depending on their age
            if age >= 12 and age <=45:
                if age >= 18:
                    vc_codes = ['BV' , "EC" , 'AF' , "CZ" , "DM"]
                    #displayVaccine(vc_codes , vaccine_details)
                else:
                    vc_codes =['AF' , "CZ" , "DM"]
                    #displayVaccine(vc_codes , vaccine_details)
            else:
                vc_codes = ['BV' , "EC" , 'AF' , "CZ" , "DM"]


        displayVaccine(vc_codes , vaccine_details)

        code = input("Enter Vaccine Code")

        # vc_codes = ['AF' , "BV" , "CZ" , "DM" , "EC"]
        while code.upper() not in vc_codes:
            code = input("\nPlease Select Only available Options")
            
        #get other details
        name = input("Enter your name")
        contact = input("Enter your email or phone number  ")
    #     blood_group = input("Blood Group  ")
    #     height = input("Height   ")
    #     wieght = input("Weight   ")



        #get the already existing records to get the current id
        vac , records = GetData()
        #extract the last integer from the 
        id_nums = [int(x.split("/")[1]) for x in list(records.keys())]
        #format it well
        
        #if there was no record use 1 as the id
        if len(id_nums) ==0:
            patId = "Pat/1"
            new_id = 1
        else:
            new_id =max(id_nums)+1
            patId =  f"Pat/{max(id_nums)+1}" 
            
        #add the record to the patient file
        with open("patients.txt" , "a+") as patients:
            patients.write(f"{patId},{name},{contact},{age},{vc},{code.upper()}\n")
            
        patients.close()
        print(f"\n\nDear {name } You have successfully Registered for Vaccination at center {vc}")
        print(f"You Can Visit the Center and Start your Vaccination")
        print(f"Please Use   {new_id} as your id on your dosage vaccination ")
    else:
        print("Exiting...")
        return


def GetData():
    """
    used to extract details from vaccination.txt and patient.txt
    returns : returns two dictionarys having patient and vaccination records
    """
    #open vaccination file and create a dictionary keys being ids
    with open("vaccination.txt") as vaccine:
        vac = {}
        vaccine = vaccine.readlines()
        for each_record in vaccine:
            pat_id = each_record.strip().split(",")[0]
            vac[pat_id] = each_record.strip().split(",")

    #open patients file and create a dictionary with its keys as ids
    with open("patients.txt") as patients:
        records = {}
        patients = patients.readlines()
        #iterate through all lines
        for patient in patients:
            patId = patient.strip().split(",")[0]
            records[patId] = patient.strip().split(",")
    #returns vaccination and patient records 
    return vac , records



def Vaccinate_user():
    """
    It is used to add new data or update in vaccination.txt
    If a record does not exists in the vaccination.txt it is added as new record with first vaccination
    dose given else the second vaccination dose is given
    returns :None
    """
    #get all data from the files
    vac , records = GetData()
    patientId = input("Please Enter your patient Id That you were given")

    # check if he has been vaccinated or record exists in vaccine or patient files
    if records.get(f"Pat/{patientId}" , None) is None:
        print("\nSorry You need to register first as your Details Does not appear in the system")
        print("Press Enter to continue or any key to Exit\n\n")
        choice = input("Choice")
        if choice =="":
            #call registration function
            RegisterUser()
        else:
            print("Exiting....\n")
            return
    elif vac.get(f"Pat/{patientId}" , None) is not None:
        #get the details
        details = vac.get(f"Pat/{patientId}" , None)
        #check if he has been vaccinated Dose1.
        vc = details[2]
        if vc.upper() == "EC":
            print("\nYou only had One Dose for EC Vaccine Which you have completed")
            print("Thanks for Trusting in us BYEE")
            print("Exiting.....\n\n")
            return
        #extract dose1 and dose2 details
        dose1 = details[4]
        dose2 = details[6]
        #if dose2 is given consider as vaccination is finished
        if dose2 == "True":
            print("\nYou have already completed your vaccination.")
            print("Thank you for using our System .....")
            print("Exiting ....\n\n")
            return
        #allow for dose2 to be administered
        elif dose1 == "True" and dose2 == "False":
            print("Press ENTER to Continue to DOSE 2 or any Key to exit")
            choice = input("Your Choice  ")
            if choice =="":
                #edit the vaccination file to update dosage 
                UpdateRecord(patientId)
                print("\nYou have fully completed your vaccination")
                print("Ensure You keep yourself Safe BYEE")
                print("Exiting.....\n\n")
            else:
                return
        else:
            pass
    else:
        #add the details to vaccination file incase no record is found in the vaccination.txt
        with open("vaccination.txt" , "a+") as vaccine_append:
            detail = records.get(f"Pat/{patientId}" ,None)
            
            #get the cuurrent time
            curr_date = datetime.now()
            next_date = curr_date + timedelta(days=14)
            curr_date = curr_date.strftime('%d/%m/%Y')
            #next dose time
            next_date = next_date.strftime('%d/%m/%Y')
            
            #EC has only one dose
            if detail[5].upper() == "EC":
                dose2 = "N/A"
                next_date = "N/A"
            else:
                dose2 ="False"
            if not detail:
                print("Unable to retrieve the records")
                print("Exiting...")
                return 
            vaccine_type = detail[5].upper()
            # ID , CENTER , VC, NAME , DOSE1 D1_DATE DOSE2 D2_DATE
            data_write = f"Pat/{patientId},{detail[4]},{vaccine_type},{detail[1]},{True},{curr_date},{dose2},{next_date}"
            #update the data files
            vaccine_append.write(f"{data_write}\n")

            
            if detail[5].upper() == "EC":
                print("\n\nYou have fully completed your vaccination")
                print("Ensure You keep yourself Safe BYEE")
                print("Exiting.....\n")
                return
                
            print(f"\n\nYou have successfull been Vaccinated for {vaccine_type} at Center  {detail[4]}")
            print(f"Please Ensure you come Back on    {next_date} for the Second Dosage\n\n")
            



def UpdateRecord(pat_id):
    """
    It updates a record that has a matching patient Id
    to make a file to current updated status
    params :
        pat_id  -> an Int which represents patient id
    returns : None
    """
    # get vaccination details where you want to update
    vaccine_details , _ = GetData()
    #get the record to be updated
    data_update = vaccine_details.get(f"Pat/{pat_id}" , None)
    #open the file for update
    with open("vaccination.txt" , "r") as update:
        update = update.readlines()
        update = [x.strip() for x in update]
        #get the index of the record to be updated
        update_index = update.index(",".join(data_update))
        up_date = update[update_index].strip().split(",")
        #update the second dose as administered
        up_date[6] = "True"
        update[update_index] = ",".join(up_date)
        #update the whole files and save the details
        with open("vaccination.txt" , "w") as new_update:
            new_update.writelines("\n".join(update)+"\n")
            new_update.close()


def SearchById(pat_id):
    """
    Searchs and prints out a record using pattient Id given.
    params :
        pat_id -> patient Id for the record to be printed
    returns None
    """
    data = []
    vac , records = GetData()
    #extract the data from vaccinations record
    details = vac.get(f"Pat/{pat_id}" , None)
    #extract the data from patient record
    patient_record = records.get(f"Pat/{pat_id}" , None)
    
    #if not in patient record return None
    if not patient_record:
        print("No record with Such ID Found in our System..")
    else:
        if details:
            #update the vaccination status
            if (details[6] == "True" and details[4] == "True") or (details[6] == "N/A" and details[4] == "True"):
                status = "completed"
            else:
                status = "Not completed"

            if details[6] == "True":
                details[6] = "done"
            elif details[6] == "False":
                details[6] ="Not Done"

            if details[4] == "True":
                details[4] = "done"
            else:
                details[4] ="Not Done"      

            if patient_record:
                #print the data in tabulated format
                data.append(["ID", "CENTER" , "VC", "NAME" , "DOSE1", "D1_DATE"," DOSE2", "D2_DATE" , "CONTACT" , "AGE" , "STATUS"])
                details.append(patient_record[2])
                details.append(patient_record[3])
                details.append(status)
                data.append(details)
                print(tabulate(data, headers='firstrow', tablefmt='fancy_grid' , showindex=0 , missingval='N/A') )
        else:
            #if no vaccine dose is given print the patient record
            data.append(['ID' , "NAME" , "CONTACT" , "AGE", "VACCINE CENTER", "VACCINE CODE" , "STATUS"])
            patient_record.extend(["Not Vaccinated"])
            data.append(patient_record)
            print(tabulate(data, headers='firstrow', tablefmt='fancy_grid' , showindex=0 , missingval='N/A'))
        



def DisplayStats():
    """
    Used to Display Statistics of all vaccines administered to each center
    It also prints those administered completely and those waiting for dose 2
    returns :None
    """
    #variables to hold various data for both centers
    vc1 =[]
    vc2 =[]
    vc1_completed = 0
    vc2_completed =0
    vc1_counter =0
    vc2_counter =0
    #create a formatable table that is good looking
    vc1.append(["","","","","","CENTER","VC1","","",""])
    #add headers to each center record
    vc1.append(["ID", "VC", "NAME" , "DOSE1", "D1_DATE"," DOSE2", "D2_DATE" , "CONTACT" , "AGE" , "STATUS"])
    vc2.append(["ID" , "VC", "NAME" , "DOSE1", "D1_DATE"," DOSE2", "D2_DATE" , "CONTACT" , "AGE" , "STATUS"])
    vac , records = GetData()
    
    #iterate through all vaccination details and extract details 
    for details in vac.values():
        patId = details[0]
        if (details[6] == "True" and details[4] == "True") or (details[6] == "N/A" and details[4] == "True"):
            if details[1].upper() == "VC1":
                vc1_completed +=1
            else:
                vc2_completed +=1
            status = "completed"
        else:
            status = "Not completed"

        if details[6] == "True":
            details[6] = "done"
        elif details[6] == "False":
            details[6] ="Not Done"

        if details[4] == "True":
            details[4] = "done"
        else:
            details[4] ="Not Done"
        
        #add details from patient record
        patient_record = records.get(f"{patId}" , None)
        if patient_record:
            details.append(patient_record[2])
            details.append(patient_record[3])
            details.append(status)
        #update count for each vaccination center
        if details[1] == "VC1":
            vc1_counter +=1
            details.remove("VC1")
            vc1.append(details)
        elif details[1] == "VC2":
            vc2_counter +=1
            details.remove("VC2")
            vc2.append(details)
    vc1.append(["","","TOtal VC2",f"{vc1_counter}","","","","","",""])
    vc1.append(["","","","","Completed",f"{vc1_completed}","","","",""])
    vc1.append(["","","","","Waiting Dose 2",f"{vc1_counter-vc1_completed}","","","",""])
    vc1.append(["","","","","","","","","",""])
    vc1.append(["","","","","","CENTER","VC2","","",""])
    vc1.extend(vc2[1:])
    
    vc1.append(["","","TOtal VC2",f"{vc2_counter}","","","","","",""])
    vc1.append(["","","","","Completed",f"{vc2_completed}","","","",""])
    vc1.append(["","","","","Waiting Dose 2",f"{vc2_counter-vc2_completed}","","","",""])
    vc1.append(["","","","","","","","","",""])
    #print formated data
    print("Displaying Stats................")
    print(tabulate(vc1, headers='firstrow', tablefmt='fancy_grid' , showindex=0 , missingval='N/A') )



def main():
    """
    This works as the app Controller.
    Display GUIDE MENU for user calling required functions for each user action
    returns : None
    """
    print("   WELCOME TO E-VACCINATION APP")
    print(
    """
      Select An Option To Continue

          1 .  Register as a New User.
          2 .  Take Vaccination Dosage
          3 .  Search user By ID 
          4 .  View Vaccination Stats
          5 .  Exit 
    """)

    selection = input("Enter your Option  ")
    while selection not in ["1" ,"2" ,"3" , "4" , "5"]:
        selection = input("Please Enter Correction Option  ")

    if selection == "1":
        print("Welcome To the Registration Page..\n")
        RegisterUser()
    elif selection == "2":
        print("Please Follow The guidelines to compelete Your Vaccinations...\n")
        Vaccinate_user()

    elif selection == "3":
        pat_id = input("Enter The ID you want to Search")
        SearchById(pat_id)
    elif selection == "4":
        print("Here Is Stats For the Vaccinations")
        DisplayStats()
    elif selection == "5":
        print("\nThanks For the Support..")
        print("Exiting....\n")


# call the controller function
main()


# 




