from typing import Annotated, Any
from uuid import UUID

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Body,
    Cookie,
    Depends,
    File,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    UploadFile,
    status,
)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer

from checkers.fixed_content_query_checker import FixedContentQueryChecker
from src.db.fake_db import fake_items_db
from src.dependencies.user_dependency import get_current_user
from src.dtos.images import ImageCreationRequest
from src.dtos.items import (
    ItemCreation,
    ItemCreationRequest,
    ItemCreationResponse,
    ItemUpdate,
    ItemUpdateRequest,
    ItemUpdateResponse,
)
from src.dtos.offers import OfferCreation, OfferCreationRequest, OfferCreationResponse
from src.dtos.users import UserCreation, UserCreationRequest, UserCreationResponse
from src.exceptions.unicorn_exception import UnicornException
from src.models.model_name import ModelName
from src.models.users import User
from src.open_api.tags import Tags
from src.services.header_verification_service import verify_key, verify_token
from src.services.params_extractor_service import (
    CommonParams,
    common_params,
    query_or_cookie_extractor,
)
from src.services.users_service import fake_save_user

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer("/users/auth")


@router.get("/")
async def root():
    return {"message": "Hello World!"}


@router.get("/token")
async def read_token(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@router.post("/users/auth", tags=[Tags.authentications, Tags.users])
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    lower_username = username.lower()

    if (lower_username == "fresult" and password == "Sila") or (
        lower_username == "korn" and password == "Zilla"
    ):
        return "Logged in successfully"

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Username or Password is incorrect",
    )


@router.get("/users/me", tags=[Tags.users])
async def read_my_user(current_user: Annotated[User, Depends(get_current_user)]):
    return {"current_user": current_user}


@router.get("/users/{id}", tags=[Tags.users])
async def read_user(id: str):
    return {"id": id}


@router.post(
    "/users/",
    response_model=UserCreationResponse,
    status_code=status.HTTP_201_CREATED,
    tags=[Tags.users],
)
async def create_user(user: UserCreationRequest) -> UserCreationResponse:
    created_user = fake_save_user(user).model_dump()

    return UserCreationResponse(created_user=UserCreation(**created_user))


@router.post("/login/", tags=[Tags.authentications, Tags.users])
async def login_test(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    if username == "username" and password == "password":
        return {"username": username}

    return {"error_message": "Username or Password is invalid!"}


@router.get("users/{user_id}/items/{item_id}", tags=[Tags.users])
async def read_user_item(
    user_id: str,
    item_id: str,
    q: str | None = None,
    short: bool = False,
):
    item = {"id": item_id, "owner_id": user_id}

    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {
                "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Velit ad accusantium quae nihil vero quas rerum! Tempora, eos exercitationem. Velit animi odit molestiae, architecto dolorem vitae corporis ea porro provident."
            }
        )

    return item


@router.get("/models/{name}")
async def get_model(name: ModelName):
    if name is ModelName.alexnet:
        return {"name": name, "message": "Deep Learning FTW!"}

    if name.value == "lenet":
        return {"name": name, "message": "LeCNN all the images"}

    return {"name": name, "message": "Have some residual"}


@router.get("/files/{file_path:path}", tags=[Tags.files])
async def get_file(file_path: str):
    return {"file_path": file_path}


@router.get("/items/", tags=[Tags.items])
async def read_items(
    ads_id: Annotated[str | None, Cookie()] = None,
    skip: int = 0,
    limit: int = 0,
    item_query: Annotated[
        str,
        Query(
            alias="item-query",
            title="Query String",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
            pattern="(?i)^select.*from.*;$",
            deprecated=True,
        ),
    ] = "SELECT first_name, last_name FROM persons /* It's just example */;",
    hidden_query: Annotated[
        str | None, Query(include_in_schema=False, alias="hidden-query")
    ] = None,
):
    no_limited = limit == 0
    results: dict[str, Any] = {"items": fake_items_db}

    results.update(
        {
            "items": fake_items_db[
                skip : len(fake_items_db) if no_limited else skip + limit
            ],
        }
    )

    if item_query:
        results.update({"q": item_query})

    if hidden_query:
        results.update({"hidden_query": hidden_query})
    else:
        results.update({"hidden_query": "Not found"})

    return results


@router.get("/items/qs", tags=[Tags.items])
async def read_items_with_queries(
    q: Annotated[list[str], Query(title="Query String", min_length=3)] = [],
):
    query_items = {"q": q}
    return query_items


@router.get("/items/{id}", tags=[Tags.items])
async def read_item(
    id: Annotated[
        UUID,
        Path(
            title="ID for the item to get",
            example="018e0aa8-48a9-7ae4-9746-1dc89c3f70cd",
            openapi_examples={
                "normal": {
                    "summary": "Normal UUID",
                    "value": "018e0aa8-48a9-7ae4-9746-1dc89c3f70cd",
                },
                "not-found": {
                    "summary": "Not found UUID",
                    "value": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                },
                "invalid": {
                    "summary": "Invalid UUID",
                    "value": "wrong-uuid",
                },
            },
        ),
    ],
    q: Annotated[str | None, Query(alias="item-query")] = None,
    short: bool = False,
):
    if id == UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )

    item: dict[str, Any] = {"id": id}

    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {
                "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Velit ad accusantium quae nihil vero quas rerum! Tempora, eos exercitationem. Velit animi odit molestiae, architecto dolorem vitae corporis ea porro provident."
            }
        )

    return item


@router.post(
    "/items/",
    response_model=ItemCreationResponse,
    status_code=status.HTTP_201_CREATED,
    tags=[Tags.items],
    summary="Create an item",
    # description="Create an item with all the information, name, description, price, tax, images, and a set of unique tags",
    response_description="The created item",
)
async def create_item(
    item: ItemCreationRequest,
):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **images**: list of image, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    item_dict = item.model_dump()

    price_with_tax = item.price + (item.tax if item.tax else 0)
    item_dict.update(
        {"id": "018e0d29-45c9-7456-9827-f324fd0d65dc", "price_with_tax": price_with_tax}
    )

    return {"created_item": ItemCreation(**item_dict)}


@router.put("/items/{id}", response_model=ItemUpdateResponse, tags=[Tags.items])
async def update_item(
    id: Annotated[
        UUID,
        Path(
            openapi_examples={
                "normal": {
                    "summary": "Normal UUID",
                    "value": "018e0d2b-a90d-7d49-bb22-c9313f756920",
                },
                "invalid": {
                    "summary": "Invalid UUID",
                    "value": "wrong-uuid",
                },
            }
        ),
    ],
    item: Annotated[
        ItemUpdateRequest | None,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Bar",
                        "description": "A very nice item",
                        "price": 35.4,
                        "tax": 3.2,
                        "tags": ["Bar", "Zilla"],
                        "images": [
                            {"name": "img-1", "url": "https://example.com/"},
                            {"name": "img-2", "url": "https://example.com/"},
                        ],
                    },
                },
                "converted": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                    "value": {
                        "name": "Baz",
                        "price": "35.4",
                        "tags": [],
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Baz",
                        "price": "thirty five point four",
                        "tags": [],
                    },
                },
            }
        ),
    ] = None,
    q: str | None = None,
):
    if not item:
        return {"updated_item": None}

    item_to_update_encoded = jsonable_encoder(item)
    found_idx = fake_items_db.index({"item_name": item.name})
    fake_items_db[found_idx] = item_to_update_encoded
    print("updated fake items", fake_items_db)

    item_dict = item.model_dump(exclude_unset=True)

    price_with_tax = item.price + (item.tax if item.tax else 0)
    item_dict.update({"id": id, "price_with_tax": price_with_tax})

    if q:
        item_dict = {"q": q, **item_dict}

    return {"updated_item": ItemUpdate(**item_dict)}


@router.put("/items/{name}/json/", tags=[Tags.items])
async def update_item_json(
    name: Annotated[str, Path()],
    item: Annotated[
        dict[str, str],
        Body(
            openapi_examples={
                "normal": {
                    "summary": "A normal item",
                    "value": {"item_name": "Qux"},
                },
            }
        ),
    ],
):
    json_compatible_item_data = jsonable_encoder(item)
    print("json_compatible_item_data", json_compatible_item_data)
    # new_fake_items_db = [
    # (json_compatible_item_data if item["item_name"] == name else item)
    # for item in fake_items_db
    # ]
    foundIndex = fake_items_db.index({"item_name": name})
    old_data = fake_items_db[foundIndex]
    fake_items_db[foundIndex] = json_compatible_item_data

    return {
        "updated_item": fake_items_db[foundIndex],
        "before_update_data": old_data,
    }


@router.post(
    "/offers/",
    response_model=OfferCreationResponse,
    status_code=status.HTTP_201_CREATED,
    tags=[Tags.offers],
)
async def create_offer(offer: OfferCreationRequest):
    offer_dict = offer.model_dump()

    offer_dict.update({"id": 12})

    return {"created_offer": OfferCreation(**offer_dict)}


@router.post(
    "/images/multiple/",
    status_code=status.HTTP_201_CREATED,
)
async def create_multiple_images(images: list[ImageCreationRequest]):
    print([img.model_dump(exclude_unset=True) for img in images])
    return images


@router.get("/headers/")
async def read_headers(user_agent: Annotated[str | None, Header()] = None):
    return {"user-agent": user_agent}


@router.get("/portal", response_model=None)
async def get_portal(teleport: bool = False) -> Response | dict:
    if teleport:
        return RedirectResponse(url="https://youtu.be/dQw4w9WgXcQ")

    return {"message": "Here's your inter dimensional portal."}


@router.post("/files/", tags=[Tags.files])
async def create_file(
    file: Annotated[bytes, File(description="A file read as bytes")],
    file_b: Annotated[UploadFile, File(description="A file read as upload file")],
    token: Annotated[str, Form()],
):
    if not file:
        return {"message": "No file sent"}

    return {
        "file_size": len(file),
        "token": token,
        "file_content_type": file_b.content_type,
    }


@router.post("/upload-file/", tags=[Tags.files])
async def create_upload_file(
    file: Annotated[UploadFile, File(description="A file read as upload file")],
):
    if not file:
        return {"message": "No upload file sent"}

    return {"file_name": file.filename}


@router.get("/unicorns/{name}")
async def read_unicorn(name: Annotated[str, Path(min_length=3)]):
    if name == "yolo":
        raise UnicornException()
    if name == "ha ha":
        raise HTTPException(
            status_code=status.HTTP_418_IM_A_TEAPOT,
            detail=f"Nope! I don't like [{name}]",
        )

    return {"unicorn_name": name}


@router.get("/elements", tags=[Tags.items], deprecated=True)
async def read_elements():
    """Read items

    Please use [/items/](#items/read_items_items__get) instead.
    """
    return [{"item_id": "Foo"}]


@router.get("/somethings-1/", tags=[Tags.somethings])
async def read_somethings_1(commons: Annotated[dict, Depends(common_params)]):
    response = {}

    if commons["q"]:
        response.update({"q": commons["q"]})

    items = fake_items_db[commons["skip"] : commons["skip"] + commons["limit"]]
    response.update({"items": items})

    return response


@router.get("/somethings-2/", tags=[Tags.somethings])
async def read_somethings_2(commons: Annotated[CommonParams, Depends()]):
    response: dict[str, Any] = {}

    if commons.q:
        response.update({"q": commons.q})

    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})

    return response


@router.get("/something-3/", tags=[Tags.somethings])
async def read_something_3(
    query_or_default: Annotated[str, Depends(query_or_cookie_extractor)],
):
    return {"q_or_cookie": query_or_default}


@router.get(
    "/somethings-4",
    dependencies=[Depends(verify_token), Depends(verify_key)],
    tags=[Tags.somethings],
)
async def read_something_4():
    return "My Something 4"


@router.post("/send-notification/{email}", tags=[Tags.notifications])
async def send_notification(email: str, background_tasks: BackgroundTasks):
    # TODO: Move this function
    def _write_notification(email: str, message: str = ""):
        with open("log.txt", mode="w") as email_file:
            content = f"notification for {email}: {message}\n"
            email_file.write(content)

    background_tasks.add_task(_write_notification, email, message="Some Notification")
    return {"message": "Notification sent in the background"}


checker = FixedContentQueryChecker("SELECT first_name, last_name FROM persons;")


@router.get("/query-checker/", tags=[Tags.query_checkers])
async def read_query_checker(
    fixed_content_included: Annotated[bool, Depends(checker)]
) -> dict[str, bool]:
    return {"fixed_content_in_query": fixed_content_included}


# TODO: Move this function
def _write_log(message: str) -> None:
    with open("log.txt", mode="a") as log:
        log.write(message)


# TODO: Move this function
def _get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(_write_log, message)


@router.post("/send-notification-with-dep/{email}", tags=[Tags.notifications])
async def send_notification_with_dep(
    email: str,
    background_tasks: BackgroundTasks,
    q: Annotated[str, Depends(_get_query)],
):

    message = f"message to {email}\n"
    background_tasks.add_task(_write_log, message)

    return {"message": "Message sent"}
