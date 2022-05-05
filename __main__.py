# Purpose : To get all my haters IC numbers
# Programmer : Asuna
# Version 1.9.6

import os
import sys
import json
import time
import datetime
import random

from _GetDetails_ import ClearScreen, _PlacesOfBirth, _Areas, _Schools, _Get

def Option(Number) : # New Switch-case function only for Python Version >= 3.10
    match Number :
        case 0 :
            while True :
                BirthDate = str ( input( "Please enter the birth date : (031231) "))
                if ValidateDatetime(BirthDate) :
                    break
            while True :
                UserInputPlaceCode = str ( input( "Please enter the place of birth : (13)(If no just keep it blank) "))
                if _Get.VerifyCode(UserInputPlaceCode) :
                    break
            while True :
                Gender = str ( input( "Please enter the gender : (Female)(If no just keep it blank) ")).upper()
                if Gender in ("MALE", "FEMALE", "M", "F", "") :
                    break
            while True :
                UserInputSchoolCode = str ( input( "Please enter the school code : (YCC4102)(If no just keep it blank) ")).upper()
                if _Get.VerifyCode(UserInputSchoolCode) or UserInputSchoolCode == "" :
                    break
        case default :
            return
        
def ValidateDatetime(Date):
    try :
        datetime.datetime.strptime(Date, "%y%m%d")
        return True
    except ValueError:
        return False
    
def FileDumpWithSchools(Response) : 
    # Response return [True, IdentityCode, SchoolCodeReturn, SchoolNameReturn, StudentNameReturn, PlaceCodeReturn, PlaceNameReturn, AreaCodeReturn, AreaNameReturn]
    PlaceCode = Response[5]
    PlaceName = Response[6]
    AreaCode = Response[7]
    AreaName = Response[8]
    SchoolCode = Response[2]
    SchoolName = Response[3]
    IdentityCode = Response[1]
    StudentName = Response[4]

    try : # Retrieve Data first using "r" mode, if using "w" mode, it will truncate the data
        Data = json.load(open ("HereYouGo.json", "r", encoding ="utf8"))
    except :
        Data = {}
    
    # Write into a .txt file
    with open ("HereYouGo.txt", "a", encoding ="utf8") as TxTFile, open ("HereYouGo.json", "w", encoding ="utf8") as JsonFile :
        TxTFile.write( f"{IdentityCode}\t{StudentName}\t{SchoolCode}\t{SchoolName}\t{PlaceName}\t{AreaName}\n")
    
    # Write into a .json file
            
        '''
        Data[PlaceCode] = {
                            "PlaceName": PlaceName,
                            "Areas": {
                                AreaCode: {
                                    "AreaName": AreaName,
                                    "Schools": {
                                        SchoolCode: {
                                            "SchoolName": SchoolName,
                                            "Students": {
                                                IdentityCode: {
                                                    "StudentName": StudentName
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
        '''
        
        if PlaceCode not in Data.keys() :
            Data[PlaceCode] = {
                "PlaceName": PlaceName,
                "Areas": {
                    AreaCode: {
                        "AreaName": AreaName,
                        "Schools": {
                            SchoolCode: {
                                "SchoolName": SchoolName,
                                "Students": {
                                    IdentityCode: {
                                        "StudentName": StudentName
                                    }
                                }
                            }
                        }
                    }
                }
            }
            
        if AreaCode not in Data[PlaceCode]["Areas"].keys() :
            Data[PlaceCode]["Areas"][AreaCode] = {
                "AreaName": AreaName,
                "Schools": {
                    SchoolCode: {
                        "SchoolName": SchoolName,
                        "Students": {
                            IdentityCode: {
                                "StudentName": StudentName
                            }
                        }
                    }
                }
            }

        if SchoolCode not in Data[PlaceCode]["Areas"][AreaCode]["Schools"] :
            Data[PlaceCode]["Areas"][AreaCode]["Schools"][SchoolCode] = {
                "SchoolName": SchoolName,
                "Students": {
                    IdentityCode: {
                        "StudentName": StudentName
                    }
                }
            }

        if IdentityCode not in Data[PlaceCode]["Areas"][AreaCode]["Schools"][SchoolCode]["Students"] :
            Data[PlaceCode]["Areas"][AreaCode]["Schools"][SchoolCode]["Students"][IdentityCode] = {
                "StudentName": StudentName
            }
            
        json.dump (Data, JsonFile, indent = 4, ensure_ascii = False, sort_keys = False)
        

if __name__ == "__main__" :
    
    try:
        with open ("HereYouGo.json", "r", encoding ="utf8") as f:
            pass
    except FileNotFoundError:
        with open ("HereYouGo.json", "w+", encoding ="utf8") as f:
            pass
    try:
        with open ("HereYouGo.txt", "r", encoding ="utf8") as f:
            pass
    except FileNotFoundError:
        with open ("HereYouGo.txt", "w+", encoding ="utf8") as f:
            pass
    
    ClearScreen()
    
    
    Option(0) # New Switch-case function only for Python Version >= 3.10
    
    ExistingList = []
    Output = True
    
    if _Get.VerifyCode(UserInputPlaceCode) : # If PlaceOfBirth Code entered by user is valid
        
        if _Get.VerifyCode(UserInputSchoolCode) : # If School Code entered by user is valid
            
            for i in range(0, 10000) : 
                if Output :
                    ClearScreen()
                    print ("\tGot'cha ------------\n")
                    
                    if not ExistingList :
                        print ("\tEmpty~~ :(\n")
                        
                    for Existing in ExistingList :
                        print ( f"\t{Existing}\n")
                        
                    print ("\t" + "-"*20, "\n")
                    Output = False
                
                FourDigitsNumber = _Get.FourDigitsNumber(i, Gender)
                if FourDigitsNumber == None :
                    continue
                
                InitResponse = _Get()
                Response = InitResponse.Response(BirthDate, UserInputPlaceCode, FourDigitsNumber) 
                    # Response return [Bool, IdentityCode]
                
                Progression = (i / 10000) * 100
                print ("  "*100, end = "\r") # Clear Last Line
                print ( f"Current Progress ({Progression:.1f}%) : {Response[1]}\t{UserInputSchoolCode}", end = "\r")
                
                if not Response[0] : 
                    continue
                                
                InitResponseWithSchool = _Get(SchoolCode = UserInputSchoolCode)
                ResponseWithSchool = InitResponseWithSchool.Response(BirthDate, UserInputPlaceCode, FourDigitsNumber)
                    # Response return [Bool, IdentityCode, SchoolCodeReturn, SchoolNameReturn, StudentNameReturn, PlaceCodeReturn, PlaceNameReturn, AreaCodeReturn, AreaNameReturn]
                    
                if not ResponseWithSchool[0] : 
                    continue
                
                FileDumpWithSchools(ResponseWithSchool)
                ExistingList.append( f"{ResponseWithSchool[1]}\t{ResponseWithSchool[2]}\t{ResponseWithSchool[3]}\t{ResponseWithSchool[4]}\t{ResponseWithSchool[6]}\t{ResponseWithSchool[8]}")
                Output = True
                            
        
        if not _Get.VerifyCode(UserInputSchoolCode) : # If School Code entered by user is invalid
            Areas = _Areas(UserInputPlaceCode).Response() # return (AreasCodeList, AreasNameList)
            
            for i in range(0, 10000) : 
                if Output :
                    ClearScreen()
                    print ("\tGot'cha ------------\n")
                    
                    if not ExistingList :
                        print ("\tEmpty~~ :(\n")
                        
                    for Existing in ExistingList :
                        print ( f"\t{Existing}\n")
                        
                    print ("\t" + "-"*20, "\n")
                    Output = False
                
                FourDigitsNumber = _Get.FourDigitsNumber(i, Gender)
                if FourDigitsNumber == None :
                    continue
                
                InitResponse = _Get()
                Response = InitResponse.Response(BirthDate, UserInputPlaceCode, FourDigitsNumber) 
                    # Response return [Bool, IdentityCode]
                
                if not Response[0] : 
                    
                    Progression = (i / 10000) * 100
                    print ("  "*100, end = "\r") # Clear Last Line
                    print ( f"Current Progress ({Progression:.1f}%) : {Response[1]}", end = "\r")
                    continue

                try :
                    print ("  "*100, end = "\r") # Clear Last Line
                    print ( f"You may press <CTRL + C> to skip finding user {Response[1]}")
                    time.sleep(5)
                    
                    for AreaCode in Areas[0] :
                        Schools = _Schools(UserInputPlaceCode, AreaCode).Response() # return (SchoolsCodeList, SchoolsNameList)
                        
                        for SchoolCode in Schools[0] :
                            if Output :
                                ClearScreen()
                                print ("\tGot'cha ------------\n")
                                
                                if not ExistingList :
                                    print ("\tEmpty~~ :(\n")
                                    
                                for Existing in ExistingList :
                                    print ( f"\t{Existing}\n")
                                    
                                print ("\t" + "-"*20, "\n")
                                
                                print ( f"You may press <CTRL + C> to skip finding user {Response[1]}")
                                Output = False
                                
                            InitResponseWithSchool = _Get(SchoolCode = SchoolCode)
                            ResponseWithSchool = InitResponseWithSchool.Response(BirthDate, UserInputPlaceCode, FourDigitsNumber)
                                # Response return [Bool, IdentityCode, SchoolCodeReturn, SchoolNameReturn, StudentNameReturn, PlaceCodeReturn, PlaceNameReturn, AreaCodeReturn, AreaNameReturn]
                                
                            ProgressionAreas = [Areas[0].index(AreaCode), len(Areas[0])]
                            ProgressionSchools = (Schools[0].index(SchoolCode) / len(Schools[0])) * 100
                            print ("  "*100, end = "\r") # Clear Last Line
                            print ( f"Current Progress ({ProgressionAreas[0]}/{ProgressionAreas[1]})({ProgressionSchools:.1f}%) : {ResponseWithSchool[1]}\t{ResponseWithSchool[2]}\t{ResponseWithSchool[3]}", end = "\r")
                            
                            if not ResponseWithSchool[0] : 
                                continue
                            
                            FileDumpWithSchools(ResponseWithSchool)
                            ExistingList.append( f"{ResponseWithSchool[1]}\t{ResponseWithSchool[2]}\t{ResponseWithSchool[3]}\t{ResponseWithSchool[4]}\t{ResponseWithSchool[6]}\t{ResponseWithSchool[8]}")
                            Output = True
                            
                    else :
                        Output = True
                            
                except KeyboardInterrupt:
                    Output = True
                    continue
                    
    if not _Get.VerifyCode(UserInputPlaceCode) : # If PlaceOfBirth Code entered by user is invalid
        
        if _Get.VerifyCode(UserInputSchoolCode) : # If School Code entered by user is valid
            Places = _PlacesOfBirth.Response() # return (PlacesCodeList, PlacesNameList)
            for PlaceCode in Places[0] :
                
                for i in range(0, 10000) : 
                    if Output :
                        ClearScreen()
                        print ("\tGot'cha ------------\n")
                        
                        if not ExistingList :
                            print ("\tEmpty~~ :(\n")
                            
                        for Existing in ExistingList :
                            print ( f"\t{Existing}\n")
                            
                        print ("\t" + "-"*20, "\n")
                        Output = False
                    
                    FourDigitsNumber = _Get.FourDigitsNumber(i, Gender)
                    if FourDigitsNumber == None :
                        continue
                    
                    InitResponse = _Get()
                    Response = InitResponse.Response(BirthDate, PlaceCode, FourDigitsNumber) 
                        # Response return [Bool, IdentityCode]
                    
                    ProgressionPlaces = [Places[0].index(PlaceCode), len(Places[0])]
                    Progression = (i / 10000) * 100
                    print ("  "*100, end = "\r") # Clear Last Line
                    print ( f"Current Progress ({ProgressionPlaces[0]}/{ProgressionPlaces[1]})({Progression:.1f}%) : {Response[1]}\t{UserInputSchoolCode}", end = "\r")
                    
                    if not Response[0] : 
                        continue
                                    
                    InitResponseWithSchool = _Get(SchoolCode = UserInputSchoolCode)
                    ResponseWithSchool = InitResponseWithSchool.Response(BirthDate, PlaceCode, FourDigitsNumber)
                        # Response return [Bool, IdentityCode, SchoolCodeReturn, SchoolNameReturn, StudentNameReturn, PlaceCodeReturn, PlaceNameReturn, AreaCodeReturn, AreaNameReturn]
                        
                    if not ResponseWithSchool[0] : 
                        continue
                    
                    FileDumpWithSchools(ResponseWithSchool)
                    ExistingList.append( f"{ResponseWithSchool[1]}\t{ResponseWithSchool[2]}\t{ResponseWithSchool[3]}\t{ResponseWithSchool[4]}\t{ResponseWithSchool[6]}\t{ResponseWithSchool[8]}")
                    Output = True
                            
        if not _Get.VerifyCode(UserInputSchoolCode) : # If School Code entered by user is invalid
            Places = _PlacesOfBirth.Response() # return (PlacesCodeList, PlacesNameList)
            
            for PlaceCode in Places[0] :
                Areas = _Areas(PlaceCode).Response() # return (AreasCodeList, AreasNameList)
                
                for i in range(0, 10000) : 
                    if Output :
                        ClearScreen()
                        print ("\tGot'cha ------------\n")
                        
                        if not ExistingList :
                            print ("\tEmpty~~ :(\n")
                            
                        for Existing in ExistingList :
                            print ( f"\t{Existing}\n")
                            
                        print ("\t" + "-"*20, "\n")
                        Output = False
                    
                    FourDigitsNumber = _Get.FourDigitsNumber(i, Gender)
                    if FourDigitsNumber == None :
                        continue
                    
                    InitResponse = _Get()
                    Response = InitResponse.Response(BirthDate, PlaceCode, FourDigitsNumber) 
                        # Response return [Bool, IdentityCode]
                    
                    if not Response[0] : 
                        ProgressionPlaces = [Places[0].index(PlaceCode), len(Places[0])]
                        Progression = (i / 10000) * 100
                        print ("  "*100, end = "\r") # Clear Last Line
                        print ( f"Current Progress ({ProgressionPlaces[0]}/{ProgressionPlaces[1]})({Progression:.1f}%) : {Response[1]}", end = "\r")
                        continue

                    try :
                        print ("  "*100, end = "\r") # Clear Last Line
                        print ( f"You may press <CTRL + C> to skip finding user {Response[1]}")
                        time.sleep(5)
                        
                        for AreaCode in Areas[0] :
                            Schools = _Schools(PlaceCode, AreaCode).Response() # return (SchoolsCodeList, SchoolsNameList)
                            
                            for SchoolCode in Schools[0] :
                                if Output :
                                    ClearScreen()
                                    print ("\tGot'cha ------------\n")
                                    
                                    if not ExistingList :
                                        print ("\tEmpty~~ :(\n")
                                        
                                    for Existing in ExistingList :
                                        print ( f"\t{Existing}\n")
                                        
                                    print ("\t" + "-"*20, "\n")
                                    
                                    print ( f"You may press <CTRL + C> to skip finding user {Response[1]}")
                                    Output = False
                                    
                                InitResponseWithSchool = _Get(SchoolCode = SchoolCode)
                                ResponseWithSchool = InitResponseWithSchool.Response(BirthDate, PlaceCode, FourDigitsNumber)
                                    # Response return [Bool, IdentityCode, SchoolCodeReturn, SchoolNameReturn, StudentNameReturn, PlaceCodeReturn, PlaceNameReturn, AreaCodeReturn, AreaNameReturn]
                                    
                                ProgressionAreas = [Areas[0].index(AreaCode), len(Areas[0])]
                                ProgressionSchools = (Schools[0].index(SchoolCode) / len(Schools[0])) * 100
                                print ("  "*100, end = "\r") # Clear Last Line
                                print ( f"Current Progress ({ProgressionAreas[0]}/{ProgressionAreas[1]})({ProgressionSchools:.1f}%) : {ResponseWithSchool[1]}\t{ResponseWithSchool[2]}\t{ResponseWithSchool[3]}", end = "\r")
                                
                                if not ResponseWithSchool[0] : 
                                    continue
                                
                                FileDumpWithSchools(ResponseWithSchool)
                                ExistingList.append( f"{ResponseWithSchool[1]}\t{ResponseWithSchool[2]}\t{ResponseWithSchool[3]}\t{ResponseWithSchool[4]}\t{ResponseWithSchool[6]}\t{ResponseWithSchool[8]}")
                                Output = True
                                
                        else :
                            Output = True
                                
                    except KeyboardInterrupt:
                        Output = True
                        continue
                        


    Quotes = [
        "I will run as fast as I can to wherever my customer desires. I am the Auto Memories Doll, Violet Evergarden.\n-Violet Evergarden",
        "Do I have any right after I killed so many people as a weapon? I must have prevented them from keeping promises of their own.\n-Violet Evergarden",
        "Live and be free.\n-Gilbert Bougainvillea"
    ]
    
    print ("  "*100, end = "\r") # Clear Last Line
    print (random(Quotes))
    