import database_processor
import meter_connection

import datetime
import logging
import logging.config
import Queue

# Configure application logging
logging.config.fileConfig("config.logging")

# Construct required variables
incomingXmlQueue = Queue.Queue()
meterConnection = meter_connection.MeterConnection('/dev/ttyUSB0', datetime.date(2009, 10, 19), incomingXmlQueue)
registeredProcessors = [
    database_processor.MySQLDatabaseProcessor()
]

# Start workers running
meterConnection.daemon = True
meterConnection.start()

# Pump message queue
try:
    while(True):
        xmlItem = incomingXmlQueue.get(True, 60)
        print xmlItem
        for processor in registeredProcessors:
            try:
                processor.process(xmlItem)
            except:
                logging.exception('Exception while running processor {0}'.format(processor))
                raise
except:
    logging.exception('Exception while pumping incoming message queue')
    