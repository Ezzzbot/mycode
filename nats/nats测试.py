import asyncio
from nats.aio.client import Client as NATS
import json

async def call_task():
    nc = NATS()

    # 连接配置（注意：新版nats-py的connect()没有timeout参数）
    nats_server = "nats://test:123@192.168.24.100:4222"

    try:
        # 正确连接方式（移除了timeout参数）
        await nc.connect(servers=[nats_server])

        # 构造请求
        subject = "VersionArm6D.r.do.task.get_dpd_2_jdpd"
        #request_data = {}

        # 发送请求（这里可以设置超时）
        response = await nc.request(
            subject,

            timeout=30  # 请求超时（单位：秒）
        )
        # result = json.loads(response.data.decode())
        # print("任务执行结果:", result)

    except Exception as e:
        print(f"调用失败: {str(e)}")
    finally:
        if nc.is_connected:
            await nc.close()

# 运行调用
asyncio.run(call_task())
