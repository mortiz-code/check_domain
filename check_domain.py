"""
Autor: Matias Ortiz.
Contact: matias.ortiz@bvstv.com
Date: 21/02/2021
Version 3
"""

import dns.resolver
from argparse import ArgumentParser
from sys import exit, argv
from rich import print
import re


def main():
    """
    main run app with args.
    """
    # Construct an argument parser
    all_args = ArgumentParser()
    all_args.add_argument("-d", dest="Domain", help="Domain to be analyzed.", required=True)
    all_args.add_argument("-s", dest="Selector_DKIM", help="Selector DKIM.")
    all_args.add_argument("-b", dest="Selector_BIMI", help="Selector BIMI.")
    all_args.add_argument("-v", "--verbose", action="count", default=None, help="Verbose mode.")
    args = all_args.parse_args()
    domain = args.Domain
    selector_dkim = args.Selector_DKIM
    selector_bimi = args.Selector_BIMI
    verbose = args.verbose
    if selector_dkim == None and verbose == None and selector_bimi == None:
        check(domain)
    elif selector_dkim != None and selector_bimi == None and verbose == None:
        check(domain, selector_dkim, selector_bimi)
    elif selector_bimi != None and selector_dkim == None and verbose == None:
        check(domain, selector_dkim, selector_bimi)
    elif verbose != None and selector_dkim == None and selector_bimi == None:
        check_verbose(domain)
    elif verbose != None and selector_dkim != None and selector_bimi == None:
        check_verbose(domain, selector_dkim)
    else:
        check_verbose(domain, selector_dkim, selector_bimi)


def main2():
    """
    main2 run app interactive.
    """
    print("=" * 50)
    try:
        domain = input("Domain to be analyzed: ").lower()
        verbose = input("Verbose mode? [Y/N]: ").lower()
        opt = input("Do you know DKIM or BIMI selector? [Y/N]: ").lower()
        if verbose in "y" and opt == "y":
            selector_dkim = input("Choose DKIM selector: ")
            selector_bimi = input("Choose BIMI selector: ")
            check_verbose(domain, selector_dkim, selector_bimi)

        elif verbose in "y" and opt != "y":
            check_verbose(domain)

        elif verbose in "n" and opt in "y":
            selector_dkim = input("Choose DKIM selector: ")
            selector_bimi = input("Choose BIMI selector: ")
            check(domain, selector_dkim, selector_bimi)

        else:
            check(domain)

    except KeyboardInterrupt as e:
        print("\n", "=" * 50, "Closing app...", sep="\n")
        exit(e)


def check(domain, selector_dkim=None, selector_bimi=None):
    """
    Check DNS Record.

    Args:
        domain (str): Domain to be analyzed.
        manual_selector (str, optional): Selector for DKIM checks. Defaults to None.
        selector_bimi (str, optional): Selector for BIMI checks. Defaults to None.
    """
    print("=" * 50)

    selector = domain.split(".")

    type = [
        "A",
        "AAAA",
        "MX",
        "TXT",
    ]

    for record in type:
        try:
            result = dns.resolver.resolve(domain, record)
            for val in result:
                if "spf" in val.to_text():
                    print("[+] SPF Record: ", val.to_text())
                else:
                    print(f"[+] {record} Record :", val.to_text())
        except:
            print(f"[.] Record not found {record} in domain '{domain}'.")

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
    try:
        result = dns.resolver.resolve(f"_dmarc.{domain}", "TXT")
        for val in result:
            print(f"[+] DMARC Record :", val.to_text())

    except:
        print(f"[.] DMARC : Record not found in DNS record. Check DKIM configuration.")

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


def check_verbose(domain, selector_dkim=None, selector_bimi=None):

    """
    Check DNS Record verbose mode.

    Args:
        domain (str): Domain to be analyzed.
        manual_selector (str, optional): Selector for DKIM checks. Defaults to None.
        selector_bimi (str, optional): Selector for BIMI checks. Defaults to None.
    """
    print("=" * 50)

    selector = domain.split(".")

    type = [
        "A",
        "AAAA",
        "MX",
        "TXT",
    ]

    count = 0

    reg_ip = r"(?:\d{1,3}\.)+(?:\d{1,3})"
    reg_mask = r"(?:\d{1,3}\.)+(?:\d{1,3})['/']\d{1,2}"

    for record in type:
        try:
            result = dns.resolver.resolve(domain, record)
            for val in result:
                if "spf" in val.to_text():
                    records = val.to_text().split(" ")
                    print("[+] SPF Records: ")
                    for rec in range(len(records)):
                        count += 1
                        j = records[rec]
                        if "v=" in j:
                            j = j.replace('"', "")
                            print(f" {count}) {j}")
                        elif "ip4:" in records[rec]:
                            if re.search("/", records[rec]):
                                i = re.findall(reg_mask, records[rec])
                                print(f" {count}) ipv4 -> {i}")
                            else:
                                i = re.findall(reg_ip, records[rec])
                                print(f" {count}) ipv4 -> {i}")
                        elif "include:" in j:
                            j = j.replace('"', "")
                            ips = j.split("include:")
                            print(
                                f" {count}) {ips[1]} -> 'Third-party email service as a trustworthy sender.' Recursive query: ",
                                end="",
                            )
                            try:
                                result = dns.resolver.resolve(ips[1], "TXT")
                                for val in result:
                                    print(val.to_text())
                            except:
                                print(f"[.] Record not found {ips[1]} in domain '{domain}'.")
                        elif "redirect=" in j:
                            j = j.replace('"', "")
                            ips = j.split("redirect=")
                            print(
                                f" {count}) {ips[1]} -> 'Replaces domain with the current record.' Recursive query: ",
                                end="",
                            )
                            try:
                                result = dns.resolver.resolve(ips[1], "TXT")
                                for val in result:
                                    print(val.to_text())
                            except:
                                print(f"[.] Record not found {ips[1]} in domain '{domain}'.")
                        elif "all" in j:
                            if "+all" in val.to_text():
                                j = j.replace('"', "")
                                print(
                                    f" {count}) {j} -> 'The SPF record designates the host to be allowed to send.'"
                                )
                            elif "-all" in val.to_text():
                                j = j.replace('"', "")
                                print(
                                    f" {count}) {j} -> 'The SPF record has designated the host as NOT being allowed to send.'"
                                )
                            elif "~all" in val.to_text():
                                j = j.replace('"', "")
                                print(
                                    f" {count}) {j} -> 'The SPF record has designated the host as NOT being allowed to send but is in transition.'"
                                )
                            elif "?all" in val.to_text():
                                j = j.replace('"', "")
                                print(
                                    f" {count}) {j} -> 'The SPF record specifies explicitly that nothing can be said about validity.'"
                                )
                            else:
                                j = j.replace('"', "")
                                print(
                                    f" {count}) The domain '{domain}' does not have an SPF record or the SPF record does not evaluate to a result."
                                )

                        else:
                            print(f" {count}) {j}")

                else:
                    print(f"[+] {record} Record :", val.to_text())
        except:
            print(f"[.] Record not found {record} in domain '{domain}'.")

    # Printing record
    if selector_dkim != None:
        try:
            result = dns.resolver.resolve(f"{selector_dkim}._domainkey.{domain}", "TXT")
            count = 0
            for val in result:
                print("[+] DKIM Records:")
                records = val.to_text().split(" ")
                for record in records:
                    count += 1
                    record = record.replace('"', "")
                    record = record.replace(" ", "")
                    print(f"{count}) {record}")
        except:
            print(
                f"[.] DKIM Record : Selector '{selector_dkim}' not found in DNS record. Check DKIM configuration."
            )
    else:
        try:
            result = dns.resolver.resolve(f"{selector[0]}._domainkey.{domain}", "TXT")
            count = 0
            for val in result:
                print("[+] DKIM Records:")
                records = val.to_text().split(" ")
                for record in records:
                    count += 1
                    record = record.replace('"', "")
                    record = record.replace(" ", "")
                    print(f"{count}) {record}")
        except:
            try:
                result = dns.resolver.resolve(f"selector1._domainkey.{domain}", "TXT")
                count = 0
                for val in result:
                    print("[+] DKIM Records:")
                    records = val.to_text().split(" ")
                    for record in records:
                        count += 1
                        record = record.replace('"', "")
                        record = record.replace(" ", "")
                        print(f"{count}) {record}")
            except:
                print(
                    f"[.] DKIM Record : Selector '{selector[0]}' or 'selector1' is not found in the DNS records. Check DKIM configuration or choose the manual selector option."
                )

    # Printing record
    try:
        result = dns.resolver.resolve(f"_dmarc.{domain}", "TXT")
        count = 0
        for val in result:
            print("[+] DMARC Records:")
            records = val.to_text().split(" ")
            for record in records:
                count += 1
                record = record.replace('"', "")
                record = record.replace(" ", "")
                if "p=" in record:
                    print(f" {count}) {record} -> 'Policy for organizational domain.'")
                elif "adkim=" in record:
                    print(f" {count}) {record} -> 'Alignment mode for DKIM.'")
                elif "aspf=" in record:
                    print(f" {count}) {record} -> 'Alignment mode for SPF.'")
                elif "pct=" in record:
                    print(f" {count}) {record} -> 'Percentage of messages subjected to filtering.'")
                elif "rua=" in record:
                    print(f" {count}) {record} -> 'Reporting URI of aggregate reports.'")
                elif "ruf=" in record:
                    print(f" {count}) {record} -> 'Reporting URI for forensic reports.'")
                elif "sp=" in record:
                    print(f" {count}) {record} -> 'Policy for subdomains of the OD.'")
                else:
                    print(f" {count}) {record}")

    except:
        print(f"[.] DMARC : Record not found in DNS record. Check DKIM configuration.")

    # Printing record
    if selector_bimi != None:
        try:
            result = dns.resolver.resolve(f"{selector_bimi}._bimi.{domain}", "TXT")
            count = 0
            for val in result:
                print("[+] BIMI Records:")
                records = val.to_text().split(" ")
                for record in records:
                    count += 1
                    record = record.replace('"', "")
                    record = record.replace(" ", "")
                    print(f"{count}) {record}")
        except:
            print(
                f"[.] BIMI Record : Policy not found in DNS record using selector '{selector_bimi}'. Check BIMI configuration."
            )
    else:
        try:
            result = dns.resolver.resolve(f"default._bimi.{domain}", "TXT")
            count = 0
            for val in result:
                print("[+] BIMI Records:")
                records = val.to_text().split(" ")
                for record in records:
                    count += 1
                    record = record.replace('"', "")
                    record = record.replace(" ", "")
                    print(f"{count}) {record}")
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
