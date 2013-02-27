import datetime
import MySQLdb

class MySQLDatabaseProcessor():
    """Stores incoming data in a MySQL database
    """
    
    def __init__(this):
        """
        """
        this.m_database = MySQLdb.connect(host = "localhost",
                                           user = "PowerMeter",
                                           passwd = "pqCSj6PNVz3PLsXJ",
                                           db = "PowerMeter")

    def process(this, xmlItem):
        """
        """
        
        if(xmlItem['type'] == 'reading'):
            transaction = this.m_database.cursor()
            try:
                transaction.execute("CALL StoreMeterReading(%s, %s, %s)", 
                    (datetime.datetime.combine(xmlItem['date'], xmlItem['time']), xmlItem['temperature'], xmlItem['channel1']))
            finally:
                transaction.close()

        this.m_database.commit()