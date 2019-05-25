import os
from platform import python_version

from tiflash.core.helpers import resolve_ccs_path
from tiflash.version import version_string as __version__, release_date
from tiflash.core.core import TIFlashSession, TIFlashError
from tiflash.core.helpers import resolve_session_args
from tiflash.utils.ccxml import (
    CCXMLError,
    get_device_xml,
    get_devicetype,
    get_connection,
    get_serno,
    get_connection_xml,
    get_ccxml_path,
    get_ccxml_directory,
)
from tiflash.utils.ccs import (
    find_ccs,
    get_workspace_dir,
    FindCCSError,
    get_ccs_version,
    get_ccs_prefix,
    get_ccs_pf_filters,
)
from tiflash.utils import flash_properties
from tiflash.utils import cpus
from tiflash.utils import connections
from tiflash.utils import devices
from tiflash.utils import dss
from tiflash.utils import xds110
from tiflash.utils import detect


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


def get_connections(ccs=None, search=None):
    """Gets list of all connections installed on machine (ccs installation)

    Args:
        search (str): String to filter connections by
        ccs (str): version number of CCS to use or path to custom installation

    Returns:
        list: list of connection types installed in ccs

    Raises:
        FindCCSError: raises exception if cannot find ccs installation
    """
    ccs_path = resolve_ccs_path(ccs)

    connection_list = connections.get_connections(ccs_path)

    if search:
        connection_list = [
            connection for connection in connection_list if search in connection
        ]

    return connection_list


def get_devicetypes(ccs=None, search=None):
    """Gets list of all devicetypes installed on machine (ccs installation)

    Args:
        search (str): String to filter devices by
        ccs (str): version number of CCS to use or path to custom installation

    Returns:
        list: list of device types installed in ccs

    Raises:
        FindCCSError: raises exception if cannot find ccs installation
    """
    ccs_path = resolve_ccs_path(ccs)

    device_list = devices.get_devicetypes(ccs_path)

    if search:
        device_list = [dev for dev in device_list if search in dev]

    return device_list


def get_cpus(ccs=None, search=None):
    """Gets list of all cpus installed on machine (ccs installation)

    Args:
        search (str): String to filter cpus by
        ccs (str): version number of CCS to use or path to custom installation

    Returns:
        list: list of cpus types installed in ccs

    Raises:
        FindCCSError: raises exception if cannot find ccs installation
    """
    ccs_path = resolve_ccs_path(ccs)

    cpu_list = cpus.get_cpus(ccs_path)

    if search:
        cpu_list = [cpu for cpu in cpu_list if search in cpu]

    return cpu_list


def list_options(option_id=None, ccs=None, **session_args):
    """"Gets all options for the session device.

    Args:
        option_id (str, optional): string used to filter options returned
        ccs (str): version number of CCS to use or path to custom installation

    Returns:
        list(dict): list of option dictionaries
    """
    ccs_path = resolve_ccs_path(ccs)

    serno = session_args.get("serno", None)
    devicetype = session_args.get("devicetype", None)
    connection = session_args.get("connection", None)
    ccxml = session_args.get("ccxml", None)

    session = resolve_session_args(
        ccs_path, ccxml=ccxml, connection=connection, devicetype=devicetype, serno=serno
    )

    # Check we received a valid devicetype
    if session["devicetype"] is None:
        raise TIFlashError("Could not determine devicetype.")

    # Get devicetype for retrieving properties xml
    devicetype = session["devicetype"]

    dev_prop_xml = flash_properties.get_device_properties_xml(devicetype, ccs_path)
    gen_prop_xml = flash_properties.get_generic_properties_xml(ccs_path)

    property_elements = flash_properties.get_property_elements(dev_prop_xml)
    property_elements.extend(
        flash_properties.get_property_elements(gen_prop_xml, target="generic")
    )

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


def get_option(option_id, pre_operation=None, ccs=None, **session_args):
    """Reads and returns the value of the option_id.

    Args:
        option_id (str): Option ID to request the value of. These ids are
            device specific and can viewed using TIFlash.print_options().
        pre_operation (str): Operation to run prior to reading option_id.
        ccs (str): version number of CCS to use or path to custom installation
        session_args (**dict): keyword arguments containing settings for
            the device connection

    Returns:
        str: Value of option_id

    Raises:
        TIFlashError: raises error if option does not exist
    """
    ccs_path = resolve_ccs_path(ccs)

    dev = TIFlashSession(ccs_path=ccs_path, **session_args)
    if "chip" not in session_args.keys():
        core = __get_cpu_from_ccxml(dev.get_config(), ccs_path)
    else:
        core = session_args["chip"]

    dev.core = dev.get_core(core)
    dev.core.connect()

    if pre_operation is not None:
        dev.core.perform_operation(pre_operation)
    option_val = dev.core.get_option(option_id)

    return option_val


def set_option(option_id, option_val, post_operation=None, ccs=None, **session_args):
    """Sets the value of the option_id.

    Args:
        option_id (str): Option ID to set value of. These ids are
            device specific and can viewed using TIFlash.print_options().
        option_val (str or int): Value to set option to.
        post_operation (str): Operation to run after to setting option_id.
        ccs (str): version number of CCS to use or path to custom installation
        session_args (**dict): keyword arguments containing settings for
            the device connection

    Raises:
        TIFlashError: raises error if option does not exist
    """
    ccs_path = resolve_ccs_path(ccs)

    dev = TIFlashSession(ccs_path=ccs_path, **session_args)
    if "chip" not in session_args.keys():
        core = __get_cpu_from_ccxml(dev.get_config(), ccs_path)
    else:
        core = session_args["chip"]

    dev.core = dev.get_core(core)
    dev.core.connect()

    dev.core.set_option(option_id, option_val)

    if post_operation is not None:
        dev.core.perform_operation(post_operation)


def reset(ccs=None, options=None, **session_args):
    """Performs a Board Reset on device

      Args:
          ccs (str): version number of CCS to use or path to custom installation
          options (dict): dictionary of options in the format
              {option_id: option_val}; These options are set first before
              calling reset function.
          session_args (**dict): keyword arguments containing settings for
              the device connection

      Returns:
          bool: True if reset was successful; False otherwise
    """
    ccs_path = resolve_ccs_path(ccs)

    dev = TIFlashSession(ccs_path=ccs_path, **session_args)
    if "chip" not in session_args.keys():
        core = __get_cpu_from_ccxml(dev.get_config(), ccs_path)
    else:
        core = session_args["chip"]

    dev.core = dev.get_core(core)
    dev.core.connect()
    if options is not None:
        for optionID in options.keys():
            dev.core.set_option(optionID, options[optionID])
    dev.core.reset()

    return True


def erase(ccs=None, options=None, **session_args):
    """Erases device; setting 'options' before erasing device

      Args:
          options (dict): dictionary of options in the format
              {option_id: option_val}; These options are set first before
              calling erase function.
          ccs (str): version number of CCS to use or path to custom installation
          session_args (**dict): keyword arguments containing settings for
              the device connection

      Returns:
          bool: Result of erase operation (success/failure)

      Raises:
          TIFlashError: raises error if option invalid
    """
    ccs_path = resolve_ccs_path(ccs)

    dev = TIFlashSession(ccs_path=ccs_path, **session_args)
    if "chip" not in session_args.keys():
        core = __get_cpu_from_ccxml(dev.get_config(), ccs_path)
    else:
        core = session_args["chip"]

    dev.core = dev.get_core(core)
    dev.core.connect()
    if options is not None:
        for optionID in options.keys():
            dev.core.set_option(optionID, options[optionID])
    dev.core.erase()

    return True


def verify(image, binary=False, address=None, options=None, ccs=None, **session_args):
    """Verifies device; setting 'options' before erasing device

    Args:
        image (str): path to image to use for verifying
        binary (bool): verifies image as binary if True
        address(int): offset address to verify image
        options (dict): dictionary of options in the format
            {option_id: option_val}; These options are set first before
            calling verify function.
        ccs (str): version number of CCS to use or path to custom installation
        session_args (**dict): keyword arguments containing settings for
            the device connection

    Returns:
        bool: Result of verify operation (success/failure)

    Raises:
        TIFlashError: raises error if option invalid
    """
    ccs_path = resolve_ccs_path(ccs)

    dev = TIFlashSession(ccs_path=ccs_path, **session_args)
    if "chip" not in session_args.keys():
        core = __get_cpu_from_ccxml(dev.get_config(), ccs_path)
    else:
        core = session_args["chip"]

    dev.core = dev.get_core(core)
    dev.core.connect()
    if options is not None:
        for optionID in options.keys():
            dev.core.set_option(optionID, options[optionID])
    dev.core.verify(image, binary=binary, address=address)

    return True


def flash(image, binary=False, address=None, options=None, ccs=None, **session_args):
    """Flashes device; setting 'options' before flashing device

    Args:
        image (str): path to image to use for flashing
        binary (bool): flashes image as binary if True
        address(int): offset address to flash image
        options (dict): dictionary of options in the format
            {option_id: option_val}; These options are set first before
            calling flash function.
        ccs (str): version number of CCS to use or path to custom installation
        session_args (**dict): keyword arguments containing settings for
            the device connection

    Returns:
        bool: Result of flash operation (success/failure)

    Raises:
        TIFlashError: raises error if option invalid
    """
    ccs_path = resolve_ccs_path(ccs)

    dev = TIFlashSession(ccs_path=ccs_path, **session_args)
    if "chip" not in session_args.keys():
        core = __get_cpu_from_ccxml(dev.get_config(), ccs_path)
    else:
        core = session_args["chip"]

    dev.core = dev.get_core(core)
    dev.core.connect()
    if options is not None:
        for optionID in options.keys():
            dev.core.set_option(optionID, options[optionID])
    dev.core.load(image, binary=binary, address=address)

    return True


def memory_read(address, num_bytes=1, page=0, ccs=None, **session_args):
    """Reads specified bytes from memory

    Args:
        address (long): memory address to read from
        num_bytes (int): number of bytes to read
        page (int, optional): page number to read memory from
        ccs (str): version number of CCS to use or path to custom installation
        session_args (**dict): keyword arguments containing settings for
            the device connection

    Returns:
        list: Returns list of bytes read from memory
    """
    ccs_path = resolve_ccs_path(ccs)

    dev = TIFlashSession(ccs_path=ccs_path, **session_args)
    if "chip" not in session_args.keys():
        core = __get_cpu_from_ccxml(dev.get_config(), ccs_path)
    else:
        core = session_args["chip"]

    dev.core = dev.get_core(core)
    dev.core.connect()

    return dev.core.read_memory(address, num_bytes=num_bytes, page=page)


def memory_write(address, data, page=0, ccs=None, **session_args):
    """Writes specified data to memory

    Args:
        address (long): memory address to read from
        data (list): list of bytes to write to memory
        page (int, optional): page number to read memory from
        ccs (str): version number of CCS to use or path to custom installation
        session_args (**dict): keyword arguments containing settings for
            the device connection

    Raises:
        TIFlashError: raises error when memory read error received
    """
    ccs_path = resolve_ccs_path(ccs)

    dev = TIFlashSession(ccs_path=ccs_path, **session_args)
    if "chip" not in session_args.keys():
        core = __get_cpu_from_ccxml(dev.get_config(), ccs_path)
    else:
        core = session_args["chip"]

    dev.core = dev.get_core(core)
    dev.core.connect()

    dev.core.write_memory(data, address, page=0)


def register_read(regname, ccs=None, **session_args):
    """Reads specified register of device

    Args:
        regname (str): register name to read from
        ccs (str): version number of CCS to use or path to custom installation
        session_args (**dict): keyword arguments containing settings for
            the device connection

    Returns:
        int: value of register

    Raises:
        TIFlashError: raised if regname is invalid
    """
    ccs_path = resolve_ccs_path(ccs)

    dev = TIFlashSession(ccs_path=ccs_path, **session_args)
    if "chip" not in session_args.keys():
        core = __get_cpu_from_ccxml(dev.get_config(), ccs_path)
    else:
        core = session_args["chip"]

    dev.core = dev.get_core(core)
    dev.core.connect()

    return dev.core.read_register(regname)


def register_write(regname, value, ccs=None, **session_args):
    """Writes a value to specified register of device

    Args:
        regname (str): register name to read from
        value (int): value to write to register
        ccs (str): version number of CCS to use or path to custom installation
        session_args (**dict): keyword arguments containing settings for
            the device connection

    Raises:
        TIFlashError: raised if regname is invalid
    """
    ccs_path = resolve_ccs_path(ccs)

    dev = TIFlashSession(ccs_path=ccs_path, **session_args)
    if "chip" not in session_args.keys():
        core = __get_cpu_from_ccxml(dev.get_config(), ccs_path)
    else:
        core = session_args["chip"]

    dev.core = dev.get_core(core)
    dev.core.connect()

    return dev.core.write_register(regname, value)


def evaluate(expr, symbol_file=None, ccs=None, **session_args):
    """Evaluates the given C/GEL expression

    Args:
        expr (str): C or GEL expression
        symbol_file (str): .out or GEL symbol file to load before evaluating
        ccs (str): version number of CCS to use or path to custom installation
        session_args (**dict): keyword arguments containing settings for
            the device connection

    Returns:
        str: String result from evaluating expression

    Raises:
        TIFlashError: raises error when expression error is raised
    """
    ccs_path = resolve_ccs_path(ccs)

    dev = TIFlashSession(ccs_path=ccs_path, **session_args)
    if "chip" not in session_args.keys():
        core = __get_cpu_from_ccxml(dev.get_config(), ccs_path)
    else:
        core = session_args["chip"]

    dev.core = dev.get_core(core)
    dev.core.connect()

    return dev.core.evaluate(expr, file=symbol_file)


def attach(ccs=None, **session_args):
    """Attach command; opens a CCS session and attaches to device.

    Args:
        ccs (str): version number of CCS to use or path to custom installation
        session_args (**dict): keyword arguments containing settings for
            the device connection

    Raises:
        TIFlashError: raises error when expression error is raised
    Warning:
        Implicitly sets 'keep_alive' to True; this means the DebugServer will
        not shutdown after the command is run and thus will need to be manually shutdown.
    """
    ccs_path = resolve_ccs_path(ccs)

    dev = TIFlashSession(ccs_path=ccs_path, **session_args)
    if "chip" not in session_args.keys():
        core = __get_cpu_from_ccxml(dev.get_config(), ccs_path)
    else:
        core = session_args["chip"]

    dev.core = dev.get_core(core)
    dev.attach_ccs(keep_alive=True)


def xds110_reset(ccs=None, **session_args):
    """Calls xds110reset command on specified serno.

    Args:
        ccs (str): version number of CCS to use or path to custom installation
        session_args (**dict): keyword arguments containing settings for
            the device connection

    Returns:
        bool: True if xds110reset was successful

    Raises:
        TIFlashError: raises if serno not set
        XDS110Error: raises if xds110_reset fails
    """
    ccs_path = resolve_ccs_path(ccs)

    if "serno" not in session_args.keys():
        raise TIFlashError("Must provide 'serno' to call xds110_reset")
    xds110.xds110_reset(ccs_path, serno=session_args["serno"])

    return True


def xds110_list(ccs=None, **session_args):
    """Returns list of sernos and xds110 version numbers of connected XDS110 devices.

    Args:
        ccs (str): version number of CCS to use or path to custom installation
        session_args (**dict): keyword arguments containing settings for
            the device connection

    Returns:
        list: list of tuples (serno, version) of connected XDS110 devices

    Raises:
        XDS110Error: raises if xdsdfu does not exist or fails
    """
    ccs_path = resolve_ccs_path(ccs)

    return xds110.xds110_list(ccs_path)


def xds110_upgrade(ccs=None, **session_args):
    """Upgrades/Flashes XDS110 firmware on board.

    Firmware flashed is found in xds110 directory (firmware.bin). This function
    uses the 'xdsdfu' executable to put device in DFU mode. Then performs the
    flash + reset functions of xdsdfu to flash the firmware.bin image

    Args:
        ccs (str): version number of CCS to use or path to custom installation
        session_args (**dict): keyword arguments containing settings for
            the device connection

    Returns:
        bool: True if successful

    Raises:
        XDS110Error: raises if xds110 firmware update fails
    """

    ccs_path = resolve_ccs_path(ccs)

    ccxml_args = __handle_ccxml_args(ccs_path, **session_args)

    if "serno" not in session_args.keys():
        raise TIFlashError("Must provide 'serno' to call xds110_upgrade")

    xds110.xds110_upgrade(ccs_path, serno=session_args["serno"])

    return True


def detect_devices(ccs=None, **session_args):
    """Detect devices connected to machine.

    Returns:
        list: list of dictionaries describing connected devices
    """
    ccs_path = resolve_ccs_path(ccs)

    device_list = list()
    detected_devices = detect.detect_devices()

    for vid, pid, serno in detected_devices:
        try:
            connection_xml = connections.get_connection_xml_from_vidpid(
                vid, pid, ccs_path
            )
            connection = connections.get_connection_name(connection_xml)
        except connections.ConnectionsError:
            continue  # only include TI Devices

        try:
            devicetype_xml = devices.get_device_xml_from_serno(serno, ccs_path)
            devicetype = devices.get_devicetype(devicetype_xml)
        except devices.DeviceError:
            devicetype = None

        dev = {"connection": connection, "devicetype": devicetype, "serno": serno}

        device_list.append(dev)

    return device_list


def get_info(ccs=None, **session_args):
    """Returns dict of information regarding tiflash environment

    Args:
        ccs (str): version number of CCS to use or path to custom installation

    Returns:
        dict: dictionary of information regarding tiflash environment
    """
    info_dict = dict()
    ccs_path = resolve_ccs_path(ccs)

    info_dict["tiflash version"] = __version__
    info_dict["release date"] = release_date
    info_dict["python version"] = python_version()
    info_dict["ccs version"] = (
        get_ccs_version(ccs_path) if ccs_path is not None else "N/A"
    )
    info_dict["ccs location"] = ccs_path if ccs_path is not None else "N/A"
    info_dict["ccs prefix"] = get_ccs_prefix()
    info_dict["device drivers"] = (
        ",".join(get_ccs_pf_filters(ccs_path)) if ccs_path is not None else "N/A"
    )

    return info_dict


def create_config(output, ccs=None, **session_args):
    """Creates a ccxml file using the given session args

    Args:
        output (str): path to output configuration file
        ccs (str, optional): version number of CCS to use or path to custom installation
        session_args (**dict): keyword arguments containing settings for
            the device connection

    Returns:
        str: full path to file generated

    Raises:
        Exception: raised if invalid session_args

    """
    ccs_path = resolve_ccs_path(ccs)

    serno = session_args.get("serno", None)
    devicetype = session_args.get("devicetype", None)
    connection = session_args.get("connection", None)
    ccxml = session_args.get("ccxml", None)

    session = resolve_session_args(
        ccs_path, ccxml=ccxml, connection=connection, devicetype=devicetype, serno=serno
    )

    output = os.path.expanduser(output)
    output = os.path.expandvars(output)
    fullpath = os.path.abspath(output)

    config_name = os.path.basename(fullpath) if output is not None else None
    config_dir = os.path.dirname(fullpath) if output is not None else None

    dev = TIFlashSession(ccs_path=ccs_path)
    return dev.create_config(name=config_name, directory=config_dir, **session)
