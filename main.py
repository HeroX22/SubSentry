import subprocess
import os
import sys
import re

def run_theharvester(target, sources, verbose):
    print("Running theHarvester...")
    output_filename = f"theHarvester_{target}.txt"
    with open(output_filename, 'w') as output_file:
        for source in sources:
            command = f"theHarvester -d {target} -b {source}"
            if verbose:
                print(f"Command: {command}")
            result = subprocess.check_output(command, shell=True, text=True)
            output_file.write(result)
            output_file.write("\n")
            if verbose:
                print(result)
    print(f"theHarvester results saved to {output_filename}.")
    return output_filename

def run_sublist3r(target, verbose):
    print("Running Sublist3r...")
    command = f"sublist3r -o Sublist3r_{target}.txt -d {target} -t 30"
    if verbose:
        print(f"Command: {command}")
    subprocess.run(command, shell=True)
    print(f"Sublist3r results saved to Sublist3r_{target}.txt.")

def run_subfinder(target, verbose):
    print("Running Subfinder...")
    command = f"subfinder -d {target} -all -o Subfinder_{target}.txt"
    if verbose:
        print(f"Command: {command}")
    subprocess.run(command, shell=True)
    print(f"Subfinder results saved to Subfinder_{target}.txt.")

def clean_theharvester_results(target):
    print(f"Cleaning results from theHarvester...")
    input_filename = f"theHarvester_{target}.txt"
    output_filename = f"theHarvester_clean_{target}.txt"
    email_filename = f"email_{target}.txt"
    ip_filename = f"ip_address_{target}.txt"
    
    # Load the cleanup word list
    with open('cleanup.txt', 'r') as cleanup_file:
        cleanup_words = [line.strip() for line in cleanup_file]

    cleaned_subdomains = set()
    emails = set()
    ip_addresses = set()

    # Regular expression to match IP addresses
    ip_regex = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')

    # Process theHarvester results
    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile, open(email_filename, 'w') as emailfile, open(ip_filename, 'w') as ipfile:
        for line in infile:
            cleaned_line = line.strip()
            
            if "@" in cleaned_line:
                emails.add(cleaned_line)
                emailfile.write(cleaned_line + "\n")
            elif ip_regex.search(cleaned_line):
                ip_addresses.add(cleaned_line)
                ipfile.write(cleaned_line + "\n")
            elif cleaned_line and not any(word in cleaned_line for word in cleanup_words):
                cleaned_subdomains.add(cleaned_line)
                outfile.write(cleaned_line + "\n")

    print(f"Cleaned theHarvester results saved to {output_filename}, emails saved to {email_filename}, and IP addresses saved to {ip_filename}.")
    return cleaned_subdomains

def combine_and_deduplicate(target):
    print("Combining and deduplicating results...")
    all_subdomains = set()

    # Load results from theHarvester
    cleaned_subdomains = clean_theharvester_results(target)
    all_subdomains.update(cleaned_subdomains)

    # Load results from Sublist3r
    with open(f"Sublist3r_{target}.txt", 'r') as sublist3r_file:
        sublist3r_results = set(line.strip() for line in sublist3r_file if line.strip())
        all_subdomains.update(sublist3r_results)

    # Load results from Subfinder
    with open(f"Subfinder_{target}.txt", 'r') as subfinder_file:
        subfinder_results = set(line.strip() for line in subfinder_file if line.strip())
        all_subdomains.update(subfinder_results)

    # Remove duplicates and save to domain.txt
    with open('domain.txt', 'w') as domain_file:
        for subdomain in sorted(all_subdomains):
            domain_file.write(subdomain + "\n")
    
    print("All subdomains combined and deduplicated in domain.txt.")
    return all_subdomains

def run_subsnipe(verbose):
    print("Running Subsnipe...")
    command = "./subsnipe -f domain.txt -t 30"
    if verbose:
        print(f"Command: {command}")
    result = subprocess.check_output(command, shell=True, text=True)
    with open('output.md', 'w') as output_file:
        output_file.write(result)
    print("Subsnipe results saved to output.md.")
    return result

def save_final_results(target):
    print(f"Saving final results to {target}_final.txt...")
    with open('domain.txt', 'r') as domain_file, open(f"email_{target}.txt", 'r') as email_file, open(f"ip_address_{target}.txt", 'r') as ip_file, open('output.md', 'r') as vuln_file, open(f"{target}_final.txt", 'w') as final_file:
        final_file.write("-=subdomain=-\n")
        final_file.write(domain_file.read())
        
        final_file.write("\n-=E-Mail=-\n")
        final_file.write(email_file.read())
        
        final_file.write("\n-=IP-Address=-\n")
        final_file.write(ip_file.read())
        
        final_file.write("\n-=Vuln=-\n")
        final_file.write(vuln_file.read())
    
    print(f"Final results saved to {target}_final.txt.")

def main():
    if len(sys.argv) < 2 or (len(sys.argv) == 2 and not any(arg.startswith('-t') or arg.startswith('--target') for arg in sys.argv)):
        print("Usage: python3 script.py -t domain.com [-v]")
        sys.exit(1)

    verbose = '-v' in sys.argv or '--verbose' in sys.argv
    target = next((arg.split('=')[-1] for arg in sys.argv if arg.startswith('-t') or arg.startswith('--target')), None)
    
    if not target:
        print("Error: Target not specified.")
        sys.exit(1)

    sources = [
        "anubis", "baidu", "bingapi", "certspotter", "crtsh",
        "dnsdumpster", "duckduckgo", "hackertarget", "otx", "rapiddns",
        "sitedossier", "subdomaincenter", "subdomainfinderc99", "threatminer",
        "urlscan", "virustotal", "yahoo"
    ]

    # Run theHarvester
    run_theharvester(target, sources, verbose)
    
    # Run Sublist3r (results saved automatically)
    run_sublist3r(target, verbose)
    
    # Run Subfinder (results saved automatically)
    run_subfinder(target, verbose)
    
    # Combine and deduplicate subdomains
    combine_and_deduplicate(target)
    
    # Run Subsnipe for vulnerability analysis
    run_subsnipe(verbose)
    
    # Save final results
    save_final_results(target)

if __name__ == "__main__":
    main()
