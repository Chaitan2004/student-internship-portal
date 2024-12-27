# **Internship Monitoring Software for ECIL.co**

The SIP Software is a specialized database application for managing student internship details at ECIL. It securely stores joining forms, mentor acceptance forms, and facilitates the generation of certificates and due forms. Designed for simplicity and reliability, it ensures efficient data handling and documentation.

# **Installation:**
1)	Install Python
2)	Install MySQL server and MySQL workbench (Set password = 2612)
3)	Install requirements.txt file by running the following command in the terminal.
>> Pip install -r requirements.txt

# **Setting up the Database** 
1)	Create new connection with name “stuint” with the default port 3306 in MySQL Workbench.
2)	Click on the connection to open the connection tab and then click on Server>>Data Import.
3)  After clicking on data import click on the radio button “import from self contained file” and select “studentinternportal.sql” file.
4)  Click on <start import> to import the database.
   
# **Running the SIP software**
Go to the dist folder and click on “stuint.exe” to run the sip software (if exe file is provided).
If you downloaded the code from Github then follow these steps.
  1.	Open a new terminal in the folder where the stuint.py file is located.
  2.	Run “stuint.py” file by using this command in the terminal.
  >> python stuint.py
