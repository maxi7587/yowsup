#!/bin/bash

# Should run the following line (using example data):
# python yowsup-cli registration --requestcode sms --config-phone 46766921516 --config-cc 46 --config-mcc 240 --config-mnc 01

default_phone_number=46766921516
default_cc_number=46
default_mcc_number=240
default_mnc_number=01

read -p "Enter your number (leave blank to use stored default value): " phone_number

if [ phone_number ]
then
    read -p "Enter your CC (CountyCode) number (leave blank to use stored default value): " cc_number
    read -p "Enter your MCC (MobileCountyCode) number (leave blank to use stored default value): " mcc_number
    read -p "Enter your MNC (MobileNetworkCode) number (leave blank to use stored default value): " mnc_number
    yowsup-cli registration --requestcode sms --config-phone $phone_number --config-cc $cc_number --config-mcc $mcc_number --config-mnc $mnc_number
else
    yowsup-cli registration --register 123456 --config-phone $default_phone_number
    yowsup-cli registration --requestcode sms --config-phone $default_phone_number --config-cc $default_cc_number --config-mcc $default_mcc_number --config-mnc $default_mnc_number
fi
