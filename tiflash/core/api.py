import os

from tiflash.core.core import TIFlash, TIFlashError
from tiflash.utils.ccxml import (CCXMLError, get_device_xml,
                                get_devicetype, get_connection, get_serno,
                                 get_connection_xml, get_ccxml_path)
from tiflash.utils.ccs import find_ccs, get_workspace_dir, FindCCSError
from tiflash.utils import flash_properties
from tiflash.utils import cpus
from tiflash.utils import connections
from tiflash.utils import devices
from tiflash.utils import dss
from tiflash.utils import xds110
from tiflash.utils import detect


class TIFlashAPIError(TIFlashError):
    """Generic TIFlash API Error"""
    pass


def __get_cpu_from_ccxml(ccxml_path, ccs_path):
    """Returns the cpu name determined from the ccxml file

    Args:
        ccxml_path (str): full path to ccxml file
        ccs_path (str): full path to ccs directory

    Returns:
        str: returns cpu name
    """
    device_xml = get_device_xml(ccxml_path, ccs_path)
    cpu = devices.get_cpu(device_xml)

    return cpu


def __handle_ccs(ccs):
    """Takes either ccs version number or path to custom ccs installation and
    verifies and returns the path to the ccs installation

    Args:
        ccs (int or str): can be an int representing the ccs version number to
        use or a str being the custom ccs installation path

    Returns:
        str: returns full path to ccs installation

    Raises:
        FindCCSError: raises error if cannot find ccs installation
    """
    ccs_path = None
    if type(ccs) is str:
        if not os.path.exists(ccs):
            raise FindCCSError(
                "Invalid path to ccs installation: %s" % ccs)
        else:
            ccs_path = ccs

    else:
        ccs_path = find_ccs(ccs)

    return ccs_path

def __generate_ccxml(ccs_path, serno=None,
                   devicetype=None, connection=None, debug=False):
    """Helper function for generating ccxml files using the provided
    information.

    Args:
        ccs_path (str): path to ccs installation
        connection type (str, optional): connection type to use when
            generating new ccxml file
        devicetype (str, optional): devicetype to use when generating new
            ccxml file
        serno (str, optional): serial number to use when creating new
            ccxml file
        debug (bool): option to display all output when running
    """
    devicexml = None
    flash = TIFlash(ccs_path)
    flash.set_debug(on=debug)

    if devicetype is None:
        raise TIFlashError("Could not determine devicetype to use.")

    if connection is None:
        raise TIFlashError("Could not determine connection type to use.")


    ccxml_path = flash.generate_ccxml(connection, devicetype, serno)
    return ccxml_path

def __handle_ccxml_args(ccs_path, ccxml=None, serno=None,
                   devicetype=None, connection=None, **ignored):
    """Takes ccxml arguments and returns a dictionary containing serno,
    devicetype, connection, and ccxml_path.

    Args:
        ccs_path (str): path to ccs installation
        ccxml (str, optional): name (full path) to ccxml file to use
            (only arg needed if ccxml already exists).
        connection type (str, optional): connection type to use when
            generating new ccxml file
        devicetype (str, optional): devicetype to use when generating new
            ccxml file
        serno (str, optional): serial number to use when creating new
            ccxml file
        ignored (dict): any further args are ignored (this allows to just pass
                        **session_args directly to this function)
    Returns:
        dict: dictionary containing serno, devicetype, connection and
        ccxml_path (or None for any key that cannot be determined).
    """
    ccxml_args = {
        'serno': None,
        'devicetype': None,
        'connection': None,
        'ccxml_path' : None,
    }


    # GET CCXML
    if ccxml:
        if os.path.exists(ccxml):
            ccxml_args['ccxml_path'] = ccxml

    elif serno:
        serno_ccxml = get_ccxml_path(serno)
        if serno_ccxml is not None and os.path.exists(serno_ccxml):
            ccxml_args['ccxml_path'] = serno_ccxml

    elif devicetype:
        devicetype_ccxml = get_ccxml_path(devicetype)
        if devicetype_ccxml is not None and os.path.exists(devicetype_ccxml):
            ccxml_args['ccxml_path'] = devicetype_ccxml

    # GET SERNO
    if serno:
        ccxml_args['serno'] = serno
    elif ccxml_args['ccxml_path'] is not None:
        try:
            ccxml_args['serno'] = get_serno(ccxml_path)
        except Exception:
            pass    # Device may not use serial numbers

    # GET DEVICETYPE
    if devicetype:
        ccxml_args['devicetype'] = devicetype
    elif ccxml_args['ccxml_path'] is not None:
        ccxml_args['devicetype']  = get_devicetype(ccxml_args['ccxml_path'])
    elif serno:
        ccxml_args['devicetype'] = devices.get_device_from_serno(serno, ccs_path)

    # GET CONNECTION
    if connection:
        ccxml_args['connection'] = connection
    elif ccxml_args['ccxml_path'] is not None:
        ccxml_args['connection']  = get_connection(ccxml_args['ccxml_path'])
    elif ccxml_args['devicetype'] is not None:
        try:
            device_xml = devices.get_device_xml_from_devicetype(ccxml_args['devicetype'], ccs_path)
            connection_xml = devices.get_default_connection_xml(device_xml, ccs_path)
            ccxml_args['connection'] = connections.get_connection_name(connection_xml)
        except Exception:
            pass    # Not all device xml will have default connection

    return ccxml_args



def __handle_ccxml(ccs_path, ccxml=None, serno=None, devicetype=None,
                    connection=None, fresh=False, debug=False):
    """Takes ccxml args and returns a corresponding ccxml file.

    CCXML args can be an existing ccxml file path itself or the necessary
    components to create a ccxml file. If a serial number or devicetype
    is provided, a check will be done to see if the ccxml file already
    exists. If a serno is provided but not the devicetype and/or
    connection, AND the ccxml needs to be generated, then an attempt
    will be made to get the devicetype and/or connection to use based
    off of the serial number.

    Args:
        ccs_path (str): path to ccs installation
        ccxml (str, optional): name (full path) to ccxml file to use
            (only arg needed if ccxml already exists).
        connection type (str, optional): connection type to use when
            generating new ccxml file
        devicetype (str, optional): devicetype to use when generating new
            ccxml file
        serno (str, optional): serial number to use when creating new
            ccxml file
        fresh (bool): option to force a new (fresh) ccxml file to be generated
        debug (bool): option to display all output when running

    Returns:
        str: full path to ccxml file
    """
    ccxml_path = None
    default_devicetype = None
    default_connection = None
    default_serno = None

    ccxml_args = __handle_ccxml_args(ccs_path, ccxml=ccxml, serno=serno,
                            devicetype=devicetype, connection=connection)
    ccxml_path = ccxml_args['ccxml_path']

    if ccxml and ccxml_path is None:
        raise TIFlashError("Could not find ccxml: %s" % ccxml)

    if ccxml_path is not None:
        default_devicetype = get_devicetype(ccxml_path)
        default_connection = get_connection(ccxml_path)
        try:
            default_serno = get_serno(ccxml_path)
        except Exception:
            pass    # Device may not use serial numbers

        if devicetype is not None and ccxml_args['devicetype'] != default_devicetype:
            fresh = True

        if connection is not None and ccxml_args['connection'] != default_connection:
            fresh = True

        if serno is not None and ccxml_args['serno'] != default_serno:
            fresh = True

    if fresh or ccxml_path is None:
        # Generate ccxml
        ccxml_path = __generate_ccxml(ccs_path, serno=ccxml_args['serno'],
                                     devicetype=ccxml_args['devicetype'],
                                     connection=ccxml_args['connection'],
                                     debug=debug)

    return ccxml_path


def __handle_session(ccs_path, chip=None, timeout=None, devicetype=None,
                     ccxml=None, connection=None, serno=None, debug=False,
                     fresh=False, attach=False):
    """Takes session args and returns a TIFlash object with given session
    settings

    At the very least you'll need to provide a device serno (serial
    number). TIFlash will attempt to determine the rest of the necessary
    information. If any information cannot be determined an error will be
    thrown. In this case you'll need to provide that specific argument.

    Args:
        ccs_path (str): path to ccs installation
        chip (str, optional): chip/cpu name to use when starting a DS session
        timeout (float, optional): timeout value to give command
        ccxml (str): name (full path) to ccxml file to use (only arg needed if
            ccxml already exists).
        devicetype (str): devicetype to use when generating new ccxml file
        connection type (str): connection type to use when generating new
            ccxml file
        serno (str, optional): serialnumber to use when creating new ccxml file
        debug (bool): option to display all output when running
        fresh (bool): option create new ccxml (ignoring if ccxml already exists
            or not)
        attach (bool): option to attach CCS session to device after completing
            an action


    Returns:
        core.TIFlash: returns a TIFlash object with given session settings

    Raises:
        CCXMLError: raises Exception if provided parameters are invalid
    """
    ccxml_path = __handle_ccxml(ccs_path, ccxml=ccxml, devicetype=devicetype,
                            connection=connection, serno=serno, fresh=fresh,
                            debug=debug)

    chip = chip or __get_cpu_from_ccxml(ccxml_path, ccs_path)

    flash = TIFlash(ccs_path)
    flash.set_debug(on=debug)
    flash.set_session(ccxml_path, chip)
    flash.set_timeout(timeout)
    flash.set_attach(attach)
    if attach:
        workspace = os.path.basename(ccxml_path)
        workspace = os.path.splitext(workspace)[0]

        workspace_dir = get_workspace_dir()

        workspace_path = workspace_dir + os.sep + workspace

        flash.set_workspace(workspace_path)

    return flash


def get_connections(ccs=None, search=None):
    """Gets list of all connections installed on machine (ccs installation)

    Args:
        ccs (int or str): Version Number of CCS to use or path to
            custom installation
        search (str): String to filter connections by

    Returns:
        list: list of connection types installed in ccs

    Raises:
        FindCCSError: raises exception if cannot find ccs installation
    """
    ccs_path = __handle_ccs(ccs)

    connection_list = connections.get_connections(ccs_path)

    if search:
        connection_list = [ connection for connection in connection_list \
                            if search in connection ]

    return connection_list


def get_devicetypes(ccs=None, search=None):
    """Gets list of all devicetypes installed on machine (ccs installation)

    Args:
        ccs (int or str): Version Number of CCS to use or path to
            custom installation
        search (str): String to filter devices by

    Returns:
        list: list of device types installed in ccs

    Raises:
        FindCCSError: raises exception if cannot find ccs installation
    """
    ccs_path = __handle_ccs(ccs)

    device_list = devices.get_devicetypes(ccs_path)

    if search:
        device_list = [ dev for dev in device_list if search in dev ]

    return device_list


def get_cpus(ccs=None, search=None):
    """Gets list of all cpus installed on machine (ccs installation)

    Args:
        ccs (int or str): Version Number of CCS to use or path to
            custom installation
        search (str): String to filter cpus by

    Returns:
        list: list of cpus types installed in ccs

    Raises:
        FindCCSError: raises exception if cannot find ccs installation
    """
    ccs_path = __handle_ccs(ccs)

    cpu_list = cpus.get_cpus(ccs_path)

    if search:
        cpu_list = [ cpu for cpu in cpu_list if search in cpu ]

    return cpu_list


def list_options(option_id=None, ccs=None, **session_args):
    """"Gets all options for the session device.

    Args:
        option_id (str, optional): string used to filter options returned

    Returns:
        list(dict): list of option dictionaries
    """
    ccs_path = __handle_ccs(ccs)

    ccxml_args = __handle_ccxml_args(ccs_path, **session_args)

    # Check we received a valid devicetype
    if ccxml_args['devicetype'] is None:
        raise TIFlashError("Could not determine devicetype.")

    # Get devicetype for retrieving properties xml
    devicetype = ccxml_args['devicetype']

    dev_prop_xml = flash_properties.get_device_properties_xml(devicetype, ccs_path)
    gen_prop_xml = flash_properties.get_generic_properties_xml(ccs_path)

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


def print_options(option_id=None, ccs=None, **session_args):
    """"Prints all available options for the session device.

    Args:
        option_id (str, optional): regex string used to filter options printed

    """
    ccs_path = __handle_ccs(ccs)

    flash = __handle_session(ccs_path, **session_args)

    flash.print_options(option_id=option_id)


def get_bool_option(option_id, pre_operation=None, ccs=None,
                    **session_args):
    """Reads and returns the boolean value of the option_id.

    Args:
        option_id (str): Option ID to request the value of. These ids are
            device specific and can viewed using TIFlash.print_options().
        pre_operation (str): Operation to run prior to reading option_id.
        ccs (int or str): Version Number of CCS to use or path to
            custom installation
        session_args (**dict): keyword arguments containing settings for
            the device connection

    Returns:
        bool: Boolean value of option_id

    Raises:
        TIFlashError: raises error if option does not exist
    """

    option_val = get_option(option_id, pre_operation=pre_operation,
                            ccs=ccs, **session_args)

    bool_val = dss.parse_response_bool(option_val)

    return bool_val


def get_float_option(option_id, pre_operation=None, ccs=None,
                     **session_args):
    """Reads and returns the float value of the option_id.

    Args:
        option_id (str): Option ID to request the value of. These ids are
            device specific and can viewed using TIFlash.print_options().
        pre_operation (str): Operation to run prior to reading option_id.
        ccs (int or str): Version Number of CCS to use or path to
            custom installation
        session_args (**dict): keyword arguments containing settings for
            the device connection

    Returns:
        float: Boolean value of option_id

    Raises:
        TIFlashError: raises error if option does not exist
    """

    option_val = get_option(option_id, pre_operation=pre_operation,
                            ccs=ccs, **session_args)

    float_val = dss.parse_response_float(option_val)

    return float_val


def get_option(option_id, pre_operation=None, ccs=None,
               **session_args):
    """Reads and returns the value of the option_id.

    Args:
        option_id (str): Option ID to request the value of. These ids are
            device specific and can viewed using TIFlash.print_options().
        pre_operation (str): Operation to run prior to reading option_id.
        ccs (int or str): Version Number of CCS to use or path to
            custom installation
        session_args (**dict): keyword arguments containing settings for
            the device connection

    Returns:
        str: Value of option_id

    Raises:
        TIFlashError: raises error if option does not exist
    """
    ccs_path = __handle_ccs(ccs)

    flash = __handle_session(ccs_path, **session_args)

    option_val = flash.get_option(option_id, pre_operation)

    return option_val


def reset(options=None, ccs=None, **session_args):
    """Performs a Board Reset on device

      Args:
          options (dict): dictionary of options in the format
              {option_id: option_val}; These options are set first before
              calling reset function.
          ccs (int or str): Version Number of CCS to use or path to
              custom installation
          session_args (**dict): keyword arguments containing settings for
              the device connection

      Returns:
          bool: True if reset was successful; False otherwise
    """
    ccs_path = __handle_ccs(ccs)

    flash = __handle_session(ccs_path, **session_args)

    return flash.reset(options)


def erase(options=None, ccs=None, **session_args):
    """Erases device; setting 'options' before erasing device

      Args:
          options (dict): dictionary of options in the format
              {option_id: option_val}; These options are set first before
              calling erase function.
          ccs (int or str): Version Number of CCS to use or path to
              custom installation
          session_args (**dict): keyword arguments containing settings for
              the device connection

      Returns:
          bool: Result of erase operation (success/failure)

      Raises:
          TIFlashError: raises error if option invalid
    """
    ccs_path = __handle_ccs(ccs)

    flash = __handle_session(ccs_path, **session_args)

    return flash.erase(options)


def verify(image, binary=False, address=None, options=None, ccs=None,
           **session_args):
    """Verifies device; setting 'options' before erasing device

    Args:
        image (str): path to image to use for verifying
        binary (bool): verifies image as binary if True
        address(int): offset address to verify image
        options (dict): dictionary of options in the format
            {option_id: option_val}; These options are set first before
            calling verify function.
        ccs (int or str): Version Number of CCS to use or path to
            custom installation
        session_args (**dict): keyword arguments containing settings for
            the device connection

    Returns:
        bool: Result of verify operation (success/failure)

    Raises:
        TIFlashError: raises error if option invalid
    """
    ccs_path = __handle_ccs(ccs)

    flash = __handle_session(ccs_path, **session_args)

    return flash.verify(image, binary=binary, address=address, options=options)


def flash(image, binary=False, address=None, options=None, ccs=None,
          **session_args):
    """Flashes device; setting 'options' before flashing device

    Args:
        image (str): path to image to use for flashing
        binary (bool): flashes image as binary if True
        address(int): offset address to flash image
        options (dict): dictionary of options in the format
            {option_id: option_val}; These options are set first before
            calling flash function.
        ccs (int or str): Version Number of CCS to use or path to
            custom installation
        session_args (**dict): keyword arguments containing settings for
            the device connection

    Returns:
        bool: Result of flash operation (success/failure)

    Raises:
        TIFlashError: raises error if option invalid
    """
    ccs_path = __handle_ccs(ccs)

    flash = __handle_session(ccs_path, **session_args)

    return flash.flash(image, binary=binary, address=address, options=options)


def memory_read(address, num_bytes=1, page=0, ccs=None, **session_args):
    """Reads specified bytes from memory

    Args:
        address (long): memory address to read from
        num_bytes (int): number of bytes to read
        page (int, optional): page number to read memory from
        ccs (int or str): Version Number of CCS to use or path to
            custom installation
        session_args (**dict): keyword arguments containing settings for
            the device connection

    Returns:
        list: Returns list of bytes read from memory
    """
    ccs_path = __handle_ccs(ccs)

    flash = __handle_session(ccs_path, **session_args)

    return flash.memory_read(address, num_bytes, page)


def memory_write(address, data, page=0, ccs=None, **session_args):
    """Writes specified data to memory

    Args:
        address (long): memory address to read from
        data (list): list of bytes to write to memory
        page (int, optional): page number to read memory from
        ccs (int or str): Version Number of CCS to use or path to
            custom installation
        session_args (**dict): keyword arguments containing settings for
            the device connection

    Raises:
        TIFlashError: raises error when memory read error received
    """
    ccs_path = __handle_ccs(ccs)

    flash = __handle_session(ccs_path, **session_args)

    flash.memory_write(address, data, page=0)


def register_read(regname, ccs=None, **session_args):
    """Reads specified register of device

    Args:
        regname (str): register name to read from
        ccs (int or str): Version Number of CCS to use or path to
            custom installation
        session_args (**dict): keyword arguments containing settings for
            the device connection

    Returns:
        int: value of register

    Raises:
        TIFlashError: raised if regname is invalid
    """
    ccs_path = __handle_ccs(ccs)

    flash = __handle_session(ccs_path, **session_args)

    return flash.register_read(regname)


def register_write(regname, value, ccs=None, **session_args):
    """Writes a value to specified register of device

    Args:
        regname (str): register name to read from
        value (int): value to write to register
        ccs (int or str): Version Number of CCS to use or path to
            custom installation
        session_args (**dict): keyword arguments containing settings for
            the device connection

    Raises:
        TIFlashError: raised if regname is invalid
    """
    ccs_path = __handle_ccs(ccs)

    flash = __handle_session(ccs_path, **session_args)

    return flash.register_write(regname, value)


def evaluate(expr, symbol_file=None, ccs=None, **session_args):
    """Evaluates the given C/GEL expression

    Args:
        expr (str): C or GEL expression
        symbol_file (str): .out or GEL symbol file to load before evaluating
        ccs (int or str): Version Number of CCS to use or path to
            custom installation
        session_args (**dict): keyword arguments containing settings for
            the device connection

    Returns:
        str: String result from evaluating expression

    Raises:
        TIFlashError: raises error when expression error is raised
    """
    ccs_path = __handle_ccs(ccs)

    flash = __handle_session(ccs_path, **session_args)

    return flash.evaluate(expr, symbol_file=symbol_file)


def attach(ccs=None, **session_args):
    """Attach command; opens a CCS session and attaches to device.

    Args:
        ccs (int or str): Version Number of CCS to use or path to
            custom installation
        session_args (**dict): keyword arguments containing settings for
            the device connection

    Raises:
        TIFlashError: raises error when expression error is raised
    """
    # Set attach for session args
    session_args['attach'] = True

    ccs_path = __handle_ccs(ccs)

    flash = __handle_session(ccs_path, **session_args)

    flash.nop()


def nop(ccs=None, **session_args):
    """No-op command. This essentially just calls the dss with the provided
    session args.

    Args:
        ccs (int or str): Version Number of CCS to use or path to
            custom installation
        session_args (**dict): keyword arguments containing settings for
            the device connection

    Raises:
        TIFlashError: raises error when expression error is raised
    """
    ccs_path = __handle_ccs(ccs)

    flash = __handle_session(ccs_path, **session_args)

    flash.nop()


def xds110_reset(ccs=None, **session_args):
    """Calls xds110reset command on specified serno.

    Args:
        ccs (int or str): Version Number of CCS to use or path to
            custom installation
        session_args (**dict): keyword arguments containing settings for
            the device connection

    Returns:
        bool: True if xds110reset was successful

    Raises:
        TIFlashError: raises if serno not set
        XDS110Error: raises if xds110_reset fails
    """
    ccs_path = __handle_ccs(ccs)

    ccxml_args = __handle_ccxml_args(ccs_path, **session_args)

    if ccxml_args['serno'] is None :
        raise TIFlashError("Must provide 'serno' to call xds110_reset")

    return xds110.xds110_reset(ccs_path, serno=ccxml_args['serno'])



def xds110_list(ccs=None, **session_args):
    """Returns list of sernos and xds110 version numbers of connected XDS110 devices.

    Args:
        ccs (int or str): Version Number of CCS to use or path to
            custom installation
        session_args (**dict): keyword arguments containing settings for
            the device connection

    Returns:
        list: list of tuples (serno, version) of connected XDS110 devices

    Raises:
        XDS110Error: raises if xdsdfu does not exist or fails
    """
    ccs_path = __handle_ccs(ccs)

    return xds110.xds110_list(ccs_path)


def xds110_upgrade(ccs=None, **session_args):
    """Upgrades/Flashes XDS110 firmware on board.

    Firmware flashed is found in xds110 directory (firmware.bin). This function
    uses the 'xdsdfu' executable to put device in DFU mode. Then performs the
    flash + reset functions of xdsdfu to flash the firmware.bin image

    Args:
        ccs (int or str): Version Number of CCS to use or path to
            custom installation
        session_args (**dict): keyword arguments containing settings for
            the device connection

    Returns:
        bool: True if successful

    Raises:
        XDS110Error: raises if xds110 firmware update fails
    """

    ccs_path = __handle_ccs(ccs)

    ccxml_args = __handle_ccxml_args(ccs_path, **session_args)

    if ccxml_args['serno'] is None :
        raise TIFlashError("Must provide 'serno' to call xds110_upgrade")

    return xds110.xds110_upgrade(ccs_path, serno=ccxml_args['serno'])

def detect_devices(ccs=None, **session_args):
    """Detect devices connected to machine.

    Returns:
        list: list of dictionaries describing connected devices
    """
    ccs_path = __handle_ccs(ccs)

    device_list = list()
    detected_devices = detect.detect_devices()

    for vid, pid, serno in detected_devices:
        try:
            connection_xml = connections.get_connection_xml_from_vidpid(
                vid, pid, ccs_path)
            connection = connections.get_connection_name(connection_xml)
        except connections.ConnectionsError:
            continue # only include TI Devices

        try:
            devicetype_xml = devices.get_device_xml_from_serno(
                                                    serno, ccs_path)
            devicetype = devices.get_devicetype(devicetype_xml)
        except devices.DeviceError:
            devicetype = None

        dev = { 'connection': connection,
                'devicetype': devicetype,
                'serno':serno }

        device_list.append(dev)

    return device_list
