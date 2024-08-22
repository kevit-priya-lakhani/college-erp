import logging

#Create and configure logger using the basicConfig() function  
logging.basicConfig(filename="logfile.log",  
               format='%(asctime)s %(message)s',  
               filemode='w')  
  
#Creating an object of the logging  
logger=logging.getLogger()  

  
logger.setLevel(logging.DEBUG)

# Suppress logs from libraries like Flask, Werkzeug, MongoDB, etc.
# This keeps the log file cleaner, only capturing the messages you explicitly log
logging.getLogger('werkzeug').setLevel(logging.WARNING)
logging.getLogger('flask').setLevel(logging.WARNING)
logging.getLogger('bson').setLevel(logging.WARNING)
logging.getLogger('passlib').setLevel(logging.WARNING)
logging.getLogger('pymongo').setLevel(logging.WARNING)