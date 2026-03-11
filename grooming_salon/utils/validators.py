import re
from django.core.exceptions import ValidationError

#-----------------------------------------------------------------------------------------------------------------------
# Validiramo da li su svi karakteri slova ili razmak i da li je prvo slovo svake reči veliko
def validate_capitalized_name(value):
    if not all(x.isalpha() or x.isspace() for x in value) or not value.istitle():
        raise ValidationError(message='Unos mora početi velikim slovom i sadržati samo slova i razmake.')

#-----------------------------------------------------------------------------------------------------------------------
# Validiramo da li su svi karakteri brojevi, bez razmaka, koji mogu početi sa "+"
def validate_phone_number(value):
    if not re.fullmatch(r'\+?\d+', value):
        raise ValidationError(message='Broj telefona mora sadržati samo cifre ili početi sa "+" pa cifre.')

#-----------------------------------------------------------------------------------------------------------------------
# Validiramo veličinu fotografije koja se otprema
def validate_file_size(image_object):
    if image_object.size > 5242880:
        raise ValidationError(message='Maksimalna veličina fotografije koja se može otpremiti je 5MB.')

#-----------------------------------------------------------------------------------------------------------------------
