#!/usr/bin/env python

# -*- coding: utf-8 -*-

# Import modules
import os
import pandas as pd
import logging
import zipfile
import configparser
import re

# Class and function definitions

class ResultWriter:
    """
    Class to write output tables
    """

    def __init__(self, workDirPath, infile, log):

        self.logging = log
        self.workDir = workDirPath
        self.infile = infile
        self.combinedOutFileName = os.path.splitext(infile)[0] + "_AllResults.xlsx"
        self.combinedOutFileFullPath = os.path.join(self.workDir, self.combinedOutFileName)
        # self.writer = pd.ExcelWriter(self.combinedOutFileFullPath, engine="openpyxl")

        # Read configUser.ini to get outputName and outPutColumns given by the user
        self.configUser = configparser.ConfigParser()
        self.configUser.read(os.path.join(self.workDir, 'configUser.ini'))

        self.tableFileNames = [] # list with the name of tables added (.tsv here)
        self.finalFileNames = [] # list with name of final files (.xlsx here)


    def addTable(self, fileName, module=None):
        """
        Method used to add file to combined results and (if selected) write it apart.
        If "module" contains the name of a module (e.g. Tagger), the table will be read
        and written with outputName and outputColumns selected by the user (see self.writeTable)
        """

        # open table
        if module: 
            try:
                df = self.openTable(fileName)
            
            except:
                self.logging.error(f"TPErr: Error when reading table: {fileName}")
                return None


        # write apart if selected
        self.writeTable(fileName, df, module) if module else self.finalFileNames.append(fileName)
        
        # add to combined results
        # self.addSheet(fileName, df)

        self.logging.info(f"Table was added: {fileName}")


    def openTable(self, fileName):

        self.logging.info(f"Reading table: {fileName}")
        baseName, extension = os.path.splitext(fileName)

        if extension == ".xls":
            df = pd.read_excel(os.path.join(self.workDir, fileName), engine="xlrd")
        
        if extension == ".xlsx":
            df = pd.read_excel(os.path.join(self.workDir, fileName), engine="openpyxl")
        
        if extension == ".tsv":
            df = pd.read_csv(os.path.join(self.workDir, fileName), sep="\t")
        
        self.tableFileNames.append(fileName)

        self.logging.info(f"Table read")
        
        return df
    

    def writeTable(self, fileName, df, module):
        """
        Write table in an isolated file (xlsx or tsv¿? --> Change the code (Aless and Anna decide...))
        """
        self.logging.info(f"Writing table: {fileName}")

        # Set output name of the table (select between user and default)
        outFileName_noExt, outFileName_ext = self.getOutFileName(fileName, module)
        outFileName = outFileName_noExt + outFileName_ext

        # Get output columns
        outColumnNames = self.getOutColumnNames(df.columns, module)

        if outFileName_ext in ['.xlsx', '.xls']:
            # Execute this if output table is in .xlsx format
            # outFileName = f"{os.path.splitext(fileName)[0]}_{os.path.splitext(self.infile)[0]}.xlsx"
            df.to_excel(os.path.join(self.workDir, outFileName), index=False, engine="openpyxl", columns=outColumnNames)
        
        elif outFileName_ext in ['.tsv']:
            # Execute this if output table is in .tsv format
            #outFileName = f"{os.path.splitext(fileName)[0]}_{os.path.splitext(self.infile)[0]}.tsv"
            df.to_csv(os.path.join(self.workDir, outFileName), index=False, sep="\t", columns=outColumnNames)

        self.finalFileNames.append(outFileName)
        
        self.logging.info(f"Table written")


    def getOutFileName(self, fileName, module):
        """
        Method to get file name of output table for a given module (and its extension),
        considering configUser.ini
        """

        # Get default and user names (then, we select one)
        outFileName_default = f"{os.path.splitext(fileName)[0]}_{os.path.splitext(self.infile)[0]}.tsv"
        outFileName_user = self.configUser[module]['output_name'].strip()

        # If user name match regex, discard default
        outFileName = outFileName_default if not re.fullmatch(r'^[^\\/:*?\"<>|]+$', outFileName_user) else outFileName_user
        
        # Get file extension
        outFileName_ext = os.path.splitext(outFileName)[1]

        # If file extension is different from tsv, xls or xlsx, use tsv.
        outFileName += '.tsv' if outFileName_ext not in ['.tsv', '.xlsx', '.xls'] else ''
    
        return os.path.splitext(outFileName)


    def getOutColumnNames(self, df_columns, module):
        """
        Get name of the columns present in output table of given module
        """

        user_columns_config = [i.strip().lower() for i in self.configUser[module]["output_columns"].split(',')]

        # If user writes {1}, we get df_columns[0]
        user_columns = user_columns_config.copy()
        for i, col in enumerate(user_columns_config):
            matchObj = re.search(r'^{(\d+)}$', col)
            if matchObj:
                indexCol = int(matchObj.groups()[0])-1
                if indexCol < len(df_columns): user_columns[i] = df_columns[indexCol].lower() 
                
        outColumnNames = [i for i in df_columns if i.lower() in  user_columns]
        
        # if there is no column, take all...
        if len(outColumnNames) == 0: outColumnNames = df_columns

        return outColumnNames
        

    def addSheet(self, fileName, df):
        """
        Add sheet to combined excel file
        """
        sheetName = os.path.splitext(fileName)[0]
        df.to_excel(self.writer, index=False, sheet_name=sheetName)
    
    
    def saveCombinedTable(self):
        """
        Save xlsx file with all tables
        """
        self.writer.save()
        self.writer.close()
        self.finalFileNames.append(self.combinedOutFileName)
        self.logging.info(f"File was written: {self.combinedOutFileName}")


    def zipResults(self):
        """
        Make a zip with result tables
        """
        self.logging.info("Make a zip with all result files")

        zipName = f"TurboPutative_results.zip"
        fullPath = os.path.join(self.workDir, zipName)

        with zipfile.ZipFile(fullPath, 'w') as myzip:
            _ = [myzip.write(os.path.join(self.workDir, i), i) for i in self.finalFileNames]
            myzip.close()
        
        # remove files added to zip
        _ = [os.remove(os.path.join(self.workDir, i)) for i in self.finalFileNames]
        
        self.logging.info(f"Zip was created: {zipName}")