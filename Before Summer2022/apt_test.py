import thorlabs_apt as apt

print(apt.list_available_devices())

hwp_a = apt.Motor(83811904)

hwp_a.move_to(45, blocking=True)
hwp_a.move_to(0, blocking=True)
