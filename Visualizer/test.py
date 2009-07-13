import Visualizer.displayable as svg

system = svg.VisSystem()
system.add_node('192.168.100.100')
system.add_node('192.168.222.222')

system.add_manager('192.168.100.100:5000')

system.add_host('192.168.100.100:7000')
system.add_host('192.168.100.100:7001')
system.add_host('192.168.100.100:7002')
system.add_host('192.168.100.100:7003')
system.add_host('192.168.222.222:7000')

system.add_actor('192.168.100.100:7000-ExampleActor-0')
system.add_actor('192.168.100.100:7001-ExampleActor-1')
system.add_actor('192.168.100.100:7001-AnotherActor-22')
system.add_actor('192.168.100.100:7002-ExampleActor-2')
system.add_actor('192.168.100.100:7003-ExampleActor-3')

system.add_actor('192.168.222.222:7000-ExampleActor-0')
system.add_actor('192.168.222.222:7000-AnotherActor-22')

system.store_name('badger', '192.168.100.100:7000-ExampleActor-0', '192.168.100.100:5000')
system.store_type('192.168.100.100:7000-ExampleActor-0', '192.168.100.100:5000')
system.store_type('192.168.100.100:7001-ExampleActor-1', '192.168.100.100:5000')
system.store_type('192.168.100.100:7002-ExampleActor-2', '192.168.100.100:5000')
system.store_type('192.168.100.100:7003-ExampleActor-3', '192.168.100.100:5000')

system.draw()
