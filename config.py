
# API
from api_helper import ShoonyaApiPy
api = ShoonyaApiPy()

import pyotp



test_mode = 1 # 1 means enable (if enabled orders will not execute)



# finvasia api login

try:

    user = ""
    u_pwd = ""
    factor2 = pyotp.TOTP("").now()
    vc = ""
    app_key = ""
    imei = "" #random string

    ret = api.login(userid=user, password=u_pwd, twoFA=factor2, vendor_code=vc, api_secret=app_key, imei=imei)

except Exception as e:
    print("\n\n\n\n\nError while login through api\n\n\n\n\n")

# finvasia api login