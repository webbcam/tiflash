import os

from tiflash.utils import dss
from tiflash.utils import ccxml
from tiflash.utils import connections
from tiflash.utils import devices
from tiflash.utils import cpus
from tiflash.utils import flash_properties
from tiflash.utils import xds110
from tiflash.utils import detect

CMD_DEFAULT_TIMEOUT = 60

class TIFlashError(Exception):
    """Generic TI Flash error"""
    pass


class TIFlash(object):
    """TIFlash class for performing TIFlash commands on an object"""

    def __init__(self, ccs_path):
        """Initializes TIFlash object.

        Args:
            ccs_path (str): Path to ccs directory to use
        """
        self.set_ccs_path(ccs_path)
        self.ccxml = None   # path to ccxml file
        self.chip = None    # chip name to use when starting a session
        self.attach = False
        self.workspace = None
        self.timeout = CMD_DEFAULT_TIMEOUT
        self.args = dict()

    def __run_cmd(self, args):
        """PRIVATE FUNCTION: Runs dss cmd script with given arguments

        This function should be called by wrapper functions that are specific
        to the given arguments (i.e. flash, reset, etc)

        Args:
            args (dict): argument dictionary to use (often a copy of self.args
            with function specific args added)

        Returns:
            (bool, str): returns a tuple of format (result, msg) where result
            is a boolean based off of the success/failure of running the
            command and 'msg' is a string that represents any return value or
            error message passed by javascript side.
        """
        arg_list = dss.format_args(args)

        (retcode, retval) = dss.call_dss(self.dss_path, arg_list,
                                        workspace=self.workspace,
                                        timeout=self.timeout)

        return (retcode, retval)

    def set_debug(self, on=True):
        """Turns debug mode on/off for dss calls.

        Sets/Unsets debug argument in self.args

        Args:
            on (bool): Value to set Debug Mode: True = on; False = off
        """
        # Turn Debugging on
        if on:
            self.args['debug'] = True

        # Turn Debugging off
        elif 'debug' in self.args.keys():
            self.args.pop('debug')

    def set_attach(self, attach=True):
        """Attaches CCS session after action completes.

        Args:
            attach (bool): True = attach; False = do not attach
        """
        if attach:
            self.args['attach'] = True

        # Turn Attach
        elif 'attach' in self.args.keys():
            self.args.pop('attach')

    def set_ccs_path(self, ccs_path):
        """Explicitly sets the ccs_path and updates the dss_path automatically
        """
        self.ccs_path = ccs_path
        self.dss_path = dss.find_dss(ccs_path)

    def set_ccxml(self, ccxml_path):
        """Explicitly set ccxml file to use.

        Sets the ccxml file to use. If None is provided, no ccxml file will be
        used when running commands (which may cause errors if certain commands
        depend on a ccxml set).

        Args:
            ccxml_path (str): full path to ccxml file to use
        """
        if not os.path.exists(ccxml_path):
            raise TIFlashError("Could not find ccxml at: %s" % ccxml_path)

        self.ccxml = ccxml_path
        if 'session' not in self.args.keys():
            self.args['session'] = dict()

        self.args['session']['ccxml'] = ccxml_path

    def set_chip(self, chip):
        """Explicitly set chip to use when starting a Debug Server Session.

        Args:
            chip (str): chip name (you can see chip options running
                get_cpus())
        """
        # TODO: Add verification of chip name

        self.chip = chip
        if 'session' not in self.args.keys():
            self.args['session'] = dict()

        self.args['session']['chip'] = chip

    def set_workspace(self, workspace):
        """Explicitly set workspace to use when starting a Debug Server Session.

        Args:
            workspace (str): workspace name to use
        """

        # Set workspace
        self.workspace = workspace

    def set_timeout(self, timeout):
        """Explicitly set timeout to use when starting a Debug Server Session.

        Args:
            timeout (float): timeout value to give command (in seconds)
        """

        # Set timeout to default if None provided
        if timeout is None:
            timeout = CMD_DEFAULT_TIMEOUT

        self.timeout = timeout

        if 'session' not in self.args.keys():
            self.args['session'] = dict()

        # Adjust timeout for javascript side to be in seconds (default in ms)
        self.args['session']['timeout'] = int(self.timeout * 1000)

    def set_session(self, ccxml_path, chip):
        """Sets the session information (ccxml file to use and chip to use)

        Args:
            ccxml_path (str): full path to ccxml file to use
            chip (str): chip name (you can see chip options running
                get_cpus())
        """

        self.set_ccxml(ccxml_path)
        self.set_chip(chip)

    def generate_ccxml(self, connection, devicetype, serno=None):
        """Generates a ccxml given the serial number, connection type, and
        devicetype.

        Generates a ccxml with javascript using the given connection type
        and devicetype, then uses python to modify and add the serial number

        Args:
            connection (str): connection type to use in ccxml
            devicetype (str): device type to use in ccxml
            serno (str, optional): serial number of device to use for ccxml
        """
        genccxml_args = dict()

        # Add ccxml directory
        ccxml_directory = ccxml.get_ccxml_directory()
        genccxml_args.update({'directory': ccxml_directory})

        # Add ccxml name
        ccxml_name = "%s.ccxml" % (serno or devicetype)
        genccxml_args.update({'ccxml': ccxml_name})

        # Add connection
        genccxml_args.update({'connection': connection})

        # Add devicetype
        genccxml_args.update({'devicetype': devicetype})

        ccxml_path = "%s/%s" % (ccxml_directory, ccxml_name)
        ccxml_path = os.path.normpath(ccxml_path)

        # Make a copy of self.args so we are not modifying directly
        args = self.args.copy()
        # Add genccxml args to self.args
        args.update({'genccxml': genccxml_args})

        (code, msg) = self.__run_cmd(args)
        if not code or not os.path.exists(ccxml_path):
            raise TIFlashError(msg)
            #raise TIFlashError("Could not successfully generate ccxml file")

        # Add serial number to ccxml file
        if serno:
            ccxml.add_serno(ccxml_path, serno, self.ccs_path)

        return ccxml_path

    def get_connections(self):
        """Returns a list of possible connections.

        Connections are based off of the connection drivers installed in CCS

        Returns:
            (list): A list of possible connections based off of the connection
            drivers installed in CCS
        """
        # DSS method of getting connections
        # result = self.get_list("connections")

        # XML Parsing method of getting connections
        result = connections.get_connections(self.ccs_path)

        return result

    def get_devicetypes(self):
        """Returns a list of possible devicetypes.

        Devicetypes are based off of the device drivers installed in CCS

        Returns:
            (list): A list of possible devicetypes based off of the device
            drivers installed in CCS
        """
        # DSS method of getting devicetypes
        # result =  self.get_list("devices")

        # XML Parsing method of getting connections
        result = devices.get_devicetypes(self.ccs_path)

        return result

    def get_cpus(self):
        """Returns a list of possible cpus.

        CPUs are based off of the device drivers installed in CCS

        Returns:
            (list): A list of possible cpus based off of the device
            drivers installed in CCS
        """
        # DSS method of getting cpus
        # result =  self.get_list("cpus")

        # XML Parsing method of getting connections
        result = cpus.get_cpus(self.ccs_path)

        return result

    def get_list(self, list_type):
        """Returns a list of 'list_type' elements.

        'list_type' elements are based off of the 'list_type' drivers
        installed in CCS. this method uses a DebugServer to get these values.
        A quicker way is by parsing the XML files themselves.

        Args:
            list_type (str): type of list to get. this can be lists such as
            connections, device, cpus, etc.

        Returns:
            (list): A list of possible 'list_types' options based off the
            drivers installed in CCS
        """
        list_args = {'list': list_type}

        # Make a copy of self.args so we are not modifying directly
        args = self.args.copy()
        args.update(list_args)

        (code, vals) = self.__run_cmd(args)

        if not code:
            raise TIFlashError("Could not get %s list" % list_type)
        else:
            parsed_vals = dss.parse_response_list(vals)
            return parsed_vals

    def perform_operation(self, operation):
        """Peforms device specifc operation

        Args:
            operation (str): operation to perform (must be supported by device)
        """
        op_args = {'opcode': operation}

        # Make a copy of self.args so we are not modifying directly
        args = self.args.copy()
        args.update({'operation': op_args})

        (code, vals) = self.__run_cmd(args)

        if not code:
            raise TIFlashError("Could not perform operation %s" % operation)
        else:
            # parsed_vals = dss.parse_response_list(vals)
            # return parsed_vals
            return True

    def list_options(self, option_id=None):
        # Get devicetype for retrieving properties xml
        devicexml = ccxml.get_device_xml(self.ccxml, self.ccs_path)
        devicetype = devices.get_devicetype(devicexml)

        dev_prop_xml = flash_properties.get_device_properties_xml(devicetype,
                                                       self.ccs_path)
        gen_prop_xml = flash_properties.get_generic_properties_xml(self.ccs_path)

        property_elements = flash_properties.get_property_elements(dev_prop_xml)
        property_elements.extend(flash_properties.get_property_elements(gen_prop_xml, target="generic"))

        # Convert elements to dictionaries
        options = dict()
        for opt in property_elements:
            opt_dict = flash_properties.parse_property_element(opt)
            options.update(opt_dict)

        # Filter options to only option_id if provided
        if option_id:
            option_keys = list(options.keys())
            for oid in option_keys:
                if option_id not in oid:
                    options.pop(oid)

        return options

    def print_options(self, option_id=None):
        # Make a copy of self.args so we are not modifying directly
        args = self.args.copy()
        if option_id:
            args.update({'printoptions': {'id': option_id}})
        else:
            args.update({'printoptions': True})

        (code, vals) = self.__run_cmd(args)

        if not code:
            raise TIFlashError("Could not print options")
        else:
            # parsed_vals = dss.parse_response_list(vals)
            # return parsed_vals
            return True

    def get_option(self, option_id, pre_operation=None):
        """Get the value of an option.

        Args:
            option_id (str): The name/id of the option to retrieve
            pre_operation (str, optional): An operation to run before
                retrieving the option value.

        Returns:
            (str): Returns the value of the option as a string

        Raises:
            (TIFlashError): Raises error if option does not exist
        """
        operation_args = {'opcode': pre_operation}
        option_args = {'id': option_id}

        # Make a copy of self.args so we are not modifying directly
        args = self.args.copy()
        if pre_operation:
            args.update({'operation': operation_args})

        args.update({'getoption': option_args})

        (code, response) = self.__run_cmd(args)

        if not code:
            raise TIFlashError("Could not get option: %s" % option_id)

        return response

    def set_option(self, option_id, option_val):
        """Sets an option to specified value. Option will persist for all
        functions called after setting. If you want to unset an option you'll
        have to set it to another value or call 'unset_option()'.

        Args:
            option_id (str): id of option to set
            option_val (?): value to set option to
                (type can be str, float, bool)

        Raises:
            (TIFlashError): Raises error if option does not exist
        """
        if 'setoption' not in self.args.keys():
            self.args['setoption'] = dict()

        self.args['setoption'].update({option_id: option_val})

    def set_options(self, options):
        """Sets all options given in 'options' dict.

        Args:
            options (dict): dictionary of options in the format
                {option_id: option_val}; These options are set first before
                calling erase function.

        Raises:
            TIFlashError: raises error if option invalid
        """
        for option_id in options.keys():
            self.set_option(option_id, options[option_id])

    def unset_option(self, option_id):
        """Removes an option that was set from calling 'set_option()'

        Args:
            option_id (str): id of option to set

        Notes:
            Does nothing if option does not exist or is not set in args
        """
        if 'setoption' in self.args.keys():
            if option_id in self.args['setoption'].keys():
                self.args['setoption'].pop(option_id)

            if len(self.args['setoption'].keys()) == 0:
                self.args.pop('setoption')

    def unset_options(self, options):
        """Sets all options given in 'options' dict.

        Args:
            options (dict or list): dictionary or list of options in the
                format {option_id: option_val} or [option_id, option_id]

        Raises:
            TIFlashError: raises error if options is not a dict or list

        Notes:
            Does nothing if option does not exist or is not set in args
        """
        if type(options) is not dict and type(options) is not list:
            raise TIFlashError("""'options' arg must be a dict or list
                of option ids""")

        option_ids = options.keys() if type(options) == dict else options

        for option_id in option_ids:
            self.unset_option(option_id)

    def reset(self, options=None):
        """Performs a Board Reset on device

        Args:
            options (dict): dictionary of options in the format
                {option_id: option_val}; These options are set first before
                calling reset function.

            Returns:
                bool: True if reset was successful; False otherwise
        """
        # Set options before calling reset()
        if options is not None:
            self.set_options(options)

        # Make a copy of self.args so we are not modifying directly
        args = self.args.copy()
        args['reset'] = True

        (code, result) = self.__run_cmd(args)

        # Unset options so they do not persist
        if options is not None:
            self.unset_options(options)

        if not code:
            if result:
                # raise TIFlashError("Could not reset device")
                raise TIFlashError(result)
            return False
        else:
            return True

    def erase(self, options=None):
        """Erases device; setting 'options' before erasing device

        Args:
            options (dict): dictionary of options in the format
                {option_id: option_val}; These options are set first before
                calling erase function.

        Returns:
            bool: Result of erase operation (success/failure)

        Raises:
            TIFlashError: raises error if option invalid
        """

        # Set options before calling erase()
        if options is not None:
            self.set_options(options)

        # Make a copy of self.args so we are not modifying directly
        args = self.args.copy()
        args['erase'] = True

        # call erase()
        (code, result) = self.__run_cmd(args)

        # Unset options so they do not persist
        if options is not None:
            self.unset_options(options)

        if not code:
            if result:
                # raise TIFlashError("Could not erase device")
                raise TIFlashError(result)
            return False
        else:
            return True

    def verify(self, image, binary=False, address=None, options=None):
        """Verifies device; setting 'options' before erasing device

        Args:
            image (str): path to image to use for verifying
            binary (bool): verifies image as binary if True
            address(int): offset address to verify image
            options (dict): dictionary of options in the format
                {option_id: option_val}; These options are set first before
                calling verify function.

        Returns:
            bool: Result of verify operation (success/failure)

        Raises:
            TIFlashError: raises error if option invalid
        """

        verify_args = {'image': image}
        if binary:
            verify_args['bin'] = True
        if address:
            verify_args['address'] = str(address)

        # Set options before calling verify()
        if options is not None:
            self.set_options(options)

        # Make a copy of self.args so we are not modifying directly
        args = self.args.copy()
        args['verify'] = verify_args

        # call verify()
        (code, result) = self.__run_cmd(args)

        # Unset options so they do not persist
        if options is not None:
            self.unset_options(options)

        if not code:
            if result:
                # raise TIFlashError("Could not verify device")
                raise TIFlashError(result)
            return False
        else:
            return True

    def flash(self, image, binary=False, address=None, options=None):
        """Flashes device; setting 'options' before flashing device

        Args:
            image (str): path to image to use for flashing
            binary (bool): flashes image as binary if True
            address(int): offset address to flash image
            options (dict): dictionary of options in the format
                {option_id: option_val}; These options are set first before
                calling flash function.

        Returns:
            bool: Result of flash operation (success/failure)

        Raises:
            TIFlashError: raises error if option invalid
        """
        flash_args = {'image': image}
        if binary:
            flash_args['binary'] = True
        if address:
            flash_args['address'] = str(address)

        # Set options before calling flash()
        if options is not None:
            self.set_options(options)

        # Make a copy of self.args so we are not modifying directly
        args = self.args.copy()
        args['flash'] = flash_args

        # call flash()
        (code, result) = self.__run_cmd(args)

        # Unset options so they do not persist
        if options is not None:
            self.unset_options(options)

        if not code:
            if result:
                # raise TIFlashError("Could not flash device")
                raise TIFlashError(result)
            return False
        else:
            return True

    def memory_read(self, address, num_bytes=1, page=0):
        """Reads specified bytes from memory

        Args:
            address (long): memory address to read from
            num_bytes (int): number of bytes to read
            page (int, optional): page number to read memory from

        Returns:
            list: Returns list of bytes read from memory
        """
        memory_args = {'read': True}
        memory_args['address'] = str(address)
        memory_args['numBytes'] = str(num_bytes)
        memory_args['page'] = str(page)

        # Make a copy of self.args so we are not modifying directly
        args = self.args.copy()
        args['memory'] = memory_args

        # call memory_read
        (code, result) = self.__run_cmd(args)

        if not code:
            raise TIFlashError(result)
        else:
            parsed_result = dss.parse_response_list(result)
            parsed_result.reverse() # Reverse order
            parsed_result = [ int(e) for e in parsed_result ]
            return parsed_result


    def memory_write(self, address, data, page=0):
        """Writes specified data to memory

        Args:
            address (long): memory address to read from
            data (list): list of bytes to write to memory
            page (int, optional): page number to read memory from

        Raises:
            TIFlashError: raises error when memory read error received
        """
        memory_args = {'write': True}
        memory_args['address'] = str(address)
        data = [ str(e) for e in list(data) ]
        memory_args['data'] = ' '.join(data)
        memory_args['page'] = str(page)

        # Make a copy of self.args so we are not modifying directly
        args = self.args.copy()
        args['memory'] = memory_args

        # call memory_write
        (code, result) = self.__run_cmd(args)

        if not code:
            raise TIFlashError(result)

    def evaluate(self, expr, symbol_file=None):
        """Evaluates the given C/GEL expression

        Args:
            expr (str): C or GEL expression
            symbol_file (str): .out or GEL symbol file to load before evaluating

        Returns:
            str: String result from evaluating expression

        Raises:
            TIFlashError: raises error when expression error is raised
        """
        expression_args = {'expression': expr}

        if symbol_file is not None:
            expression_args['symbols'] = symbol_file

        # Make a copy of self.args so we are not modifying directly
        args = self.args.copy()
        args['evaluate'] = expression_args

        # call expression
        (code, result) = self.__run_cmd(args)

        if not code:
            raise TIFlashError(result)

        return result

    def nop(self):
        """No-op command. This essentially just calls the dss script with the
        set arguments.

        Raises:
            TIFlashError: raises error when expression error is raised
        """
        # Make a copy of self.args so we are not modifying directly
        args = self.args.copy()

        # call dss
        (code, result) = self.__run_cmd(args)

        if not code:
            raise TIFlashError(result)

        # No return on a no-op
        #return result

    def xds110_reset(self):
        """Calls xds110_reset command on specified serno.

        Returns:
            bool: True if xds110_reset was successful

        Raises:
            TIFlashError: raises if serno not set
            XDS110Error: raises if xds110_reset fails
        """
        serno = ccxml.get_serno(self.ccxml)

        if not serno:
            raise TIFlashError("Must provide 'serno' to call xds110_reset")

        return xds110.xds110_reset(self.ccs_path, serno=serno)


    def xds110_list(self):
        """Returns a list of sernos of currently connected XDS110 devices

        Returns:
            list: list of sernos of connected XDS110 devices

        Raises:
            XDS110Error: raises if xdsdfu does not exist or fails
        """
        return xds110.xds110_list(self.ccs_path)


    def xds110_upgrade(self):
        """Upgrades/Flashes XDS110 firmware on board.

        Firmware flashed is found in xds110 directory (firmware.bin). This function
        uses the 'xdsdfu' executable to put device in DFU mode. Then performs the
        flash + reset functions of xdsdfu to flash the firmware.bin image

        Returns:
            bool: True if successful/False if unsuccessful

        Raises:
            XDS110Error: raises if xds110 firmware update fails
        """
        serno = ccxml.get_serno(self.ccxml)

        if not serno:
            raise TIFlashError("Must provide 'serno' to call xds110_upgrade")

        return xds110.xds110_upgrade(self.ccs_path, serno=serno)
