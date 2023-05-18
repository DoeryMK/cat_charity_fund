from app.crud.base import CRUDBase
from app.models import Donation
from app.schemas.donation import DonationCreate


class CRUDonation(
    CRUDBase[
        Donation, DonationCreate
    ]
):
    pass


donation_crud = CRUDonation(Donation)

