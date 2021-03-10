#!/usr/bin/env python3

# Copyright (c) 2020 Seagate Technology LLC and/or its Affiliates
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU Affero General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License along
# with this program. If not, see <https://www.gnu.org/licenses/>. For any questions
# about this software or licensing, please email opensource@seagate.com or
# cortx-questions@seagate.com.

#from ha.core.error import HAUnimplemented
#from  ha.cli import cluster

import inspect

from ha.core.error import HAInvalidCommand
from ha.cli.command_factory import cmdFactory
from ha.cli.exec.commandExecutor import CLIUsage
from ha.cli.exec.permissions import Permissions
from ha.cli.exec import clusterExecutor
from ha.cli.exec import nodeExecutor
from ha.cli.exec import commandExecutor
from ha.cli.exec import serviceExecutor
from ha.cli.exec import storagesetExecutor


class Command:

    def __init__(self):
        self.module_name = None
        self.operation_name = None
        self.options = None
        self.cmd_factory = cmdFactory()

        # Modules where executor classes are defined
        self.execute = [commandExecutor, clusterExecutor, nodeExecutor, serviceExecutor, storagesetExecutor]


    def parse(self, args):
        """ Parse the CLI string to identify parameters"""

        try:
            self.module_name = args[0]
            self.operation_name = args[1]
            self.options = args[2:]

        except Exception:

            print(CLIUsage.usage())
            if self.module_name != "-h" and self.module_name != "--help":
                raise HAInvalidCommand("Invalid parameters passed; refer to help for details")
            else:
                return False
        return True


    def get_class(self, commandExecutor):

        for module in self.execute:
            cmds = inspect.getmembers(module, inspect.isclass)
            for name , cmd in cmds:
                if name == commandExecutor:
                    return cmd
        return None


    def process(self, args):
        """ Process the command """

        # Raise exception if user does not have proper permissions
        self.validate = Permissions()
        self.validate.validate_permissions()

        if self.parse(args) == True:
            commandExecutor = self.cmd_factory.get_executor(self.module_name, self.operation_name)

            if commandExecutor == None:
                print(CLIUsage.usage())
                raise HAInvalidCommand("Invalid parameters passed; refer to help for details")

            classnm = self.get_class(commandExecutor)
            executorClass = classnm()
            executorClass.execute()

"""
SupportBundleCommand is currently broken, so removed the code.
This will be added when the support bundle user story is started 
"""
