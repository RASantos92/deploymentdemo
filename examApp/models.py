from django.db import models
import re
import bcrypt

class QuoteManager(models.Manager):
	def quoteValidator(self, postData):
		errors = {}
		if len(postData['quote']) < 10:
			errors['quoteReq'] = "quote needs to be at least 10 characters"
		if len(postData['author']) < 3:
			errors['authorReq'] = "author needs to be at least 3 characters"
		if len(postData['quote']) == 0:
			errors['quoteReq'] = "You need to input a quote to add"
		if len(postData['author']) == 0:
			errors['authorReq'] = "You need to input a author to add"
		return errors

class UserManager(models.Manager):
	def loginValidator(self, postData):
		errors = {}
		usersWithEmail = User.objects.filter(email=postData['email'])
		#fill out the email
		if len(postData['password']) == 0:
			errors['passwordRed'] = "A password is required to login"
		if len(postData['email']) == 0:
			errors['emailReq'] = "Email is required to log in"
		#check if email exist in db
		elif len(usersWithEmail) == 0:
			errors['emailNotFound'] = "Email is not found please register to login"
		# #if email is found check if pasword matches
		else:
			userToCheck = usersWithEmail[0]
			# print(usersWithEmail)
			# print(usersWithEmail[0])
			# print(usersWithEmail[0].password)
			if bcrypt.checkpw(postData['password'].encode(), usersWithEmail[0].password.encode()):
				print("password matches")
			else:
				errors['pwmatch'] = "Password incorrect"
		return errors
	
	def editValidator(self, postData):
		EMAIL_REGEX = re.compile(r'^[a-zA-z0-9.+_-]+@[a-zA-z0-9._-]+\.[a-zA-Z]+$')
		errors = {}
		if len(postData['userName']) < 3:
			errors["userName"] = "User name should be at least 3 characters"
		if len(postData['firstName']) < 3:
			errors["firstName"] = "First name should be at least 3 characters"
		if len(postData['lastName']) < 3:
			errors["lastName"] = "Last name should be at least 3 characters"
		if len(postData['email']) == 0:
			errors['emailreq'] = "Email is required"
		elif not EMAIL_REGEX.match(postData['email']):
			errors['invalidEmail'] = "This email is not real"
		else:
			repeatEmail = User.objects.filter(email = postData['email'])
			if len(repeatEmail)> 0 and postData['email'] != postData['userEmail']:
				errors['invalidEmail'] = "This email is already taken"
		# for user in User.objects.all():
		# 	if user.email == postData['email']:
		# 		errors['email'] = ("Email already in use")
		if len(postData['password']) < 4:
			errors['passwordReq'] = "password must be at least 4 characters"
		if postData['password'] != postData['cPassword']:
			errors['password'] = ("Passwords do not match")
		return errors


	def basic_validator(self, postData):
		EMAIL_REGEX = re.compile(r'^[a-zA-z0-9.+_-]+@[a-zA-z0-9._-]+\.[a-zA-Z]+$')
		errors = {}
		if len(postData['userName']) < 3:
			errors["userName"] = "User name should be at least 3 characters"
		if len(postData['firstName']) < 3:
			errors["firstName"] = "First name should be at least 3 characters"
		if len(postData['lastName']) < 3:
			errors["lastName"] = "Last name should be at least 3 characters"
		if len(postData['email']) == 0:
			errors['emailreq'] = "Email is required"
		elif not EMAIL_REGEX.match(postData['email']):
			errors['invalidEmail'] = "This email is not real"
		else:
			repeatEmail = User.objects.filter(email = postData['email'])
			if len(repeatEmail)> 0:
				errors['invalidEmail'] = "This email is already taken"
		# for user in User.objects.all():
		# 	if user.email == postData['email']:
		# 		errors['email'] = ("Email already in use")
		if len(postData['password']) < 4:
			errors['passwordReq'] = "password must be at least 4 characters"
		if postData['password'] != postData['cPassword']:
			errors['password'] = ("Passwords do not match")
		return errors

class User(models.Model):
	userName = models.CharField(max_length=45)
	firstName = models.CharField(max_length=45)
	lastName = models.CharField(max_length=45)
	email = models.CharField(max_length=45)
	password = models.CharField(max_length=45)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Quotes(models.Model):
	quote = models.TextField()
	author = models.CharField(max_length=45, null=True)
	uploader = models.ForeignKey(User, related_name="quoteUploaded", on_delete = models.CASCADE)
	likes = models.ManyToManyField(User, related_name="quotesLiked")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = QuoteManager()

