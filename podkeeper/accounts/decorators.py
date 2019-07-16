

def email_confirmed(user):
  if user.is_anonymous:
    return False
  else:
    return user.email_confirmed