
import logging
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


instances_holder = []  # 保存所有实例。这样可以避免对象ID重复


class Service:
    def __init__(self):
        logger.info("Service initialized")
        instances_holder.append(self)


class Facade:
    def __init__(self, service: Service):
        self.service = service
        logger.info("Facade initialized")
        instances_holder.append(self)

    def process(self):
        logger.info("F id: %s, S id: %s", id(self), id(self.service))


class DI(containers.DeclarativeContainer):
    service1 = providers.Factory(Service)
    service2 = providers.Singleton(Service)

    facade1 = providers.Factory(Facade, service=service1)
    facade2 = providers.Singleton(Facade, service=service1)

    facade3 = providers.Factory(Facade, service=service2)
    facade4 = providers.Singleton(Facade, service=service2)


@inject
def main1(facade: Facade = Provide[DI.facade1]):
    facade.process()


@inject
def main2(facade: Facade = Provide[DI.facade2]):
    facade.process()


@inject
def main3(facade: Facade = Provide[DI.facade3]):
    facade.process()


@inject
def main4(facade: Facade = Provide[DI.facade4]):
    facade.process()


if __name__ == "__main__":
    di = DI()
    di.wire(modules=[__name__])

    logger.info("-" * 100)
    logger.info("main1, Facade is Factory, Service is Factory")
    main1()
    main1()
    logger.info("-" * 100)
    logger.info("main2, Facade is Singleton, Service is Factory")
    main2()
    main2()

    logger.warning(
        "dangerous! if Facade is Singleton, Service is Factory, Facade will use the same Service instance."
    )

    logger.info("-" * 100)
    logger.info("main3, Facade is Factory, Service is Singleton")
    main3()
    main3()
    logger.info("-" * 100)
    logger.info("main4, Facade is Singleton, Service is Singleton")
    main4()
    main4()
