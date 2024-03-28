import os
import json
import logging
import sentry_sdk
from pluginbase import PluginBase
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

# PluginBase インスタンスを作成
plugin_base = PluginBase(package="plugins")
# プラグインのソースを作成（プラグインが置かれるディレクトリを指定）
function_source = plugin_base.make_plugin_source(searchpath=["./functions"])

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    enable_tracing=True,
    traces_sample_rate=0.1,
    profiles_sample_rate=0.1,
    integrations=[
        AwsLambdaIntegration(timeout_warning=True),
    ],
)


def handler(event, context):
    path = event["resource"]
    method = event["httpMethod"]
    arguments = json.loads(event["body"]) if method == "POST" else {}
    function_name = os.path.basename(path)
    return function_call(function_name, arguments)


def function_call(function_name, arguments):
    result = ""
    # プラグインとその優先度を格納するリスト
    for plugin_name in function_source.list_plugins():
        # プラグインをロード
        plugin_module = function_source.load_plugin(plugin_name)
        if function_name == plugin_name:
            try:
                logging.info(f"run extractor {plugin_name}")
                # プラグインモジュールから関数を呼び出す
                result = plugin_module.run(**arguments)
                return {
                    "statusCode": 200,
                    "body": json.dumps(
                        {
                            "result": result,
                        },
                        ensure_ascii=False,
                    ),
                }
            except Exception as e:
                sentry_sdk.capture_exception(e)
                logging.exception(e)
                return {
                    "statusCode": 500,
                    "body": json.dumps({"message": str(e)}),
                }
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "unknown actions"}),
    }
