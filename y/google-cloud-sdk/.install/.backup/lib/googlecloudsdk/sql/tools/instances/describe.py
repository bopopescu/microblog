# Copyright 2013 Google Inc. All Rights Reserved.

"""Retrieves information about a Cloud SQL instance."""

from googlecloudsdk.calliope import base
from googlecloudsdk.core import remote_completion
from googlecloudsdk.sql import util


class Get(base.Command):
  """Retrieves information about a Cloud SQL instance."""

  @staticmethod
  def Args(parser):
    """Args is called by calliope to gather arguments for this command.

    Args:
      parser: An argparse parser that you can use it to add arguments that go
          on the command line after this command. Positional arguments are
          allowed.
    """
    instance = parser.add_argument(
        'instance',
        help='Cloud SQL instance ID.')
    cli = Get.GetCLIGenerator()
    instance.completer = (remote_completion.RemoteCompletion.
                          GetCompleterForResource('sql.instances', cli))

  @util.ReraiseHttpException
  def Run(self, args):
    """Retrieves information about a Cloud SQL instance.

    Args:
      args: argparse.Namespace, The arguments that this command was invoked
          with.

    Returns:
      A dict object representing the instance resource if fetching the instance
      was successful.
    Raises:
      HttpException: A http error response was received while executing api
          request.
      ToolException: An error other than http error occured while executing the
          command.
    """
    sql_client = self.context['sql_client']
    resources = self.context['registry']

    util.ValidateInstanceName(args.instance)
    instance_ref = resources.Parse(args.instance, collection='sql.instances')

    return sql_client.instances.Get(instance_ref.Request())

  def Display(self, unused_args, result):
    """Display prints information about what just happened to stdout.

    Args:
      unused_args: The same as the args in Run.
      result: the value returned by Run().
    """
    self.format(result)
