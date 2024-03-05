from src.daos.users import UserDAO
from src.dtos.users import UserCreationRequest


def fake_user_hasher(raw_password: str) -> str:
    return "supersecret" + raw_password


def fake_save_user(user: UserCreationRequest) -> UserDAO:
    hashed_password = fake_user_hasher(user.password)
    created_user = UserDAO(
        id="018e0d76-b4df-7c74-a511-47cf55317329",
        **user.model_dump(),
        hashed_password=hashed_password,
    )

    print("User saved! ... not really")

    return created_user
