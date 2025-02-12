from pydantic import BaseModel


class UserData(BaseModel):
	id: str
	email: str
	name: str
	given_name: str = "Anonymous"
	picture: str = "https://api.dicebear.com/7.x/personas/svg"
