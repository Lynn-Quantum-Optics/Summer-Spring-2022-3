import thorlabs_apt as apt

_, available = zip(*apt.list_available_devices())
connections = {m: apt.Motor(m) for m in available}


print('motor connections loaded')
print()


last = None

print('available connections')
print(available)

try:
    while True:
        m = None
        while True:
            try:
                m = input('which motor? ' if last is None else 'which motor (default: {})? '.format(last))
                
                if not m and last is not None:
                    m = last
                    break
                
                m = int(m)
                
                if m not in available:
                    print('not an available motor')
                    continue
                    
                break
            except ValueError:
                print('enter a valid serial number')
                
        pos = 0
        while True:
            try:
                pos = input('position (default 0): ')
                if not pos:
                    pos = 0
                    break
                pos = float(pos)
                break
            except ValueError:
                print('enter a valid number')
                
        if m not in connections:
            connections[m] = apt.Motor(m)
            
        print('moving motor {} to position {}...'.format(m, pos))
        connections[m].move_to(pos, True)
        print('done moving')
        last = m
        for sn, c in connections.items():
            print('motor {} is at position {}'.format(sn, c.position))
 
 except KeyboardInterrupt:
    print('interrupted; exiting')