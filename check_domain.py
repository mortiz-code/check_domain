"""
Autor: Matias Ortiz.
Contact: matias.ortiz@bvstv.com
Date: 24/01/2021
"""

import dns.resolver
from argparse import ArgumentParser
from sys import exit, argv


def main():
    """
    main run app with args.
    """
    # Construct an argument parser
    all_args = ArgumentParser()
    all_args.add_argument("-d", dest="Domain", help="Domain to be analyzed.")
    all_args.add_argument("-s", dest="Selector_DKIM", help="Selector DKIM.")
    all_args.add_argument("-b", dest="Selector_BIMI", help="Selector BIMI.")
    args = all_args.parse_args()
    domain = args.Domain
    selector_dkim = args.Selector_DKIM
    selector_bimi = args.Selector_BIMI
    if selector_dkim and selector_bimi != None:
        check(domain, selector_dkim, selector_bimi)
    elif selector_dkim != None:
        check(domain, selector_dkim)
    else:
        check(domain)


def main2():
    """
    main2 run app interactive.
    """
    print("=" * 50)
    try:
        domain = input("Domain to be analyzed: ")
        opt = input("Do you know DKIM or BIMI selector? [Y/N]: ").lower()
        if opt == "y":
            selector_dkim = input("Choose DKIM selector: ")
            selector_bimi = input("Choose BIMI selector: ")
            check(domain, selector_dkim, selector_bimi)
        else:
            check(domain)
    except:
        print("=" * 50, "Closing app...", sep="\n")
        exit()


def check(domain, selector_dkim=None, selector_bimi=None):
    """
    check Check DNS Record

    Args:
        domain (str): Domain to be analyzed.
        manual_selector (str, optional): Selector for DKIM checks. Defaults to None.
    """
    print("=" * 50)

    selector = domain.split(".")

    type = [
        "A",
        "AAAA",
        "MX",
        "TXT",
    ]
    for i in type:
        try:
            result = dns.resolver.resolve(domain, i)
            for val in result:
                print(f"[+] {i} Record :", val.to_text())
        except:
            print(f"[.] Record not found {i} in domain '{domain}'.")

    # Printing record
    if selector_dkim != None:
        try:
            result = dns.resolver.resolve(f"{selector_dkim}._domainkey.{domain}", "TXT")
            for val in result:
                print("[+] DKIM Record :", val.to_text())
        except:
            print(
                f"[.] DKIM Record : Selector '{selector_dkim}' not found in DNS record. Check DKIM configuration."
            )
    else:
        try:
            result = dns.resolver.resolve(f"{selector[0]}._domainkey.{domain}", "TXT")
            for val in result:
                print("[+] DKIM Record :", val.to_text())
        except:
            try:
                result = dns.resolver.resolve(f"selector1._domainkey.{domain}", "TXT")
                for val in result:
                    print("[+] DKIM Record :", val.to_text())
            except:
                print(
                    f"[.] DKIM Record : Selector '{selector[0]}' or 'selector1' is not found in the DNS records. Check DKIM configuration or choose the manual selector option."
                )

    # Printing record
    if selector_bimi != None:
        try:
            result = dns.resolver.resolve(f"{selector_bimi}._bimi.{domain}", "TXT")
            for val in result:
                print("[+] BIMI Record :", val.to_text())
        except:
            print(
                f"[.] BIMI Record : Policy not found in DNS record using selector '{selector_bimi}'. Check BIMI configuration."
            )
    else:
        try:
            result = dns.resolver.resolve(f"default._bimi.{domain}", "TXT")
            for val in result:
                print("[+] BIMI Record :", val.to_text())
        except:
            print(
                f"[.] BIMI Record : Policy not is found in DNS record using selector 'default'. Check BIMI configuration or choose the manual selector option."
            )


if __name__ == "__main__":
    if len(argv) > 1:
        main()
        exit()

    else:
        main2()
        exit()

else:
    exit()
