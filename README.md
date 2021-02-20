# check_domain 

[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/mortiz-code/check_domain)

Check DNS A, AAAA, SPF, DKIM, DMARC and BIMI records easily and quickly.

## Use Case Description

When you want to analyze a domain to check protocols like SPF, DKIM, DMARC, and BIMI or registers A, AAAA you need to do different queries. This app helps you to do it with only one line. Useful when working with email solutions such as Cisco Email Security Appliance / Cisco Cloud Email Security / Cisco Domain Protection.


## Installation

Clone the repository:

```sh
git clone https://github.com/mortiz-code/check_domain.git
cd check_domain
```

Create virtual environment and activate it:

***NOTE**: You may require to install the "python3-venv" package in your Linux.*

```python
python3 -m venv check_domain && source check_domain/bin/activate
pip install -r requirements.txt
```

Now you're ready to run the script.


## Usage

You can run the app to check domains in two modes, using interactive steps or using arguments.
By default, the app will try to check DKIM with selector 'domain' and if it fails, will try with 'selector1'. For BIMI verification, it will use 'default' as the selector.
Both selectors can be defined manually. For domain use "-d" and set optional flags "-s" for DKIM selector and/or "-b" for BIMI selector. Also, you can use '-v' for verbose mode. This option will do a recursive DNS lookup for SPF records and add extra info to the output.
Another way is using the interactive mode.

```python
└─$ python check_domain.py -h
usage: check_domain.py [-h] -d DOMAIN [-s SELECTOR_DKIM] [-b SELECTOR_BIMI] [-v]
optional arguments:
-h, --help        show this help message and exit
-d DOMAIN         Domain to be analyzed.
-s SELECTOR_DKIM  Selector DKIM.
-b SELECTOR_BIMI  Selector BIMI.
-v, --verbose     Verbose mode.
```

Option 1:

```python
└─$ python check_domain.py
==================================================
Domain to be analyzed: bvstv.com
Verbose mode? [Y/N]: y
Do you know DKIM or BIMI selector? [Y/N]: y
Choose DKIM selector: bvstv
Choose BIMI selector: default
==================================================
[+] A Record : 190.61.250.160
[.] Record not found AAAA in domain 'bvstv.com'.
[+] MX Record : 0 mx2.hc4885-28.iphmx.com.
[+] MX Record : 0 mx1.hc4885-28.iphmx.com.
[+] TXT Record : "cisco-ci-domain-verification=56425da1647ff1346e2c9345925928b74fc75b04c218da0f7928711df8fc160b"
[+] TXT Record : "v=DKIM1; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA13K6/iYmOCA+KH62zxDWdH+wn1X2ZOllAMZ/KZfvwZWKwhHQGGSU+eHCsyWbz0jJYiS1X/4C6NLya
2GXrLAAkxVA8l74aPTN5yBeZP0iXBvZ1Yl47VW9C6ElRdlPyAimSiyOta5tDjSamJHGFxvwzJ5y2zh11qOYGQMCq8jEQAFX8+9CWx4t4HQ5uAwHrzXTPS3kNRn2" "H/ubJYnZmk943v51rBb2iM9D
PymWMObfjIH7rgFJUb5j6+PGwNbFgw42cjbhEBd1YGBh+K4+/PBPSuOSG+miAApD+4Ki3icjt0KaOdrKaGiah+elSgElprDIIADlRHyNxsXPSLrsBXghrQIDAQAB;"
[+] TXT Record : "duo_sso_verification=ntfsmAmvYMYMnwjgk6SpssPl5t7hZADsv9NCBLtCS7AnylaapsIfsFB9k6PItJVr"
[+] SPF Records:
 1) v=spf1
 2) ipv4 -> ['190.61.250.160']
 3) ipv4 -> ['68.232.140.76']
 4) ipv4 -> ['68.232.146.126']
 5) ipv4 -> ['68.232.143.39']
 6) ipv4 -> ['68.232.148.166']
 7) ipv4 -> ['23.90.98.133']
 8) ipv4 -> ['181.166.215.252']
 9) servers.mcsv.net -> 'Third-party email service as a trustworthy sender.' Recursive query: "v=spf1 ip4:205.201.128.0/20 ip4:198.2.128.0/18 ip4:148.105.8.0/21 ?all"
 10) -all -> 'The SPF record specifies explicitly that nothing can be said about validity.'
[+] TXT Record : "MS=ms87202626"
[+] DKIM Records:
1) v=DKIM1;
2) p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA13K6/iYmOCA+KH62zxDWdH+wn1X2ZOllAMZ/KZfvwZWKwhHQGGSU+eHCsyWbz0jJYiS1X/4C6NLya2GXrLAAkxVA8l74aPTN5yBeZ
P0iXBvZ1Yl47VW9C6ElRdlPyAimSiyOta5tDjSamJHGFxvwzJ5y2zh11qOYGQMCq8jEQAFX8+9CWx4t4HQ5uAwHrzXTPS3kNRn2H/ubJYnZmk943v51rBb2iM9DPymWMObfjIH7rgFJUb5j6+PGwNbFgw42cjbhEBd1YGBh+K4+/PBPSuOSG+miAApD+4Ki3icjt0KaOdrKaGiah+elSgElprDIIADlRHyNxsXPSLrsBXghrQIDAQAB;
[+] DMARC Records:
 1) v=DMARC1;
 2) p=reject; -> 'Policy for organizational domain.'
 3) adkim=r; -> 'Alignment mode for DKIM.'
 4) aspf=r; -> 'Alignment mode for SPF.'
 5) fo=0;
 6) pct=100; -> 'Percentage of messages subjected to filtering.'
 7) rf=afrf;
 8) ri=86400;
 9) rua=mailto:bvstv@rua.dmp.cisco.com,mailto:netsec@bvstv.com; -> 'Reporting URI of aggregate reports.'
 10) ruf=mailto:bvstv@ruf.dmp.cisco.com,mailto:netsec@bvstv.com -> 'Reporting URI for forensic reports.'
[+] BIMI Records:
1) v=BIMI1;
2) l=https://bvstv.com/img/bvs_bimi.svg;
3) a=self;
```

Option 2:

```python
└─$ python check_domain.py -d cisco.com -s iport -v
==================================================
[+] A Record : 72.163.4.185
[+] AAAA Record : 2001:420:1101:1::185
[+] MX Record : 10 alln-mx-01.cisco.com.
[+] MX Record : 20 rcdn-mx-01.cisco.com.
[+] MX Record : 30 aer-mx-01.cisco.com.
[+] TXT Record : "MS=ms35724259"
[+] TXT Record : "926723159-3188410"
[+] SPF Records:
 1) v=spf1
 2) spfa._spf.cisco.com -> 'Replaces domain with the current record.' Recursive query: "v=spf1 ip4:173.37.147.224/27 ip4:173.37.142.64/26 ip4:173.38.212.128/27 ip4:173.38.203.0/24 ip4:72.163.7.160/27 ip4:72.163.197.0/24
ip4:66.187.208.0/20 ip4:173.37.86.0/24 include:spf.protection.outlook.com include:spfb._spf.cisco.com ~all"
[+] TXT Record : "apple-domain-verification=qOInipPgso3W8cmK"
[+] TXT Record : "QuoVadis=94d4ae74-ecd5-4a33-975e-a0d7f546c801"
[+] TXT Record : "SFMC-o7HX74BQ79k7glpt_qjlF2vmZO9DpqLtYxKLwg87"
[+] TXT Record : "docusign=5e18de8e-36d0-4a8e-8e88-b7803423fa2f"
[+] TXT Record : "docusign=95052c5f-a421-4594-9227-02ad2d86dfbe"
[+] TXT Record : "amazonses:7LyiKZmpuGja4+KbA4xX3lN69yajYKLkHH4QJcWnuwo="
[+] TXT Record : "amazonses:QbUv5pPHGQxRy1vKA0J7Y/biE9oR6MTxOTI1bZIfjsw="
[+] TXT Record : "amazonses:mX+ylQj+fJAfh9pr03yIR7YvjKZ1bOo5ABegqM/5pvI="
[+] TXT Record : "fastly-domain-delegation-w049tcm0w48ds-341317-20210209"
[+] TXT Record : "facebook-domain-verification=1zoxo8z7t013gpruxmhc8dkerq47vh"
[+] TXT Record : "facebook-domain-verification=qr2nigspzrpa96j1nd9criovuuwino"
[+] TXT Record : "mixpanel-domain-verify=2c6cb1aa-a3fb-44b9-ad10-d6b744109963"
[+] TXT Record : "onetrust-domain-verification=20345dd0c33946f299f14c1498b41f67"
[+] TXT Record : "identrust_validate=JnSSfW+y58dEQju6mVBe8lu1MGFepXI50P27OE1ZZQmL"
[+] TXT Record : "identrust_validate=Wns4/AOM0Ij2kQCQhzvNbMcoBzxItOa+44O7KF06lIp3"
[+] TXT Record : "fastly-domain-delegation-e9a758d22183504af2d5ab4d9a9853da-20210127"
[+] TXT Record : "google-site-verification=9MlQU9MMQ1jHLMUkONKe6QzZ-ZIGRv0BCD1_rY1Zdmc"
[+] TXT Record : "google-site-verification=lW5eqPMJI4VrLc28YW-JBkqA-FDNVnhFCXQVDvFqZTo"
[+] TXT Record : "google-site-verification=qPS9ZkoQ-Og1rBrM1_N7z-tNJNy2BVxE8lw6SB2iFdk"
[+] TXT Record : "duo_sso_verification=AxenLdoqIXzjl2RJzE1BlOfkawDbDFlnbyvjAt8vcjKHBkvYwEMySDRk5QmBd66v"
[+] TXT Record : "zpSH7Ye/seyY61hH8+Rq5Kb+ZJ9hDa+qeFBaD/6sPAAg+2POkGdP0byHb1pFVK9uZgYF2AIosUSZq4MB17oydQ=="
[+] TXT Record : "atlassian-domain-verification=672RcADvt8BPqsb9gCN2ZC5DoTAhUT8abC1blYKQxi/MHMaGoA/BuvjFMaWRtgd7"
[+] DKIM Records:
1) v=DKIM1;
2) p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCctxGhJnvNpdcQLJM6a/0otvdpzFIJuo73OYFuw6/8bXcf8/p5JG/iME1r9fUlrNZs3kMn9ZdPYvTyRbyZ0UyMrsM3ZN2JAIop3M7sitqHg
p8pbORFgQyZxq+L23I2cELq+qwtbanjWJzEPpVvrvbuz9QL8CUtS+V5N5ldq8L/lwIDAQAB;
[+] DMARC Records:
 1) v=DMARC1;
 2) p=quarantine; -> 'Policy for organizational domain.'
 3) pct=0; -> 'Percentage of messages subjected to filtering.'
 4) fo=1;
 5) ri=3600;
 6) rua=mailto:cisco@rua.agari.com; -> 'Reporting URI of aggregate reports.'
 7) ruf=mailto:cisco@ruf.agari.com -> 'Reporting URI for forensic reports.'
[.] BIMI Record : Policy not is found in DNS record using selector 'default'. Check BIMI configuration or choose the manual selector option.
```

Another output example:

```python
└─$ python check_domain.py -d news.united.com -s united
==================================================
[+] A Record : 12.130.158.199
[.] Record not found AAAA in domain 'news.united.com'.
[+] MX Record : 10 imh.rsys2.net.
[+] MX Record : 10 imh2.rsys2.net.
[+] TXT Record : "google-site-verification=HGVPo1CIhFResq9hBTAJ2y_s78Na02V6MsJLKwHGJas"
[+] SPF Record:  "v=spf1 ip4:12.130.136.0/22 ip4:12.130.153.0/24 ip4:12.130.154.0/24 -all"
[+] DKIM Record : "g=*; k=rsa; n=" "Contact" "postmaster@responsys.com" "with" "any" "questions" "concerning" "this" "signing" "; p=MIGfMA0GCSqGSIb3DQ
EBAQUAA4GNADCBiQKBgQC/Vh/xq+sSRLhL5CRU1drFTGMXX/Q2KkWgl35hO4v6dTy5Qmxcuv5AwqxLiz9d0jBaxtuvYALjlGkxmk5MemgAOcCr97GlW7Cr11eLn87qdTmyE5LevnTXxVDMjIfQJt6O
Fzmw6Tp1t05NPWh0PbyUohZYt4qpcbiz9Kc3UB2IBwIDAQAB;"
[+] DMARC Record : "v=DMARC1; p=reject; fo=1; rua=mailto:dmarc_rua@emaildefense.proofpoint.com; ruf=mailto:dmarc_ruf@emaildefense.proofpoint.com"
[+] BIMI Record : "v=BIMI1; f=svg; z=256x256; l=https://static.cdn.responsys.net/i2/responsysimages/content/united/UA-email-tailfin_256x256.svg"
```


## Getting help

Here an useful document related secure email:

    https://www.cisco.com/c/en/us/support/docs/security/email-security-appliance/215360-best-practice-for-email-authentication.html 


## Author(s)

This project was written and is maintained by the following individuals:

* Matias Ortiz <matias.ortiz@bvstv.com>

