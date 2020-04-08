#!/usr/bin/env python3
#pip3 install blowfish hotpie
#this script will store, manage, and display RFC6238 TOTPs
#the encrypted repository (~/.totp-secrets) requires a passphrase to generate and maintain
###
from getpass import getpass
from hotpie import TOTP
import os,argparse,blowfish,hashlib,time,signal,base64

def signal_handler(sig, frame):
    print('\nctrl+c pressed, exiting.')
    exit()

def getphrase():
    passphrase = getpass("Passphrase:")
    if len(passphrase) < 4:
        print("Passphrase too short")
        exit()
    iv = hashlib.sha256(passphrase.encode('utf-8')).hexdigest()
    iv = bytes(iv[:8],'utf-8') #blowfish iv must be exactly 8 bytes
    passphrase=bytes(passphrase,"utf-8")
    return iv,passphrase

def parse_enc_file(db_file):
    data_encrypted = b''
    secrets_dict={}
    iv,passphrase = getphrase()
    cipher = blowfish.Cipher(passphrase)
    infile = open(db_file, 'rb')
    data_encrypted = infile.read()
    infile.close()
    all_lines=data_encrypted.split(b"\n")
    for line in all_lines:
        data_decrypted = b"".join(cipher.decrypt_ofb(line, iv))
        fields = data_decrypted.split(b',')
        if len(fields) > 1:
            secrets_dict.update({fields[0]:fields[1]})
        if len(fields) == 1 and len(secrets_dict) == 0:
            print("Decryption failed.")
            exit()
    iv = ''
    passphrase = ''
    return(secrets_dict)

def main():
    db_file=os.environ['HOME']+"/.totp-secrets"
    signal.signal(signal.SIGINT, signal_handler)
    parser = argparse.ArgumentParser(description="Manage and Display TOTP's")
    parser.add_argument('-a', '--add', action='store_true', help='add TOTP name and secret')
    parser.add_argument('-s', '--show', help='show TOTP secrets with matching case insensitive name')
    parser.add_argument('-d', '--delete', help='delete TOTP secrets with exact case sensitive name')
    parser.add_argument('-e', '--export', action='store_true', help="export all TOTP secrets to STDOUT")
    args = parser.parse_args()
    # add, delete, export
    if args.add:
        new_totp_name=input('Enter a name for your TOTP entry, end with newline:')
        if not new_totp_name:
            print("Nothing entered. Aborting.")
            return

        new_totp_secret=input('Enter a Base32 encoded TOTP secret for '+new_totp_name+', end with newline:')
        if not new_totp_secret:
            print("Nothing entered. Aborting.")
            return

        data = new_totp_name+","+new_totp_secret # gathered new TOTP entry
        data = bytes(data, "utf-8")
        iv,passphrase = getphrase()
        cipher = blowfish.Cipher(passphrase)
        data_encrypted = b"".join(cipher.encrypt_ofb(data, iv))+b"\n" # add separator
        outfile = open(db_file, 'ab')
        outfile_results = outfile.write(data_encrypted)
        outfile.close()
        return

    if args.show:
        secrets_dict=parse_enc_file(db_file)
        for name, secret in secrets_dict.items():
            if args.show.casefold() in name.decode().casefold():
                print("Argument Supplied: "+args.show+", matched: "+name.decode()+","+secret.decode())
        return

    if args.delete:
        secrets_dict=parse_enc_file(db_file)
        for name, secret in secrets_dict.items():
            if args.delete == name.decode():
                print("Argument Supplied: "+args.delete+", matched: "+name.decode()+","+secret.decode())
                input("Press Enter to delete TOTP entry with name: "+name.decode())
                secrets_dict.pop(name)
                iv,passphrase = getphrase()
                cipher = blowfish.Cipher(passphrase)
                output_contents = b''
                for name, secret in secrets_dict.items():
                    data = name+b","+secret
                    data_encrypted = b"".join(cipher.encrypt_ofb(data, iv))+b"\n"
                    output_contents = output_contents + data_encrypted
                outfile = open(db_file, 'wb')
                outfile_results = outfile.write(output_contents)
                outfile.close()
                return
        return

    if args.export:
        secrets_dict=parse_enc_file(db_file)
        for name, secret in secrets_dict.items():
            print(name.decode()+","+secret.decode())
        return

    else: # Display all TOTP's in collection, update every 30 seconds
        secrets_dict=parse_enc_file(db_file)
        if (len(secrets_dict)) == 0: #didn't work, no secrets
            return

    while True:
        totp_str=' | '
        sec_str=time.strftime('%S', time.localtime())
        if int(sec_str) >= 0 and int(sec_str) <= 29:
            sec_str = 30-int(sec_str)
        if int(sec_str) >= 30 and int(sec_str) <= 59:
            sec_str = 60-int(sec_str)
        for name, secret in sorted(secrets_dict.items(),key=lambda x:x[0]):
            try:
                val=TOTP(base64.b32decode(secret), digits=6)
                totp_str=totp_str+name.decode()+" "+val+" | "
            except:
                print("Decoding failed. Exiting")
                exit()
        print(".. "+str(sec_str).zfill(2)+totp_str, end="\r", flush=True)
        time.sleep(1)

if __name__ == "__main__":
    main()
