import os
import uuid
from db import database
from models import complaint, RoleType, State, transaction
from services.s3 import S3Serivce
from constants import TEMP_FILE_FOLDER
from util.helpers import decode_photo
from services.wise import WiseService

s3 = S3Serivce()
wise = WiseService()


class ComplaintManager:
    @staticmethod
    async def get_complaints(user):
        q = complaint.select()
        if user["role"] == RoleType.complainer:
            q = q.where(complaint.c.complainer_id == user["id"])
        elif user["role"] == RoleType.approver:
            q = q.where(complaint.c.state == State.pending)
            print(await database.fetch_all(q))
        return await database.fetch_all(q)

    @staticmethod
    async def create_complaint(complaint_data, user):
        data = complaint_data.dict()
        data["complainer_id"] = user["id"]
        encoded_photo = data.pop("encoded_photo")
        extension = data.pop("extension")
        name = f"{uuid.uuid4().hex.upper()}.{extension}"
        path = os.path.join(TEMP_FILE_FOLDER, name)
        decode_photo(path, encoded_photo)
        data["photo_url"] = s3.upload(path, name, extension)
        os.remove(path)
        id_ = await database.execute(complaint.insert().values(**data))
        await ComplaintManager.issue_transaction(data["amount"], f"{user['first_name']} {user['last_name']}",
                                                 user['iban'], id_)
        return await database.fetch_one(complaint.select().where(complaint.c.id == id_))

    @staticmethod
    async def delete(complaint_id):
        await database.execute(complaint.delete().where(complaint.c.id == complaint_id))

    @staticmethod
    async def approve(complaint_id):
        transaction_data = await database.fetch_one(
            transaction.select()
            .where(transaction.c.complaint_id == complaint_id))
        wise.fund_transfer(transaction_data["transfer_id"])
        await database.execute(complaint.update().where(complaint.c.id == complaint_id).values(status=State.approved))


    @staticmethod
    async def reject(complaint_id):
        transaction_data = await database.fetch_one(
            transaction.select()
            .where(transaction.c.complaint_id == complaint_id))
        wise.fund_transfer_cancel(transaction_data["transfer_id"])
        await database.execute(complaint.update().where(complaint.c.id == complaint_id).values(status=State.rejected))

    @staticmethod
    async def issue_transaction(amount, full_name, iban, complaint_id):
        quote_id = wise.create_a_quote(amount)
        recipient_id = wise.create_recipient(full_name, iban)
        transfer_id = wise.create_transfer(target_account_id=recipient_id, quote_id=quote_id)
        print(f"The fund transfer: {wise.fund_transfer(transfer_id)}")
        data = {
            "quote_id": str(quote_id),
            "transfer_id": transfer_id,
            "target_account_id": str(recipient_id),
            "amount": amount,
            "complaint_id": complaint_id
        }
        await database.execute(transaction.insert().values(**data))
