# Copyright 2013 Google Inc. All Rights Reserved.

"""Lists instances in a given project.

Lists instances in a given project in the alphabetical order of the
 instance name.
"""

from googlecloudapis.apitools.base import py as apitools_base
from googlecloudsdk.calliope import base
from googlecloudsdk.core import properties
from googlecloudsdk.core.util import list_printer
from googlecloudsdk.sql import util


class List(base.Command):
  """Lists Cloud SQL instances in a given project.

  Lists Cloud SQL instances in a given project in the alphabetical
  order of the instance name.
  """

  @staticmethod
  def Args(parser):
    """Args is called by calliope to gather arguments for this command.

    Args:
      parser: An argparse parser that you can use to add arguments that go
          on the command line after this command. Positional arguments are
          allowed.
    """
    parser.add_argument(
        '--limit',
        default=None,
        type=int,
        help='Maximum number of instances to list.')

  @util.ReraiseHttpException
  def Run(self, args):
    """Lists Cloud SQL instances in a given project.

    Args:
      args: argparse.Namespace, The arguments that this command was invoked
          with.

    Returns:
      SQL instance resource iterator.
    Raises:
      HttpException: An http error response was received while executing api
          request.
      ToolException: An error other than an http error occured while executing
          the command.
    """
    sql_client = self.context['sql_client']
    sql_messages = self.context['sql_messages']

    project_id = properties.VALUES.core.project.Get(required=True)

    return apitools_base.YieldFromList(
        sql_client.instances,
        sql_messages.SqlInstancesListRequest(project=project_id),
        args.limit)

  def Display(self, unused_args, result):
    list_printer.PrintResourceList('sql.instances', result)
