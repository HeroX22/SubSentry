import subprocess
import os
import sys

def run_theharvester(target, sources, verbose):
    print("Running theHarvester...")
    results = []
    for source in sources:
        print(f"Searching with source: {source}")
        command = f"theHarvester -d {target} -b {source}"
        if verbose:
            print(f"Command: {command}")
        result = subprocess.check_output(command, shell=True, text=True)
        results.append(result)
        if verbose:
            print(result)
    print("theHarvester completed.")
    return results

def run_sublist3r(target, verbose):
    print("Running Sublist3r...")
    command = f"sublist3r -d {target} -t 30"
    if verbose:
        print(f"Command: {command}")
    result = subprocess.check_output(command, shell=True, text=True)
    if verbose:
        print(result)
    print("Sublist3r completed.")
    return result

def run_subfinder(target, verbose):
    print("Running Subfinder...")
    command = f"subfinder -d {target} -all"
    if verbose:
        print(f"Command: {command}")
    result = subprocess.check_output(command, shell=True, text=True)
    if verbose:
        print(result)
    print("Subfinder completed.")
    return result

def run_subsnipe(verbose):
    print("Running Subsnipe...")
    command = "./subsnipe -f vuln_subsnipe/domain.txt -t 30"
    if verbose:
        print(f"Command: {command}")
    result = subprocess.check_output(command, shell=True, text=True)
    if verbose:
        print(result)
    print("Subsnipe completed.")
    return result

def save_results(filename, subdomains, emails, vuln_results):
    print(f"Saving results to {filename}...")
    with open(filename, 'w') as file:
        file.write("-=subdomain=-\n")
        for subdomain in subdomains:
            file.write(f"{subdomain}\n")
        
        file.write("\n-=E-Mail=-\n")
        for email in emails:
            file.write(f"{email}\n")
        
        file.write("\n-=Vuln=-\n")
        file.write(vuln_results)
    print("Results saved.")

def main():
    if len(sys.argv) < 2 or (len(sys.argv) == 2 and sys.argv[1] != '--target='):
        print("Usage: python3 script.py --target=domain.com [-v]")
        sys.exit(1)

    verbose = '-v' in sys.argv
    target = next((arg for arg in sys.argv if arg.startswith('--target=')), '').replace("--target=", "")
    
    if not target:
        print("Error: Target not specified.")
        sys.exit(1)

    sources = [
        "anubis", "baidu", "bingapi", "certspotter", "crtsh",
        "dnsdumpster", "duckduckgo", "hackertarget", "otx", "rapiddns",
        "sitedossier", "subdomaincenter", "subdomainfinderc99", "threatminer",
        "urlscan", "virustotal", "yahoo", "zoomeye"
    ]

    # Run theHarvester
    harvester_results = run_theharvester(target, sources, verbose)
    
    # Run Sublist3r
    sublist3r_results = run_sublist3r(target, verbose)
    
    # Run Subfinder
    subfinder_results = run_subfinder(target, verbose)
    
    # Save intermediate results to domain.txt
    print("Combining results into domain.txt...")
    with open('vuln_subsnipe/domain.txt', 'w') as file:
        for result in harvester_results:
            file.write(result)
        file.write("\n")
        file.write(sublist3r_results)
        file.write("\n")
        file.write(subfinder_results)

    # Run Subsnipe
    vuln_results = run_subsnipe(verbose)
    
    # Process and remove duplicates
    print("Processing results and removing duplicates...")
    subdomains = set()
    emails = set()
    # Process theHarvester results
    for result in harvester_results:
        lines = result.splitlines()
        is_email_section = False
        for line in lines:
            if "Emails found" in line:
                is_email_section = True
            elif "Hosts found" in line:
                is_email_section = False
            elif is_email_section:
                if line:
                    emails.add(line.strip())
            elif line and line not in ["[*] Hosts found:", "---------------------"]:
                subdomains.add(line.strip())

    # Process Sublist3r results
    lines = sublist3r_results.splitlines()
    for line in lines:
        if line and line not in ["[-] Total Unique Subdomains Found:", ""]:
            subdomains.add(line.strip())

    # Process Subfinder results
    lines = subfinder_results.splitlines()
    for line in lines:
        if line and line not in ["[INF] Found", "subdomains for", "in"]:
            subdomains.add(line.strip())

    # Process vuln_results
    vuln_results = vuln_results.replace('### Not Exploitable', '').replace('### Exploitability Unknown', '')

    # Save final results
    output_filename = f"{target}_subdomain.txt"
    save_results(output_filename, subdomains, emails, vuln_results)

    # Cleanup
    #print("Cleaning up...")
    print("Debungging mode!")
    #os.remove('vuln_subsnipe/domain.txt')
    print("Done.")

if __name__ == "__main__":
    main()
