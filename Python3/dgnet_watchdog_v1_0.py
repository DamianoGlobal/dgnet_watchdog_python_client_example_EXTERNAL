from datetime import datetime
import requests
import base64
import threading

import time

def parse_exception(action_description=None,exception_object=None,variables=None):    
    variables_string = ''
    e_str = ''
    
    if type(action_description) != str:
        action_description = "Not Specified"
    
    
    if variables != None:
        try:
            variables_string = ' . variables:' +  str(variables) + '.'
        except:
            variables_string = ' . Could not convert variables to strings.'
            
    try:
        e_str = str(exception_object)
    except:
        e_str = "could not convert exception to string"
    
    output_string = 'expection occured while trying to: ' + action_description + ' .exception:' + e_str + variables_string
    return output_string

class ErrorTypes():
    input_validation = 3
    comm_tx = 4
    comm_rx = 5
    
class Datavalidation():



    
    
    def __DeviceID(self,value):
        return_msg = 'DataValidation:__DeviceID '
        debug_data = []
        if type(value)  == str:
            try:
                number_value = int(value)
            except Exception as e:
                return_msg += "value should be a text number. "
                return_msg += parse_exception('converting value to number',e,value)
                return {'success': ErrorTypes.input_validation,
                        'return_msg': return_msg, 'debug_data': debug_data}
        else:
            number_value = value
        
        if number_value > 19999 or number_value < 0:
            return_msg += "device IDs should be between 1 and 19999. its %d" % number_value
            return {'success': False,'return_msg': return_msg, 'debug_data': debug_data} 
        
        return {'success': True,'return_msg': return_msg, 'debug_data': debug_data}
    

    def __AttributeID(self,value):
        return_msg = 'DataValidation:__AttributeID '
        debug_data = []
        if type(value)  == str:
            try:
                number_value = int(value)
            except Exception as e:
                return_msg += "value should be a text number. "
                return_msg += parse_exception('converting value to number',e,value)                
                return {'success': ErrorTypes.input_validation,
                        'return_msg': return_msg, 'debug_data': debug_data}
        else:
            number_value = value
        
        if number_value < 20000 or number_value > 65000:
            return_msg += "attribute IDs should be between 20000 and 65000. its %d" % number_value
            return {'success': False,'return_msg': return_msg, 'debug_data': debug_data} 
        
        return {'success': True,'return_msg': return_msg, 'debug_data': debug_data}
    
        
    def __name(self,value):
        return_msg = 'DataValidation:__name '
        debug_data = []
        
        if type(value) != str:
            return_msg += "names must a type string, this value is a type %s" % type(value)
            return {'success': False,'return_msg': return_msg, 'debug_data': debug_data} 
        
        if len(value) > 150 or len(value) < 1:
            return_msg += "names must be between 1 and 150 characters in length in length and this name is %d long." % len(value)
            return {'success': False,'return_msg': return_msg, 'debug_data': debug_data} 
        
        return {'success': True,'return_msg': return_msg, 'debug_data': debug_data}
    
        
    def __description(self,value):
        return_msg = 'DataValidation:__description '
        debug_data = []
        
        if type(value) != str:
            return_msg += "descriptions must a type string, this value is a type %s" % type(value)
            return {'success': False,'return_msg': return_msg, 'debug_data': debug_data} 
        
        if len(value) > 999:
            return_msg += "descriptions must be 999 or less in length and this name is %d long" % len(value)
            return {'success': False,'return_msg': return_msg, 'debug_data': debug_data} 
        
        return {'success': True,'return_msg': return_msg, 'debug_data': debug_data}
     
    
    def __organization_uid(self,value):
        return_msg = 'DataValidation:__organization_uid '
        debug_data = []
        
        if type(value) != str:
            return_msg += "organization unique identifier must a type string, this value is a type %s" % type(value)
            return {'success': False,'return_msg': return_msg, 'debug_data': debug_data} 
        
        if len(value) != 22:
            return_msg += " organization unique identifier be 22 characters long and this value is %d long. first 100 characters of value are:%s" % (len(value),value[:100])
            return {'success': False,'return_msg': return_msg,'debug_data':debug_data}
        
        
        if value[:5] != "uorg_" and value[:5] != "porg_": 
            return_msg += "prefix should be uorg_ or porg_. first 100 characters of value are:%s" % value[:100]
            return {'success': False,'return_msg': return_msg,'debug_data':debug_data}
        
        return {'success': True,'return_msg': return_msg,'debug_data':debug_data}

    def __deviceData(self,value):
        return_msg = 'DataValidation:__deviceData '
        debug_data = []
        
        if type(value) not in (str,bool,int):
            return_msg += "Device data a str,bool or int type. its a %s type" % type(value)
            return {'success': False,'return_msg': return_msg, 'debug_data': debug_data} 
        
        
        if type(value) == str and len(value) > 10000:
            return_msg += "Device data must be sent in strings of 10000 charactors or less in length and this RX data is %d long" % len(value)
            return {'success': False,'return_msg': return_msg, 'debug_data': debug_data} 
        
        return {'success': True,'return_msg': return_msg, 'debug_data': debug_data}

    def __callback_function(self,value):
        return_msg = 'DataValidation:__callback_function '
        debug_data = []
        
        if callable(value) == False:
            return_msg += "the variable specified as a callback function is not callable. its type is %s" % type(value)
            return {'success': False,'return_msg': return_msg, 'debug_data': debug_data} 
        
        return {'success': True,'return_msg': return_msg, 'debug_data': debug_data}
        
    
    def checkValue(self,rule=None,value=None):
        return_msg = "Datavalidation:checkValue "
        debug_data = []
        
        if rule == None:
            return_msg += "no rule specified"
            return {'success': ErrorTypes.input_validation,
                    'return_msg': return_msg, 'debug_data': debug_data}
        
        if type(rule) != str:
            return_msg += "rule is not a string type its %s" % (type(rule))
            return {'success': ErrorTypes.input_validation,
                    'return_msg': return_msg, 'debug_data': debug_data}
        
        
        #the indexes in this must match function_refs
        rule_list = ("device_id","attribute_id",
                 "name","description",
                     "organization_uid","device_data",
                     "callback_function")
        
        #the indexes in this list much match rule_list
        function_refs = [self.__DeviceID,self.__AttributeID,
                              self.__name,self.__description,
                              self.__organization_uid,self.__deviceData,
                              self.__callback_function]

        
        rule_found = False
        for rule_index,rule_name in enumerate(rule_list):
            if rule == rule_name:
                rule_found = True
                call_result = function_refs[rule_index](value)
                return call_result
        
        if rule_found == False:    
            return_msg += "No rule found with the name %s" % rule
            return {'success': ErrorTypes.input_validation,
                    'return_msg': return_msg, 'debug_data': debug_data}
        


class WatchdogDevice(Datavalidation):
    #~KS any error in the data provided to the class that is incorrect enough to prevent it from communicating with watchdog will be in this list
    validation_errors = []
    
    def __init__(self,device_id=None,name=None,description="",debug_id=""):
        error_msg ="WatchdogDevice:__init__ %s:" % str(debug_id)
        debug_data = []
        self.name = ""
        self.description = ""
        self.id = 0
        self.valid_instance = False
        self.TX_sender_enabled = False
        self.TX_sender_callback = None
        self.TX_data = ""
        self.RX_data = ""
        self.RX_TX_monitoring_enabled = False
        
    ## input validaiton
        debug_data.append(self.checkValue("device_id", device_id))
        debug_data.append(self.checkValue("name", name))
        debug_data.append(self.checkValue("description", description))
        
        validation_failed = False
         
        for data in debug_data:
            if data['success'] != True:
                error_msg += "invalid watchdog device data. debug_data:" + str(debug_data)
                validation_failed = True
        
        if validation_failed == True:
            self.validation_errors.append(error_msg)
            print(error_msg)
            return        
    ##</end> input validaiton
    
        self.name = name
        self.description = description
        self.id = device_id
        self.valid_instance = True
        
            
    def RxListenerCallback(self,new_RX_data,debug_id=""):
        if self.RX_TX_monitoring_enabled != True or self.valid_instance == False: 
            return True
        
        #FIXME add a lockout for if the Watchdog class is building data to send to the server
        error_msg = "WatchdogDevice:RxListenerCallback %s: device id:%d"  % (debug_id,self.id)
        
        if type(new_RX_data) not in (str,int,bool,bytes):
            error_msg += "RX_data must of type str,int or bool the value passed was a %s" % type(new_RX_data)
            print(error_msg)
            return False
        
        #only transmit 10000 characters at a time
        new_RX_data_len = len(new_RX_data)
        if  new_RX_data_len > 10000:
            new_RX_data_len = 10000
            new_RX_data = new_RX_data[-10000:]
        
        if type(new_RX_data) != str:
            new_RX_data = str(new_RX_data)
        
        new_RX_data = datetime.now().strftime("<||:RX~>/%Y/%m/%d-%H-%M-%S:") + base64.urlsafe_b64encode(bytes(new_RX_data.replace("-_.~-","-_|.~-"),"utf-8")).decode("utf-8")
        if len(self.RX_data) + new_RX_data_len > 10000:
            #temp value is since multiple classes read / write this value
            temp_RX_data = ""
            temp_RX_data =  self.RX_data[:(10000-new_RX_data_len)]
            self.RX_data = temp_RX_data + new_RX_data
        else:
            self.RX_data += new_RX_data
        
        return True
            

    def TxListenerCallback(self,new_TX_data,debug_id=""):
        if self.RX_TX_monitoring_enabled != True or self.valid_instance == False:
            return
        #FIXME add a lockout for if the Watchdog class is building data to send to the server
        error_msg = "WatchdogDevice:TxListenerCallback %s: device id:%d"  % (debug_id,self.id)
        
        if type(new_TX_data) not in (str,int,bool,bytes):
            error_msg += "TX_data must of type str,int or bool the value passed was a %s" % type(new_TX_data)
            print(error_msg)
            return False
            
        if type(new_TX_data) != str:
            new_TX_data = str(new_TX_data)

        new_TX_data = datetime.now().strftime("<||:TX~>/%Y/%m/%d-%H-%M-%S:") + base64.urlsafe_b64encode(bytes(new_TX_data.replace("-_.~-","-_|.~-"),"utf-8")).decode("utf-8")
        #only transmit 10000 characters at a time
        new_TX_data_len = len(new_TX_data)
        if  new_TX_data_len > 10000:
            new_TX_data = 10000
            new_TX_data = new_TX_data[-10000:]
        
        if len(self.TX_data) + new_TX_data_len > 10000:
            #temp value is since multiple classes read / write this value
            temp_TX_data =  self.TX_data[:(10000-new_TX_data)]
            self.temp_TX_data = temp_TX_data + new_TX_data
        else:
            self.TX_data +=  new_TX_data
            
        
        return True

    def setTxSenderCallback(self,callback_function,debug_id=""):
    #callback_function will be called when the watchdog server needs to send TX data to the device
        error_msg = "WatchdogDevice:setTxSenderCallback "
        
        validation_failed = False
        if self.valid_instance == False:
            error_msg += "Can't run this function on an  instance with invalid data"
            validation_failed = True
            
        call_result = self.checkValue("callback_function", callback_function)
        if call_result['success'] != True:
            error_msg += ". msg:invalid callback_function input. debug_data:%s" % str(call_result)
            validation_failed = True
        
        if validation_failed == True:
            self.validation_errors.append(error_msg)
            self.valid_instance = False
            print(error_msg)
            return False
        
        self.TX_sender_enabled = True
        self.TX_sender_callback = callback_function
        return True

    
    
class WatchdogAttribute(Datavalidation):
    #~KS any error in the data provided to the class that is incorrect enough to prevent it from communicating with watchdog will be in this list
    validation_errors = []
    
    def __init__(self,attribute_id=None,name=None,description="",debug_id=""):
        error_msg ="WatchdogDevice:__init__ %s:" % str(debug_id)
        debug_data = []
        self.name = ""
        self.description = ""
        self.id = 0
        self.valid_instance = False
    
    ## input validaiton
        debug_data.append(self.checkValue("attribute_id", attribute_id))
        debug_data.append(self.checkValue("name", name))
        debug_data.append(self.checkValue("description", description))
        
        validation_failed = False
         
        for data in debug_data:
            if data['success'] != True:
                error_msg += ". msg:invalid watchdog attribute data. debug_data:" + str(debug_data)
                validation_failed = True
        
        if validation_failed == True:
            self.validation_errors.append(error_msg)
            print(error_msg)
            return
    ##</end> input validaiton
    
        self.name = name
        self.description = description
        self.id = attribute_id
        self.valid_instance = True

#this class is designed to be initilized ONLY from Watch:registerDeviceAttribute() .it has no datavalidation as the Watchdog class does all the datavalidation




class WatchdogDeviceAttribute(Datavalidation):
#this class should be never initilized directly, the watchdog class will do it, input validation is done in the watchdog class instead of here    
    def __init__(self,watchdog_device=None,watchdog_attribute=None,debug_id=""):
        error_msg ="WatchdogDeviceAttribute:__init__ %s:" % str(debug_id)
        self.device = watchdog_device
        self.attribute = watchdog_attribute
        #see setSettableValueType for values
        self.settable_value_type = 0
        #setSettableValuesString for documentation used when settable_value_type is a string
        self.settable_string_values = ""
        
        #min and max values are only used when settable_value_type is an integer
        self.settable_value_min = 0
        self.settable_value_max = 65535
        #this callback will be called with the first argument pa
        self.settable_value_callback = None
        #if validation of any input data has failed, this will be false
        self.valid_instance = True
        #the current value for this device attribute combination
        self.current_value = None
        #the last value for this device attribute combination used to prevent sending the same value over and over
        self.last_value = None
        #flag for if this value needs to be sent to the server
        self.send_value_flag = False
        #flag for if this value needs to be sent instantly to the server
        self.send_value_instantly_flag = False
        #
        self.validation_errors = []
        
    def setSettableValueMinMax(self,minimum,maximum,debug_id=""):
        error_msg = "WatchdogDeviceAttribute:setSettableValueMinMax %s: device id:%d name:%s , attribute id:%d name:%s" % (str(debug_id),self.device.id,self.device.name,self.attribute.id,self.attribute.name)
        
        validation_failed = False 

        if self.settable_value_type != 4:
            error_msg += ". msg:attempting to set a number min/max value on non-number settable value type. settable value type is %d" % self.settable_value_type 
            validation_failed = True

        if type(minimum) != int:
            error_msg += ". msg:minimum should be an int not a %s" % type(minimum)
            validation_failed = True
        elif minimum < 0 or minimum > 65535:
            error_msg += ". msg:minimum should be a number between 0 and 65535. its %d" % minimum
            validation_failed = True
        
        
        if type(maximum) != int:
            error_msg += ". msg:maximum should be an int not a %s" % type(maximum)
            validation_failed = True
        elif maximum < 0 or maximum > 65535:
            error_msg += ". msg:maximum should be a number between 0 and 65535. its %d" % maximum
            validation_failed = True
        
        if validation_failed == False:
            if minimum > maximum:
                error_msg += ". msg:minimum value is greather than the maximum value"
                validation_failed = True
        
        
        if validation_failed == True:
            self.validation_errors.append(error_msg)
            self.valid_instance = False
            print(error_msg)
            return False  
        
        self.settable_value_min = minimum
        self.settable_value_max = maximum
        
        return True
        

    def setSettableValueType(self,value_type=0,debug_id=""):
    #value_type values 2 = string, 3= bool, 4 = integer
        error_msg = "WatchdogDeviceAttribute:setSettableValueType %s: device id:%d name:%s , attribute id:%d name:%s" % (str(debug_id),self.device.id,self.device.name,self.attribute.id,self.attribute.name)
        
        validation_failed = False 

        if type(value_type) != int:
            error_msg += ". msg:value_type should be an int not a %s" % type(value_type)
            validation_failed = True
        elif value_type < 2 or value_type > 4:
            error_msg += ". msg:value_type should be a number between 2 and 4. its %d" % value_type
            validation_failed = True
        
        if validation_failed == True:
            self.validation_errors.append(error_msg)
            self.valid_instance = False
            print(error_msg)
            return False    
        
        #clear all settable value callbacks
        self.settable_string_values = ""
        self.settable_value_number_callback = None
        self.settable_value_bool_callback = None
        
        self.settable_value_type = value_type
        return True
        

    def setSettableValuesString(self,values="",debug_id=""):
    #values should be a comma seperated list of values, the server will split them, the max length of values can only be 999 characters long
        error_msg = "WatchdogDeviceAttribute:addSettableValue %s: device id:%d name:%s , attribute id:%d name:%s" % (str(debug_id),self.device.id,self.device.name,self.attribute.id,self.attribute.name)
        debug_data = []
        
        validation_failed = False
        if self.settable_value_type != 2:
            error_msg += ". msg:attempting to set a string settable value on non-string settable value type. settable value type is %d" % self.settable_value_type 
            validation_failed = True
        else:
            call_result = self.checkValue("description",values)
            if call_result['success'] != True:
                error_msg += ". msg:invalid values input. debug_data:%s" % str(debug_data)
                validation_failed = True
        
        if validation_failed == True:
            self.validation_errors.append(error_msg)
            self.valid_instance = False
            print(error_msg)
            return False
        
        self.settable_string_values = values
        


    def setSettableValueCallback(self,callback_function,debug_id=""):
    #callback_function will be called when the watchdog server sends a value to the processor with the first argument being the received value
        error_msg = "WatchdogDeviceAttribute:addSettableValue %s: device id:%d name:%s , attribute id:%d name:%s" % (str(debug_id),self.device.id,self.device.name,self.attribute.id,self.attribute.name)
        
        call_result = self.checkValue("callback_function", callback_function)
        if call_result['success'] != True:
            error_msg += ". msg:invalid callback_function input. debug_data:%s" % str(call_result)
            self.validation_errors.append(error_msg)
            self.valid_instance = False
            print(error_msg)
            return False
        
        self.settable_value_callback = callback_function
        return True
        
    def callSetValueCallback(self,data,device_id,attribute_id):
        error_msg = "WatchdogDeviceAttribute:callSetValueCallback device id:%d name:%s , attribute id:%d name:%s" % (self.device.id,self.device.name,self.attribute.id,self.attribute.name)
    
    ## convert the incoming value to the right type
        try:
            if self.settable_value_type == 2:
                data = str(data)
            elif self.settable_value_type == 3:
                data = bool(data)
            elif self.settable_value_type == 4:
                data = int(data)
            else:
                error_msg += "DGnet Watchdog is attempting to set a value but this device attribute has an invalid settableValueType of %d" % self.settable_value_type
                return {'success': False, 'error_msg':error_msg}
        except Exception as e:            
            error_msg += parse_exception('converting value from watchdog',e,[self.settable_value_type,data])
            return {'success': False, 'error_msg':error_msg}
    ##</end> convert the incoming value to the right type    

    ## call the callback
        try:
            threading.Thread(target=self.settable_value_callback,kwargs={'wcommand':data,'device_id': device_id, 'attribute_id' : attribute_id}).start()
        except Exception as e:
            error_msg += parse_exception('calling callback function', e,data)
            return {'success': False, 'error_msg':error_msg}
        
        
    ##</end> call the callback
        return {'success': True, 'error_msg':error_msg}


class Watchdog(Datavalidation):
    
    #this is used to prevent multiple instances of the Watchdog class from being created
    instance_created = False
    #used to indicate an issue with the information provided to the class at processor boot up
    boot_up_input_validation_failure = False    
    #used to send multiple device-attribute updates
    multi_update_url = ""
    #~KS used to check if the organization associated with this processor is an active organization
    active_processor_check_url = ""
    #~KS used to send device-attribute updates every 15 seconds
    update_url = "https://monitoring.dgnet.cloud/m1/p1s3t2-update-object-attribute"
    #~KS used to send devcie-attributes instantly
    instant_update_url = "https://monitoring.dgnet.cloud/m1/p1s3t8-priority-update-object-attribute"
    #~KS used to send device RX / TX data and receive TX data to send the device
    rx_tx_traffic_url = "https://monitoring.dgnet.cloud/m1/p1s3t9-tx-rx-data"
    #~KS used to create Device And attribute records in watchdog, only used on processor startup
    create_device_attribute_url = "https://monitoring.dgnet.cloud/m1/p1s3t1-create-object-attribute"
    #used when the processor has no device-attribute updates to send but needs to prevent watchdog from showing it offline
    heartbeat_url = "https://monitoring.dgnet.cloud/m1/p1s3t10-heartbeat"
    # used for sending processor and program logs to Watchdog every 5 minutes
    logging_url = "https://monitoring.dgnet.cloud/m1/p1s3t11-object-logging"
    #list of WatchdogDevice class instances registered with the Watchdog class used for TX and RX callback functions
    devices = []
    #list of WatchdogAttribute class instances registered with the Watchdog class used to prevent duplicate IDs
    attributes = []
    #~KS list of WatchdogDeviceAttribute class instances
    device_attributes = []
    #~KS any error in the data provided to the class that is incorrect enough to prevent it from communicating with watchdog will be in this list
    validation_errors = []
    #~ anything that doesn't fall under validation or comm error
    general_errors = []
    #~errors that occur when communicating with the watchdog server
    communication_errors = []
    #~maximum number of entries to keep in communication_errors
    max_comm_errors = 50
    #~KS bool flag to tell if this processor is associated with an active watchdog organization
    active_processor = False
    #~KS every X seconds a communication must occur to server to prevent it from showing the processor offline, this sets that time
    heartbeat_time = 15
    #the time of the last communication with the server
    last_communication = None
    #this flag will be set to true once the module is ready to send Device Attribute values to the server
    ready_to_send_values = False
    #this flag will be true if we are currently sending data to the server
    disable_monitoring = False
    #custom messages the programmer wants to send back to the watchdog server
    program_log = ""
    #messages from the processor itself
    processor_log = ""
    
    def __init__(self,organization_key1=None,organization_key2=None,processor_name=None,manufacturer=None,model=None,serial=None,mac_address=None,debug_id=""):
        error_msg = "Watchdog:__init__ %s:" % str(debug_id)
        
        if self.instance_created == True:
            error_msg += " an attempt was made to create a second instance of watchdog, only one instance is allowed."
            print(error_msg)
            self.general_errors.append(error_msg)
            return
        
    ## input validaiton
        debug_data = []
        debug_data.append(self.checkValue("name", processor_name))
        debug_data.append(self.checkValue("organization_uid", organization_key1))
        debug_data.append(self.checkValue("organization_uid", organization_key2))
        debug_data.append(self.checkValue("name", manufacturer))
        debug_data.append(self.checkValue("name", model))
        debug_data.append(self.checkValue("name", serial))
        debug_data.append(self.checkValue("name", mac_address))
        
        
        validation_failed = False 
        for data in debug_data:
            if data['success'] != True:
                error_msg += ". msg:invalid DGnet Watchdog init data. debug_data:" + str(debug_data)
                validation_failed = True
        
        
        if validation_failed == True:
            self.boot_up_input_validation_failure = True
            self.validation_errors.append(error_msg)
            print(error_msg)
            return
    ##</end> input validaiton
    
        self.processor_name = processor_name
        self.organization_key1 = organization_key1
        self.organization_key2 = organization_key2
        processor_hardware_uid =  "%s~%s~%s~%s" % (manufacturer,model,serial,mac_address)
        
        processor_hardware_uid = processor_hardware_uid.replace(" ","")
        self.processor_hardware_uid = processor_hardware_uid
        
    
    
    def registerDevice(self,watchdog_device,debug_id=""):
        if self.boot_up_input_validation_failure == True:
            return False
        
        error_msg = "Watchdog:registerDevice %s:" % str(debug_id)
        
    ## input validaiton
        validation_failure = False
        if watchdog_device.__class__.__name__ != "WatchdogDevice":
            error_msg += ". msg:watchdog_device is not a WatchdogDevice class instance"
            validation_failure = True
        elif watchdog_device.valid_instance != True:
            error_msg += ". msg:the WatchdogOjbect class failed its internal validation check"
            validation_failure = True
        
        if validation_failure == True:
            self.boot_up_input_validation_failure = True
            self.validation_errors.append(error_msg)
            print(error_msg)
            return False
    ##</end> input validaiton
    
        for obj in self.devices:
            if watchdog_device.id == obj.id:
                error_msg += ". msg:the device id %d for device %s has already been registered by another device with the name %s " % (watchdog_device.id,watchdog_device.name,obj.name)
                self.boot_up_input_validation_failure = True
                self.validation_errors.append(error_msg)
                print(error_msg)
                return False
        
        self.devices.append(watchdog_device)
        return True
    
    
    def registerAttribute(self,watchdog_attribute,debug_id=""):
        if self.boot_up_input_validation_failure == True:
            return False
        
        error_msg = "Watchdog:registeAttribute %s:" % str(debug_id)
        
    ## input validaiton
        validation_failure = False
        if watchdog_attribute.__class__.__name__ != "WatchdogAttribute":
            error_msg += ". msg:watchdog_attribute is not a WatchdogAttribute class instance"
            validation_failure = True
        elif watchdog_attribute.valid_instance != True:
            error_msg += ". msg:the WatchdogAttribute class failed its internal validation check"
            validation_failure = True
        
        if validation_failure == True:
            self.validation_errors.append(error_msg)
            self.boot_up_input_validation_failure = True
            print(error_msg)
            return False
    ##</end> input validaiton
    
        for attribute in self.attributes:
            if watchdog_attribute.id == attribute.id:
                error_msg += ". msg:the attribute id %d for attribute %s has already been registered by another attribute with the name %s " % (watchdog_attribute.id,watchdog_attribute.name,attribute.name)
                self.validation_errors.append(error_msg)
                self.boot_up_input_validation_failure = True
                print(error_msg)
                return False
        
        self.attributes.append(watchdog_attribute)
        return True
      
        
    def registerDeviceAttribute(self,watchdog_device=None,watchdog_attribute=None,debug_id=""):
        if self.boot_up_input_validation_failure == True:
            return False
        
        error_msg = "Watchdog:registerDeviceAttribute %s:" % str(debug_id)
    ## input validaiton
        validation_failure = False
        
        if watchdog_device.__class__.__name__ != "WatchdogDevice":
            error_msg += ". msg:watchdog_device is not a WatchdogDevice class instance"
            validation_failure = True
        elif watchdog_device.valid_instance != True:
            error_msg += ". msg:the WatchdogOjbect class failed its internal validation check"
            validation_failure = True
        elif watchdog_device not in self.devices:
            error_msg += ". msg:the specified watchdog device with id:%d,name:%s has not been registered with the Watchdog instance" % (watchdog_device.id,watchdog_device.name)
            validation_failure = True
        
        if watchdog_attribute.__class__.__name__ != "WatchdogAttribute":
            error_msg += ". msg:watchdog_attribute is not a WatchdogAttribute class instance"
            validation_failure = True
        elif watchdog_attribute.valid_instance != True:
            error_msg += ". msg:the WatchdogAttribute class failed its internal validation check"
            validation_failure = True
        elif watchdog_attribute not in self.attributes:
            error_msg += ". msg:the specified watchdog attribute with id:%d,name:%s has not been registered with the Watchdog instance" % (watchdog_attribute.id,watchdog_attribute.name)
            validation_failure = True
        
        if validation_failure == True:
            self.validation_errors.append(error_msg)
            self.boot_up_input_validation_failure = True
            print(error_msg)
            return False
    ##</end> input validaiton
        
        
        new_device_attribute = WatchdogDeviceAttribute(watchdog_device,watchdog_attribute)
        self.device_attributes.append(new_device_attribute)
        return new_device_attribute
        
    
    
    def __createDeviceAttributeOnServer(self,device_attribute):
        if self.boot_up_input_validation_failure == True:
            return {'success' : False,'error_msg' :"Watchdog:__createDeviceAttributeOnServer attempt to run this function while input validation failure flag is set"}
        
        error_msg = "Watchdog:__createDeviceAttributeOnServer device id:%d name:%s , attribute id:%d name:%s" % (device_attribute.device.id,device_attribute.device.name,device_attribute.attribute.id,device_attribute.attribute.name)
        
                
        params = {}
        params['processor_name'] = self.processor_name
        params['local_device_id'] = "%d" % (device_attribute.device.id )
        params['device_name']=  device_attribute.device.name
        params['device_description'] =  device_attribute.device.description
        params['local_attribute_id'] = "%d" % (device_attribute.attribute.id)
        params['attribute_name'] =  device_attribute.attribute.name
        params['attribute_description'] =  device_attribute.attribute.description
        params['attribute_type'] = "2"
        params['attribute_value'] =  ""
       
        
        params['settable_value_type'] = "%d" % device_attribute.settable_value_type
        if device_attribute.settable_value_type == 4:
            params['settable_value_min'] = device_attribute.settable_value_min
            params['settable_value_max'] =  device_attribute.settable_value_max
        elif device_attribute.settable_value_type == 2:
            params['settable_string_values'] =  device_attribute.settable_string_values
            
        return self.__sendPostData(self.create_device_attribute_url,params)
        
    def instantUpdateDeviceAttribute(self,device_attribute,value=None,debug_id=""):
        if self.boot_up_input_validation_failure == True:
            return False
        
        error_msg = "Watchdog:instantUpdateDeviceAttribute %s: device id:%d name:%s , attribute id:%d name:%s" % (debug_id,device_attribute.device.id,device_attribute.device.name,device_attribute.attribute.id,device_attribute.attribute.name)
        #we don't want to send "None" as the value and the urlencode will do that if its not a blank value
        if value == None:
            value = ""
        call_result = self.checkValue("device_data",value)
        if call_result['success'] != True:
            error_msg += ". msg:value failed validation with call_result:" + str(call_result)
            print(error_msg)
            return False
            
        send_data = {}
        send_data['update_data'] = ""
        if device_attribute.current_value == value:
            return True
        
        device_attribute.last_value = device_attribute.current_value
        device_attribute.current_value = value
        device_attribute.send_value_instantly_flag = True
        return True
        
    def addProgramLogEntry(self,text,debug_id =""):
        if self.boot_up_input_validation_failure == True:
            return False
        
        error_msg = "Watchdog:addProgramLogEntry %s: " % (debug_id)    
        if text == None:
            return False
        
        call_result = self.checkValue("device_data",text)
        if call_result['success'] != True:
            error_msg += ". msg:value failed validation with call_result:" + str(call_result)
            print(error_msg)
            return False   
        
        if type(text) != str:
            text = str(text)
        
        text = datetime.now().strftime("<||:Message~>/%Y/%m/%d-%H-%M-%S:") + text
        
        #only transmit 100000 characters at a time
        text_len = len(text)
        if  text_len > 10000:
            text_len = 10000
            text = text[-10000:]
        
        
        
        
        if len(self.program_log) + text_len > 10000:
            #temp value is since multiple classes read / write this value
            temp_text_data = ""
            temp_text_data =  self.program_log[:(10000-text_len)]
            self.program_log = temp_text_data + text
        else:
            self.program_log += text
        
        return True
    
        
    def addProcessorLogEntry(self,text,debug_id =""):
        if self.boot_up_input_validation_failure == True:
            return False
        
        error_msg = "Watchdog:addProcessorLogEntry %s: " % (debug_id)    
        if text == None:
            return False
        
        call_result = self.checkValue("device_data",text)
        if call_result['success'] != True:
            error_msg += ". msg:value failed validation with call_result:" + str(call_result)
            print(error_msg)
            return False   
        
        if type(text) != str:
            text = str(text)
        
        text = datetime.now().strftime("<||:Message~>/%Y/%m/%d-%H-%M-%S:") + text
        #only transmit 100000 characters at a time
        text_len = len(text)
        if  text_len > 10000:
            text_len = 10000
            text = text[-10000:]
        
        
        
        
        if len(self.processor_log) + text_len > 10000:
            #temp value is since multiple classes read / write this value
            temp_text_data = ""
            temp_text_data =  self.processor_log[:(10000-text_len)]
            self.processor_log = temp_text_data + text
        else:
            self.processor_log += text
        
        
        return True


    
    def updateDeviceAttribute(self,device_attribute,value=None,debug_id=""):
        if self.boot_up_input_validation_failure == True:
            return False
        
        error_msg = "Watchdog:updateDeviceAttribute %s: device id:%d name:%s , attribute id:%d name:%s" % (debug_id,device_attribute.device.id,device_attribute.device.name,device_attribute.attribute.id,device_attribute.attribute.name)
        #we don't want to send "None" as the value and the urlencode will do that if its not a blank value
        if value == None:
            value = ""
        call_result = self.checkValue("device_data",value)
        if call_result['success'] != True:
            error_msg += ". msg:value failed validation with call_result:" + str(call_result)
            print(error_msg)
            return False
        
        if device_attribute.current_value != value:
            device_attribute.last_value = device_attribute.current_value
            device_attribute.current_value = value
            device_attribute.send_value_flag = True

    
    def __monitoringLogLoop(self):
        if self.boot_up_input_validation_failure == True:
            return False
        
        while 1==1:                        
            error_msg = "Watchdog:__monitoringLogLoop"
            
            send_data = {}
            send_data['update_data'] = ""
            seperator = "-_.~-"
            data_send_flag = False
            
            if len(self.processor_log) > 0:
                send_data['update_data'] += seperator
                send_data['update_data'] += "log_data_19501" 
                send_data['update_data'] += ":"  + str(self.processor_log).replace(seperator,"-_|.~-")
                data_send_flag = True
                self.processor_log = ""
            
            if len(self.program_log) > 0:
                send_data['update_data'] += seperator
                send_data['update_data'] += "log_data_19502" 
                send_data['update_data'] += ":"  + str(self.program_log).replace(seperator,"-_|.~-")
                data_send_flag = True
                self.program_log = ""
            
        
            if data_send_flag == True:
                call_result = self.__sendPostData(self.logging_url,send_data)
            
            time.sleep(600)


    def __RxTxMonitoringLoop(self):
        if self.boot_up_input_validation_failure == True:
            return False
        error_msg = "Watchdog:__RxTxMonitoringLoop"
        while True:
            send_data = {}
            send_data['update_data'] = ""
            seperator = "-_.~-"
            data_send_flag = False
            
            ## if RX / TX monitoring of an object is enabled send the data back
            for device in self.devices:
                if device.RX_TX_monitoring_enabled == True:
                    if device.RX_data != "": 
                        send_data['update_data'] += seperator
                        send_data['update_data'] += "rx_data_" + str(device.id)
                        send_data['update_data'] += ":"  + device.RX_data
                        device.RX_data = ""
                        data_send_flag = True
                        
                    if device.TX_data != "": 
                        send_data['update_data'] += seperator
                        send_data['update_data'] += "tx_data_" + str(device.id)
                        send_data['update_data'] += ":"  + device.TX_data
                        device.TX_data = ""
                        data_send_flag = True
            if data_send_flag == True:
                call_result = self.__sendPostData(self.instant_update_url,send_data)
            
            
            time.sleep(2)
    ##</end> if RX / TX monitoring of an object is enabled send the data back
    
    def __processResponseData(self,RX_data):
        error_msg_prefix = "Watchdog:__processResponseData "
        retry_transaction_flag = False
        retry_time = 0
        transaction_success = False
        header_checksum = 0
        footer_checksum = 0
        #TX data to send to a device
        device_TX_data = []
        #set a device attribute to a value
        device_attribute_values = []
        command = ""
        data = ""
        for message in RX_data.split("<~!!~>"):
        
        ## attempt to parse the message
            if message == "":
                continue
            
            command = ""
            data = ""
            
            try:
                command,data =  message.split(":",1)
            except Exception as e:
                error_msg = error_msg_prefix + parse_exception('parsing message', e,message)
                print(error_msg)
                self.communication_errors.append(error_msg)
                continue
        ## attempt to parse the message  
          
            if command == "retry_transaction":
                retry_transaction_flag = True
                try:
                    retry_time = int(data)
                except Exception as e:
                    retry_time = 30
                
                if retry_time <1:
                    retry_time = 30
                    
                    
            if command == "enable_monitoring":
                self.disable_monitoring = False
            
            if command == "organization_not_active":
                error_msg = error_msg_prefix + "organization not active, disabling monitoring"
                print(error_msg)
                self.communication_errors.append(error_msg)
                self.disable_monitoring = True
            
            if command == "organization_not_found":
                error_msg = error_msg_prefix + "organization not found, disabling monitoring"
                print(error_msg)
                self.communication_errors.append(error_msg)
                self.disable_monitoring = True
            
            if command == "processor_disabled":
                error_msg = error_msg_prefix + "processor disabled, disabling monitoring"
                print(error_msg)
                self.communication_errors.append(error_msg)
                self.disable_monitoring = True
            
            if command == "device_rx_tx_enable":
                try:
                    enable_rx_tx_device_id = int(data)
                except Exception as e:
                    error_msg = error_msg_prefix + parse_exception(" getting device id to enable RX / TX comms on", e,data)                    
                    self.communication_errors.append(error_msg)
                    print(error_msg)
                    continue
                
                for device in self.devices:
                    if device.id == enable_rx_tx_device_id:
                        device.RX_TX_monitoring_enabled = True
            
            
            if command == "device_rx_tx_disable":
                try:
                    enable_rx_tx_device_id = int(data)
                except Exception as e:
                    error_msg = error_msg_prefix + parse_exception("getting device id to disable RX / TX comms on", e,data)
                    self.communication_errors.append(error_msg)
                    print(error_msg)
                    continue
                
                for device in self.devices:
                    if device.id == enable_rx_tx_device_id:
                        device.RX_TX_monitoring_enabled = False

        ### handle object_tx_data_ command
            if command == "device_tx_data":
                try:
                    device_id,attribute_id,tx_data = data.split(":",2)
                    device_id = int(device_id)
                    attribute_id = int(attribute_id)
                except Exception as e:
                    error_msg = error_msg_prefix + parse_exception(" get device id and attribute id for incoming device TX data", e,data)
                    continue
                    
            ## find the device attribute instance and attempt to call the callback function
                device_attribute_found = False
                error_msg = ""
                for device_attribute in Watchdog.device_attributes:
                    if device_attribute.device.id == device_id:
                    ## an attribute_id of 0 means write to the device directly
                        if attribute_id == 0:
                        
                            try:
                                tx_data = base64.decodestring(bytes(tx_data,"utf-8")).decode("utf-8")
                            except Exception as e:
                                error_msg = error_msg_prefix + parse_exception("decoding incoming base64 data for device id incoming device TX data", e,tx_data)                                
                                continue
                                
                            device_attribute_found = True
                        
                            if  device_attribute.device.valid_instance != True:
                                error_msg = error_msg_prefix + "could not send TX data to device id:%d due to the instace not being valid" %  device_attribute.device.id
                                break
                            elif device_attribute.device.TX_sender_enabled == True:
                                try:
                                    device_attribute.device.TX_sender_callback(tx_data)
                                except Exception as e:
                                    error_msg = error_msg_prefix + "exception occured calling callback function for device id:%d" % device_attribute.device.id
                                
                                break
                    ## </end> an attribute_id of 0 means write to the device directly  
                    
                    ## write to device attribute
                        if attribute_id == device_attribute.attribute.id:
                            device_attribute_found = True
                            if  device_attribute.valid_instance != True:
                                error_msg = error_msg_prefix + "could not send TX data to device id:%d, attribute id:%d due to the instace not being valid" %  (device_attribute.device.id,device_attribute.attribute.id)
                                break
                            
                            call_result = device_attribute.callSetValueCallback(tx_data,device_id,attribute_id)
                            if call_result['success'] != True:
                                error_msg += call_result['error_msg']
                            
                            break
                    ##</end> write to device attribute        
                    
                if len(error_msg) > 0:
                    print(error_msg)
                    Watchdog.communication_errors.append(error_msg)
                elif device_attribute_found == False:
                    error_msg = error_msg_prefix + "DGnet Watchdog attempted to send TX data to device id:%d , attribute id:%d but could not find them." % (device_attribute.device.id, device_attribute.attribute.id)
            ##</end> find the device attribute instance  and attempt to call the callback function
            
        ###</end> handle object_tx_data_ command
                    
            if command == "checksum_header":
                try:
                    header_checksum = int(data)
                except Exception as e:
                    error_msg = error_msg_prefix + "exception occurred get header checksum exception:%s . header checksum:%s" % (e,data)
                    self.communication_errors.append(error_msg)
                    print(error_msg)
                    
            if command == "checksum_footer":
                try:
                    footer_checksum = int(data)
                except Exception as e:
                    error_msg = error_msg_prefix + "exception occurred get header checksum exception:%s . header checksum:%s" % (e,data)
                    self.communication_errors.append(error_msg)
                    print(error_msg)
                    
            if command == "transaction_success":
                transaction_success = True
            
            if command == "input_validation_error":
                error_msg = error_msg_prefix + "input validation error:%s" % data
                self.communication_errors.append(error_msg)
                print(error_msg)
            
        
    ## verify we got the entire message
        if header_checksum != footer_checksum or header_checksum == 0 or header_checksum == 0:
            error_msg = error_msg_prefix + "checksum error. header checksum:%d , footer checksum:%d" % (header_checksum,footer_checksum)
            self.communication_errors.append(error_msg)
            print(error_msg)
            retry_transaction_flag = True
    ##</end> verify we got the entire message        
            
        if retry_transaction_flag == True or transaction_success != True:
            return {'retry_flag': True,'retry_time':retry_time}
        
        return {'retry_flag': False,'retry_time':retry_time}
    
    def __sendPostData(self,url,params,retry=True):        
        if self.boot_up_input_validation_failure == True:
            return {'success' : True,'error_msg' :"Watchdog:__sendPostData attempt to run this function while input validation failure flag is set"}
        error_msg_prefix = "Watchdog:__sendPostData "
        params['organization_key1'] = self.organization_key1
        params['organization_key2'] = self.organization_key2
        params['processor_hardware_uid'] = self.processor_hardware_uid
        
        retry_flag = True
        while retry_flag == True:
        
            #since this handles all outgoing traffic check if we need to prune the communication error log here
            if len(self.communication_errors) >= self.max_comm_errors:
                del self.communication_errors[:10] 
            
            error_msg = error_msg_prefix
            try:
                return_value = requests.post(url,data=params,timeout=5)
            except Exception as e:
                error_msg += parse_exception('sending post request',e,url)
                print(error_msg)
                self.communication_errors.append(error_msg)
                time.sleep(10)
                continue
            
            call_result = self.__processResponseData(return_value.text)
            
            if self.disable_monitoring == True:
                time.sleep(3600)
                continue
            
            if call_result['retry_flag'] == True and retry == True:
                retry_flag = True
                time.sleep(call_result['retry_time'])
                continue
            else:
                self.last_communication  = datetime.now()
                retry_flag = False
            
        
        return {'success' : True,'error_msg' :error_msg}
    
    def initServerConn(self):
        error_msg = "Watchdog:initServerConn "
        print("DGnet Watchdog initServerConn starting")
        if self.boot_up_input_validation_failure == True or len(self.validation_errors)  > 0:
            self.boot_up_input_validation_failure = True
            error_msg +="module has validation errors that prevent it from establishing a connection with the server, see Watchdog.validation_errors"
            print(error_msg)
            
    ## validate data before we create it
        for device_attribute in self.device_attributes:
            if (device_attribute.valid_instance != True or
                device_attribute.device.valid_instance != True or
                device_attribute.attribute.valid_instance != True) :
                    error_msg += "DGnet Watchdog will halt. invalid data for device id:%d name:%s , attribute id:%d name:%s" % (device_attribute.device.id,device_attribute.device.name,device_attribute.attribute.id,device_attribute.attribute.name)
                    self.validation_errors.append(error_msg)
                    print(error_msg)
                    self.boot_up_input_validation_failure = True
        
        if self.boot_up_input_validation_failure == True:
            error_msg +="module has validation errors that prevent it from establishing a connection with the server, see Watchdog.validation_errors"
            self.validation_errors.append(error_msg)
            print(error_msg)
            
    ##</end> validate data before we create it
        

        
        
        ## create all the Device Attributes on the server, retry indefinitely until it works    
        start_time = datetime.now()
        for device_attribute in self.device_attributes:
            create_succeeded = False
            while create_succeeded == False:
                call_result = self.__createDeviceAttributeOnServer(device_attribute)
                if call_result['success'] != True:
                    time.sleep(60)
                else:
                    create_succeeded = True
                
                continue
           
        ##</end> create all the Device Attributes on the server, retry indefinitely until it works
        
        self.ready_to_send_values = True
        
        #self.__monitoringLogLoop
        try:
            threading.Thread(target=self.__instantMonitoringLoop).start()
            threading.Thread(target=self.__monitoringLoop).start()
            threading.Thread(target=self.__RxTxMonitoringLoop).start()
        except Exception as e:
            print("failed to start watch loops with exception:%s" % e)
        
        print("DGnet Watchdog initServerConn finished")
        

    def __instantMonitoringLoop(self):
        
        error_msg_prefix = "Watchdog:monitoringLoop"
        while True:
            if self.ready_to_send_values == False:
                time.sleep(1)
                continue
            
            error_msg = error_msg_prefix
            
            seperator = "-_.~-"
            data_to_send_flag = False
            send_data = {}
            send_data['update_data'] = ""
            ## generate device attribute values data
            for device_attribute in self.device_attributes:
                if device_attribute.send_value_instantly_flag == True:
                    send_data['update_data'] += seperator
                    send_data['update_data'] += "update_value_" + str(device_attribute.device.id)
                    send_data['update_data'] += "-" + str(device_attribute.attribute.id)
                    send_data['update_data'] += ":" + str(device_attribute.current_value).replace(seperator,"-_|.~-")
                    device_attribute.send_value_instantly_flag = False
                    data_to_send_flag = True
            ##</end> generate device attribute values data
            if data_to_send_flag == True:
                call_result = self.__sendPostData(self.instant_update_url,send_data)
                #print("sent instant value to DGnet Watchdog")
            else:
                time.sleep(1)
               

    def __monitoringLoop(self):
        
        error_msg_prefix = "Watchdog:monitoringLoop"
        
        while True:
            if self.ready_to_send_values == False:
                time.sleep(15)
                continue
            
            error_msg = error_msg_prefix
            
            seperator = "-_.~-"
            data_to_send_flag = False
            send_data = {}
            send_data['update_data'] = ""
            ## generate device attribute values data
            for device_attribute in self.device_attributes:
                if device_attribute.send_value_flag == True:
                    send_data['update_data'] += seperator
                    send_data['update_data'] += "update_value_" + str(device_attribute.device.id)
                    send_data['update_data'] += "-" + str(device_attribute.attribute.id)
                    send_data['update_data'] += ":" + str(device_attribute.current_value).replace(seperator,"-_|.~-")
                    device_attribute.send_value_flag = False
                    data_to_send_flag = True
            ##</end> generate device attribute values data
            
            if data_to_send_flag == True:
                call_result = self.__sendPostData(self.update_url,send_data)
            else:
                send_data['update_data'] = ""
                call_result = self.__sendPostData(self.heartbeat_url,send_data)
            
            print("checked in with DGnet Watchdog")
            time.sleep(15)
               
          



