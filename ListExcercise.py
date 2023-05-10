
inviteList = ['Jobs', 'Stark', 'Sting']
print("Invite " + str(inviteList) + " for dinner")

CantAttend = 'Jobs'
inviteList.remove(CantAttend)
inviteList.append('Blue')
print(CantAttend + " cannot attend the dinner, so invite Blue for dinner")
print("Invite " + str(inviteList) + " for dinner")

inviteList.insert(0, 'Green')
print("I've found another bigger desk, hey " + str(inviteList) + " come here")

