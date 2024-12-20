# 所依赖的服务中断、恢复后，FastAPI 怎样能够无需重启自动恢复

观察 redis / mongodb / postgres 服务临时中断，FastAPI中怎样配置能够自动恢复。

自动恢复指的是：当依赖的服务恢复正常时，新的接口请求能够正常进行，不需要重启 FastAPI 服务。


## Redis 实验结论

无论依赖注入使用 `providers.Singleton` 还是 `providers.Factory` 获取 redis client，redis 服务临时中断，能够自动恢复。

这很有可能是 redis python SDK 本身支持的特性
