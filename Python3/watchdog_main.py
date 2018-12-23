from dgnet_watchdog_v1_0 import Watchdog
from dgnet_watchdog_v1_0 import WatchdogAttribute
from dgnet_watchdog_v1_0 import WatchdogDevice
from error_handling import RC
import threading
import time

def processTvGeneralCommand(wcommand=None,device_id=None,attribute_id=None):
    
    new_power_state = None
    new_input_state = None
    
    if wcommand == 'Power On':
        new_power_state = 'On'        
    elif wcommand == 'Power Off':
        new_power_state = 'Off'
    elif wcommand in ("HDMI 1,HDMI 2,TV Tuner,Digital TV Tuner,DVI,PC"):
        new_input_state = wcommand
        
        
    if new_power_state != None:
        #add logic to send commands to the TV here, normally feedback would be sent to DGnet watchdog after querying the device
        G_watchdog_object.instantUpdateDeviceAttribute(G_device_attributes_dict['tv/power'], 
                                                      new_power_state, 
                                                       'processTvGeneralCommand/power')
            
    if new_input_state != None:
        #add logic to send commands to the TV here, normally feedback would be sent to DGnet watchdog after querying the device
        G_watchdog_object.instantUpdateDeviceAttribute(G_device_attributes_dict['tv/input'], 
                                                      new_input_state, 
                                                       'processTvGeneralCommand/input')
                
    return

def processTvChannelCommand(wcommand=None,device_id=None,attribute_id=None):
    #add your logic to send a command to the TV here, normally feedback would be sent to DGnet watchdog after querying the device
    G_watchdog_object.instantUpdateDeviceAttribute(G_device_attributes_dict['tv/channel'], 
                                                      str(wcommand), 
                                                       'processTvGeneralCommand/channel')
    return

def processTvVolumeCommand(wcommand=None,device_id=None,attribute_id=None):
    #add your logic to send a command to the TV here, normally feedback would be sent to DGnet watchdog after querying the device
    G_watchdog_object.updateDeviceAttribute(G_device_attributes_dict['tv/volume'], 
                                                      str(wcommand) + ' Percent', 
                                                       'processTvGeneralCommand/volume')
    return

def generateTempHumidityData():
    
    temp_fake_data = (66.2,66.7,67,67.5,68,69,70)
    humidity_fake_data = (25,26,27,29,31,32,33)
    fake_data_index = 0
    fake_data_max = 6
    ## inifinite loop to generate fake data
    while True:
        G_watchdog_object.updateDeviceAttribute(G_device_attributes_dict['sensor1/temperature'], 
                                                  str(temp_fake_data[fake_data_index]), 
                                                   'generateTempHumidityData/temperature')
        
        G_watchdog_object.updateDeviceAttribute(G_device_attributes_dict['sensor1/humidity'], 
                                          str(humidity_fake_data[fake_data_index]), 
                                           'generateTempHumidityData/humidity')
        
        fake_data_index += 1
        if fake_data_index > fake_data_max:
            fake_data_index = 0
    ##</end> inifinite loop to generate fake data        
        time.sleep(60)
    
    return

def watchdogInitializationStep1(watchdog_object=None,devices=None,attributes=None,device_attributes=None):    
    return_msg = 'watchdogIinitialization: '
    debug_data = []
    
    
    devices['tv'] = WatchdogDevice(1,"TV","","d1")
    devices['sensor1'] = WatchdogDevice(2,"Enviromental Sensor","","d2")
    
    attributes['power'] =  WatchdogAttribute(20001,"Device Power","","a1")
    attributes['input'] =  WatchdogAttribute(20002,"Active Input","","a2")
    attributes['volume'] = WatchdogAttribute(20003,"Volume","","a3")
    attributes['channel'] = WatchdogAttribute(20004,"Active Channel","","a4")
    attributes['temperature'] = WatchdogAttribute(20005,"Temperature","","a5")
    attributes['humidity'] = WatchdogAttribute(20006,"Humidity","","a6")

## register devices and attributes inside the watchdog class
    for key in devices:
        watchdog_object.registerDevice(devices[key])
            
    for key in attributes:        
        watchdog_object.registerAttribute(attributes[key])
    
    
    if watchdog_object.boot_up_input_validation_failure == True:
        return_msg  += 'failued to do initial setup of DGnet Watchdog devices and attributes'
        debug_data.append(watchdog_object.validation_errors)
        return {'success': RC.input_validation,'return_msg':return_msg,'debug_data':debug_data}
##</end> register devices and attributes inside the watchdog class

## link attributes to their devices
    device_attributes['tv/power'] = watchdog_object.registerDeviceAttribute(devices['tv'],attributes["power"])
    device_attributes['tv/input'] = watchdog_object.registerDeviceAttribute(devices['tv'],attributes["input"])
    device_attributes['tv/volume'] = watchdog_object.registerDeviceAttribute(devices['tv'],attributes["volume"])
    device_attributes['tv/channel'] = watchdog_object.registerDeviceAttribute(devices['tv'],attributes["channel"])
    
    device_attributes['sensor1/temperature'] = watchdog_object.registerDeviceAttribute(devices['sensor1'],attributes["temperature"])
    device_attributes['sensor1/humidity'] = watchdog_object.registerDeviceAttribute(devices['sensor1'],attributes["humidity"])
    
    if watchdog_object.boot_up_input_validation_failure == True:
        return_msg  += 'failued to  link attributes to devices during setup of DGnet Watchdog'
        debug_data.append(watchdog_object.validation_errors)
        return {'success': RC.input_validation,'return_msg':return_msg,'debug_data':debug_data}
##</end> link attributes to their devices

## set up the supplemental control
    device_attributes['tv/power'].setSettableValueType(2)
    device_attributes['tv/power'].setSettableValuesString("Power On,Power Off")
    device_attributes['tv/power'].setSettableValueCallback(processTvGeneralCommand)
    
    device_attributes['tv/input'].setSettableValueType(2)
    device_attributes['tv/input'].setSettableValuesString("HDMI 1,HDMI 2,TV Tuner,Digital TV Tuner,DVI,PC")
    device_attributes['tv/input'].setSettableValueCallback(processTvGeneralCommand)
    
    device_attributes['tv/channel'].setSettableValueType(4)
    device_attributes['tv/channel'].setSettableValueMinMax(0,100)
    device_attributes['tv/channel'].setSettableValueCallback(processTvChannelCommand)
    
    device_attributes['tv/volume'].setSettableValueType(4)
    device_attributes['tv/volume'].setSettableValueMinMax(0,100)
    device_attributes['tv/volume'].setSettableValueCallback(processTvVolumeCommand)       
    ##</end> control for the settings device    
        
    
    if watchdog_object.boot_up_input_validation_failure == True:
        return_msg  += 'failued to setup supplemental control during setup of DGnet Watchdog'
        debug_data.append(watchdog_object.validation_errors)
        return {'success': RC.input_validation,'return_msg':return_msg,'debug_data':debug_data}
##</end> set up the supplemental control    
    
    
    return {'success': RC.success,'return_msg':return_msg,'debug_data':debug_data}

def watchdogInitializationStep2(watchdog_object=None):
    return_msg = 'watchdogInitializationStep2: '
    debug_data = []
    
    ## start functions that continouslly query for changes, these need to run in a separate thread than the DGnet Watchdog thread
    try:
        threading.Thread(target=generateTempHumidityData).start()
    except Exception as e:
        return_msg += "Error: unable to start thread. Exception:%s" % str(e)
        return {'success': RC.input_validation,'return_msg':return_msg,'debug_data':debug_data}
    ##</end> start functions that continouslly query for changes, these need to run in a separate thread than the DGnet Watchdog thread
    
    watchdog_object.initServerConn()
    return {'success': RC.success,'return_msg':return_msg,'debug_data':debug_data}





def Startup():
    call_result = {}
    global G_watchdog_object
    global G_device_attributes_dict
    
    #your client will receive an email with their organization keys.
    org_key1 = ""
    org_key2 = ""
    
    device_serial_number = "12341235acd"
    device_mac_address = "14:B1:C8:00:8E:2F"
    attributes_dict = {}
    devices_dict = {}
    G_watchdog_object = Watchdog(organization_key1=org_key1,organization_key2=org_key2,
             processor_name="DGnet Watchdog Example",manufacturer="TvManufacturer",model="TV_model",serial=device_serial_number,mac_address=device_mac_address)
    
    #locally register all the devices and attributes
    call_result = watchdogInitializationStep1(G_watchdog_object, devices_dict, attributes_dict, G_device_attributes_dict)
    if(call_result['success'] != True):
        print (call_result)
        return
    
    #create the devices and attributes in the cloud service and start any needed threads for monitoring values
    call_result = watchdogInitializationStep2(G_watchdog_object)
    if(call_result['success'] != True):
        print (call_result)
        return


G_watchdog_object = None
G_device_attributes_dict = {}

Startup()