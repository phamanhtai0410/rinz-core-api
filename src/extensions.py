# -*- coding: utf-8 -*-
from lib.rz_payment import RzPaymentAPI
from flask_redis import Redis
from flask_pymongo import PyMongo

from rediscluster import RedisCluster
from .config import DefaultConfig

# Redis cache
redis_cache = Redis()
mdb = PyMongo()
mdb_payment = PyMongo()

RzPayment = RzPaymentAPI()
# Redis user info, will initialized in app
redis_cluster = RedisCluster(
    startup_nodes=DefaultConfig.REDIS_USERS_STARTUP_NODES,
    decode_responses=True
)
# print('Init Redis user info successfully')
