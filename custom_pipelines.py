#!/usr/bin/env python
"""
Example for defining Custom Pipelines
using pipelines to emit a Pipeline XML or ResolvedPipeline Template JSON file
"""
import logging
import sys

from pbsmrtpipe.core import PipelineRegistry
from pbsmrtpipe.cli_custom_pipeline import registry_runner_main

# This should probably be removed
from pbsmrtpipe.pb_pipelines.pb_pipelines_sa3 import Constants, Tags

log = logging.getLogger(__name__)


class C(object):
    # This should be rethought to be consistent with the repo name
    PT_NAMESPACE = "pbpipelines_internal"


registry = PipelineRegistry(C.PT_NAMESPACE)


def _example_topts():
    return {"pbpipelines_internal.task_options.dev_message": "Preset Custom Dev Message from register pipeline",
            "pbpipelines_internal.task_options.custom_alpha": 12345}


@registry("dev_a", "Custom Example 01", "0.1.0", tags=("dev", "hello-world"), task_options=_example_topts())
def to_bs():
    """Custom Pipeline Registry for dev hello world tasks"""
    b1 = [('$entry:e_01', 'pbsmrtpipe.tasks.dev_hello_world:0')]

    # Dev tasks that are bundled with pbsmrtpipe
    b2 = [('pbsmrtpipe.tasks.dev_hello_world:0', 'pbsmrtpipe.tasks.dev_hello_worlder:0'),
          ('pbsmrtpipe.tasks.dev_hello_world:0', 'pbsmrtpipe.tasks.dev_hello_garfield:0')]

    b3 = [('pbsmrtpipe.tasks.dev_hello_world:0', 'pbsmrtpipe.tasks.dev_txt_to_fasta:0')]

    return b1 + b2 + b3


@registry("dev_b", "Custom Example 02", "0.1.0", tags=("dev",), task_options=_example_topts())
def to_bs():
    """Custom Pipeline B for testing"""

    b3 = [("pbpipelines_internal.pipelines.dev_a:pbsmrtpipe.tasks.dev_txt_to_fasta:0", 'pbsmrtpipe.tasks.dev_filter_fasta:0')]
    return b3


@registry("internal_cond_dev", "Dev Reseq Cond Report", "0.1.0", tags=(Tags.DEV, ))
def to_bs():
    """Hello World test for Conditions JSON"""
    b1 = [(Constants.ENTRY_COND_JSON, "pbinternal2.tasks.cond_to_report:0")]

    return b1


@registry("internal_cond_dev2", "Dev Align Report", "0.1.0", tags=(Tags.DEV, ))
def to_bs():
    """Dev Test for AlignmentSet Condition Summary"""
    b1 = [(Constants.ENTRY_COND_JSON, "pbinternal2.tasks.cond_to_report:0")]

    b2 = [(Constants.ENTRY_COND_JSON, "pbinternal2.tasks.cond_to_alignmentsets_report:0")]

    return b1 + b2


@registry("internal_cond_dev_r", "Dev R (hello world)", "0.1.0", tags=(Tags.DEV, ))
def to_bs():
    """Hello World for R + Reports"""
    # Call the Python cond report for dev/testing purposes
    b1 = [(Constants.ENTRY_COND_JSON, "pbinternal2.tasks.cond_to_report:0")]

    # RRRRRRRR. This tasks should be renamed
    b2 = [(Constants.ENTRY_COND_JSON, "pbcommandR.tasks.hello_reseq_condition:0")]

    return b1 + b2


@registry("internal_cond_dev_r_reports", "Dev R (hello+Report)", "0.1.0", tags=(Tags.DEV, ))
def to_bs():
    """Hello World for R"""
    # Call the Python cond report for dev/testing purposes
    b1 = [(Constants.ENTRY_COND_JSON, "pbinternal2.tasks.cond_to_report:0")]

    # RRRRRRRR. This stupid typo should be fixed
    b2 = [(Constants.ENTRY_COND_JSON, "pbcommandR.tasks.hello_reseq_condition:0")]

    b3 = [(Constants.ENTRY_COND_JSON, "pbcommandR.tasks.hello_reseq_condition_report:0")]

    return b1 + b2 + b3


@registry("internal_cond_acc_density", "Accuracy Density Plots", "0.1.0", tags=(Tags.INTERNAL, ))
def to_bs():
    """Internal Condition Accuracy Density Plots"""
    b1 = [(Constants.ENTRY_COND_JSON, "pbinternal2.tasks.cond_to_report:0")]

    b2 = [(Constants.ENTRY_COND_JSON, "pbcommandR.tasks.accplot_reseq_condition:0")]

    return b1 + b2


if __name__ == '__main__':
    sys.exit(registry_runner_main(registry)(argv=sys.argv))
