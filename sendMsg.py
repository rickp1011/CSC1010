from twilio.rest import Client

account_sid ="ACfffef1535b193c03b17db5eb59c713e4" # Put your Twilio account SID here
auth_token ="4ccf6e0c7fd3a2f48a891e07dbdd37ce" # Put your auth token here

client = Client(account_sid, auth_token)

message = client.api.account.messages.create(
		to="+83996753", # Put your cellphone number here
		from_="+14144414293", # Put your Twilio number here
		body="This is my message that I am sending to my phone!")