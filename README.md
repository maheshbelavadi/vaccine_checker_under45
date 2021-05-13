# Under 45 vaccine availability checker

This script will check for vaccine availability and print it when available, optionally will give you a callback as well (_Only when there are more than 10 free slots availabile_).

### Running this script

#### Pre-requisites
* [python 3.x](https://www.python.org/downloads/)
* [Twilio](https://www.twilio.com/) (only if you need a call back).

#### Running the script

##### Simple mode (Without callback)
* Open command prompt and install all required modules.
    ```sh
    pip install -r .\requirements.txt
    ```

* Edit the arealist/pincode to monitor in the script:
    * Add all the area paths you wish to monitor in line 18.
(Refer line 14 and 15 to get the area path)
    * Add all the pincode you wish to monitor in line 19.

* Run the script.
    ```sh
    python vaccine_checker.py
    ```

##### Alert mode (with callback)
* Open command prompt and install all required modules.
    ```sh
    pip install -r .\requirements.txt
    ```

* Create a twilio account and get the following (Register using this link www.twilio.com/referral/Cx4z0S): 
    * Get a [twilio phone number](https://www.twilio.com/docs/voice/quickstart/python)
    * Get account sid and auth token by [referring this](https://www.twilio.com/docs/voice/quickstart/python?code-sample=code-make-a-phone-call-using-twilio&code-language=Python&code-sdk-version=6.x#replace-the-placeholder-credential-values)
    * Setup a number where want to get a callback by adding it to [verified numbers](https://www.twilio.com/console/phone-numbers/verified)


* Edit the twilio paramaetrs in the script:
    * Set the sid ```account_sid``` in line 8
    * Set the token```auth_token``` in line 9
    * Set the twilio phone number ```account_phone_number``` in line 10
    * Set the callback phone number ```phone_number_to_call``` in line 11

* Edit the arealist/pincode to monitor:
    * Add all the area paths you wish to monitor in line 21.
(Refer line 14 and 15 to get the area path)
    * Add all the pincode you wish to monitor in line 22.

* Run the script.
    ```sh
    python vaccine_checker.py
    ```

If you plan to improve this script, feel free to create a PR (few wishlist: parameterize all values, avoid repeated calls)
##### And if you like this script, do give a star to this repo (on the top right corner on this page)
