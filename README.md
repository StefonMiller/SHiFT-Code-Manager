# SHiFT-Code-Manager
In this program, I used Google Sheets API to access an online spreadsheet. This spreadsheet provides users with redeemable codes and information about said codes. The program itself uses PyQT GUI framework for an interface that allows users to both view and add codes to the database.

This project was one of my first experiences with Python, it helped me learn some of its differences from java, particularly its lack of explicitness.  In addition, I have never used Sheets API or any online authentication so figuring out how to use JSON files and such was an obstacle for this particular project.  This was also my first time using a GUI that was actually going to be seen by others, so keeping user experience in mind was another challenge I had to face.  

In order to distribute this software to my friends, I decided to use pyinstaller to create a standalone exe file for a more portable program. At first the exe file would not work, so I had to debug what files were missing from the exe's directory. This was made more difficult with the addition of json files, icon pictures, and GUI elements.

