import pytest
import subprocess

from clihelpers import get_cmd_with_device_params

ADDRESS = "0x500012F0"

@pytest.mark.usefixtures("device")
class TestMemoryCli():

    def test_basic_memory_read_single_byte(self, device):
        """Tests simple memory read"""
        cmd = get_cmd_with_device_params(device)

        cmd.extend(["memory-read", "\"%s\"" % ADDRESS])

        # Implicitly set 1 byte length
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)

        # Explicitly set 1 byte length
        cmd.extend(["-n", "1"])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)


    def test_basic_memory_read_multiple_bytes(self, device):
        """Tests simple memory read of multiple bytes"""
        NUM_BYTES = "4"
        cmd = get_cmd_with_device_params(device)

        cmd.extend(["memory-read", "\"%s\"" % ADDRESS, "-n", NUM_BYTES])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)


    def test_basic_memory_write(self, device):
        """Tests simple memory write"""
        WRITE_ADDRESS = "0x20000000"
        WRITE_DATA = "0x11 0x22 0x33"
        cmd = get_cmd_with_device_params(device)

        cmd.extend(["memory-write", "\"%s\"" % WRITE_ADDRESS, "-d", WRITE_DATA])

        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)


    def test_invalid_address_memory_read(self, device):
        """Tests an Error is raised when trying to access invalid memory for
        memory read"""
        INVALID_ADDRESS = "0xFFFFFFFF"
        NUM_BYTES = "4"

        with pytest.raises(subprocess.CalledProcessError):
            cmd = get_cmd_with_device_params(device)

            cmd.extend(["memory-read", "\"%s\"" % INVALID_ADDRESS, "-n", NUM_BYTES])
            cmd_str = " ".join(cmd)

            subprocess.check_call(cmd_str, shell=True)


    def test_invalid_address_memory_write(self, device):
        """Tests an Error is raised when trying to access invalid memory for
        memory write"""
        INVALID_ADDRESS = "0x10000000"
        WRITE_DATA = "0x11 0x22 0x33"

        with pytest.raises(subprocess.CalledProcessError):
            cmd = get_cmd_with_device_params(device)

            cmd.extend(["memory-write", "\"%s\"" % INVALID_ADDRESS, "-d", WRITE_DATA])
            cmd_str = " ".join(cmd)

            subprocess.check_call(cmd_str, shell=True)
