import pytest
import time
import shutil
import tiflash


class TestTIFlashSession:
    class TestServer:
        def test_instantiation(self):
            """Tests basic instantation of TIFlashSession object with no parameters"""
            device = tiflash.TIFlashSession()

        def test_instantiation_with_deprecated_ccs_path(self, tenv):
            """Tests basic instantation of TIFlashSession object with provided ccs path"""
            ccs_path = tenv["paths"]["ccs"]
            device = tiflash.TIFlashSession(ccs=ccs_path)

        def test_instantiation_with_deprecated_ccs_version(self, tenv):
            """Tests basic instantation of TIFlashSession object with provided ccs path"""
            ccs_version = tenv["ccs"]["versions"][0]
            device = tiflash.TIFlashSession(ccs=ccs_version)

        def test_instantiation_with_ccs_path(self, tenv):
            """Tests basic instantation of TIFlashSession object with provided ccs path"""
            ccs_path = tenv["paths"]["ccs"]
            device = tiflash.TIFlashSession(ccs_path=ccs_path)

        def test_instantiation_with_ccs_version(self, tenv):
            """Tests basic instantation of TIFlashSession object with provided ccs path"""
            ccs_version = tenv["ccs"]["versions"][0]
            device = tiflash.TIFlashSession(ccs_version=ccs_version)

        def test_instantiation_with_ccs_prefix_and_version(self, tenv):
            """Tests basic instantation of TIFlashSession object with provided ccs path"""
            ccs_version = tenv["ccs"]["versions"][0]
            ccs_prefix = tenv["ccs"]["prefix"]
            device = tiflash.TIFlashSession(
                ccs_path=ccs_prefix, ccs_version=ccs_version
            )

        def test_instantiation_with_device_params(self, tenv, tdev):
            """Tests basic instantation of TIFlashSession object with provided device params"""
            serno = tdev.get("serno", None)
            devicetype = tdev.get("devicetype", None)
            connection = tdev.get("connection", None)
            device = tiflash.TIFlashSession(
                serno=serno, devicetype=devicetype, connection=connection
            )

        def test_instantiation_with_ccxml(self, tenv, tdev):
            """Tests basic instantation of TIFlashSession object with provided device params"""
            ccxml = tdev["ccxml-path"]
            device = tiflash.TIFlashSession(ccxml=ccxml)

            assert device._ccxml_path == ccxml

            if "serno" in tdev.keys():
                assert device._serno == tdev["serno"]
            assert device._devicetype == tdev["devicetype"]
            assert device._connection == tdev["connection"]

        def test_instantiation_with_ccxml_new_serno(self, tenv, tdev):
            """Tests basic instantation of TIFlashSession object with provided ccxml and different serno"""
            if "serno" not in tdev.keys():
                pytest.skip("Device %s has no serial number" % tdev["devicetype"])

            ccxml = tenv["paths"]["tmp"] + "/" + tdev["serno"] + ".ccxml"
            serno = "NEW_SERNO"

            # Going to be altering the ccxml file so making a copy to modify
            shutil.copyfile(tdev["ccxml-path"], ccxml)

            device = tiflash.TIFlashSession(serno=serno, ccxml=ccxml)

            assert device._ccxml_path == ccxml
            assert device._serno != tdev["serno"]
            assert device._serno == serno
            assert device._devicetype == tdev["devicetype"]
            assert device._connection == tdev["connection"]

            # Check the new serial number was updated on the provided ccxml file
            with open(ccxml) as f:
                text = f.read()
                assert serno in text
                assert tdev["serno"] not in text

        def test_attach_ccs(self, tenv, tdev):
            """Tests attaching CCS GUI to TIFlashSession"""
            serno = tdev.get("serno", None)
            devicetype = tdev.get("devicetype", None)
            connection = tdev.get("connection", None)
            device = tiflash.TIFlashSession(
                serno=serno, devicetype=devicetype, connection=connection
            )
            device.attach_ccs()

            time.sleep(10)  # allow 10 sec for CCS GUI to spin up

        def test_get_config(self, tenv, tdev):
            """Tests getting config path"""
            ccxml = tdev["ccxml-path"]
            device = tiflash.TIFlashSession(ccxml=ccxml)

            assert ccxml == device.get_config()

        def test_get_config_when_not_set(self, tenv, tdev):
            """Tests getting config path when not set"""
            device = tiflash.TIFlashSession()

            assert device.get_config() is None

        def test_get_list_of_connections(self, tenv, tdev):
            """Tests getting list of available connections"""
            device = tiflash.TIFlashSession()

            conns = device.get_list_of_connections()

            assert type(conns) is list
            assert len(conns) > 0  # at least one connection type should be installed

        def test_get_list_of_cores(self, tenv, tdev):
            """Tests getting list of available cores for device"""
            ccxml = tdev["ccxml-path"]
            device = tiflash.TIFlashSession(ccxml=ccxml)

            cores = device.get_list_of_cores()

            assert type(cores) is list
            assert len(cores) > 0  # at least one cpu type should be installed

        def test_get_list_of_cores_when_no_config_set(self, tenv, tdev):
            """Tests getting list of available cores for device when no config set"""
            device = tiflash.TIFlashSession()

            with pytest.raises(Exception):
                cores = device.get_list_of_cores()

        def test_get_list_of_devices(self, tenv, tdev):
            """Tests getting list of available devices"""
            device = tiflash.TIFlashSession()

            devices = device.get_list_of_devices()

            assert type(devices) is list
            assert len(devices) > 0  # at least one device type should be installed

    class TestCore:
        def test_get_core(self, tenv, tdev):
            """Tests simple get_core()"""
            core_name = tdev["session"]
            ccxml = tdev["ccxml-path"]
            device = tiflash.TIFlashSession(ccxml=ccxml)

            core = device.get_core(core_name)

        def test_core_connect(self, tenv, tdev):
            """Tests simple core.connect()"""
            core_name = tdev["session"]
            ccxml = tdev["ccxml-path"]
            device = tiflash.TIFlashSession(ccxml=ccxml)

            core = device.get_core(core_name)
            core.connect()

        def test_core_disconnect(self, tenv, tdev):
            """Tests simple core.disconnect()"""
            core_name = tdev["session"]
            ccxml = tdev["ccxml-path"]
            device = tiflash.TIFlashSession(ccxml=ccxml)

            core = device.get_core(core_name)
            core.connect()
            core.disconnect()

        def test_core_erase(self, tenv, tdev):
            """Tests simple core.erase()"""
            core_name = tdev["session"]
            ccxml = tdev["ccxml-path"]
            device = tiflash.TIFlashSession(ccxml=ccxml)

            core = device.get_core(core_name)
            core.connect()
            core.erase()

        def test_core_evaluate(self, tenv, tdev):
            """Tests simple core.evaluate()"""
            core_name = tdev["session"]
            ccxml = tdev["ccxml-path"]
            device = tiflash.TIFlashSession(ccxml=ccxml)

            core = device.get_core(core_name)
            core.connect()
            result = core.evaluate(tdev["expression-name"])
            assert result == tdev["expression-value"]

        def test_core_evaluate_with_symbols_file(self, tenv, tdev):
            """Tests simple core.evaluate()"""
            core_name = tdev["session"]
            ccxml = tdev["ccxml-path"]
            device = tiflash.TIFlashSession(ccxml=ccxml)

            core = device.get_core(core_name)
            core.connect()
            core.evaluate(tdev["symbol-name"], file=tdev["symbol-image"])

        def test_core_get_option(self, tenv, tdev):
            """Tests simple core.get_option()"""
            core_name = tdev["session"]
            ccxml = tdev["ccxml-path"]
            device = tiflash.TIFlashSession(ccxml=ccxml)

            core = device.get_core(core_name)
            core.connect()
            result = core.get_option(tdev["option"])

            assert result == tdev["option-val"]

        def test_core_halt(self, tenv, tdev):
            """Tests simple core.halt()"""
            core_name = tdev["session"]
            ccxml = tdev["ccxml-path"]
            device = tiflash.TIFlashSession(ccxml=ccxml)

            core = device.get_core(core_name)
            core.connect()
            core.halt()

        def test_core_halt_and_wait(self, tenv, tdev):
            """Tests simple core.halt(wait=True)"""
            core_name = tdev["session"]
            ccxml = tdev["ccxml-path"]
            device = tiflash.TIFlashSession(ccxml=ccxml)

            core = device.get_core(core_name)
            core.connect()
            core.halt(wait=True)

        def test_core_load(self, tenv, tdev):
            """Tests simple core.load()"""
            core_name = tdev["session"]
            ccxml = tdev["ccxml-path"]
            device = tiflash.TIFlashSession(ccxml=ccxml)

            core = device.get_core(core_name)
            core.connect()
            core.load(tdev["hex-image"])

        def test_core_load_binary(self, tenv, tdev):
            """Tests simple core.load(binary=True)"""
            core_name = tdev["session"]
            ccxml = tdev["ccxml-path"]
            device = tiflash.TIFlashSession(ccxml=ccxml)

            core = device.get_core(core_name)
            core.connect()
            core.load(tdev["binary-image"], binary=True)

        def test_core_perform_operation(self, tenv, tdev):
            """Tests simple core.perform_operation()"""
            core_name = tdev["session"]
            ccxml = tdev["ccxml-path"]
            device = tiflash.TIFlashSession(ccxml=ccxml)

            core = device.get_core(core_name)
            core.connect()
            core.perform_operation(tdev["opcode"])

        def test_core_read_memory(self, tenv, tdev):
            """Tests simple core.read_memory()"""
            core_name = tdev["session"]
            ccxml = tdev["ccxml-path"]
            device = tiflash.TIFlashSession(ccxml=ccxml)

            core = device.get_core(core_name)
            core.connect()
            result = core.read_memory(tdev["read-address"])
            assert len(result) == 1

        def test_core_read_memory_multiple_bytes(self, tenv, tdev):
            """Tests simple core.read_memory(num_bytes=4)"""
            core_name = tdev["session"]
            ccxml = tdev["ccxml-path"]
            device = tiflash.TIFlashSession(ccxml=ccxml)

            core = device.get_core(core_name)
            core.connect()
            result = core.read_memory(tdev["read-address"], num_bytes=4)
            assert len(result) == 4

        def test_core_read_register(self, tenv, tdev):
            """Tests simple core.read_register()"""
            core_name = tdev["session"]
            ccxml = tdev["ccxml-path"]
            device = tiflash.TIFlashSession(ccxml=ccxml)

            core = device.get_core(core_name)
            core.connect()
            result = core.read_register("PC")

        def test_core_reset(self, tenv, tdev):
            """Tests simple core.reset()"""
            core_name = tdev["session"]
            ccxml = tdev["ccxml-path"]
            device = tiflash.TIFlashSession(ccxml=ccxml)

            core = device.get_core(core_name)
            core.connect()
            core.reset()

        def test_core_run_with_async(self, tenv, tdev):
            """Tests simple core.run()"""
            core_name = tdev["session"]
            ccxml = tdev["ccxml-path"]
            device = tiflash.TIFlashSession(ccxml=ccxml)

            core = device.get_core(core_name)
            core.connect()
            core.run(asynchronous=True)

        def test_core_set_option(self, tenv, tdev):
            """Tests simple core.set_option()"""
            core_name = tdev["session"]
            ccxml = tdev["ccxml-path"]
            device = tiflash.TIFlashSession(ccxml=ccxml)

            core = device.get_core(core_name)
            core.connect()
            core.set_option(tdev["option"], tdev["option-val"])

        def test_core_verify(self, tenv, tdev):
            """Tests simple core.verify()"""
            core_name = tdev["session"]
            ccxml = tdev["ccxml-path"]
            device = tiflash.TIFlashSession(ccxml=ccxml)

            core = device.get_core(core_name)
            core.connect()
            core.load(tdev["hex-image"])
            core.verify(tdev["hex-image"])

        @pytest.mark.xfail
        def test_core_verify_binary(self, tenv, tdev):
            """Tests simple core.verify(binary=True)"""
            core_name = tdev["session"]
            ccxml = tdev["ccxml-path"]
            device = tiflash.TIFlashSession(ccxml=ccxml)

            core = device.get_core(core_name)
            core.connect()
            core.load(tdev["binary-image"], binary=True)
            core.verify(tdev["binary-image"], binary=True)

        def test_core_write_memory(self, tenv, tdev):
            """Tests simple core.write_memory()"""
            core_name = tdev["session"]
            ccxml = tdev["ccxml-path"]
            device = tiflash.TIFlashSession(ccxml=ccxml)

            core = device.get_core(core_name)
            core.connect()
            core.write_memory(data=[0xFF, 0xFF], address=int(tdev["write-address"], 16))

        def test_core_write_register(self, tenv, tdev):
            """Tests simple core.write_register()"""
            core_name = tdev["session"]
            ccxml = tdev["ccxml-path"]
            device = tiflash.TIFlashSession(ccxml=ccxml)

            core = device.get_core(core_name)
            core.connect()
            core.write_register("R1", 0xBEEF)
