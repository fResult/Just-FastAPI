from dataclasses import dataclass
from typing import Any, Callable

from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel

from src.open_api.tags import Tags

router = APIRouter(prefix="/cqrs", tags=[Tags.cqrs])


@dataclass
class CommandRecord[BaseModel]:
    type: str
    payload: dict

    def model_dump(self) -> dict:
        return {"type": self.type, "payload": self.payload}


fake_events_store: list[CommandRecord] = [
    CommandRecord(type="electronics", payload={"name": "phone", "price": 1000}),
    CommandRecord(type="vehicles", payload={"name": "car", "price": 20000}),
    CommandRecord(type="electronics", payload={"name": "laptop", "price": 1500}),
    CommandRecord(type="vehicles", payload={"name": "bike", "price": 5000}),
    CommandRecord(type="toys", payload={"name": "car", "price": 50}),
    CommandRecord(type="toys", payload={"name": "doll", "price": 25}),
]

type_to_data: dict[str, list[dict]] = {}


def group_types() -> None:
    for event in fake_events_store:
        type_to_data.setdefault(event.type, []).append(event.payload)


# First call to group_types() to populate the type_to_data dictionary
group_types()


class Command(BaseModel):
    type: str
    payload: dict


class Query(BaseModel):
    type: str


@router.post("/commands")
def handle_command(
    command: Command, background_tasks: BackgroundTasks
) -> dict[str, Any]:
    fake_events_store.append(CommandRecord(**command.model_dump()))

    more_data: Callable[[dict], None] = type_to_data.setdefault(command.type, []).append

    background_tasks.add_task(more_data, command.payload)

    return {"message": "Command received", "current_events": fake_events_store}


@router.post("/queries", response_model=list[dict])
async def handle_query(query: Query) -> list[dict]:
    print(f"Received query: {query}")

    found_data = type_to_data.get(query.type, [])

    return found_data
