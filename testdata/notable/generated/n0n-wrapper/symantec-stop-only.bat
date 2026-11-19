@echo off
sc stop SepMasterService
sc config DemoService start= disabled
