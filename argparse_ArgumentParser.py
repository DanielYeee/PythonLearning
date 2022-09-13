#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File  : argparse_ArgumentParser.py
@Description  : 
@Data : 2022/09/16 20:00:11
@Author  :  DanielYe
@Version  : 1.0
'''

# import argparse

# parser = argparse.ArgumentParser(description = 'An argument inputs into command line')

# parser.add_argument('param', type = str, help = "parameter help message")

# args = parser.parse_args()
# print(args)


# ===========================
# import argparse

# parser = argparse.ArgumentParser(description = 'an argument inputs into command line')
# parser.add_argument('param', type = str, help = 'parameter help message')

# args = parser.parse_args()
# print(args.param)

# =================================

# import argparse

# parser = argparse.ArgumentParser(description = 'an argument inputs into comand line')
# parser.add_argument('data', type = int, nargs = '+', help = 'Test int parameters')
# parser.add_argument('param', type = str, nargs = '+', help = 'multiple parameters')


# args = parser.parse_args()

# print(args)
# print(args.param)

# print(args.data)


# =====================
# optional parameters
# import argparse

# parser = argparse.ArgumentParser(description = 'an argument inputs into command line')
# parser.add_argument('--param1', type = str, help = 'parameter one test')
# parser.add_argument('--param2', type = str, help = 'parameter two test')

# args = parser.parse_args()
# print(args.param1 + ' ' + args.param2)
# ========================

# default parameter
# Notes: if argument was an location parameter, default will not work

# import argparse

# parser = argparse.ArgumentParser(description = 'an argument inputs into command line')
# # parser.add_argument('param1', type = str, default = 'hello', help = 'parameter one test')
# # parser.add_argument('param2', type = str, default = 'world', help = 'parameter two test')
# parser.add_argument('--param1', type = str, default = 'hello', help = 'parameter one test')
# parser.add_argument('--param2', type = str, default = 'world', help = 'parameter two test')

# args = parser.parse_args()
# print(args.param1 + '  ' + args.param2)


# =========================================

import argparse

parser = argparse.ArgumentParser(description = 'an argument inputs into command line')
# parser.add_argument('--param1', type = str, required = True, default = '', help = 'Test one')
parser.add_argument('param1', type = str, required = True, default = '', help = 'Test one')
parser.add_argument('--param2', type = str, default = 'DEFAULT', help = 'Test two')

args = parser.parse_args()

print(args.param1 + '  ' + args.param2)


