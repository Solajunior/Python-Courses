import os
response = input("Do you want to shutdown your computer? Type yes or no.")
if response == "yes":
 print("Shutting down your computer in 5 seconds...")
os.system("shutdown -s -f -t 5")