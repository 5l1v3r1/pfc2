#!/usr/bin/env python3
# Author: Aaron Esau <pfc@aaronesau.com>

from pfc.module import *

import pfc.tools as tools

import logging, sys

class CatModule(Module):
    def execute(self, context):
        args = context.args

        for src in args.get('file', ['-']):
            content = ''

            if src == '-':
                content = context.stdin

                if isinstance(content, list) or isinstance(content, set):
                    content = '\n'.join(content)
            else:
                try:
                    with open(src, 'r') as f:
                        content = f.read()
                except FileNotFoundError as e:
                    logging.error('file not found: %s' % src)
                    context.status = FAILURE
                    continue
                except PermissionError as e:
                    logging.error('permission denied: %s' % src)
                    context.status = FAILURE
                    continue

            if args.get('stdout'):
                sys.stdout.write(str(content))
                sys.stdout.flush()

            if args.get('stderr'):
                sys.stderr.write(str(content))
                sys.stderr.flush()

            if args.get('output'):
                if not context.output:
                    context.output = ''

                context.output += str(content)

            if context.status != FAILURE:
                context.status = SUCCESS

        return context