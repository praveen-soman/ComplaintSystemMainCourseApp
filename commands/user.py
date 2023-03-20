import asyncclick as click
from models.enums import RoleType
from managers.user import UserManager
from db import database


@click.command()
@click.option("-f", "--first_name", type=str, required=True)
@click.option("-l", "--last_name", type=str, required=True)
@click.option("-e", "--email_id", type=str, required=True)
@click.option("-p", "--phone", type=str, required=True)
@click.option("-i", "--iban", type=str, required=True)
@click.option("-pa", "--password", type=str, required=True)
async def create_user(first_name, last_name, email_id, phone, iban, password):
    user_data = {"first_name": first_name, "last_name": last_name, "email_id": email_id, "phone": phone, "iban": iban,
                 "role": RoleType.admin, "password": password}
    await database.connect()
    await UserManager.register(user_data)
    await database.disconnect()


if __name__ == "__main__":
    create_user(_anyio_backend="asyncio")
