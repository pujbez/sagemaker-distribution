import os

from sagemaker_studio_jupyter_scheduler.scheduler import (
    SagemakerEnvironmentManager,
    SageMakerJobFilesManager,
    SageMakerUnifiedStudioScheduler,
)

c.ServerApp.terminado_settings = {"shell_command": ["/bin/bash"]}
region = os.environ.get("AWS_REGION")
csp_rule = os.environ.get("JUPYTERSERVER_CSP_RULE")

c.ServerApp.tornado_settings = {"compress_response": True, "headers": {"Content-Security-Policy": csp_rule}}

# Do not delete files to trash. Instead, permanently delete files.
c.FileContentsManager.delete_to_trash = False

# Allow deleting non-empty directory via file browser. Related documentation:
# https://github.com/jupyter-server/jupyter_server/blob/main/jupyter_server/services/contents/filemanager.py#L125-L129
c.FileContentsManager.always_delete_dir = True

# Enable `allow_hidden` by default, so hidden files are accessible via Jupyter server
# Related documentation: https://jupyterlab.readthedocs.io/en/stable/user/files.html#displaying-hidden-files
c.ContentsManager.allow_hidden = True

# This will set the LanguageServerManager.extra_node_roots setting if amazon_sagemaker_sql_editor exists in the
# environment. Ignore otherwise, don't fail the JL server start
# Related documentation: https://jupyterlab-lsp.readthedocs.io/en/v3.4.0/Configuring.html
try:
    import os

    module = __import__("amazon_sagemaker_sql_editor")
    module_location = os.path.dirname(module.__file__)
    c.LanguageServerManager.extra_node_roots = [f"{module_location}/sql-language-server"]
except:
    pass

c.SchedulerApp.scheduler_class = SageMakerUnifiedStudioScheduler
c.SchedulerApp.environment_manager_class = SagemakerEnvironmentManager
c.SchedulerApp.job_files_manager_class = SageMakerJobFilesManager
