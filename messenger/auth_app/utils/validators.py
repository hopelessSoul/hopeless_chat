def check_if_ppl_are_friends(person1, person2):
    friends = list(person1.friends.all())
    for i in friends:
        if person2.user == i:
            return True
    return False
