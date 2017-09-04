import redis

class RedisHelper(object):
    def __init__(self):
        self.__conn = redis.Redis(host='192.168.0.130', port=6379)
        self.channel = 'vm_info'

    def publish(self, msg):
        self.__conn.publish(self.channel, msg)

    def subscribe(self):
        pub = self.__conn.pubsub()
        pub.subscribe(self.channel)
        pub.parse_response()
        return pub
