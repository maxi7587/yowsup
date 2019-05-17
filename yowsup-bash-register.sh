#!/bin/bash
default_phone_number=46766921516

read -p "Enter your number (leave blank to use stored default value): " phone_number

if [ phone_number ]
then
    yowsup-cli registration --register 123456 --config-phone $phone_number
else
    yowsup-cli registration --register 123456 --config-phone $default_phone_number
fi
