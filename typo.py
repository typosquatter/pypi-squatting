import requests
import json
import os
import argparse
import inflect
import math
import string
import yaml

numerals = [
    ["0", "zero"],
    ["1", "one", "first"],
    ["2", "two", "second"],
    ["3", "three", "third"],
    ["4", "four", "fourth", "for"],
    ["5", "five", "fifth"],
    ["6", "six", "sixth"],
    ["7", "seven", "seventh"],
    ["8", "eight", "eighth"],
    ["9", "nine", "ninth"]
]

algo_list = ["omission", "repetition", "changeOrder", "replacement", "addition", "missingDot", "stripDash", "vowelSwap", "addDash", "homoglyph", "commonMisspelling", "homophones", "singularePluralize", "changeDotDashUnderscore", "numeralSwap"]


def merge_loc_main_list(loc_variations_list, variations_list, givevariations, algoName=''):
    for element in loc_variations_list:
        if givevariations:
            flag = False
            for var in algo_list:
                if [element, var] in variations_list:
                    flag = True
            if not flag:
                variations_list.append([element, algoName])
        else:
            if element not in variations_list:
                variations_list.append(element)
    return variations_list


def final_treatment(package_name, variations_list, limit, givevariations, keeporiginal, algo_name):
    """ Final treatment of a variation's function, keep original and name of variations' algorithm """
    if not keeporiginal:
        try:
            if givevariations:
                variations_list.remove([package_name, algo_name])
            else:
                variations_list.remove(package_name)
        except:
            pass
    elif givevariations:
        try:
            variations_list.remove([package_name, algo_name])
        except:
            pass
        if not [package_name, 'original'] in variations_list:
            variations_list.insert(0, [package_name, 'original'])
    else:
        if package_name not in variations_list:
            variations_list.insert(0, package_name)

    while len(variations_list) > limit:
        variations_list.pop()

    return variations_list



def addDash(package_name, variations_list, verbose, limit, givevariations, keeporiginal):
    if not len(variations_list) >= limit:
        cp_variations = 0
        if verbose:
            print("[+] addDash")

        loc_variations_list = list()

        if len(package_name) > 1:
            for i in range(1, len(package_name)):
                variation = package_name[:i] + "-" + package_name[i:]
                if variation not in loc_variations_list:
                    cp_variations += 1
                    loc_variations_list.append(variation)
        
        if verbose:
            print(f"{cp_variations}\n")

        variations_list = merge_loc_main_list(loc_variations_list, variations_list, givevariations, algoName='addDash')
        variations_list = final_treatment(package_name, variations_list, limit, givevariations, keeporiginal, "addDash")

    return variations_list


def addition(package_name, variations_list, verbose, limit, givevariations, keeporiginal):
    if not len(variations_list) >= limit:
        cp_variations = 0
        if verbose:
            print("[+] addition")

        loc_variations_list = list()

        for i in (*range(48, 58), *range(97, 123)):
            # Adding 'i' in front of 'name'
            variation = chr(i) + package_name
            if variation not in loc_variations_list:
                loc_variations_list.append(variation)
                cp_variations += 1

            for j in range(0, len(package_name)):
                variation = package_name[:j] + chr(i) + package_name[j:]
                if variation not in loc_variations_list:
                    loc_variations_list.append(variation)
                    cp_variations += 1
                
            # Adding 'i' at the end of 'name'
            variation = package_name + chr(i)
            if variation not in loc_variations_list:
                loc_variations_list.append(variation)
            
        loc_variations_list.append(f"python-{package_name}")
        loc_variations_list.append(f"python3-{package_name}")
        cp_variations += 2

        if verbose:
            print(f"{cp_variations}\n")

        variations_list = merge_loc_main_list(loc_variations_list, variations_list, givevariations, algoName='addition')
        variations_list = final_treatment(package_name, variations_list, limit, givevariations, keeporiginal, "addition")

    return variations_list


def changeOrder(package_name, variations_list, verbose, limit, givevariations, keeporiginal):
    if not len(variations_list) >= limit:
        cp_variations = 0
        if verbose:
            print("[+] changeOrder")

        loc_variations_list = list()

        if len(package_name) > 1:
            for i in range(0, len(package_name)):
                loc = package_name[0:i] + package_name[i+1:]
                for j in range(0, len(loc)):
                    variation = loc[:j] + package_name[i] + loc[j:]
                    if not variation in loc_variations_list:
                        loc_variations_list.append(variation)
                        cp_variations += 1
        
        if verbose:
            print(f"{cp_variations}\n")

        variations_list = merge_loc_main_list(loc_variations_list, variations_list, givevariations, algoName='changeOrder')
        variations_list = final_treatment(package_name, variations_list, limit, givevariations, keeporiginal, "changeOrder")
    return variations_list


def changeDotDashUnderscore(package_name, variations_list, verbose, limit, givevariations, keeporiginal):
    if not len(variations_list) >= limit:
        cp_variations = 0
        if verbose:
            print("[+] changeDotDashUnderscore")

        loc_variations_list = list()

        loc = package_name
        while "." in loc:
            ch_dash_inv = loc[::-1].replace(".", "-", 1)[::-1]
            ch_dash = loc.replace(".", "-", 1)

            ch_und_inv = loc[::-1].replace(".", "_", 1)[::-1]
            ch_und = loc.replace(".", "_", 1)

            if ch_dash_inv not in loc_variations_list:
                loc_variations_list.append(ch_dash_inv)
                cp_variations += 1
            if ch_dash not in loc_variations_list:
                loc_variations_list.append(ch_dash)
                cp_variations += 1

            if ch_und_inv not in loc_variations_list:
                loc_variations_list.append(ch_und_inv)
                cp_variations += 1
            if ch_und not in loc_variations_list:
                loc_variations_list.append(ch_und)
                cp_variations += 1

            loc = loc.replace(".", "-", 1)

        loc = package_name
        while "-" in loc:
            ch_dot_inv = loc[::-1].replace("-", ".", 1)[::-1]
            ch_dot = loc.replace("-", ".", 1)

            ch_und_inv = loc[::-1].replace("-", "_", 1)[::-1]
            ch_und = loc.replace("-", "_", 1)

            if ch_dot_inv not in loc_variations_list:
                loc_variations_list.append(ch_dot_inv)
                cp_variations += 1
            if ch_dot not in loc_variations_list:
                loc_variations_list.append(ch_dot)
                cp_variations += 1

            if ch_und_inv not in loc_variations_list:
                loc_variations_list.append(ch_und_inv)
                cp_variations += 1
            if ch_und not in loc_variations_list:
                loc_variations_list.append(ch_und)
                cp_variations += 1

            loc = loc.replace("-", ".", 1)

        loc = package_name
        while "_" in loc:
            ch_dot_inv = loc[::-1].replace("_", ".", 1)[::-1]
            ch_dot = loc.replace("_", ".", 1)

            ch_dash_inv = loc[::-1].replace("_", "-", 1)[::-1]
            ch_dash = loc.replace("_", "-", 1)

            if ch_dot_inv not in loc_variations_list:
                loc_variations_list.append(ch_dot_inv)
                cp_variations += 1
            if ch_dot not in loc_variations_list:
                loc_variations_list.append(ch_dot)
                cp_variations += 1

            if ch_dash_inv not in loc_variations_list:
                loc_variations_list.append(ch_dash_inv)
                cp_variations += 1
            if ch_dash not in loc_variations_list:
                loc_variations_list.append(ch_dash)
                cp_variations += 1

            loc = loc.replace("_", ".", 1)

        if verbose:
            print(f"{cp_variations}\n")

        variations_list = merge_loc_main_list(loc_variations_list, variations_list, givevariations, algoName='changeDotDashUnderscore')
        variations_list = final_treatment(package_name, variations_list, limit, givevariations, keeporiginal, "changeDotDashUnderscore")
    
    return variations_list


def commonMisspelling(package_name, variations_list, verbose, limit, givevariations, keeporiginal):
    if not len(variations_list) >= limit:
        cp_variations = 0
        if verbose:
            print("[+] commonMisspelling")

        loc_variations_list = list()

        with open(os.getcwd() + "/etc/common-misspellings.json", "r") as read_json:
            misspelling = json.load(read_json)
            keys = misspelling.keys()

        if package_name in keys:
            misspell = misspelling[package_name].split(",")
            for mis in misspell:
                if mis.replace(" ","") not in loc_variations_list:
                    loc_variations_list.append(mis.replace(" ",""))
                    cp_variations += 1

        if verbose:
            print(f"{cp_variations}\n")

        variations_list = merge_loc_main_list(loc_variations_list, variations_list, givevariations, algoName='commonMisspelling')
        variations_list = final_treatment(package_name, variations_list, limit, givevariations, keeporiginal, "commonMisspelling")
    
    return variations_list


def homophones(package_name, variations_list, verbose, limit, givevariations, keeporiginal):
    if not len(variations_list) >= limit:
        cp_variations = 0
        if verbose:
            print("[+] homophones")

        loc_variations_list = list()

        with open(os.getcwd() + "/etc/homophones.txt", "r") as read_file:
            homophones = read_file.readlines()
        
        for lines in homophones:
            line = lines.split(",")
            for word in line:
                if package_name == word.rstrip("\n"):
                    for otherword in line:
                        if otherword.rstrip("\n") not in loc_variations_list and otherword.rstrip("\n") != package_name:
                            loc_variations_list.append(otherword.rstrip("\n"))
                            cp_variations += 1
        
        if verbose:
            print(f"{cp_variations}\n")

        variations_list = merge_loc_main_list(loc_variations_list, variations_list, givevariations, algoName='homophones')
        variations_list = final_treatment(package_name, variations_list, limit, givevariations, keeporiginal, "homophones")

    return variations_list

    
def missingDot(package_name, variations_list, verbose, limit, givevariations, keeporiginal):
    if not len(variations_list) >= limit:
        cp_variations = 0
        if verbose:
            print("[+] missingDot")

        loc_variations_list = list()

        loc = package_name
        while "." in loc:
            loc = loc.replace(".", "", 1)
            if loc not in loc_variations_list:
                loc_variations_list.append(loc)
                cp_variations += 1

        if verbose:
            print(f"{cp_variations}\n")

        variations_list = merge_loc_main_list(loc_variations_list, variations_list, givevariations, algoName='missingDot')
        variations_list = final_treatment(package_name, variations_list, limit, givevariations, keeporiginal, "missingDot")

    return variations_list


def numeralSwap(package_name, variations_list, verbose, limit, givevariations, keeporiginal):
    if not len(variations_list) >= limit:
        cp_variations = 0
        if verbose:
            print("[+] numeralSwap")

        loc_variations_list = list()

        for numerals_list in numerals:
            for nume in numerals_list:
                if nume in package_name:
                    for nume2 in numerals_list:
                        if not nume2 == nume:
                            loc = package_name.replace(nume, nume2)
                            if not loc in loc_variations_list:
                                loc_variations_list.append(loc)
                                cp_variations += 1
        
        if verbose:
            print(f"{cp_variations}\n")

        variations_list = merge_loc_main_list(loc_variations_list, variations_list, givevariations, algoName='numeralSwap')
        variations_list = final_treatment(package_name, variations_list, limit, givevariations, keeporiginal, "numeralSwap")
    
    return variations_list

def omission(package_name, variations_list, verbose, limit, givevariations, keeporiginal):
    if not len(variations_list) >= limit:
        cp_variations = 0
        if verbose:
            print("[+] omission")

        loc_variations_list = list()

        for i in range(0,len(package_name)):
            loc = package_name[0:i]
            loc += package_name[i+1:len(package_name)]

            if loc not in loc_variations_list:
                loc_variations_list.append(loc)
                cp_variations += 1

        if verbose:
            print(f"{cp_variations}\n")

        variations_list = merge_loc_main_list(loc_variations_list, variations_list, givevariations, algoName='omission')
        variations_list = final_treatment(package_name, variations_list, limit, givevariations, keeporiginal, "omission")
    
    return variations_list


def repetition(package_name, variations_list, verbose, limit, givevariations, keeporiginal):
    if not len(variations_list) >= limit:
        cp_variations = 0
        if verbose:
            print("[+] repetition")

        loc_variations_list = list()

        for i, c in enumerate(package_name):
            variation = package_name[:i] + c + package_name[i:]
            if variation not in loc_variations_list:
                loc_variations_list.append(variation)
                cp_variations += 1

        if verbose:
            print(f"{cp_variations}\n")

        variations_list = merge_loc_main_list(loc_variations_list, variations_list, givevariations, algoName='repetition')
        variations_list = final_treatment(package_name, variations_list, limit, givevariations, keeporiginal, "repetition")

    return variations_list


def replacement(package_name, variations_list, verbose, limit, givevariations, keeporiginal):
    if not len(variations_list) >= limit:
        cp_variations = 0
        if verbose:
            print("[+] replacement")
        
        loc_variations_list = list()

        for i in (*range(48, 58), *range(97, 123)):
            for j in range(0, len(package_name)):
                pre = package_name[:j]
                suf = package_name[j+1:]
                variation = pre + chr(i) + suf

                if variation not in loc_variations_list:
                    loc_variations_list.append(variation)
                    cp_variations += 1
        
        if verbose:
            print(f"{cp_variations}\n")

        variations_list = merge_loc_main_list(loc_variations_list, variations_list, givevariations, algoName='replacement')
        variations_list = final_treatment(package_name, variations_list, limit, givevariations, keeporiginal, "replacement")

    return variations_list


def stripDash(package_name, variations_list, verbose, limit, givevariations, keeporiginal):
    if not len(variations_list) >= limit:
        cp_variations = 0
        if verbose:
            print("[+] stripDash")

        loc_variations_list = list()

        loc = package_name
        while "-" in loc:
            loc = loc.replace("-", "", 1)
            if loc not in loc_variations_list:
                loc_variations_list.append(loc)
                cp_variations += 1

        if verbose:
            print(f"{cp_variations}\n")

        variations_list = merge_loc_main_list(loc_variations_list, variations_list, givevariations, algoName='stripDash')
        variations_list = final_treatment(package_name, variations_list, limit, givevariations, keeporiginal, "stripDash")

    return variations_list


def singularPluralize(package_name, variations_list, verbose, limit, givevariations, keeporiginal):
    if not len(variations_list) >= limit:
        cp_variations = 0
        if verbose:
            print("[+] singularPluralize")

        loc_variations_list = list()

        inflector = inflect.engine()
        loc = inflector.plural(package_name)

        if loc and loc not in loc_variations_list:
            loc_variations_list.append(loc)
            cp_variations += 1

        if verbose:
            print(f"{cp_variations}\n")

        variations_list = merge_loc_main_list(loc_variations_list, variations_list, givevariations, algoName='singularPluralize')
        variations_list = final_treatment(package_name, variations_list, limit, givevariations, keeporiginal, "singularPluralize")
    
    return variations_list


def vowelSwap(package_name, variations_list, verbose, limit, givevariations, keeporiginal):
    if not len(variations_list) >= limit:
        cp_variations = 0
        if verbose:
            print("[+] vowelSwap")

        loc_variations_list = list()

        vowels = ["a", "e", "i", "o", "u", "y"]

        for j in vowels:
            for k in vowels:
                if j != k:
                    loc = package_name.replace(k, j)
                    if loc not in variations_list:
                        variations_list.append(loc)
                        cp_variations += 1

        if verbose:
            print(f"{cp_variations}\n")

        variations_list = merge_loc_main_list(loc_variations_list, variations_list, givevariations, algoName='vowelSwap')
        variations_list = final_treatment(package_name, variations_list, limit, givevariations, keeporiginal, "vowelSwap")
    
    return variations_list




def formatYara(resultList, domain, givevariations=False):
    """Output in yara format"""
    domainReplace = domain.replace(".", "_")

    rule = f"rule {domainReplace} {{\n\tmeta:\n\t\t"
    rule += f'domain = "{domain}"\n\t'
    rule += "strings: \n"

    cp = 0
    for result in resultList: 
        if givevariations:
            result = result[0]
        rule += f'\t\t$s{cp} = "{result}"\n'
        cp += 1
    
    rule += "\tcondition:\n\t\t any of ($s*)\n}" 

    return rule

def formatRegex(resultList, givevariations=False):
    """Output in regex format"""
    regex = ""
    for result in resultList:
        if givevariations:
            result = result[0]
        reg = ""
        for car in result:
            if car in string.ascii_letters or car in string.digits:
                reg += car
            elif car in string.punctuation:
                reg += "\\" + car
        regex += f"{reg}|"
    regex = regex[:-1]

    return regex

def formatYaml(resultList, domain, givevariations=False):
    """Output in yaml format"""
    yaml_file = {"title": domain}
    variations = list()

    for result in resultList:
        if givevariations:
            variations.append(result[0])
        else:
            variations.append(result)

    yaml_file["variations"] = variations

    return yaml_file


def formatOutput(format, variations_list, domain, pathOutput, givevariations=False):
    """
    Call different function to create the right format file
    """

    if format == "text":
        if pathOutput and not pathOutput == "-":
            with open(f"{pathOutput}/{domain}.txt", "w", encoding='utf-8') as write_file:
                for element in variations_list:
                    if givevariations:
                        write_file.write(f"{element[0]}, {element[1]}\n")
                    else:
                        write_file.write(element + "\n")
        elif pathOutput == "-":
            for element in variations_list:
                if givevariations:
                    print(f"{element[0]}, {element[1]}")
                else:
                    print(element)

    elif format == "yara":
        yara = formatYara(variations_list, domain, givevariations)
        if pathOutput and not pathOutput == "-":
            with open(f"{pathOutput}/{domain}.yar", "w", encoding='utf-8') as write_file:
                write_file.write(yara)
        elif pathOutput == "-":
            print(yara)

    elif format == "regex":
        regex = formatRegex(variations_list, givevariations)
        if pathOutput and not pathOutput == "-":
            with open(f"{pathOutput}/{domain}.regex", "w", encoding='utf-8') as write_file:
                write_file.write(regex)
        elif pathOutput == "-":
            print(regex)

    elif format == "yaml":
        yaml_file = formatYaml(variations_list, domain, givevariations)
        if pathOutput and not pathOutput == "-":
            with open(f"{pathOutput}/{domain}.yml", "w", encoding='utf-8') as write_file:
                yaml.dump(yaml_file, write_file)
        elif pathOutput == "-":
            print(yaml_file)
    else:
        print(f"Unknown format: {format}. Will use text format instead")
        formatOutput("text", variations_list, domain, pathOutput, givevariations)


def package_resolver(variations_list, package_name, pathOutput, verbose, givevariations):
    package_resolved = dict()

    for package_variation_name in variations_list:
        loc_dict = dict()
        if givevariations:
            to_resolve = package_variation_name[0]
            variations_algo = package_variation_name[1]
            if not variations_algo in package_resolved:
                package_resolved[variations_algo] = list()
            loc_dict[to_resolve] = dict()
        else:
            to_resolve = package_variation_name
            package_resolved[to_resolve] = dict()

        response = requests.get(f"https://pypi.org/pypi/{to_resolve}/json")
        if response.status_code == 200:
            if givevariations:
                loc_dict[to_resolve]["exist"] = True
                loc_dict[to_resolve]["url"] = f"https://pypi.org/project/{to_resolve}"
                loc_dict[to_resolve]["json"] = dict()
                loc_dict[to_resolve]["json"]["info"] = response.json()["info"]
                loc_dict[to_resolve]["json"]["urls"] = response.json()["urls"]
                loc_dict[to_resolve]["json"]["vulnerabilities"] = response.json()["vulnerabilities"]
            else:
                package_resolved[to_resolve]["exist"] = True
                package_resolved[to_resolve]["url"] = f"https://pypi.org/project/{to_resolve}"
                package_resolved[to_resolve]["json"] = response.json()
                package_resolved[to_resolve]["json"] = dict()
                package_resolved[to_resolve]["json"]["info"] = response.json()["info"]
                package_resolved[to_resolve]["json"]["urls"] = response.json()["urls"]
                package_resolved[to_resolve]["json"]["vulnerabilities"] = response.json()["vulnerabilities"]
        else:
            if givevariations:
                loc_dict[to_resolve]["exist"] = False
                loc_dict[to_resolve]["json"] = response.json()
            else:
                package_resolved[to_resolve]["exist"] = False
                package_resolved[to_resolve]["json"] = response.json()
        
        if loc_dict:
            package_resolved[variations_algo].append(loc_dict)

        if pathOutput and not pathOutput == "-":
            with open(f"{pathOutput}/{package_name}_resolve.json", "w", encoding='utf-8') as write_json:
                json.dump(package_resolved, write_json, indent=4)
    
    if pathOutput == '-':
        print()
        print(json.dumps(package_resolved), flush=True)
    
    return package_resolved


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--packageName", help="package name", required=True)

    parser.add_argument("-v", help="verbose, more display", action="store_true")
    parser.add_argument("-l", "--limit", help="limit of variations")
    parser.add_argument("-var", "--givevariations", help="give the algo that generate variations", action="store_true")
    parser.add_argument("-ko", "--keeporiginal", help="Keep in the result list the original package name", action="store_true")
    parser.add_argument("-pr", "--pypiresolver", help="Find which variations is a package on pypi", action="store_true")

    parser.add_argument("-o", "--output", help="path to ouput location")
    parser.add_argument("-fo", "--formatoutput", help="format for the output file, yara - regex - yaml - text. Default: text")

    parser.add_argument("-a", "--all", help="Use all algo", action="store_true")

    parser.add_argument("-ada", "--adddash", help="Add a dash between the first and last character in a string", action="store_true")
    parser.add_argument("-add", "--addition", help="Add a character", action="store_true")
    parser.add_argument("-cho", "--changeorder", help="Change the order of letters in word", action="store_true")
    parser.add_argument("-cddu", "--changedotdashunderscore", help="Change dot to dash", action="store_true")
    parser.add_argument("-cm", "--commonmisspelling", help="Change a word by is misspellings", action="store_true")
    parser.add_argument("-hp", "--homophones", help="Change word by an other who sound the same when spoken", action="store_true")
    parser.add_argument("-md", "--missingdot", help="Delete dots one by one", action="store_true")
    parser.add_argument("-ns", "--numeralswap", help="Change a numbers to words and vice versa. Ex: circlone.lu, circl1.lu", action="store_true")
    parser.add_argument("-om", "--omission", help="Leave out a letter", action="store_true")
    parser.add_argument("-repe", "--repetition", help="Character Repeat", action="store_true")
    parser.add_argument("-repl", "--replacement", help="Character replacement", action="store_true")
    parser.add_argument("-sd", "--stripdash", help="Delete of a dash", action="store_true")
    parser.add_argument("-sp", "--singularpluralize", help="Create by making a singular package name plural and vice versa", action="store_true")
    parser.add_argument("-vs", "--vowelswap", help="Swap vowels", action="store_true")

    args = parser.parse_args()

    
    variations_list = list()

    package_name = args.packageName
    verbose = args.v
    givevariations = args.givevariations
    keeporiginal = args.keeporiginal

    limit = math.inf
    if args.limit:
        limit = int(args.limit)
    reachLimit = False

    pathOutput = args.output

    if pathOutput and not pathOutput == "-":
        try:
            os.makedirs(pathOutput)
        except:
            pass

    if args.formatoutput:
        if args.formatoutput == "text" or args.formatoutput == "yara" or args.formatoutput == "yaml" or args.formatoutput == "regex":
            formatoutput = args.formatoutput
        else:
            print("[-] Format type error")
            exit(-1)
    else:
        formatoutput = "text"


    if args.adddash or args.all:
        variations_list = addDash(package_name, variations_list, verbose, limit, givevariations, keeporiginal)

    if args.addition or args.all:
        variations_list = addition(package_name, variations_list, verbose, limit, givevariations, keeporiginal)

    if args.changeorder or args.all:
        variations_list = changeOrder(package_name, variations_list, verbose, limit, givevariations, keeporiginal)

    if args.changedotdashunderscore or args.all:
        variations_list = changeDotDashUnderscore(package_name, variations_list, verbose, limit, givevariations, keeporiginal)

    if args.commonmisspelling or args.all:
        variations_list = commonMisspelling(package_name, variations_list, verbose, limit, givevariations, keeporiginal)

    if args.homophones or args.all:
        variations_list = homophones(package_name, variations_list, verbose, limit, givevariations, keeporiginal)

    if args.missingdot or args.all:
        variations_list = missingDot(package_name, variations_list, verbose, limit, givevariations, keeporiginal)

    if args.numeralswap or args.all:
        variations_list = numeralSwap(package_name, variations_list, verbose, limit, givevariations, keeporiginal)

    if args.omission or args.all:
        variations_list = omission(package_name, variations_list, verbose, limit, givevariations, keeporiginal)

    if args.repetition or args.all:
        variations_list = repetition(package_name, variations_list, verbose, limit, givevariations, keeporiginal)

    if args.replacement or args.all:
        variations_list = replacement(package_name, variations_list, verbose, limit, givevariations, keeporiginal)

    if args.singularpluralize or args.all:
        variations_list = singularPluralize(package_name, variations_list, verbose, limit, givevariations, keeporiginal)
    
    if args.stripdash or args.all:
        variations_list = stripDash(package_name, variations_list, verbose, limit, givevariations, keeporiginal)

    if args.vowelswap or args.all:
        variations_list = vowelSwap(package_name, variations_list, verbose, limit, givevariations, keeporiginal)
    

    if verbose:
        print(f"Total: {len(variations_list)}")

    formatOutput(formatoutput, variations_list, package_name, pathOutput, givevariations)

    if args.pypiresolver:
        package_resolver(variations_list, package_name, pathOutput, verbose, givevariations)

