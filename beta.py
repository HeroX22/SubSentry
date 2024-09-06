import subprocess
import os
import sys

# Helper function to log messages
def log_message(message, log_enabled):
    if log_enabled:
        with open('log.txt', 'a') as log_file:
            log_file.write(message + '\n')
    print(message)

def run_theharvester(target, sources, verbose, log_enabled):
    log_message("Running theHarvester...", log_enabled)
    results = []
    for source in sources:
        log_message(f"Searching with source: {source}", log_enabled)
        command = f"theHarvester -d {target} -b {source}"
        if verbose:
            log_message(f"Command: {command}", log_enabled)
        result = subprocess.check_output(command, shell=True, text=True)
        results.append(result)
        if verbose:
            log_message(result, log_enabled)
    log_message("theHarvester completed.", log_enabled)
    return results

def run_sublist3r(target, verbose, log_enabled):
    log_message("Running Sublist3r...", log_enabled)
    command = f"sublist3r -d {target} -t 30"
    if verbose:
        log_message(f"Command: {command}", log_enabled)
    result = subprocess.check_output(command, shell=True, text=True)
    if verbose:
        log_message(result, log_enabled)
    log_message("Sublist3r completed.", log_enabled)
    return result

def run_subfinder(target, verbose, log_enabled):
    log_message("Running Subfinder...", log_enabled)
    command = f"subfinder -d {target} -all"
    if verbose:
        log_message(f"Command: {command}", log_enabled)
    result = subprocess.check_output(command, shell=True, text=True)
    if verbose:
        log_message(result, log_enabled)
    log_message("Subfinder completed.", log_enabled)
    return result

def run_subsnipe(verbose, log_enabled):
    log_message("Running Subsnipe...", log_enabled)
    command = "./subsnipe -f domain.txt -t 30"
    if verbose:
        log_message(f"Command: {command}", log_enabled)
    result = subprocess.check_output(command, shell=True, text=True)
    if verbose:
        log_message(result, log_enabled)
    log_message("Subsnipe completed.", log_enabled)
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
        print("Usage: python3 script.py --target=domain.com [-v] [--debug]")
        sys.exit(1)

    verbose = '-v' in sys.argv
    debug = '--debug' in sys.argv
    target = next((arg for arg in sys.argv if arg.startswith('--target=')), '').replace("--target=", "")
    
    if not target:
        print("Error: Target not specified.")
        sys.exit(1)

    # Enable or disable logging
    log_enabled = '--debug' in sys.argv

    sources = [
        "anubis", "baidu", "bingapi", "certspotter", "crtsh",
        "dnsdumpster", "duckduckgo", "hackertarget", "otx", "rapiddns",
        "sitedossier", "subdomaincenter", "subdomainfinderc99", "threatminer",
        "urlscan", "virustotal", "yahoo", "zoomeye"
    ]

    # Run theHarvester
    harvester_results = run_theharvester(target, sources, verbose, log_enabled)
    
    # Run Sublist3r
    sublist3r_results = run_sublist3r(target, verbose, log_enabled)
    
    # Run Subfinder
    subfinder_results = run_subfinder(target, verbose, log_enabled)
    
    # Save intermediate results to domain.txt with tool markers
    log_message("Combining results into domain.txt...", log_enabled)
    with open('domain.txt', 'w') as file:
        if debug:
            file.write("-=DEBUG MODE ENABLED=-\n")
        
        file.write("-=TheHarvester=-\n")
        for result in harvester_results:
            lines = result.splitlines()
            for line in lines:
                # Filter out lines containing 'Target' and '*******************************************************************'
                if 'Target' in line or '*******************************************************************' in line:
                    continue
                if ':' in line:  # Handles <subdomain>:<IP>
                    subdomain = line.split(':')[0]
                    file.write(subdomain + '\n')
                elif line and not line.startswith('[') and ' ' not in line:  # Only subdomains
                    file.write(line + '\n')

        file.write("\n-=Sublist3r=-\n")
        file.write(sublist3r_results)

        file.write("\n-=Subfinder=-\n")
        file.write(subfinder_results)

    # Run Subsnipe
    vuln_results = run_subsnipe(verbose, log_enabled)
    
    # Process and remove duplicates
    log_message("Processing results and removing duplicates...", log_enabled)
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
    log_message("Debungging mode!", log_enabled)
    #os.remove('domain.txt')
    print("Done.")

if __name__ == "__main__":
    main()
