from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from rest_framework.authtoken.admin import User
from django.utils import timezone
from django.db.models import Q
from django.db import models

from datetime import timedelta
from uuid import uuid4
from io import BytesIO
from PIL import Image
import os
