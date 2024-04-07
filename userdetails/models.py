from django.db import models
import uuid
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE


class UserDetails(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )
    name = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True,)
    password = models.TextField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    #relationship
    referral_code = models.TextField(null=True, blank=True)
    