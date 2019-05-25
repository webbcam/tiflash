import os
import warnings
from tiflash.utils.ccs import find_ccs
from tiflash.utils.ccxml import (
    get_ccxml_path,
    get_serno,
    get_devicetype,
    get_connection,
)
from tiflash.utils.devices import (
    get_device_from_serno,
    get_device_xml_from_devicetype,
    get_default_connection_xml,
)
from tiflash.utils.connections import get_connection_name


def DEPRECATED(message, stacklevel=1):
    warnings.warn(message, DeprecationWarning, stacklevel=stacklevel)


def resolve_ccs_path(ccs_info):
    """Takes either ccs version number or path to custom ccs installation and
    verifies and returns the path to the ccs installation

    Args:
        ccs_info (str): version number of CCS to use or path to custom installation

    Returns:
        str: returns full path to ccs installation

    Raises:
        Exception: raises error if cannot find ccs installation
    """
    ccs_path = None

    if ccs_info is None:  # Get latest ccs installation
        ccs_path = find_ccs()

    else:

        # Convert any int to str to support backwards-compatibility
        if type(ccs_info) is int:
            ccs = str(ccs_info)

        # check if string is version number or a file path
        try:  # TODO: Hacky? Look into better solution
            int(ccs_info.replace(".", ""))  # Throws error if not a version number
            ccs_path = find_ccs(version=ccs_info)

        except ValueError:
            if not os.path.exists(ccs_info):
                raise FindCCSError("Invalid path to ccs installation: %s" % ccs_info)
            else:
                ccs_path = find_ccs(ccs_prefix=ccs_info)

    return ccs_path


def resolve_ccxml_path(ccxml=None, serno=None, devicetype=None):
    """Attempts to find an existing ccxml file given the above parameters.

    Order of priority:
        1. ccxml: if ccxml path provided (and ccxml file exists), will use this
        2. serno: if serno provided, will look for a ccxml file of the format: <serno>.ccxml
        3. devicetype: if devicetype provided, will look for a ccxml file of the format: <devicetype>.ccxml

    Args:
        ccxml (str, optional): full path to ccxml file
        serno (str, optional): serial number of the device for ccxml file in search of
        devicetype (str, optional): devicetype of the device for ccxml file in search of

    Returns:
        str: full path to ccxml file if one was found

    Raises:
        Exception: raised if no ccxml file was found
    """
    ccxml_path = None

    if ccxml is not None:
        ccxml = os.path.expanduser(ccxml)
        ccxml = os.path.expandvars(ccxml)
        if os.path.exists(ccxml):
            ccxml_path = ccxml
        else:
            raise Exception("Could not find ccxml file: %s" % ccxml)

    elif serno is not None:
        serno_ccxml = get_ccxml_path(serno)
        if serno_ccxml is not None and os.path.exists(serno_ccxml):
            ccxml_path = serno_ccxml

    elif devicetype is not None:
        devicetype_ccxml = get_ccxml_path(devicetype)
        if devicetype_ccxml is not None and os.path.exists(devicetype_ccxml):
            ccxml_path = devicetype_ccxml

    #    if ccxml_path is None:
    #        raise Exception("Could not resolve ccxml path from (%s, %s, %s)" % (ccxml, serno, devicetype))

    return ccxml_path


def resolve_serno(serno=None, ccxml=None):
    """Attempts to find the device serial number from the above parameters.

    Order of priority:
        1. serno: if serno provided, will use this
        2. ccxml: if ccxml provided, will look for a serial number in the ccxml file

    Args:
        serno (str, optional): serial number of the device
        ccxml (str, optional): full path to ccxml file

    Returns:
        str: serial number of device

    Raises:
        Exception: raised if no serial number could be resolved
    """
    resolved_serno = None
    if serno is not None:
        resolved_serno = serno

    elif ccxml is not None:
        try:
            resolved_serno = get_serno(ccxml)
        except Exception:
            pass

    #    if resolved_serno is None:
    #        raise Exception("Could not resolve serno from (%s, %s)" % (serno, ccxml))

    return resolved_serno


def resolve_devicetype(devicetype=None, serno=None, ccxml=None, ccs_path=None):
    """Attempts to find the devicetype from the above parameters.

    Order of priority:
        1. devicetype: if devicetype provided, will use this
        2. ccxml: if ccxml provided, will look for a serial number in the ccxml file
        3. serno: if serno provided, will look-up table to try to detemine
        devicetype

    Args:
        devicetype (str, optional): devicetype name of the device
        ccxml (str, optional): full path to ccxml file
        serno (str, optional): serial number of the device
        ccs_path (str, optional): full path to ccs installation to use

    Returns:
        str: device's devicetype name

    Raises:
        Exception: raised if no devicetype could be resolved
    """
    devtype = None

    if devicetype is not None:
        devtype = devicetype
    elif ccxml is not None:
        devtype = get_devicetype(ccxml)
    elif serno is not None:
        devtype = get_device_from_serno(serno, ccs_path)

    #    if devtype is None:
    #        raise Exception("Could not resolve devicetype from (%s, %s, %s)" % (devicetype, ccxml, serno))

    return devtype


def resolve_connection(connection=None, ccxml=None, devicetype=None, ccs_path=None):
    """Attempts to find the connection from the above parameters.

    Order of priority:
        1. connection: if connection provided, will use this
        2. ccxml: if ccxml provided, will extract the connection from the ccxml
        3. devicetype: if devicetype provided, will look for the default connection in device xml

    Args:
        connection (str, optional): connection name
        ccxml (str, optional): full path to ccxml file
        devicetype (str, optional): devicetype name of the device
        ccs_path (str, optional): full path to ccs installation to use

    Returns:
        str: device's connection name

    Raises:
        Exception: raised if no connection could be resolved
    """
    conn = None
    if connection is not None:
        conn = connection
    elif ccxml is not None:
        conn = get_connection(ccxml)
    elif devicetype is not None:
        try:
            devxml = get_device_xml_from_devicetype(devicetype, ccs_path)
            connxml = get_default_connection_xml(devxml, ccs_path)
            conn = get_connection_name(connxml)
        except:
            pass  # Not all device xml will have default connection

    #    if conn is None:
    #        raise Exception("Could not resolve connection from (%s, %s, %s)" % (connection, ccxml, devicetype))

    return conn


def resolve_session_args(
    ccs_path, ccxml=None, serno=None, devicetype=None, connection=None
):
    """Takes session arguments and resolves any missing arguments

    Args:
        ccs_path (str): full path to ccs to use
        ccxml (str): full path to ccxml file to compare with
        serno (str, optional): serial number of the device
        devicetype (str, optional): devicetype name of the device
        connection (str, optional): connection name

    Returns:
        dict: dictionary containing resolved session arguments
    """
    r_ccxml = resolve_ccxml_path(ccxml=ccxml, serno=serno, devicetype=devicetype)

    r_serno = resolve_serno(serno=serno, ccxml=r_ccxml)

    r_devicetype = resolve_devicetype(
        devicetype=devicetype, serno=r_serno, ccxml=r_ccxml, ccs_path=ccs_path
    )

    r_connection = resolve_connection(
        connection=connection, ccxml=r_ccxml, devicetype=r_devicetype, ccs_path=ccs_path
    )

    return {
        "ccxml": r_ccxml,
        "serno": r_serno,
        "devicetype": r_devicetype,
        "connection": r_connection,
    }


def compare_session_args(ccxml_path, serno=None, devicetype=None, connection=None):
    """Compares provided session args with session args in ccxml file.

    Args:
        ccxml (str): full path to ccxml file to compare with
        serno (str, optional): serial number of the device
        devicetype (str, optional): devicetype name of the device
        connection (str, optional): connection name

    Returns:
        bool: True if ccxml contains same values for session args; False if different
    """
    result = True

    # Check ccxml exists
    if not os.path.exists(ccxml_path):
        raise Exception("Could not find ccxml file: %s" % ccxml_path)

    if serno is not None:
        ccxml_serno = get_serno(ccxml_path)
        result = result and (ccxml_serno == serno)

    if devicetype is not None:
        ccxml_devicetype = get_devicetype(ccxml_path)
        result = result and (ccxml_devicetype == devicetype)

    if connection is not None:
        ccxml_connection = get_connection(ccxml_path)
        result = result and (ccxml_connection == connection)

    return result
