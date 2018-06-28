import os

from tiflash.core.core import TIFlash, TIFlashError
from tiflash.utils.ccxml import (CCXMLError, get_device_xml,
                                 get_connection_xml, get_ccxml_path)
from tiflash.utils.ccsfinder import find_ccs, FindCCSError
from tiflash.utils import cpus
from tiflash.utils import connections
from tiflash.utils import devices
from tiflash.utils import dss


class TIFlashAPIError(TIFlashError):
    """Generic TIFlash API Error"""
    pass


def __get_connection_from_ccxml(ccxml_path, ccs_path):
    """Returns the connection name determined from the ccxml file

    Args:
        ccxml_path (str): full path to ccxml file
        ccs_path (str): full path to ccs directory

    Returns:
        str: returns devicetype name
    """
    conn_xml = get_connection_xml(ccxml_path, ccs_path)
    connection = connections.get_connection_name(conn_xml)

    return connection


def __get_devicetype_from_ccxml(ccxml_path, ccs_path):
    """Returns the devicetype determined from the ccxml file

    Args:
        ccxml_path (str): full path to ccxml file
        ccs_path (str): full path to ccs directory

    Returns:
        str: returns devicetype name
    """
    device_xml = get_device_xml(ccxml_path, ccs_path)
    devicetype = devices.get_device_name(device_xml)

    return devicetype


def __get_cpu_from_ccxml(ccxml_path, ccs_path):
    """Returns the cpu name determined from the ccxml file

    Args:
        ccxml_path (str): full path to ccxml file
        ccs_path (str): full path to ccs directory

    Returns:
        str: returns cpu name
    """
    device_xml = get_device_xml(ccxml_path, ccs_path)
    cpu_xml = devices.get_cpu_xml(device_xml, ccs_path)
    cpu = cpus.get_cpu_name(cpu_xml)

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


# TODO: This function is shit; need to refactor and clean it up
def __handle_ccxml(ccs_path, ccxml=None, serno=None,
                   devicetype=None, connection=None, fresh=False):
    """Takes ccxml args and returns a corresponding ccxml file.

    CCXML args can be an existing ccxml file path itself or the necessary
    components to create a ccxml file. If a serial number is provided, a check
    will be done to see if the ccxml file already exists. If a serno is
    provided but not the devicetype and/or connection, AND the ccxml needs
    to be generated, then an attempt will be made to get the devicetype
    and/or connection to use based off of the serial number.

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

    """
    ccxml_path = None
    flash = TIFlash(ccs_path)

    # if ccxml provided check it exists
    if ccxml is not None:
        if not os.path.exists(ccxml):
            raise CCXMLError("Provided ccxml file does not exist: %s" % ccxml)

        ccxml_path = ccxml

    # if serno check if ccxml exists already
    elif serno is not None:
        ccxml_path = get_ccxml_path(serno)

    # Get devicetype/connection from ccxml
    if ccxml_path is not None:
        current_devicetype = __get_devicetype_from_ccxml(ccxml_path, ccs_path)
        current_connection = __get_connection_from_ccxml(ccxml_path, ccs_path)

        if devicetype is None or devicetype == current_devicetype:
            devicetype = current_devicetype
        else:
            fresh = True

        if connection is None or connection == current_connection:
            connection = current_connection
        else:
            fresh = True

    # Get devicetype/connection from serno (defaults)
    else:
        # Generate new ccxml
        fresh = True

        # Get default devicetype if none provided
        if devicetype is None:
            try:
                device_xml = devices.get_device_xml_by_serno(serno, ccs_path)
                devicetype = devices.get_device_name(device_xml)
            except Exception:
                pass

        # Get default connection if none provided
        if connection is None:
            try:
                if devicetype is not None:
                    device_xml = devices.get_device_xml(devicetype, ccs_path)
                else:
                    device_xml = devices.get_device_xml_by_serno(
                        serno, ccs_path)
                conn_xml = devices.get_default_connection_xml(
                    device_xml, ccs_path)
                connection = connections.get_connection_name(conn_xml)
            except Exception:
                pass

    # Generate ccxml
    if fresh is True:
        if not devicetype:
            raise connections.ConnectionsError("Could not determine "
                "device type. Please provide device type to use.")

        if not connection:
            raise connections.ConnectionsError("Could not determine "
                "connection type. Please provide connection type to use.")

        ccxml_path = flash.generate_ccxml(connection, devicetype, serno)

    return ccxml_path


def __handle_session(ccs_path, chip=None, devicetype=None, ccxml=None,
                     connection=None, serno=None, debug=False, fresh=False):
    """Takes session args and returns a TIFlash object with given session
    settings

    CCXML args can be the ccxml file name itself or the necessary
    components to create a ccxml file (serno, devicetype, connection type).
    You can also provide the chip name to start a session with. If no chip
    name is provided, an attempt will be made to get the default chip used for
    the given devicetype.

    Args:
        ccs_path (str): path to ccs installation
        chip (str, optional): chip/cpu name to use when starting a DS session
        ccxml (str): name (full path) to ccxml file to use (only arg needed if
            ccxml already exists).
        devicetype (str): devicetype to use when generating new ccxml file
        connection type (str): connection type to use when generating new
            ccxml file
        serno (str, optional): serialnumber to use when creating new ccxml file
        new (bool): option create new ccxml (ignoring if ccxml already exists
            or not)
        debug (bool): option to display all output when running

    Returns:
        core.TIFlash: returns a TIFlash object with given session settings

    Raises:
        CCXMLError: raises Exception if provided parameters are invalid
    """
    ccxml_path = __handle_ccxml(ccs_path, ccxml=ccxml, devicetype=devicetype,
                            connection=connection, serno=serno, fresh=fresh)

    chip = chip or __get_cpu_from_ccxml(ccxml_path, ccs_path)

    flash = TIFlash(ccs_path)
    flash.set_debug(on=debug)
    flash.set_session(ccxml_path, chip)

    return flash


def get_connections(ccs=None):
    """Gets list of all connections installed on machine (ccs installation)

    Args:
        ccs (int or str): Version Number of CCS to use or path to
            custom installation

    Returns:
        list: list of connection types installed in ccs

    Raises:
        FindCCSError: raises exception if cannot find ccs installation
    """
    ccs_path = __handle_ccs(ccs)

    flash = TIFlash(ccs_path)

    connection_list = flash.get_connections()

    return connection_list


def get_devices(ccs=None):
    """Gets list of all devices installed on machine (ccs installation)

    Args:
        ccs (int or str): Version Number of CCS to use or path to
            custom installation

    Returns:
        list: list of device types installed in ccs

    Raises:
        FindCCSError: raises exception if cannot find ccs installation
    """
    ccs_path = __handle_ccs(ccs)

    flash = TIFlash(ccs_path)

    device_list = flash.get_devices()

    return device_list


def get_cpus(ccs=None):
    """Gets list of all cpus installed on machine (ccs installation)

    Args:
        ccs (int or str): Version Number of CCS to use or path to
            custom installation

    Returns:
        list: list of cpus types installed in ccs

    Raises:
        FindCCSError: raises exception if cannot find ccs installation
    """
    ccs_path = __handle_ccs(ccs)

    flash = TIFlash(ccs_path)

    cpu_list = flash.get_cpus()

    return cpu_list


def list_options(option_id=None, ccs=None, **session_args):
    """"Gets all options for the session device.

    Args:
        option_id (str, optional): string used to filter options returned

    Returns:
        list(dict): list of option dictionaries
    """
    ccs_path = __handle_ccs(ccs)

    flash = __handle_session(ccs_path, **session_args)

    return flash.list_options(option_id=option_id)


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
        bin (bool): verifies image as binary if True
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
        bin (bool): flashes image as binary if True
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
