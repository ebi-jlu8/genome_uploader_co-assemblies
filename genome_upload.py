import os
import sys
import logging
import argparse
import re
import json
import pandas as pd
from datetime import date, datetime as dt
from time import sleep
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

metagenomes = ["activated carbon metagenome", "activated sludge metagenome", 
    "aerosol metagenome", "air metagenome", "algae metagenome", "alkali sediment metagenome", 
    "amphibian metagenome", "anaerobic digester metagenome", "anchialine metagenome", 
    "annelid metagenome", "ant fungus garden metagenome", "ant metagenome", 
    "aquaculture metagenome", "aquatic eukaryotic metagenome", "aquatic metagenome", 
    "aquatic viral metagenome", "aquifer metagenome", "ballast water metagenome", 
    "bat gut metagenome", "bat metagenome", "beach sand metagenome", "beetle metagenome", 
    "bentonite metagenome", "bioanode metagenome", "biocathode metagenome", 
    "biofilm metagenome", "biofilter metagenome", "biofloc metagenome", 
    "biogas fermenter metagenome", "bioleaching metagenome", "bioreactor metagenome", 
    "bioreactor sludge metagenome", "bioretention column metagenome", "biosolids metagenome", 
    "bird metagenome", "blood metagenome", "bog metagenome", "book metagenome", 
    "bovine gut metagenome", "bovine metagenome", "brine metagenome", "canine metagenome", 
    "cave metagenome", "cetacean metagenome", "chemical production metagenome", 
    "chicken gut metagenome", "ciliate metagenome", "clay metagenome", "clinical metagenome", 
    "cloud metagenome", "coal metagenome", "cold seep metagenome", "cold spring metagenome", 
    "compost metagenome", "concrete metagenome", "coral metagenome", "coral reef metagenome", 
    "cow dung metagenome", "crab metagenome", "crude oil metagenome", 
    "Crustacea gut metagenome", "crustacean metagenome", "ctenophore metagenome", 
    "decomposition metagenome", "desalination cell metagenome", "dietary supplements metagenome", 
    "dinoflagellate metagenome", "drinking water metagenome", "dust metagenome", 
    "ear metagenome", "echinoderm metagenome", "egg metagenome", "electrolysis cell metagenome", 
    "endophyte metagenome", "epibiont metagenome", "estuary metagenome", "eukaryotic metagenome", 
    "eukaryotic plankton metagenome", "eye metagenome", "factory metagenome", "feces metagenome", 
    "feline metagenome", "fermentation metagenome", "fertilizer metagenome", 
    "fish gut metagenome", "fishing equipment metagenome", "fish metagenome", 
    "floral nectar metagenome", "flotsam metagenome", "flower metagenome", 
    "food contamination metagenome", "food fermentation metagenome", "food metagenome", 
    "food production metagenome", "fossil metagenome", "freshwater metagenome", 
    "freshwater sediment metagenome", "frog metagenome", "fuel tank metagenome", 
    "fungus metagenome", "gas well metagenome", "gill metagenome", "glacier lake metagenome", 
    "glacier metagenome", "gonad metagenome", "grain metagenome", "granuloma metagenome", 
    "groundwater metagenome", "gut metagenome", "halite metagenome", 
    "herbal medicine metagenome", "honeybee metagenome", "honey metagenome", "horse metagenome", 
    "hospital metagenome", "hot springs metagenome", "human bile metagenome", 
    "human blood metagenome", "human brain metagenome", "human eye metagenome", 
    "human feces metagenome", "human gut metagenome", "human hair metagenome", 
    "human lung metagenome", "human metagenome", "human milk metagenome", 
    "human nasopharyngeal metagenome", "human oral metagenome", 
    "human reproductive system metagenome", "human saliva metagenome", 
    "human semen metagenome", "human skeleton metagenome", "human skin metagenome", 
    "human sputum metagenome", "human tracheal metagenome", "human urinary tract metagenome", 
    "human vaginal metagenome", "human viral metagenome", "HVAC metagenome", 
    "hydrocarbon metagenome", "hydrothermal vent metagenome", "hydrozoan metagenome", 
    "hypersaline lake metagenome", "hyphosphere metagenome", "hypolithon metagenome", 
    "ice metagenome", "indoor metagenome", "industrial waste metagenome", 
    "insect gut metagenome", "insect metagenome", "insect nest metagenome", 
    "internal organ metagenome", "interstitial water metagenome", "invertebrate gut metagenome", 
    "invertebrate metagenome", "jellyfish metagenome", "karst metagenome", "koala metagenome", 
    "lagoon metagenome", "lake water metagenome", "landfill metagenome", "leaf litter metagenome", 
    "leaf metagenome", "lichen crust metagenome", "lichen metagenome", "liver metagenome", 
    "lung metagenome", "macroalgae metagenome", "mangrove metagenome", "manure metagenome", 
    "marine metagenome", "marine plankton metagenome", "marine sediment metagenome", 
    "marsh metagenome", "marsupial metagenome", "medical device metagenome", "metagenome", 
    "microbial eukaryotic metagenome", "microbial fuel cell metagenome", 
    "microbial mat metagenome", "microeukaryotic metagenome", "milk metagenome", 
    "mine drainage metagenome", "mine metagenome", "mine tailings metagenome", 
    "mite metagenome", "mixed culture metagenome", "mollusc metagenome", "money metagenome", 
    "moonmilk metagenome", "mosquito metagenome", "moss metagenome", "mouse gut metagenome", 
    "mouse metagenome", "mouse skin metagenome", "mud metagenome", "museum specimen metagenome", 
    "musk metagenome", "nematode metagenome", "neuston metagenome", "nutrient bag metagenome", 
    "oasis metagenome", "oil field metagenome", "oil metagenome", 
    "oil production facility metagenome", "oil sands metagenome", "oral metagenome", 
    "oral-nasopharyngeal metagenome", "oral viral metagenome", "outdoor metagenome", 
    "ovine metagenome", "oyster metagenome", "painting metagenome", "paper pulp metagenome", 
    "parasite metagenome", "parchment metagenome", "peat metagenome", "periphyton metagenome", 
    "permafrost metagenome", "photosynthetic picoeukaryotic metagenome", "phycosphere metagenome", 
    "phyllosphere metagenome", "phytotelma metagenome", "pig gut metagenome", "pig metagenome", 
    "pipeline metagenome", "pitcher plant inquiline metagenome", "placenta metagenome", 
    "plant metagenome", "plastic metagenome", "plastisphere metagenome", "pollen metagenome", 
    "pond metagenome", "poultry litter metagenome", "power plant metagenome", "primate metagenome", 
    "probiotic metagenome", "protist metagenome", "psyllid metagenome", "rat gut metagenome", 
    "rat metagenome", "reproductive system metagenome", "respiratory tract metagenome", 
    "retting metagenome", "rhizoplane metagenome", "rhizosphere metagenome", 
    "rice paddy metagenome", "riverine metagenome", "rock metagenome", 
    "rock porewater metagenome", "rodent metagenome", "root associated fungus metagenome", 
    "root metagenome", "runoff metagenome", "saline spring metagenome", "saltern metagenome", 
    "salt lake metagenome", "salt marsh metagenome", "salt mine metagenome", 
    "salt pan metagenome", "sand metagenome", "scorpion gut metagenome", 
    "sea anemone metagenome", "seagrass metagenome", "sea squirt metagenome", 
    "sea urchin metagenome", "seawater metagenome", "sediment metagenome", "seed metagenome", 
    "semen metagenome", "shale gas metagenome", "sheep gut metagenome", "sheep metagenome", 
    "shoot metagenome", "shrew metagenome", "shrimp gut metagenome", "silage metagenome", 
    "skin metagenome", "slag metagenome", "sludge metagenome", "snake metagenome", 
    "snow metagenome", "soda lake metagenome", "soda lime metagenome", "soil crust metagenome", 
    "soil metagenome", "solid waste metagenome", "spider metagenome", "sponge metagenome", 
    "starfish metagenome", "steel metagenome", "stomach metagenome", "stromatolite metagenome", 
    "subsurface metagenome", "surface metagenome", "symbiont metagenome", "synthetic metagenome", 
    "tannin metagenome", "tar pit metagenome", "termitarium metagenome", 
    "termite fungus garden metagenome", "termite gut metagenome", "termite metagenome", 
    "terrestrial metagenome", "tick metagenome", "tidal flat metagenome", "tin mine metagenome", 
    "tobacco metagenome", "tomb wall metagenome", "tree metagenome", 
    "upper respiratory tract metagenome", "urban metagenome", "urinary tract metagenome", 
    "urine metagenome", "urogenital metagenome", "vaginal metagenome", "viral metagenome", 
    "volcano metagenome", "wallaby gut metagenome", "wasp metagenome", "wastewater metagenome", 
    "wetland metagenome", "whale fall metagenome", "whole organism metagenome", "wine metagenome", 
    "Winogradsky column metagenome", "wood decay metagenome", "zebrafish metagenome"]
geographicLocations = ["Afghanistan", "Albania", "Algeria", "American Samoa", "Andorra", 
    "Angola", "Anguilla", "Antarctica", "Antigua and Barbuda", "Arctic Ocean", "Argentina", 
    "Armenia", "Aruba", "Ashmore and Cartier Islands", "Atlantic Ocean", "Australia", "Austria", 
    "Azerbaijan", "Bahamas", "Bahrain", "Baker Island", "Baltic Sea", "Bangladesh", 
    "Barbados", "Bassas da India", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", 
    "Bhutan", "Bolivia", "Borneo", "Bosnia and Herzegovina", "Botswana", "Bouvet Island", 
    "Brazil", "British Virgin Islands", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", 
    "Cambodia", "Cameroon", "Canada", "Cape Verde", "Cayman Islands", "Central African Republic", 
    "Chad", "Chile", "China", "Christmas Island", "Clipperton Island", "Cocos Islands", 
    "Colombia", "Comoros", "Cook Islands", "Coral Sea Islands", "Costa Rica", "Cote d'Ivoire", 
    "Croatia", "Cuba", "Curacao", "Cyprus", "Czech Republic", "Democratic Republic of the Congo", 
    "Denmark", "Djibouti", "Dominica", "Dominican Republic", "East Timor", "Ecuador", "Egypt", 
    "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Ethiopia", "Europa Island", 
    "Falkland Islands (Islas Malvinas)", "Faroe Islands", "Fiji", "Finland", "France", 
    "French Guiana", "French Polynesia", "French Southern and Antarctic Lands", "Gabon", 
    "Gambia", "Gaza Strip", "Georgia", "Germany", "Ghana", "Gibraltar", "Glorioso Islands", 
    "Greece", "Greenland", "GrENAda", "Guadeloupe", "Guam", "Guatemala", "Guernsey", "Guinea", 
    "Guinea-Bissau", "Guyana", "Haiti", "Heard Island and McDonald Islands", "Honduras", 
    "Hong Kong", "Howland Island", "Hungary", "Iceland", "India", "Indian Ocean", "Indonesia", 
    "Iran", "Iraq", "Ireland", "Isle of Man", "Israel", "Italy", "Jamaica", "Jan Mayen", "Japan", 
    "Jarvis Island", "Jersey", "Johnston Atoll", "Jordan", "Juan de Nova Island", "Kazakhstan", 
    "Kenya", "Kerguelen Archipelago", "Kingman Reef", "Kiribati", "Kosovo", "Kuwait", "Kyrgyzstan", 
    "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", 
    "Luxembourg", "Macau", "Macedonia", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", 
    "Malta", "Marshall Islands", "Martinique", "Mauritania", "Mauritius", "Mayotte", 
    "Mediterranean Sea", "Mexico", "Micronesia", "Midway Islands", "Moldova", "Monaco", 
    "Mongolia", "Montenegro", "Montserrat", "Morocco", "Mozambique", "Myanmar", "Namibia", 
    "Nauru", "Navassa Island", "Nepal", "Netherlands", "New Caledonia", "New Zealand", 
    "Nicaragua", "Niger", "Nigeria", "Niue", "Norfolk Island", "Northern Mariana Islands", 
    "North Korea", "North Sea", "Norway", "not applicable", "not collected", "not provided", 
    "Oman", "Pacific Ocean", "Pakistan", "Palau", "Palmyra Atoll", "Panama", "Papua New Guinea", 
    "Paracel Islands", "Paraguay", "Peru", "Philippines", "Pitcairn Islands", "Poland", 
    "Portugal", "Puerto Rico", "Qatar", "Republic of the Congo", "restricted access", "Reunion", 
    "Romania", "Ross Sea", "Russia", "Rwanda", "Saint HelENA", "Saint Kitts and Nevis", 
    "Saint Lucia", "Saint Pierre and Miquelon", "Saint Vincent and the GrENAdines", "Samoa", 
    "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", 
    "Sierra Leone", "Singapore", "Sint Maarten", "Slovakia", "Slovenia", "Solomon Islands", 
    "Somalia", "South Africa", "Southern Ocean", "South Georgia and the South Sandwich Islands", 
    "South Korea", "Spain", "Spratly Islands", "Sri Lanka", "Sudan", "Suriname", "Svalbard", 
    "Swaziland", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", 
    "Tasman Sea", "Thailand", "Togo", "Tokelau", "Tonga", "Trinidad and Tobago", 
    "Tromelin Island", "Tunisia", "Turkey", "Turkmenistan", "Turks and Caicos Islands", 
    "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "Uruguay", 
    "USA", "Uzbekistan", "Vanuatu", "Venezuela", "Viet Nam", "Virgin Islands", "Wake Island", 
    "Wallis and Futuna", "West Bank", "Western Sahara", "Yemen", "Zambia", "Zimbabwe"]

RETRY_COUNT = 5
HQ = ("Multiple fragments where gaps span repetitive regions. Presence of the "
    "23S, 16S, and 5S rRNA genes and at least 18 tRNAs.")
MQ = ("Many fragments with little to no review of assembly other than reporting "
    "of standard assembly statistics.")

class NoDataException(ValueError):
    pass

def parse_args(argv):
    parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter,
        description="Allows to create xmls and manifest files for genome upload to ENA. " +
        "--xmls and --manifests are needed to determine the action the script " +
        "should perform. The use of more than one option is encouraged. To spare time, " +
        "-xmls and -manifests should be called only if respective xml or manifest files " +
        "do not already exist.")
    
    parser.add_argument('-u', '--upload_study', type=str, help="Study accession for genomes upload")
    parser.add_argument('--genome_info', type=str, required=True, help="Genomes metadata file")

    genomeType = parser.add_mutually_exclusive_group(required=True)
    genomeType.add_argument('-m', '--mags', action='store_true', help="Select for MAG upload")
    genomeType.add_argument('-b', '--bins', action='store_true', help="Select for bin upload")
    
    parser.add_argument('--out', type=str, help="Output folder. Default: working directory")
    parser.add_argument('--force', action='store_true', help="Forces reset of sample xml's backups")
    parser.add_argument('--live', action='store_true', help="Uploads on ENA. Omitting this " +
        "option allows to validate samples beforehand")
    parser.add_argument('--tpa', action='store_true', help="Select if uploading TPA-generated genomes")
    
    parser.add_argument('--webin', required=True, help="Webin id")
    parser.add_argument('--password', required=True, help="Webin password")
    parser.add_argument('--centre_name', required=True, help="Name of the centre uploading genomes")

    args = parser.parse_args(argv)

    if not args.upload_study:
        raise ValueError("No project selected for genome upload [-u, --upload_study].")
    
    if not os.path.exists(args.genome_info):
        raise FileNotFoundError('Genome metadata file "{}" does not exist'.format(args.genome_info))

    return args

'''
Input table: expects the following parameters:
    genome_name: genome file name
    accessions: run(s) or assembly(ies) the genome was generated from
    assembly_software: assembler_vX.X
    binning_software: binner_vX.X
    binning_parameters: binning parameters
    stats_generation_software: software_vX.X
    completeness: float
    contamination: float
    rRNA_presence: True/False if 5S, 16S, and 23S genes have been detected in the genome
    NCBI_lineage: full NCBI lineage, either in tax id or strings
    broad_environment: string
    local_environment: string
    environmental_medium: string
    metagenome: string
    co-assembly: True/False, whether the genome was generated from a co-assembly
    genome_coverage : genome coverage
    genome_path: path to genome to upload
'''
def read_and_cleanse_metadata_tsv(inputFile, genomeType):
    print('\tRetrieving info for genomes to submit...')
    
    binMandatoryFields = ["genome_name", "accessions",
        "assembly_software", "binning_software", 
        "binning_parameters", "stats_generation_software", "NCBI_lineage",
        "broad_environment", "local_environment", "environmental_medium", "metagenome",
        "co-assembly", "genome_coverage", "genome_path"]
    MAGMandatoryFields = ["rRNA_presence", "completeness", "contamination"]
    
    allFields = MAGMandatoryFields + binMandatoryFields
    metadata = pd.read_csv(inputFile, sep='\t', usecols=allFields)
    
    # make sure there are no empty cells
    cleanColumns = list(metadata.dropna(axis=1))
    if genomeType == "MAGs":
        missingValues = [item for item in allFields if item not in cleanColumns]
    else:
        missingValues = [item for item in binMandatoryFields if item not in cleanColumns]
    
    if missingValues:
        raise ValueError("The following mandatory fields have missing values in " +
            "the input file: {}".format(", ".join(missingValues)))

    # check amount of genomes to register at the same time
    if len(metadata) >= 5000:
        raise ValueError("Genomes need to be registered in batches of 5000 genomes or smaller.")

    # check whether accessions follow the right format
    accessions_regExp = re.compile("([E|S|D]R[R|Z]\d{6,})")

    accessionComparison = pd.DataFrame(columns=["genome_name", "attemptive_accessions", 
        "correct", "mismatching", "co-assembly"])
    accessionComparison["genome_name"] = metadata["genome_name"]
    accessionComparison["co-assembly"] = metadata["co-assembly"]

    accessionComparison["attemptive_accessions"] = metadata["accessions"].map(
        lambda a: len(a.split(',')))

    accessionComparison["correct"] = metadata["accessions"].map(
        lambda a: len(accessions_regExp.findall(a)))

    accessionComparison["mismatching"] = accessionComparison.apply(lambda row: 
        True if row["attemptive_accessions"] == row["correct"] 
        else None, axis=1).isna()

    mismatchingAccessions = accessionComparison[accessionComparison["mismatching"]]["genome_name"]
    if not mismatchingAccessions.empty:
        raise ValueError("Run accessions are not correctly formatted for the following " + 
            "genomes: " + ','.join(mismatchingAccessions.values))

    # check whether completeness and contamination are floats
    try:
        pd.to_numeric(metadata["completeness"])
        pd.to_numeric(metadata["contamination"])
        pd.to_numeric(metadata["genome_coverage"])
    except:
        raise ValueError("Completeness, contamination or coverage values should be formatted as floats")

    # check whether all co-assemblies have more than one run associated and viceversa
    coassemblyDiscrepancy = metadata[(
        (accessionComparison["correct"] < 2) & (accessionComparison["co-assembly"])) |
        ((accessionComparison["correct"] > 1) & (~accessionComparison["co-assembly"])
        )]["genome_name"]
    if not coassemblyDiscrepancy.empty:
        raise ValueError("The following genomes show discrepancy between number of runs "
            "involved and co-assembly status: " + ','.join(coassemblyDiscrepancy.values))

    # are provided metagenomes part of the accepted metagenome list?
    if False in metadata.apply(lambda row: 
        True if row["metagenome"] in metagenomes 
        else False, axis=1).unique():
        raise ValueError("Metagenomes associated with each genome need to belong to ENA's " +
            "approved metagenomes list.")

    # do provided file paths exist?
    if False in metadata.apply(lambda row: 
        True if os.path.exists(row["genome_path"]) 
        else False, axis =1).unique():
        raise FileNotFoundError("Some genome paths do not exist.")

    # check genome name lengths
    if not (metadata["genome_name"].map(lambda a: len(a) < 20).all()):
        raise ValueError("Genome names must be shorter than 20 characters.")

    # create dictionary while checking genome name uniqueness
    try:
        genomeInfo = metadata.set_index("genome_name").transpose().to_dict()
        return genomeInfo
    except:
        raise IndexError("Duplicate genome names were found in the input table.")

def round_stats(stats):
    newStat = round(float(stats), 2)
    if newStat == 100.0:
        newStat = 100
    if newStat == 0:
        newStat = 0.0

    return newStat

def compute_MAG_quality(completeness, contamination, RNApresence):
    RNApresent = False
    if str(RNApresence).lower() in ["true", "yes", "y"]:
        RNApresent = True
    quality = MQ
    if completeness >= 90 and contamination <= 5 and RNApresent:
        quality = HQ
    
    completeness = str(round_stats(completeness))
    contamination = str(round_stats(contamination))

    return quality, completeness, contamination

def extract_tax_info(taxInfo):
    kingdoms = ["Archaea", "Bacteria", "Eukaryota"]
    kingdomTaxa = ["2157", "2", "2759"]
    lineage, position, digitAnnotation = taxInfo.split(';'), 0, False

    selectedKingdom, finalKingdom = kingdoms, ""
    if lineage[-1].isdigit():
        selectedKingdom = kingdomTaxa
        position = 1
        digitAnnotation = True
    for index, k in enumerate(selectedKingdom):
        if k in lineage[position]:
            finalKingdom = kingdoms[index]
    
    iterator = len(lineage)-1
    submittable = False
    while iterator != -1 and not submittable:
        scientificName = lineage[iterator].strip()
        if digitAnnotation:
            scientificName = query_taxid(scientificName)
        elif "__" in scientificName:
            scientificName = scientificName.split("__")[1]
        else:
            raise ValueError("Unrecognised taxonomy format.")
        submittable, taxid, rank = query_scientific_name(scientificName, searchRank=True)

        if not submittable:
            if finalKingdom == "Archaea":
                submittable, scientificName, taxid = extract_Archaea_info(scientificName, rank)
            elif finalKingdom == "Bacteria":
                submittable, scientificName, taxid = extract_Bacteria_info(scientificName, rank)
            elif finalKingdom == "Eukaryota":
                submittable, scientificName, taxid = extract_Eukaryota_info(scientificName, rank)
        iterator -= 1

    return taxid, scientificName

def query_taxid(taxid):
    url = "https://www.ebi.ac.uk/ena/taxonomy/rest/tax-id/{}".format(taxid)
    response = requests.get(url)

    try:
        # Will raise exception if response status code is non-200 
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Request failed {} with error {}".format(url, e))
        return False
    
    res = json.loads(response.text)
    
    return res.get("scientificName", "")

def query_scientific_name(scientificName, searchRank=False):
    url = "https://www.ebi.ac.uk/ena/taxonomy/rest/scientific-name/{}".format(scientificName)
    response = requests.get(url)
    
    try:
        # Will raise exception if response status code is non-200 
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if searchRank:
            return False, "", ""
        else:
            return False, ""
    
    try:
        res = json.loads(response.text)[0]
    except IndexError:
        if searchRank:
            return False, "", ""
        else:
            return False, ""

    submittable = res.get("submittable", "").lower() == "true"
    taxid = res.get("taxId", "")
    rank = res.get("rank", "")

    if searchRank:
        return submittable, taxid, rank
    else:
        return submittable, taxid

def extract_Eukaryota_info(name, rank):
    nonSubmittable = (False, "", 0)

    # Asterisks in given taxonomy suggest the classification might be not confident enough.
    if '*' in name:
        return nonSubmittable

    if rank == "super kingdom":
        name = "uncultured eukaryote"
        submittable, taxid = query_scientific_name(name)
        return submittable, name, taxid
    else:
        name = name.capitalize() + " sp."
        submittable, taxid = query_scientific_name(name)
        if submittable:
            return submittable, name, taxid
        else:
            name = "uncultured " + name
            submittable, taxid = query_scientific_name(name)
            if submittable:
                return submittable, name, taxid
            else:
                name = name.replace(" sp.", '')
                submittable, taxid = query_scientific_name(name)
                if submittable:
                    return submittable, name, taxid
                else:
                    return nonSubmittable

def extract_Bacteria_info(name, rank):
    if rank == "species":
        name = name
    elif rank == "superkingdom":
        name = "uncultured bacterium".format(name)
    elif rank in ["family", "order", "class", "phylum"]:
        name = "uncultured {} bacterium".format(name)
    elif rank == "genus":
        name = "uncultured {} sp.".format(name)
    
    submittable, taxid, rank = query_scientific_name(name, searchRank=True)
    if not submittable:
        if rank in ["species", "genus"] and name.lower().endswith("bacteria"):
            name = "uncultured {}".format(name.lower().replace("bacteria", "bacterium"))
        elif rank == "family":
            if name.lower() == "deltaproteobacteria":
                name = "uncultured delta proteobacterium"
        submittable, taxid = query_scientific_name(name)

    return submittable, name, taxid

def extract_Archaea_info(name, rank):
    if rank == "species":
        name = name
    elif rank == "superkingdom":
        name = "uncultured archaeon"
    elif rank == "phylum":
        if "Euryarchaeota" in name:
            name = "uncultured euryarchaeote"
        elif "Candidatus" in name:
            name = "{} archaeon".format(name)
        else:
            name = "uncultured {} archaeon".format(name)
    elif rank in ["family", "order", "class"]:
        name = "uncultured {} archaeon".format(name)
    elif rank == "genus":
        name = "uncultured {} sp.".format(name)
    
    submittable, taxid, rank = query_scientific_name(name, searchRank=True)
    if not submittable:
        if "Candidatus" in name:
            if rank == "phylum":
                name = name.replace("Candidatus ", '')
            elif rank == "family":
                name = name.replace("uncultured ", '')
            submittable, taxid = query_scientific_name(name)
                            
    return submittable, name, taxid

def extract_genomes_info(inputFile, genomeType):
    genomeInfo = read_and_cleanse_metadata_tsv(inputFile, genomeType)
    for gen in genomeInfo:
        genomeInfo[gen]["accessions"] = genomeInfo[gen]["accessions"].split(',')
        accessionType = "run"
        assembly_regExp = re.compile("([E|S|D]RZ\d{6,})")
        if assembly_regExp.findall(genomeInfo[gen]["accessions"][0]):
            accessionType = "assembly"
        genomeInfo[gen]["accessionType"] = accessionType

        genomeInfo[gen]["isolationSource"] = genomeInfo[gen]["metagenome"]
        
        try:
            quality, compl, cont = compute_MAG_quality(genomeInfo[gen]["completeness"],
                genomeInfo[gen]["contamination"], genomeInfo[gen]["rRNA_presence"])
            genomeInfo[gen]["MAG_quality"] = quality
            genomeInfo[gen]["completeness"] = compl
            genomeInfo[gen]["contamination"] = cont
        except IndexError:
            pass

        if str(genomeInfo[gen]["co-assembly"]).lower() in ["yes", "y", "true"]:
            genomeInfo[gen]["co-assembly"] = True
        else:
            genomeInfo[gen]["co-assembly"] = False
        
        genomeInfo[gen]["alias"] = gen + '_' + str(int(dt.timestamp(dt.now())))

        taxID, scientificName = extract_tax_info(genomeInfo[gen]["NCBI_lineage"])
        genomeInfo[gen]["taxID"] = taxID
        genomeInfo[gen]["scientific_name"] = scientificName

    return genomeInfo

# ------------------- ENA API HANDLER -------------------
# TODO: organise this into a class

RUN_DEFAULT_FIELDS = 'study_accession,secondary_study_accession,instrument_model,' \
                     'run_accession,sample_accession'

ASSEMBLY_DEFAULT_FIELDS = 'sample_accession'

SAMPLE_DEFAULT_FIELDS = 'sample_accession,secondary_sample_accession,' \
                        'collection_date,country,location'

STUDY_DEFAULT_FIELDS = 'study_accession,secondary_study_accession,description,study_title'

def get_default_params():
    return {
        'format': 'json',
        'includeMetagenomes': True,
        'dataPortal': 'ena'
    }

def post_request(data, webin, password):
    url = "https://www.ebi.ac.uk/ena/portal/api/search"
    auth = (webin, password)
    default_connection_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*"
    }
    response = requests.post(url, data=data, auth=auth, headers=default_connection_headers)
    
    return response

def get_run(run_accession, webin, password, attempt=0, search_params=None):
    data = get_default_params()
    data['result'] = 'read_run'
    data['fields'] = RUN_DEFAULT_FIELDS
    data['query'] = 'run_accession=\"{}\"'.format(run_accession)

    if search_params:
        data.update(search_params)

    response = post_request(data, webin, password)
    
    if str(response.status_code)[0] != '2' and attempt > 2:
        raise ValueError("Could not retrieve run with accession {}, returned "
            "message: {}".format(run_accession, response.text))
    elif response.status_code == 204:
        if attempt < 2:
            attempt += 1
            sleep(1)
            return get_run(run_accession, webin, password, attempt)
        else:
            raise ValueError("Could not find run {} in ENA after {}"
                " attempts".format(run_accession, RETRY_COUNT))
    try:
        run = json.loads(response.text)[0]
    except (IndexError, TypeError, ValueError):
        raise ValueError("Could not find run {} in ENA.".format(run_accession))
    except:
        raise Exception("Could not query ENA API: {}".format(response.text))

    return run

def get_run_from_assembly(assembly_name):
    manifestXml = minidom.parseString(requests.get("https://www.ebi.ac.uk" +
        "/ena/browser/api/xml/" + assembly_name).text)

    run_ref = manifestXml.getElementsByTagName("RUN_REF")
    run = run_ref[0].attributes["accession"].value
     
    return run

def get_study(webin, password, primary_accession=None, secondary_accession=None):
    data = get_default_params()
    data['result'] = 'read_study'
    data['fields'] = STUDY_DEFAULT_FIELDS

    if primary_accession and not secondary_accession:
        data['query'] = 'study_accession="{}"'.format(primary_accession)
    elif not primary_accession and secondary_accession:
        data['query'] = 'secondary_study_accession="{}"'.format(secondary_accession)
    else:
        data['query'] = 'study_accession="{}" AND secondary_study_accession="{}"' \
            .format(primary_accession, secondary_accession)

    query_params = []
    for result_type in ['study', 'read_study', 'analysis_study']:
        for data_portal in ['ena', 'metagenome']:
            param = data.copy()
            param['result'] = result_type
            param['dataPortal'] = data_portal
            if result_type == 'study':
                if 'description' in param['fields']:
                    param['fields'] = param['fields'].replace('description', 'study_description')
            query_params.append(param)

    for param in query_params:
        try:
            response = post_request(data, webin, password)
            if response.status_code == 204:
                raise NoDataException()
            try:
                study = json.loads(response.text)[0]
            except (IndexError, TypeError, ValueError, KeyError) as e:
                raise e
            if data['result'] == 'study':
                if 'study_description' in study:
                    study['description'] = study.pop('study_description')
            return study
        except NoDataException:
            print("No info found to fetch study with params {}".format(param))
            pass
        except (IndexError, TypeError, ValueError, KeyError):
            print("Failed to fetch study with params {}, returned error: {}".format(param, response.text))

    raise ValueError('Could not find study {} {} in ENA.'.format(primary_accession, secondary_accession))

def get_study_runs(study_acc, webin, password, fields=None, search_params=None):
    data = get_default_params()
    data['result'] = 'read_run'
    data['fields'] = fields or RUN_DEFAULT_FIELDS
    data['query'] = '(study_accession=\"{}\" OR secondary_study_accession=\"{}\")'.format(study_acc, study_acc)

    if search_params:
        data.update(search_params)

    response = post_request(data, webin, password)
    
    if str(response.status_code)[0] != '2':
        raise ValueError("Could not retrieve runs for study %s.", study_acc)
    elif response.status_code == 204:
        return []

    try:
        runs = json.loads(response.text)
    except:
        raise ValueError("Query against ENA API did not work. Returned "
            "message: {}".format(response.text))

    return runs

def get_sample(sample_accession, webin, password, fields=None, search_params=None, attempt=0):
    data = get_default_params()
    data['result'] = 'sample'
    data['fields'] = fields or SAMPLE_DEFAULT_FIELDS
    data['query'] = ('(sample_accession=\"{acc}\" OR secondary_sample_accession'
        '=\"{acc}\") ').format(acc=sample_accession)

    if search_params:
        data.update(search_params)

    response = post_request(data, webin, password)
    
    if response.status_code == 200:
        return json.loads(response.text)[0]
    else:
        if str(response.status_code)[0] != '2':
            raise ValueError("Could not retrieve sample with accession {}. "
                "Returned message: {}".format(sample_accession, response.text))
        elif response.status_code == 204:
            if attempt < 2:
                new_params = {'dataPortal': 'metagenome' if data['dataPortal'] == 'ena' else 'ena'}
                attempt += 1
                return get_sample(sample_accession, webin, password, fields=fields, 
                    search_params=new_params, attempt=attempt)
            else:
                raise ValueError("Could not find sample {} in ENA after "
                    "{} attempts.".format(sample_accession, RETRY_COUNT))

# -------------------------------------------------------

def extract_ENA_info(genomeInfo, uploadDir, webin, password):
    print('\tRetrieving project and run info from ENA (this might take a while)...')
    
    # retrieving metadata from runs (and runs from assembly accessions if provided)
    allRuns = []
    for g in genomeInfo:
        if genomeInfo[g]["accessionType"] == "assembly":
            derivedRuns = []
            for acc in genomeInfo[g]["accessions"]:
                derivedRuns.append(get_run_from_assembly(acc))
            genomeInfo[g]["accessions"] = derivedRuns
        allRuns.extend(genomeInfo[g]["accessions"])

    runsSet, studySet, samplesDict, tempDict = set(allRuns), set(), {}, {}
    for r in runsSet:
        run_info = get_run(r, webin, password)
        studySet.add(run_info["secondary_study_accession"])
        samplesDict[r] = run_info["sample_accession"]
    
    if not studySet:
        raise ValueError("No study corresponding to runs found.")

    backupFile = os.path.join(uploadDir, "ENA_backup.json")
    counter = 0
    if not os.path.exists(backupFile):
        with open(backupFile, 'w') as file:
            pass
    with open(backupFile, "r+") as file:
        try:
            backupDict = json.load(file)
            tempDict = dict(backupDict)
            print("\tA backup file for ENA sample metadata has been found.")
        except json.decoder.JSONDecodeError:
            backupDict = {}
        for s in studySet:
            studyInfo = get_study(webin, password, "", s)

            projectDescription = studyInfo["description"]

            ENA_info = get_study_runs(s, webin, password)
            if ENA_info == []:
                raise IOError("No runs found on ENA for project {}.".format(s))
            for run, item in enumerate(ENA_info):
                runAccession = ENA_info[run]["run_accession"]
                if runAccession not in backupDict:
                    if runAccession in runsSet:
                        sampleAccession = ENA_info[run]["sample_accession"]
                        sampleInfo = get_sample(sampleAccession, webin, password)
                        
                        location = sampleInfo["location"]
                        if 'N' in location:
                            latitude = str(float(location.split('N')[0].strip()))
                            longitude = location.split('N')[1].strip()
                        elif 'S' in location:
                            latitude = '-' + str(float(location.split('S')[0].strip()))
                            longitude = location.split('S')[1].strip()
                        else:
                            latitude = "not provided"
                            longitude = "not provided"
                        
                        if 'W' in longitude:
                            longitude = '-' + str(float(longitude.split('W')[0].strip()))
                        elif longitude.endswith('E'):
                            longitude = str(float(longitude.split('E')[0].strip()))
                        
                        country = sampleInfo["country"].split(':')[0]
                        if not country in geographicLocations:
                            country = "not provided"
                        
                        collectionDate = sampleInfo["collection_date"]
                        if collectionDate == "":
                            collectionDate = "not provided"
                        
                        tempDict[runAccession] = {
                            "instrumentModel" : ENA_info[run]["instrument_model"],
                            "collectionDate" : collectionDate,
                            "country" : country,
                            "latitude" : latitude,
                            "longitude" : longitude,
                            "projectDescription" : projectDescription,
                            "study" : s,
                            "sampleAccession" : samplesDict[runAccession]
                        }
                        counter += 1

                        if (counter%10 == 0) or (len(runsSet) - len(backupDict) == counter):
                            file.seek(0)
                            file.write(json.dumps(tempDict))
                            file.truncate()
    
    tempDict = {**tempDict, **backupDict}
    combine_ENA_info(genomeInfo, tempDict)

def multipleElementSet(metadataList):
    return len(set(metadataList))>1

def combine_ENA_info(genomeInfo, ENADict):
    for g in genomeInfo:
        # TODO: optimise all the part below
        if genomeInfo[g]["co-assembly"]:
            instrumentList, collectionList, countryList = [], [], []
            studyList, descriptionList, samplesList = [], [], []
            longList, latitList = [], []
            for run in genomeInfo[g]["accessions"]:
                instrumentList.append(ENADict[run]["instrumentModel"])
                collectionList.append(ENADict[run]["collectionDate"])
                countryList.append(ENADict[run]["country"])
                studyList.append(ENADict[run]["study"])
                descriptionList.append(ENADict[run]["projectDescription"])
                samplesList.append(ENADict[run]["sampleAccession"])
                longList.append(ENADict[run]["longitude"])
                latitList.append(ENADict[run]["latitude"])
            
            if multipleElementSet(studyList):
                print("The co-assembly your MAG has been generated from comes from " +
                "different studies.")
                sys.exit(1)
            genomeInfo[g]["study"] = studyList[0] 
            genomeInfo[g]["description"] = descriptionList[0]
            
            instrument = instrumentList[0]
            if multipleElementSet(instrumentList):
                instrument = ','.join(instrumentList)
            genomeInfo[g]["sequencingMethod"] = instrument

            collectionDate = collectionList[0]
            if multipleElementSet(collectionList):
                collectionDate = "not provided"
            genomeInfo[g]["collectionDate"] = collectionDate

            country = countryList[0]
            if multipleElementSet(countryList):
                country = "not applicable"
            genomeInfo[g]["country"] = country

            latitude = latitList[0]
            if multipleElementSet(latitList):
                latitude = "not provided"
            genomeInfo[g]["latitude"] = latitude

            longitude = longList[0]
            if multipleElementSet(longList):
                longitude = "not provided"
            genomeInfo[g]["longitude"] = longitude

            samples = samplesList[0]
            if multipleElementSet(samplesList):
                samples = ','.join(samplesList)
            genomeInfo[g]["sample_accessions"] = samples
        else:
            run = genomeInfo[g]["accessions"][0]
            genomeInfo[g]["sequencingMethod"] = ENADict[run]["instrumentModel"]
            genomeInfo[g]["collectionDate"] = ENADict[run]["collectionDate"]
            genomeInfo[g]["study"] = ENADict[run]["study"]
            genomeInfo[g]["description"] = ENADict[run]["projectDescription"]
            genomeInfo[g]["sample_accessions"] = ENADict[run]["sampleAccession"]
            genomeInfo[g]["country"] = ENADict[run]["country"]
            genomeInfo[g]["longitude"] = ENADict[run]["longitude"]
            genomeInfo[g]["latitude"] = ENADict[run]["latitude"]
        
        genomeInfo[g]["accessions"] = ','.join(genomeInfo[g]["accessions"])

def handle_genomes_registration(sample_xml, submission_xml, webin, password, live=False):
    liveSub, mode = "", "live"
    if not live:
        liveSub = "dev"
        mode = "test"
    url = "https://www{}.ebi.ac.uk/ena/submit/drop-box/submit/".format(liveSub)

    print('\tRegistering sample xml in {} mode.'.format(mode))

    f = {
        'SUBMISSION': open(submission_xml, 'r'),
        'SAMPLE': open(sample_xml, 'r')
    }

    try:
        submissionResponse = requests.post(url, files = f, auth = (webin, password))

        if submissionResponse.status_code != 200:
            if str(submissionResponse.status_code).startswith('5'):
                raise Exception("Genomes could not be submitted to ENA as the server " +
                    "does not respond. Please again try later.")
            else:
                raise Exception("Genomes could not be submitted to ENA. HTTP response: " +
                    submissionResponse.reason)

        receiptXml = minidom.parseString((submissionResponse.content).decode("utf-8"))
        receipt = receiptXml.getElementsByTagName("RECEIPT")
        success = receipt[0].attributes["success"].value
        if success == "true":
            aliasDict = {}
            samples = receiptXml.getElementsByTagName("SAMPLE")
            for s in samples:
                sraAcc = s.attributes["accession"].value
                alias = s.attributes["alias"].value
                aliasDict[alias] = sraAcc
        elif success == "false":
            errors = receiptXml.getElementsByTagName("ERROR")
            print("\tGenomes could not be submitted to ENA. Please, check the errors below.")
            for error in errors:
                print("\t" + error.firstChild.data)
            sys.exit(1)
        
        print('\t{} genome samples successfully registered.'.format(str(len(aliasDict))))

        return aliasDict

    except:
        raise ConnectionError("Genomes could not be registered to ENA.")

def getAccessions(accessionsFile):
    accessionDict = {}
    with open(accessionsFile, 'r') as f:
        for line in f:
            line = line.split('\t')
            alias = line[0]
            accession = line[1].rstrip('\n')
            accessionDict[alias] = accession

    return accessionDict

def saveAccessions(aliasAccessionDict, accessionsFile):
    with open(accessionsFile, 'a') as f:
        for elem in aliasAccessionDict:
            f.write("{}\t{}\n".format(elem, aliasAccessionDict[elem]))

def create_manifest_dictionary(run, alias, assemblySoftware, sequencingMethod, 
    MAGpath, gen, study, coverage, isCoassembly):
    manifestDict = {
        "accessions" : run,
        "alias" : alias,
        "assembler" : assemblySoftware, 
        "sequencingMethod" : sequencingMethod, 
        "genome_path" : MAGpath,
        "genome_name" : gen,
        "study" : study,
        "coverageDepth" : coverage, 
        "co-assembly" : isCoassembly
    }

    return manifestDict

def compute_manifests(genomes):
    manifestInfo = {}
    for g in genomes:
        manifestInfo[g] = create_manifest_dictionary(genomes[g]["accessions"],
            genomes[g]["alias"], genomes[g]["assembly_software"], 
            genomes[g]["sequencingMethod"], genomes[g]["genome_path"], g, 
            genomes[g]["study"], genomes[g]["genome_coverage"], genomes[g]["co-assembly"])
    
    return manifestInfo

def get_study_from_xml(sample):
    description = sample.childNodes[5].childNodes[0].data
    study = description.split(' ')[-1][:-1]

    return study

def recover_info_from_xml(genomeDict, sample_xml, live_mode):
    print("Retrieving data for genome submission...")

    # extract list of genomes (samples) to be registered
    xml_structure = minidom.parse(sample_xml)
    samples = xml_structure.getElementsByTagName("SAMPLE")
    
    for s in samples:
        study = get_study_from_xml(s)

        # extract alias from xml and find a match with genomes the user is uploading
        XMLalias = s.attributes["alias"].value
        aliasSplit = XMLalias.split("_")
        XMLgenomeName = '_'.join(aliasSplit[:-1])
        for gen in genomeDict:
            # if match is found, associate attributes listed in the xml file
            # with genomes to upload
            if XMLgenomeName == gen:
                if not live_mode:
                    currentTimestamp = str(int(dt.timestamp(dt.now())))
                    XMLalias = gen + '_' + currentTimestamp
                    s.attributes["alias"].value = XMLalias
                    sampleTitle = s.getElementsByTagName("TITLE")[0]
                    sampleTitleValue = sampleTitle.firstChild.nodeValue.split("_")
                    sampleTitleValue[-1] = currentTimestamp
                    newSampleTitle = '_'.join(sampleTitleValue)
                    s.getElementsByTagName("TITLE")[0].firstChild.replaceWholeText(newSampleTitle)
                attributes = s.childNodes[7].getElementsByTagName("SAMPLE_ATTRIBUTE")
                seqMethod, assSoftware = "", ""
                for a in attributes:
                    tagElem = a.getElementsByTagName("TAG")
                    tag = tagElem[0].childNodes[0].nodeValue
                    if tag == "sequencing method":
                        seqMethodElem = a.getElementsByTagName("VALUE")
                        seqMethod = seqMethodElem[0].childNodes[0].nodeValue
                    elif tag == "assembly software":
                        assSoftwareElem = a.getElementsByTagName("VALUE")
                        assSoftware = assSoftwareElem[0].childNodes[0].nodeValue
                    if not seqMethod == "" and not assSoftware == "":
                        break

                genomeDict[gen]["accessions"] = ','.join(genomeDict[gen]["accessions"])
                genomeDict[gen]["alias"] = XMLalias
                genomeDict[gen]["assembly_software"] = assSoftware
                genomeDict[gen]["sequencingMethod"] = seqMethod
                genomeDict[gen]["study"] = study
                break

    if not live_mode:
        for s in samples:
            xml_structure.firstChild.appendChild(s)
        
        with open(sample_xml, 'wb') as f:
            dom_string = xml_structure.toprettyxml().encode("utf-8")
            dom_string = b'\n'.join([s for s in dom_string.splitlines() if s.strip()])
            f.write(dom_string)

def create_sample_attribute(sample_attributes, data_list, mag_data=None):
    tag = data_list[0]
    value = data_list[1]
    if mag_data:
        value = str(mag_data[value])
    units = None
    if len(data_list) == 3:
        units = data_list[2]
    
    new_sample_attr = ET.SubElement(sample_attributes, "SAMPLE_ATTRIBUTE")
    ET.SubElement(new_sample_attr, 'TAG').text = tag
    ET.SubElement(new_sample_attr, 'VALUE').text = value
    if units:
        ET.SubElement(new_sample_attr, 'UNITS').text = units

def write_genomes_xml(genomes, xml_path, genomeType, centreName, tpa):
    map_sample_attributes = [
        # tag - value - unit (optional)
        ["project name", "description"],
        ["sequencing method", "sequencingMethod"],
        ["assembly software", "assembly_software"],
        ["assembly quality", "MAG_quality"],
        ["binning software", "binning_software"],
        ["binning parameters", "binning_parameters"],
        ["completeness software", "stats_generation_software"],
        ["completeness score", "completeness", "%"],
        ["contamination score", "contamination", "%"],
        ["isolation source", "isolationSource"],
        ["collection date", "collectionDate"],
        ["geographic location (country and/or sea)", "country"],
        ["geographic location (latitude)", "latitude", "DD"],
        ["geographic location (longitude)", "longitude", "DD"],
        ["broad-scale environmental context", "broad_environment"],
        ["local environmental context", "local_environment"],
        ["environmental medium", "environmental_medium"],
        ["sample derived from", "sample_accessions"],
        ["metagenomic source", "metagenome"],
    ]

    checklist, assemblyType = "ERC000047", "Metagenome-assembled genome"
    if genomeType == "bins":
        checklist = "ERC000050"
        assemblyType = "binned metagenome"

    constant_sample_attributes = [
        # tag - value
        ["taxonomic identity marker", "multi-marker approach"],
        ["investigation type", "metagenome-assembled genome"],
        ["ENA-CHECKLIST", checklist],
    ]

    tpaDescription = ""
    if tpa:
        tpaDescription = "Third Party Annotation (TPA) "

    sample_set = ET.Element("SAMPLE_SET")

    for g in genomes:
        plural = ""
        if genomes[g]["co-assembly"]:
            plural = 's'
        description = ("This sample represents a {}{} assembled from the "
            "metagenomic run{} {} of study {}.".format(tpaDescription, 
            assemblyType, plural, genomes[g]["accessions"], 
            genomes[g]["study"]))
        
        sample = ET.SubElement(sample_set, "SAMPLE")
        sample.set("alias", genomes[g]["alias"])
        sample.set("center_name", centreName)

        ET.SubElement(sample, 'TITLE').text = ("{}: {}".format(assemblyType, 
            genomes[g]["alias"]))
        sample_name = ET.SubElement(sample, "SAMPLE_NAME")
        ET.SubElement(sample_name, "TAXON_ID").text = genomes[g]["taxID"]
        ET.SubElement(sample_name, "SCIENTIFIC_NAME").text = genomes[g]["scientific_name"]
        ET.SubElement(sample_name, "COMMON_NAME")

        ET.SubElement(sample, "DESCRIPTION").text = description

        sample_attributes = ET.SubElement(sample, "SAMPLE_ATTRIBUTES")

        for mapping in map_sample_attributes:
            create_sample_attribute(sample_attributes, mapping, genomes[g])

        for constant in constant_sample_attributes:
            create_sample_attribute(sample_attributes, constant)

    with open(xml_path, 'wb') as f:
        dom = minidom.parseString(
            ET.tostring(sample_set, encoding="utf-8")
        )
        f.write(dom.toprettyxml().encode("utf-8"))

def write_submission_xml(upload_dir, centre_name, study=True):
    today = str(date.today())
    sub_xml = os.path.join(upload_dir, 'submission.xml')

    submission = ET.Element('SUBMISSION')
    submission.set('center_name', centre_name)

    # template
    actions = ET.SubElement(submission, 'ACTIONS')
    action_sub = ET.SubElement(actions, 'ACTION')
    ET.SubElement(action_sub, 'ADD')

    # attributes: function and hold date
    if study:
        action_hold = ET.SubElement(actions, 'ACTION')
        hold = ET.SubElement(action_hold, 'HOLD')
        hold.set('HoldUntilDate', today)

    with open(sub_xml, 'wb') as submission_file:
        dom = minidom.parseString(
            ET.tostring(submission, encoding="utf-8")
        )
        submission_file.write(dom.toprettyxml().encode("utf-8"))

    return sub_xml

def generate_genome_manifest(genomeInfo, study, manifestsRoot, aliasToSample, genomeType, tpa):
    manifest_path = os.path.join(manifestsRoot, f'{genomeInfo["genome_name"]}.manifest')
    
    tpaAddition, multipleRuns = "", ""
    if tpa:
        tpaAddition = "Third Party Annotation (TPA) "
    if genomeInfo["co-assembly"]:
        multipleRuns = "s"
    assemblyType = "Metagenome-Assembled Genome (MAG)"
    if genomeType == "bins":
        assemblyType = "binned metagenome"

    values = (
        ('STUDY', study),
        ('SAMPLE', aliasToSample[genomeInfo["alias"]]),
        ('ASSEMBLYNAME', genomeInfo["alias"]),
        ('ASSEMBLY_TYPE', assemblyType),
        ('COVERAGE', genomeInfo["coverageDepth"]),
        ('PROGRAM', genomeInfo["assembler"]),
        ('PLATFORM', genomeInfo["sequencingMethod"]),
        ('MOLECULETYPE', "genomic DNA"),
        ('DESCRIPTION', ("This is a {}bin derived from the primary whole genome "
            "shotgun (WGS) data set {}. This sample represents a {} from the "
            "metagenomic run{} {}.".format(tpaAddition, genomeInfo["study"], 
            assemblyType, multipleRuns, genomeInfo["accessions"]))),
        ('RUN_REF', genomeInfo["accessions"]),
        ('FASTA', os.path.abspath(genomeInfo["genome_path"]))
    )
    print("Writing manifest file (.manifest) for {}.".format(genomeInfo["alias"]))
    with open(manifest_path, "w") as outfile:
        for (k, v) in values:
            manifest = f'{k}\t{v}\n'
            outfile.write(manifest)
        if tpa:
            outfile.write("TPA\ttrue\n")

def file_generator():
    ENA_uploader = GenomeUpload()

    uploadDir = ENA_uploader.upload_dir
    live = ENA_uploader.live
    tpa = ENA_uploader.tpa
    webinUser, webinPassword = ENA_uploader.username, ENA_uploader.password
    genomeType, centre_name = ENA_uploader.genomeType, ENA_uploader.centre_name
    
    if not live:
        print("Warning: genome submission is not in live mode, " +
            "files will be validated, but not uploaded.")

    xmlGenomeFile, xmlSubFile = "genome_samples.xml", "submission.xml"
    samples_xml = os.path.join(uploadDir, xmlGenomeFile)
    submissionXmlPath = os.path.join(uploadDir, xmlSubFile)
    submission_xml = submissionXmlPath
    genomes, manifestInfo = {}, {}

    # submission xml existence
    if not os.path.exists(submissionXmlPath):
        submission_xml = write_submission_xml(uploadDir, centre_name, False)

    # sample xml generation or recovery
    genomes = ENA_uploader.create_genome_dictionary(samples_xml)
    if not os.path.exists(samples_xml) or ENA_uploader.force:
        print("\tWriting genome registration XML...")
        write_genomes_xml(genomes, samples_xml, genomeType, centre_name, tpa)
        print("\tAll files have been written to " + uploadDir)
        
    # manifests creation
    manifestDir = os.path.join(uploadDir, "manifests")
    os.makedirs(manifestDir, exist_ok=True)
    
    accessionsgen = "registered_MAGs.tsv"
    if genomeType == "bins":
        accessionsgen = accessionsgen.replace("MAG", "bin")
    if not live:
        accessionsgen = accessionsgen.replace(".tsv", "_test.tsv")
    
    accessionsFile = os.path.join(uploadDir, accessionsgen)
    save = False
    if os.path.exists(accessionsFile):
        if not live:
            save = True
        if not save:
            aliasToNewSampleAccession = getAccessions(accessionsFile)
    else:
        save = True
        
    if save:
        print("Registering genome samples XMLs...")
        aliasToNewSampleAccession = handle_genomes_registration(samples_xml, 
            submission_xml, webinUser, webinPassword, live)
        saveAccessions(aliasToNewSampleAccession, accessionsFile)
    else:
        print("Genome samples already registered, reading ERS accessions...")

    print("Generating manifest files...")
    
    manifestInfo = compute_manifests(genomes)

    for m in manifestInfo:
        generate_genome_manifest(manifestInfo[m], ENA_uploader.upStudy,  
            manifestDir, aliasToNewSampleAccession, genomeType, tpa)

class GenomeUpload:
    def __init__(self, argv=sys.argv[1:]):
        self.args = parse_args(argv)
        self.upStudy = self.args.upload_study
        self.genomeMetadata = self.args.genome_info
        self.genomeType = "bins" if self.args.bins else "MAGs"
        self.live = True if self.args.live else False
        self.username = self.args.webin
        self.password = self.args.password
        self.tpa = True if self.args.tpa else False
        self.centre_name = self.args.centre_name
        self.force = True if self.args.force else False

        workDir = self.args.out if self.args.out else os.getcwd()
        self.upload_dir = self.generate_genomes_upload_dir(workDir, self.genomeType)
    
    def generate_genomes_upload_dir(self, dir, genomeType):
        uploadName = "MAG_upload"
        if genomeType == "bins":
            uploadName = uploadName.replace("MAG", "bin")
        upload_dir = os.path.join(dir, uploadName)
        os.makedirs(upload_dir, exist_ok=True)
        return upload_dir

    def create_genome_dictionary(self, samples_xml):
        print('Retrieving data for MAG submission...')

        genomeInfo = extract_genomes_info(self.genomeMetadata, self.genomeType)
        if not os.path.exists(samples_xml) or self.force:
            extract_ENA_info(genomeInfo, self.upload_dir, self.username, self.password)
        else:
            recover_info_from_xml(genomeInfo, samples_xml, self.live)

        return genomeInfo

if __name__ == "__main__":
    file_generator()
    print('Completed')
