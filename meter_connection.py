import datetime
import decimal
import logging
import serial
import sys
import threading
import time
import xml.dom.minidom

class MeterConnection(threading.Thread):
    """Represents and maintains a serial connection to the current cost meter
    """
    
    def __init__(this, port, dateOfBirth, messageQueue, baudrate=57600, log=logging.getLogger()):
        """Upon construction, attempts to connect to the current cost meter
        """
        threading.Thread.__init__(this)
        
        this.m_port = serial.Serial(port = port, baudrate= baudrate, timeout = 0)
        this.m_queue = messageQueue
        this.m_buffer = ''
        this.m_startingTagLocation = None
        this.m_log = log
        this.m_run = True
        this.m_refreshRate = 3
        this.m_dayOfBirth = dateOfBirth
        
    def run(this):
        while(this.m_run):
            if(not this.update()):
                this.m_log.debug('Sleeping for {0} seconds'.format(this.m_refreshRate))
                time.sleep(this.m_refreshRate)
            else:
                this.m_log.debug('Additional update required this frame')
        
    def update(this):
        """Runs a single frame update of the meter connection
        
        Returns True if update should be called again this frame.
        Returns False otherwise.
        """
        bytesAvailable = this.m_port.inWaiting()
        if(bytesAvailable > 0):
            this.m_buffer += this.m_port.read(bytesAvailable)
            this.m_log.info('Read ' + str(bytesAvailable) + ' from connection')
            this.m_log.debug(this.m_buffer[-bytesAvailable:])
            
        # Scan for an opening <msg> tag
        if(this.m_startingTagLocation is None):
            startingLocation = this.m_buffer.find('<msg>')
            if(startingLocation >= 0):
                this.m_log.info('Found opening <msg> tag at offset ' + str(startingLocation))
                this.m_buffer = this.m_buffer[startingLocation:]
                this.m_startingTagLocation = 0
            else:
                this.m_log.debug('Did not find an opening <msg> tag')
                return False
            
        if(this.m_startingTagLocation is not None):
            endingLocation = this.m_buffer.find('</msg>')
            if(endingLocation >= 0):
                endingLocation += len('</msg>')
                this.m_log.info('Found closing </msg> tag at offset ' + str(endingLocation))
                this.processXmlString(this.m_buffer[this.m_startingTagLocation:endingLocation])
                this.m_buffer = this.m_buffer[endingLocation:]
                this.m_startingTagLocation = None
                return len(this.m_buffer) > 11
            else:
                this.m_log.debug('Did not find a closing </msg> tag')
                return False
                
        return False
    
    def processXmlString(this, xmlString):
        """Converts the XML string into a dictionary and stores it on the target queue
        """
        this.m_log.debug('Processing xml: ' + xmlString)
        
        # Turn it into an object of key parameters rather than a full string
        try:
            xmlDocument = xml.dom.minidom.parseString(xmlString)
            try:
                sensorData = {'type': 'reading'}
                for node in xmlDocument.documentElement.childNodes:
                    if node.tagName == 'time':
                        timestamp = datetime.datetime.strptime(node.firstChild.nodeValue, '%H:%M:%S')
                        sensorData['time'] = timestamp.time()
                    elif node.tagName == 'dsb':
                        daysSinceBirth = datetime.timedelta(days = int(node.firstChild.nodeValue))
                        sensorData['date'] = this.m_dayOfBirth + daysSinceBirth
                    elif node.tagName == 'hist':
                        this.m_log.debug('Sensor history found!')
                        return
                    elif node.tagName == 'tmpr':
                        sensorData['temperature'] = decimal.Decimal(node.firstChild.nodeValue)
                    elif node.tagName.startswith('ch'):
                        sensorData['channel' + node.tagName[2:]] = int(node.firstChild.firstChild.nodeValue)

                this.m_queue.put(sensorData)
            finally:
                xmlDocument.unlink()
        except:
            this.m_log.exception('Exception while parsing xml string {0}'.format(xmlString))