from time import sleep
import random
import hazelcast
import logging

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s%(msecs)03d [%(name)s] %(levelname)s: %(message)s', datefmt="%H:%M%:%S,")
    logging.getLogger().setLevel(logging.INFO)
    logger = logging.getLogger("main")

    config = hazelcast.ClientConfig()
    config.group_config.name = "dev"
    config.group_config.password = "dev-pass"
    config.network_config.addresses.append("127.0.0.1:5701")

    client = hazelcast.HazelcastClient(config)

    my_map = client.get_map("map")
    print(my_map)

    def item_added(event):
        print("item_added", event)

    def item_removed(event):
        print("item_removed", event)

    print(my_map.add_entry_listener(include_value=True, added=item_added, removed=item_removed))

    print("map.size", my_map.size())
    key = random.random()
    print("map.put", my_map.put(key, "value"))
    print("map.contains_key", my_map.contains_key(key))
    print("map.get", my_map.get(key))
    print("map.size", my_map.size())
    print("map.remove", my_map.remove(key))
    print("map.size", my_map.size())
    print("map.contains_key", my_map.contains_key(key))


    def put_async_cb(f):
        print("map.put_async", f.result())
    my_map.put_async(key, "async_val").add_done_callback(put_async_cb)

    def get_async_cb(f):
        print("map.get_async", f.result())
    my_map.get_async(key).add_done_callback(get_async_cb)

    def remove_async_cb(f):
        print("map.remove_async", f.result())
    my_map.remove_async(key).add_done_callback(remove_async_cb)
    #
    sleep(10)
    client.shutdown()
    #
