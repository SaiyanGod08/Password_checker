import requests
import hashlib
import sys



def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f"error fetching : {res.status_code} , check your url")
    return res



def password_leak_count(hashes, target_hash):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for hash , count in hashes:
        if target_hash == hash:
            return int(count)
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char , tail = sha1password[:5], sha1password[5:]
    url_response =  request_api_data(first5_char)
    return password_leak_count(url_response, tail)


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count > 0:
            print(f"{password} is breached and is being used {count} times")
        else:
            print(f"{password} is not breached")

main(sys.argv[1:])