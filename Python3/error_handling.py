#function return codes
class RC():
    success= True
    port_failure = 1001
    input_validation = 1002
    parsing_failure = 1003
    command_failure = 1004
    
    
#function return dictionary normal keys
class CR():
    success = 'success'
    debug_data = 'debug_data'
    return_msg = 'return_msg'
    
    
class errorFunctions():
    @staticmethod
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

    @staticmethod    
    def log_exception(function_name=None,action_description=None,exception_object=None,variables=None):
        
        variables_string = ''
        if type(function_name) != str:
            function_name = "Not Specified"
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
        
        output_string = 'expection occured in function: ' + function_name + '. while trying to: ' + action_description + ' .exception: ' + e_str + ' variables: ' + variables_string
        print (output_string)
        return output_string
        
