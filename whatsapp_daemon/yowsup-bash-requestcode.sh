#!/bin/bash

# Should run the following line (using example data):
# python yowsup-cli registration --requestcode sms --config-phone 46766921516 --config-cc 46 --config-mcc 240 --config-mnc 01

export PYTHONPATH=`pwd`

read -p "Enter your number (leave blank to use stored default value): " phone_number
read -p "Enter your CC (CountyCode) number (leave blank to use stored default value): " cc_number
read -p "Enter your MCC (MobileCountyCode) number (leave blank to use stored default value): " mcc_number
read -p "Enter your MNC (MobileNetworkCode) number (leave blank to use stored default value): " mnc_number

echo "Will request a verification code with the following data:"
echo "- cc $cc_number"
echo "- mcc $mcc_number"
echo "- mnc $mnc_number"
echo "- number $phone_number"

yowsup-cli registration --requestcode sms --config-phone $phone_number --config-cc $cc_number --config-mcc $mcc_number --config-mnc $mnc_number

echo -n "Enter the verification code: "
read verification_code

yowsup-cli registration --register $verification_code --config-phone $phone_number

echo "Now, copy this configuration object in SMSC:"
echo ""
cat ~/.config/yowsup/$phone_number/config.json
echo ""
